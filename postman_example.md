# Postman测试示例

## 1.导入Collection

1.打开Postman
2.点击Import
3。导入下面的JSON配置

---

## 2.环境变量

在Postman的Environment里设置,

| 变量名 |    值     |  说明  |
|  ---   | ---------|  ----  |
|base_url | http://127.0.0.1:8000| 服务地址|
|session_id|test_001|会话 ID|

---

## 3.请求示例

### 3.1服务状态检查

- **Method**:GET
- **URL**:'{{base_url}}/'

**发送请求后预期返回：**
```json
{
  "message": "你好，小智！"
}
```

### 3.2文本回答

- **Method**:POST
- **URL**:'{{base_url}}/ask'
- **Headers**:'Content-Type:application/json'

**Body:**
```json
{
    "text": "你好",
    "session_id": "{{session_id}}"
}
```

**发送请求后预期返回：**
```json
{
    "session_id": "{{session_id}}",
    "reply": "你好！有什么可以帮助你的吗？",
    "audio_url": "/audio/reply.mp3"
}
```
### 3.3语音回答

- **Method**:POST
- **URL**:'{{base_url}}/ask/audio'
- **Body**:form-data

**Body参数：**

| key | Type | value |
| --- | --- | --- |
| audio | File | 选择一个音频文件 |

**发送请求后预期返回：**
```json
{
    "text": "识别出的文字",
    "reply": "AI 的回复"
}
```

### 3.4获取音频文件

- **Method**:GET
- **URL**:'{{base_url}}/ask/reply.mp3'

**预期结果：**浏览器会播放或下载音频文件

## 4.测试步骤

1.启动服务：uvicorn main:app --reload
2.打开Postman
3.设置环境变量 base_url
4.一次发送上面的请求
5.检查返回结果是否符合预期