#!/usr/bin/env python3
"""调用书有引力 AIGC 生图接口：创建任务 → 轮询结果 → 下载图片。

用法示例：
  python3 aigc_image.py "一只在草地上奔跑的金毛犬，阳光明媚" --aspect 16:9 --resolution 2K
  python3 aigc_image.py "参考这张图的风格，生成一只猫" --ref https://example.com/ref.jpg
  python3 aigc_image.py --task-id 125xxxx-...        # 继续查询已创建的任务

环境变量：
  AIGC_TOKEN     可选，请求头 Authorization 的值（不设置则不带该请求头）
  AIGC_BASE_URL  可选，默认 https://api.shuyouyinli.cn/bzsq/member/cms/aigc/image
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.environ.get(
    "AIGC_BASE_URL", "https://api.shuyouyinli.cn/bzsq/member/cms/aigc/image"
).rstrip("/")

MODEL_VERSIONS = {
    "OG": ["image2_low", "image2_medium", "image2_high"],
    "GG": ["2.5", "3.0", "3.1"],
    "SI": ["4.0", "4.5", "5.0-lite"],
    "Qwen": ["0925"],
    "Hunyuan": ["3.0"],
    "Vidu": ["q2"],
    "Kling": ["2.1", "3.0", "3.0-Omni", "O1"],
}

ERR_CODES = {
    "RequestLimitExceeded": "模型调用超出并发限制",
    "InvalidParameter.VoilationContent": "输入 prompt 违反内容安全策略",
    "InvalidParameterValue": "参数错误",
    "FailedOperation": "模型任务堆积",
    "InternalError": "内部错误",
}


def fail(msg):
    print(f"错误：{msg}", file=sys.stderr)
    sys.exit(1)


def call(method, url, token, body=None):
    headers = {"accessToken": "bz"}
    if token:
        headers["Authorization"] = token
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body, ensure_ascii=False).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    # 查询是只读的，网络抖动时重试；创建任务不重试，避免重复建任务
    attempts = 4 if method == "GET" else 1
    for i in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                text = resp.read().decode()
            break
        except urllib.error.HTTPError as e:
            fail(f"{method} {url} 返回 HTTP {e.code}：{e.read().decode(errors='replace')[:500]}")
        except OSError as e:
            if i == attempts - 1:
                fail(f"{method} {url} 请求失败：{getattr(e, 'reason', e)}")
            time.sleep(2 ** (i + 1))
    try:
        res = json.loads(text)
    except ValueError:
        fail(f"{method} {url} 返回的不是 JSON：{text[:500]}")
    if res.get("code") != 200:
        fail(f"接口返回 code={res.get('code')}：{res.get('msg')}")
    return res.get("data") or {}


def build_body(a):
    if not a.prompt and not a.ref and not a.ref_file_id:
        fail("没有参考图时必须提供 prompt")
    versions = MODEL_VERSIONS.get(a.model)
    if versions is None:
        fail(f"未知模型 {a.model}，可选：{', '.join(MODEL_VERSIONS)}")
    version = a.version or versions[-1]
    if version not in versions:
        fail(f"模型 {a.model} 的版本可选：{', '.join(versions)}")
    body = {"ModelName": a.model, "ModelVersion": version}
    for key, val in [
        ("Prompt", a.prompt),
        ("NegativePrompt", a.negative),
        ("Resolution", a.resolution),
        ("AspectRatio", a.aspect),
        ("EnhancePrompt", a.enhance),
    ]:
        if val:
            body[key] = val
    files = [{"Type": "Url", "Url": u} for u in a.ref]
    files += [{"Type": "File", "FileId": f} for f in a.ref_file_id]
    if files:
        body["FileInfos"] = files
    return body


def wait_task(task_id, token, interval, timeout):
    url = f"{BASE_URL}/task?" + urllib.parse.urlencode({"taskId": task_id})
    deadline = time.time() + timeout
    last = None
    while True:
        data = call("GET", url, token)
        status, progress = data.get("status"), data.get("progress")
        if (status, progress) != last:
            print(f"状态：{status}  进度：{progress}%", file=sys.stderr)
            last = (status, progress)
        if status == "FINISH":
            return data
        if time.time() > deadline:
            fail(f"等待超时（{timeout}s），可稍后用 --task-id {task_id} 继续查询")
        time.sleep(interval)


def download(files, out):
    saved = []
    multi = len(files) > 1
    for i, f in enumerate(files, 1):
        url = f.get("fileUrl")
        if not url:
            continue
        ext = f.get("fileType") or os.path.splitext(urllib.parse.urlparse(url).path)[1].lstrip(".") or "png"
        if out.endswith(os.sep) or os.path.isdir(out):
            name = os.path.basename(urllib.parse.urlparse(url).path) or f"aigc_{i}.{ext}"
            path = os.path.join(out, name)
        else:
            root, given_ext = os.path.splitext(out)
            path = f"{root}_{i}{given_ext or '.' + ext}" if multi else (out if given_ext else f"{out}.{ext}")
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        try:
            with urllib.request.urlopen(url, timeout=120) as resp, open(path, "wb") as fh:
                fh.write(resp.read())
            saved.append(path)
        except (urllib.error.URLError, OSError) as e:
            print(f"警告：下载 {url} 失败（{e}），可直接使用该链接", file=sys.stderr)
    return saved


def main():
    p = argparse.ArgumentParser(description="AIGC 生图：创建任务并等待出图")
    p.add_argument("prompt", nargs="?", help="正向提示词（无参考图时必填）")
    p.add_argument("-n", "--negative", help="反向提示词")
    p.add_argument("-m", "--model", default="OG", help="模型：" + "/".join(MODEL_VERSIONS) + "（默认 OG）")
    p.add_argument("-v", "--version", help="模型版本，默认取该模型可选值的最后一个（OG 即 image2_high）")
    p.add_argument("-r", "--resolution", help="分辨率，如 4K、2K、1080P")
    p.add_argument("-a", "--aspect", help="画面比例，如 16:9、9:16、1:1")
    p.add_argument("--enhance", choices=["Enabled", "Disabled"], help="提示词增强")
    p.add_argument("--ref", action="append", default=[], help="参考图 URL，可重复")
    p.add_argument("--ref-file-id", action="append", default=[], help="参考图腾讯云 FileId，可重复")
    p.add_argument("-o", "--out", default="aigc-output/", help="保存路径：目录（以 / 结尾）或文件名（默认 aigc-output/）")
    p.add_argument("--no-download", action="store_true", help="只输出图片链接，不下载")
    p.add_argument("--task-id", help="跳过创建，直接查询已有任务")
    p.add_argument("--interval", type=float, default=3, help="轮询间隔秒数（默认 3）")
    p.add_argument("--timeout", type=float, default=600, help="最长等待秒数（默认 600）")
    p.add_argument("--dry-run", action="store_true", help="只打印请求体，不发请求")
    a = p.parse_args()

    body = None if a.task_id else build_body(a)
    if a.dry_run:
        print(json.dumps(body, ensure_ascii=False, indent=2))
        return
    token = os.environ.get("AIGC_TOKEN")
    task_id = a.task_id
    if not task_id:
        task_id = call("POST", f"{BASE_URL}/create", token, body).get("taskId") or fail("创建任务未返回 taskId")
        print(f"任务已创建：{task_id}", file=sys.stderr)

    data = wait_task(task_id, token, a.interval, a.timeout)
    err = data.get("errCodeExt")
    if err:
        fail(f"生图失败 {err}（{ERR_CODES.get(err, '未知错误')}）：{data.get('message')}")
    files = data.get("outputFiles") or []
    if not files:
        fail("任务已完成但没有输出图片")
    saved = [] if a.no_download else download(files, a.out)
    print(json.dumps({"taskId": task_id, "outputFiles": files, "saved": saved}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
