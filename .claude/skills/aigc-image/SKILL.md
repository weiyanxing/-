---
name: aigc-image
description: 生图 / 生成图片 / 画图 / 出图 / 文生图 / 图生图 / AI 绘图时一律使用本技能，调用书有引力 AIGC 生图接口（POST https://api.shuyouyinli.cn/bzsq/member/cms/aigc/image/create）。Use for ANY image generation request in this repo instead of other image models or hand-drawn placeholders.
---

# AIGC 生图

用户要求：**以后所有生图都调用这个接口**，不要换用其他生图服务，也不要用 SVG/占位图代替。

- 创建任务：`POST https://api.shuyouyinli.cn/bzsq/member/cms/aigc/image/create`
- 查询任务：`GET  https://api.shuyouyinli.cn/bzsq/member/cms/aigc/image/task?taskId=...`
- 请求头：`Authorization: <AIGC_TOKEN>`、`accessToken: bz`
- 完整字段说明见同目录 `reference.md`

## 用法

直接跑脚本，它会创建任务、轮询到完成、把图片下载到本地，最后在 stdout 打印 JSON（`taskId`、`outputFiles[].fileUrl`、`saved` 本地路径）：

```bash
python3 .claude/skills/aigc-image/scripts/aigc_image.py "提示词" \
  -a 16:9 -r 2K -n "模糊，低质量" -o 输出目录/文件名.png
```

| 参数 | 说明 |
|---|---|
| `prompt` | 正向提示词，无参考图时必填 |
| `-n` | 反向提示词 |
| `-m` / `-v` | 模型 / 版本，默认 `OG` + `image2_high`；只给 `-m` 时取该模型可选值的最后一个 |
| `-r` | 分辨率：4K、2K、1080P |
| `-a` | 比例：16:9、9:16、1:1 等 |
| `--enhance` | 提示词增强：Enabled / Disabled |
| `--ref URL` | 参考图 URL（图生图），可重复 |
| `--ref-file-id ID` | 参考图腾讯云 FileId，可重复 |
| `-o` | 保存位置：以 `/` 结尾为目录，否则为文件名（多张图自动加 `_1`、`_2`），默认 `aigc-output/` |
| `--no-download` | 只要链接不下载 |
| `--task-id ID` | 超时后继续查询已有任务，不重复创建 |
| `--dry-run` | 只打印请求体 |

可选模型版本：OG `image2_low/medium/high`；GG `2.5/3.0/3.1`；SI `4.0/4.5/5.0-lite`；Qwen `0925`；Hunyuan `3.0`；Vidu `q2`；Kling `2.1/3.0/3.0-Omni/O1`。

## 注意

- 需要环境变量 `AIGC_TOKEN`。没有时告诉用户在云环境设置里添加（环境变量或 Network secrets），**不要让用户把 token 贴进聊天**。
- 云环境需要放行 `api.shuyouyinli.cn`（下载结果图还需放行图片所在域名，通常是 `*.vod.myqcloud.com`）。被代理 403 拒绝时，告诉用户在环境的 Network access 里加白名单，不要绕过。
- 失败时脚本会以非 0 退出并给出 `errCodeExt` 含义：`RequestLimitExceeded` 可稍等重试；`InvalidParameter.VoilationContent` 需改写提示词；超时则用 `--task-id` 续查，不要重新创建任务。
- 生成完把图片（`saved` 里的本地文件或 `fileUrl`）发给用户。
