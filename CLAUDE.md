# 项目约定

- **生图一律调用 AIGC 生图接口**（`POST https://api.shuyouyinli.cn/bzsq/member/cms/aigc/image/create`），用 `aigc-image` 技能：
  `python3 .claude/skills/aigc-image/scripts/aigc_image.py "提示词" -a 16:9 -o 输出路径.png`
  需要环境变量 `AIGC_TOKEN`，详见 `.claude/skills/aigc-image/SKILL.md`。
