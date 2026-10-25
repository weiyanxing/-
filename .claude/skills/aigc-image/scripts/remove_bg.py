#!/usr/bin/env python3
"""把纯色背景的生成图抠成透明 PNG。

适用于提示词里要求了"纯色、无渐变、无投影"背景的图（如 #505050 深灰）。
背景色取四周边缘像素的中位数；与边缘连通的近背景色区域、以及内部较大的
纯背景色空洞会变透明，过渡像素按色差给半透明并去除背景色残留。

发光文字/霓虹类图片用 --mode glow：提示词要求纯黑背景（#000000），按亮度把
光晕还原成半透明（α = 最亮通道 / knee），亮部保持不透明，颜色去掉黑色混合。

书法、墨迹、单色笔触类图片用 --mode ink：白底（或任意纯色底）上按与背景的
色差算透明度，飞白、枯笔的淡色边缘还原成半透明的墨色，不会在深色底上留浅色毛边。

用法：
  python3 remove_bg.py 输入.png 输出.png [--crop] [--preview 预览.png]
  python3 remove_bg.py 输入.png 输出.png --mode glow [--knee 180] [--crop]
  python3 remove_bg.py 输入.png 输出.png --mode ink [--crop]
依赖：pillow numpy scipy
"""
import argparse

import numpy as np
from PIL import Image
from scipy import ndimage


def main():
    p = argparse.ArgumentParser(description="纯色背景抠图，输出透明 PNG")
    p.add_argument("src")
    p.add_argument("dst")
    p.add_argument("--low", type=float, default=12, help="色差低于此值完全透明（默认 12）")
    p.add_argument("--high", type=float, default=40, help="色差高于此值完全不透明（默认 40）")
    p.add_argument("--min-hole", type=float, default=0.0005, help="内部空洞最小面积占比（默认 0.0005）")
    p.add_argument("--mode", choices=["flat", "glow", "ink"], default="flat",
                   help="flat：纯色背景（默认）；glow：黑底发光；ink：纯色底上的墨迹/书法")
    p.add_argument("--knee", type=float, default=180, help="glow 模式下最亮通道达到此值即完全不透明（默认 180）")
    p.add_argument("--crop", action="store_true", help="裁到主体边界并留 3%% 边距")
    p.add_argument("--preview", help="另存一张棋盘格/白/黑三联预览图")
    a = p.parse_args()

    img = np.asarray(Image.open(a.src).convert("RGB")).astype(np.float32)
    h, w, _ = img.shape
    b = 16
    border = np.concatenate([img[:b].reshape(-1, 3), img[-b:].reshape(-1, 3),
                             img[:, :b].reshape(-1, 3), img[:, -b:].reshape(-1, 3)])
    bg = np.median(border, axis=0)

    if a.mode == "glow":
        # 背景噪点上限取边缘最亮通道的 99.5 分位，低于它的一律透明
        floor = np.percentile(border.max(axis=1), 99.5)
        m = np.clip(img.max(axis=2) - floor, 0, None)
        alpha = np.clip(m / (a.knee - floor), 0, 1)
        rgb = img.copy()
        vis = alpha > 0
        rgb[vis] = (img[vis] - (1 - alpha[vis, None]) * bg) / alpha[vis, None]
        finish(a, rgb, alpha, bg, h, w)
        return

    dist = np.linalg.norm(img - bg, axis=2)

    if a.mode == "ink":
        # 墨色取最浓 5% 像素的平均色；α = 色差 / 墨色色差，去掉背景混色
        floor = np.percentile(np.linalg.norm(border - bg, axis=1), 99.5)
        ink_px = img[dist >= np.percentile(dist, 99)]
        knee = np.linalg.norm(ink_px.mean(axis=0) - bg) * 0.9
        alpha = np.clip((dist - floor) / (knee - floor), 0, 1)
        rgb = img.copy()
        vis = alpha > 0
        rgb[vis] = (img[vis] - (1 - alpha[vis, None]) * bg) / alpha[vis, None]
        finish(a, rgb, alpha, bg, h, w)
        return

    labels, n = ndimage.label(dist < a.high, structure=np.ones((3, 3)))
    edge_ids = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
    keep = set(edge_ids[edge_ids > 0].tolist())
    areas = ndimage.sum(np.ones_like(dist), labels, index=np.arange(1, n + 1))
    means = ndimage.mean(dist, labels, index=np.arange(1, n + 1))
    for i, (area, mean) in enumerate(zip(areas, means), 1):
        if area >= a.min_hole * h * w and mean < a.low:
            keep.add(i)
    bgmask = np.isin(labels, list(keep))

    alpha = np.ones((h, w), np.float32)
    alpha[bgmask] = np.clip((dist[bgmask] - a.low) / (a.high - a.low), 0, 1)

    # 半透明像素去掉背景色残留：C = (P - (1 - α)·B) / α
    rgb = img.copy()
    semi = (alpha > 0) & (alpha < 1)
    rgb[semi] = (img[semi] - (1 - alpha[semi, None]) * bg) / alpha[semi, None]
    finish(a, rgb, alpha, bg, h, w)


def finish(a, rgb, alpha, bg, h, w):
    out = np.dstack([np.clip(rgb, 0, 255), alpha * 255]).astype(np.uint8)
    res = Image.fromarray(out, "RGBA")

    if a.crop:
        ys, xs = np.nonzero(alpha > 0.02)
        pad = int(0.03 * max(h, w))
        res = res.crop((max(xs.min() - pad, 0), max(ys.min() - pad, 0),
                        min(xs.max() + pad + 1, w), min(ys.max() + pad + 1, h)))
    res.save(a.dst)
    print(f"背景色 {bg.round().astype(int).tolist()}，输出 {a.dst} {res.size}")

    if a.preview:
        W, H = res.size
        tile = 32
        yy, xx = np.mgrid[:H, :W]
        checker = np.where(((yy // tile + xx // tile) % 2)[..., None], 200, 255).astype(np.uint8).repeat(3, 2)
        panels = []
        for base in (Image.fromarray(checker), Image.new("RGB", (W, H), "white"), Image.new("RGB", (W, H), (20, 20, 20))):
            base = base.convert("RGBA")
            base.alpha_composite(res)
            panels.append(base.convert("RGB"))
        sheet = Image.new("RGB", (W * 3, H))
        for i, pnl in enumerate(panels):
            sheet.paste(pnl, (W * i, 0))
        sheet.thumbnail((2400, 2400))
        sheet.save(a.preview)


if __name__ == "__main__":
    main()
