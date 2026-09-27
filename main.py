import os
import re
import edge_tts
from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel
from funasr import AutoModel


app=FastAPI()

@app.get("/")
def read_root():
    return{"message":"你好，小智！"}

class AskRequest(BaseModel):
    text:str
    session_id:str=None

client = OpenAI(
    api_key="你的API Key",
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)
conversations={}

asr_model=AutoModel(
    model="../xiaozhi-esp32-server/main/xiaozhi-server/models/SenseVoiceSmall",
    vad_kwargs={"max_single_segment_time":30000},
    disable_update=True,
    hub="hf",
    local_files_only=True,
    # device="cuda:0",  # 启用GPU加速
)

TTS_VOICE="zh-CN-XiaoxiaoNeural"
async def text_to_speech(text:str,output_path:str):
    """文字转语音"""
    communicate=edge_tts.Communicate(
        text,
        voice=TTS_VOICE,
    )
    await communicate.save(output_path)

@app.post("/ask")
async def ask(request:AskRequest):
    #生成或使用session_id
    session_id=request.session_id or "default"

    if session_id not in conversations:
        conversations[session_id]=[]

    #将用户的信息加入历史
    conversations[session_id].append({"role":"user","content":request.text})

    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=conversations[session_id]
    )
    reply = response.choices[0].message.content

    conversations[session_id].append({"role":"user","content":request.text})

    #生成语音
    audio_dir="output"
    os.makedirs(audio_dir,exist_ok=True)
    audio_path=f"{audio_dir}/reply.mp3"
    await text_to_speech(reply,audio_path)

    return{
        "session_id":session_id,
        "reply":reply,
        "audio_url":f"/audio/reply.mp3"
    }

from fastapi.responses import FileResponse
@app.get("/audio/{filename}")
async def get_audio(filename:str):
    audio_path=f"output/{filename}"
    return FileResponse(audio_path,media_type="audio/mpeg")

from fastapi import UploadFile,File

@app.post("/ask/audio")
async def ask_audio(
    audio:UploadFile=File(...)
):
    #保存上传音频
    upload_dir="uploads"
    os.makedirs(upload_dir,exist_ok=True)
    audio_path=f"{upload_dir}/{audio.filename}"

    with open(audio_path,"wb") as f:
        f.write(await audio.read())

    #语音识别
    result=asr_model.generate(
        input=audio_path,
        cache={},
        language="auto",
        use_itn=True,
        batch_size_s=60,
    )
    text=result[0]["text"]
    text=re.sub(r'<\|.*?\|>', '', text)

    #调用LLM生成回复
    response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[
                {"role":"user","content":text}
            ]
        )
    reply=response.choices[0].message.content

    return{
        "text":text,
        "reply":reply
    }