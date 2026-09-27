# 小智语音问答服务 - 部署指南

## 1.系统要求

### 硬件要求
- CPU:2核以上
- 内存:4GB以上
- 磁盘:10GB以上可用空间

### 软件要求
- Python
- Windows

---

## 2.系统架构图
```
┌─────────────────────────────────────────┐
│            客户端（浏览器 / App）            │
└───────────────────┬─────────────────────┘
│ HTTP REST API
▼
┌─────────────────────────────────────────┐
│           FastAPI 服务层（端口 8000）     │
│  ┌─────────┬─────────┬─────────┐      │
│  │ 文本问答 │ 语音问答 │ 音频下载 │      │
│  └─────────┴─────────┴─────────┘      │
└───────────────────┬─────────────────────┘
│
┌───────────┼───────────┐
▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│   ASR    │ │   LLM    │ │   TTS    │
│ 语音识别  │ │ 大模型   │ │ 语音合成  │
│(SenseVoice)│(ChatGLM) │(EdgeTTS) │
└──────────┘ └──────────┘ └──────────┘
```

## 3.安装步骤

### 3.1 克隆项目

```bash


```

### 3.2创建虚拟环境

```bash
uv venv
.venv\Scripts\activate # Windows
```

### 3.3安装依赖
 
```bash
uv pip install fastapi uvicorn openai edge-tts
```

### 3.4准备模型文件

```
将SenseVoiceSmall模型放到指定目录：
models/
└── SenseVoiceSmall/
    ├── model.pt
    ├── config.yaml
    ├── am.mvn
    └── ...
```

## 4.配置说明

### 4.1配置LLM API KEY

```
在main.py中修改
client = OpenAI(
    api_key="你的API Key",
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)
```

### 4.2配置ASR模型路径

```
在main.py中修改:
asr_model = AutoModel(
    model="../xiaozhi-esp32-server/main/xiaozhi-server/models/SenseVoiceSmall",  # 改成你的模型路径
    ...
)
```

## 5启动服务

### 5.1开发模式

```bash
uvicorn main:app --reload
```

### 5.2生产模式

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 6.验证服务

### 6.1访问接口文件

打开浏览器访问：
http://127.0.0.1:8000/docs

### 6.2测试文本回答

在/docs页面找到/ask接口，发送测试请求。
