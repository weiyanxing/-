# AIGC 生图接口文档

## 1. 创建 AIGC 生图任务

### 请求信息

- **URL**: `POST https://api.shuyouyinli.cn/bzsq/member/cms/aigc/image/create`
- **Content-Type**: `application/json`
- **Headers**: `Authorization: {token}`, `accessToken: bz`

### 请求参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| ModelName | String | 否 | OG | 模型名称，可选值：OG、GG、SI、Qwen、Hunyuan、Vidu、Kling |
| ModelVersion | String | 否 | image2_high | 模型版本，各模型可选值见下方说明 |
| Prompt | String | 否(无参考图时必填) | - | 正向提示词 |
| NegativePrompt | String | 否 | - | 反向提示词 |
| Resolution | String | 否 | - | 分辨率，如 4K、2K、1080P |
| AspectRatio | String | 否 | - | 画面比例，如 16:9、9:16、1:1 |
| EnhancePrompt | String | 否 | - | 提示词增强，可选值：Enabled、Disabled |
| SubAppId | Long | 否(配置中有则自动填充) | - | 点播应用 ID |
| InputRegion | String | 否(配置中有则自动填充) | - | 输入区域，可选值：Mainland、Oversea、OverseaUSWest |
| FileInfos | Array | 否 | - | 参考图片信息 |

### FileInfos 子项

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| Type | String | 是 | 文件类型，可选值：Url、File |
| FileId | String | Type=File时必填 | 腾讯云文件 ID |
| Url | String | Type=Url时必填 | 图片 URL 地址 |

### ModelVersion 可选值

| ModelName | 可选值 |
|-----------|--------|
| OG | image2_low、image2_medium、image2_high |
| GG | 2.5、3.0、3.1 |
| SI | 4.0、4.5、5.0-lite |
| Qwen | 0925 |
| Hunyuan | 3.0 |
| Vidu | q2 |
| Kling | 2.1、3.0、3.0-Omni、O1 |

### 请求示例

```json
{
  "ModelName": "OG",
  "ModelVersion": "image2_high",
  "Prompt": "一只在草地上奔跑的金毛犬，阳光明媚",
  "NegativePrompt": "模糊，低质量",
  "Resolution": "4K",
  "AspectRatio": "16:9"
}
```

带参考图示例：

```json
{
  "ModelName": "OG",
  "ModelVersion": "image2_high",
  "Prompt": "参考这张图片的风格，生成一只猫",
  "Resolution": "4K",
  "AspectRatio": "16:9",
  "FileInfos": [
    {
      "Type": "Url",
      "Url": "https://example.com/reference.jpg"
    }
  ]
}
```

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | Integer | 状态码，200=成功 |
| msg | String | 提示信息 |
| data.taskId | String | 任务 ID |
| data.requestId | String | 请求 ID |

### 响应示例

```json
{
  "code": 200,
  "msg": "AIGC生图任务创建成功",
  "data": {
    "taskId": "125xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "requestId": "xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  }
}
```

---

## 2. 查询 AIGC 任务详情

### 请求信息

- **URL**: `GET https://api.shuyouyinli.cn/bzsq/member/cms/aigc/image/task?taskId={taskId}`
- **Headers**: `Authorization: {token}`, `accessToken: bz`

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| taskId | String | 是 | 任务 ID（创建任务时返回） |

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | Integer | 状态码，200=成功 |
| msg | String | 提示信息 |
| data.taskType | String | 任务类型 |
| data.requestId | String | 请求 ID |
| data.taskId | String | 任务 ID |
| data.status | String | 任务状态：PROCESSING=处理中、FINISH=已完成 |
| data.errCodeExt | String | 扩展错误码，空=成功 |
| data.message | String | 错误信息 |
| data.progress | Long | 任务进度 0-100 |
| data.outputFiles | Array | 输出图片列表（任务完成后有值） |

### outputFiles 子项

| 参数名 | 类型 | 说明 |
|--------|------|------|
| fileUrl | String | 图片地址 |
| fileId | String | 文件 ID（永久存储时有值） |
| fileType | String | 文件类型 |
| storageMode | String | 存储模式：Permanent=永久、Temporary=临时 |

### errCodeExt 枚举值

| 值 | 说明 |
|----|------|
| (空) | 成功 |
| RequestLimitExceeded | 模型调用超出并发限制 |
| InvalidParameter.VoilationContent | 输入 prompt 违反内容安全策略 |
| InvalidParameterValue | 参数错误 |
| FailedOperation | 模型任务堆积 |
| InternalError | 内部错误 |

### 响应示例 - 处理中

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "taskType": "AigcImage",
    "taskId": "125xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "status": "PROCESSING",
    "progress": 50,
    "errCodeExt": "",
    "message": ""
  }
}
```

### 响应示例 - 已完成

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "taskType": "AigcImage",
    "taskId": "125xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "status": "FINISH",
    "progress": 100,
    "errCodeExt": "",
    "message": "",
    "outputFiles": [
      {
        "fileUrl": "https://xxx.vod.myqcloud.com/xxx/aigc_image.png",
        "fileId": "5285890781xxxxxx",
        "fileType": "png",
        "storageMode": "Permanent"
      }
    ]
  }
}
```

### 响应示例 - 任务失败

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "taskType": "AigcImage",
    "taskId": "125xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "status": "FINISH",
    "progress": 100,
    "errCodeExt": "InvalidParameter.VoilationContent",
    "message": "输入prompt违反内容安全策略"
  }
}
```

---

## Nacos 配置项

| 配置项 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| vod.secret-id | 是 | - | 腾讯云 SecretId |
| vod.secret-key | 是 | - | 腾讯云 SecretKey |
| vod.region | 否 | ap-guangzhou | VOD 区域 |
| vod.sub-app-id | 否 | - | 点播应用 ID（2023.12.25后开通必填） |
| vod.input-region | 否 | Mainland | 输入区域 |
