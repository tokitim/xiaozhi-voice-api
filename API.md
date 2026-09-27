# 小智语音问答服务 API文档

## 1.服务描述

小智语音问答服务是一个基于FastAPI的REST API 服务，支持文本和语音问答。

### 服务地址

- **Base URL**:'http://127.0.0.1:8000'
- **协议**:HTTP
- **数据格式**:JSON

---

## 2.接口列表

### 2.1服务状态检查

- **URL**:'/'
- **Method**:GET
- **描述**:检查服务是否正常

**响应示例**
```json
{
  "message": "你好，小智！"
}
```
### 2.2 文本问答
- **URL**:'/ask'
- **Method**:POST
- **描述**:发送文本，获取AI回复

**请求参数**：
- **参数名**:'text','session_id'
- **类型**:string,string
- **说明**:用户输入文本,会话 ID

**请求示例**
```json
{
  "text": "你好",
  "session_id": "string"
}
```

**响应参数**
- **参数名**:'session_id','reply','audio_url'
- **类型**:string,string,string
- **说明**:会话 ID;AI的回复文本;回复语音的URL 

**响应示例**
```json
{
  "session_id": "string",
  "reply": "你好👋！有什么可以帮助你的吗？",
  "audio_url": "/audio/reply.mp3"
}
```
### 2.3语言回答

- **URL**:'/ask/audio'
- **Method**:POST
- **描述**:上传音频文件，获取结果和AI回复

**请求参数**:
- **参数名**:'audio'
- **类型**:file
- **说明**:音频文件（mp3）

**响应参数**:
- **参数名**:'text','reply'
- **类型**:string,string
- **说明**:识别文本；AI的回复文本

**响应实例**:
```json
{
  "text": "开饭时间早上9点至下午五点。",
  "reply": "好的，根据您提供的时间段，开饭时间是从早上9点持续到下午5点。如果您需要关于这个时间段内的任何帮助，比如安排餐饮服务、菜单建议或者时间表安排，请告诉我具体需求。"
}
```

### 2.4获取音频文件

- **URL**:'/audio/{filename}'
- **Method**:GET
- **描述**:获取生成的音频文件

**路径参数**：
- **参数名**:'filename'
- **类型**:string
- **说明**:音频文件名

## 3.错误码

HTTP 状态码	   说明
  200	     请求成功
  422	     请求参数错误
  500	     服务器内部错误

## 4.示例

**cURL示例**:
```
#文本回答
curl -X POST "http://127.0.0.1:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"text": "你好"}'

#语音回答
curl -X POST "http://127.0.0.1:8000/ask/audio" \
     -F "audio=@test.wav"
```