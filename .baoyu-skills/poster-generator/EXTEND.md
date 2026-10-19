# poster-generator 项目偏好

- renderer: aigc-image
- backend: OG / image2_high
- quality: 2K
- language: zh

## 渲染方式

生图一律走 `aigc-image` 技能（AIGC 生图接口），不要自动搜索其他渲染器：

```bash
python3 .claude/skills/aigc-image/scripts/aigc_image.py "$(cat poster/<slug>/prompts/poster.md)" \
  -a <aspect> -r <quality> -o poster/<slug>/poster.png
```

- `--aspect` 直接传给 `-a`；`--quality` 的 1K/2K/4K 传给 `-r`（1K 时不传）。
- 生成后用 `SendUserFile`（`display: "render"`）把 `poster.png` 发到对话里。
- 模型直接画出的中文标题可能有笔画误差：渲染后放大检查标题，如有错字或变形，在总结里明确告诉用户，并提供重生成或后期用真实字体排版的选项。
