"""
<one line to give the program's name and a brief idea of what it does.>
Copyright (C) 2025  lost0427

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import requests
import json
import logging
from bs4 import BeautifulSoup
import re
import markdown
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydub import AudioSegment
import os
import edge_tts
import uuid
import time
import asyncio


def configure_logging():
    logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

configure_logging()

def markdown_to_text(md: str) -> str:
    html = markdown.markdown(md)
    return BeautifulSoup(html, "html.parser").get_text()

def fetch_messages(url: str):
    pattern = r'^https://www\.doubao\.com/thread/[a-zA-Z0-9]+$'
    if not re.match(pattern, url):
        raise ValueError("URL格式不正确，应为 https://www.doubao.com/thread/xxxxxx 格式")
    logging.info(f"接受URL：{url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/134.0.0.0 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # 获取最后一个 <script>
    scripts = soup.find_all("script")
    last_script = scripts[-1].string or scripts[-1].text
    if not last_script:
        raise ValueError("页面结构异常：最后一个 <script> 标签为空，无法提取数据")

    # 提取 window._ROUTER_DATA 的 JSON
    match = re.search(r'window\._ROUTER_DATA\s*=\s*(\{.*\});?', last_script, re.S)
    if not match:
        raise ValueError("页面结构异常：找不到 window._ROUTER_DATA JSON，无法提取数据")

    json_str = match.group(1)
    data = json.loads(json_str)

    messages = []

    def find_messages(obj):
        if isinstance(obj, dict):
            if "message_list" in obj and isinstance(obj["message_list"], list):
                for item in obj["message_list"]:
                    if isinstance(item, dict) and item.get("content_type") == 1:
                        content = item.get("content", [])
                        if isinstance(content, list):
                            for c in content:
                                if isinstance(c, dict) and "text" in c:
                                    messages.append(markdown_to_text(c["text"]))
                                elif isinstance(c, str):
                                    try:
                                        c_json = json.loads(c)
                                        if "text" in c_json:
                                            messages.append(markdown_to_text(c_json["text"]))
                                    except Exception:
                                        messages.append(c)
                        elif isinstance(content, str):
                            try:
                                c_json = json.loads(content)
                                if "text" in c_json:
                                    messages.append(markdown_to_text(c_json["text"]))
                            except Exception:
                                messages.append(content)
            for v in obj.values():
                find_messages(v)
        elif isinstance(obj, list):
            for v in obj:
                find_messages(v)

    find_messages(data)
    return messages

def cmp_mp3(input_file):
    audio = AudioSegment.from_file(input_file)
    audio = audio + 10
    audio.export(
        input_file,
        format="mp3",
        parameters=[
            "-b:a", "24k",
            "-ac", "1"
        ]
    )
    logging.info("压缩完成")

async def text_to_mp3(text_list: list[str], voice="zh-CN-XiaoxiaoNeural", output_file="output.mp3"):
    tasks = []
    for i, text in enumerate(text_list):
        task = generate_audio_segment(text, voice, i)
        tasks.append(task)
    
    audio_segments = await asyncio.gather(*tasks)
    
    audio_data = bytearray()
    for segment in audio_segments:
        audio_data.extend(segment)
    
    with open(output_file, "wb") as f:
        f.write(bytes(audio_data))

    cmp_mp3(output_file)

    logging.info(f"音频已保存为 {output_file}")
    return output_file

async def generate_audio_segment(text: str, voice: str, segment_index: int):
    audio_data = bytearray()
    communicate = edge_tts.Communicate(text, voice)
    
    async for chunked in communicate.stream():
        if chunked["type"] == "audio":
            audio_data.extend(chunked["data"])
    
    # logging.info(f"音频片段 {segment_index} 生成完成")
    return audio_data



app = FastAPI()
app.mount("/audios", StaticFiles(directory="audios"), name="audios")
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/", response_class=FileResponse)
async def home():
    return("index.html")

@app.post("/process")
async def process_url(request: Request):
    try:
        data = await request.json()
        url = data.get("url")
        
        if not url:
            return JSONResponse({"code": -1, "message": "URL不能为空"})
        
        messages = fetch_messages(url)
        
        if not messages:
            return JSONResponse({"code": -1, "message": "未找到任何消息内容"})
        
        result = "".join(messages)

        output_dir = "audios"
        os.makedirs(output_dir, exist_ok=True)

        filename = f"{uuid.uuid4().hex}.mp3"
        output_path = os.path.join(output_dir, filename)

        start_time = time.time()

        await text_to_mp3(messages, "zh-CN-XiaoxiaoNeural", output_path)

        end_time = time.time()
        elapsed_time = end_time - start_time

        logging.info(f"耗时: {elapsed_time:.2f} 秒")

        audio_url = f"/audios/{filename}"
        return JSONResponse({
            "code": 1,
            "message": "转换成功",
            "audio_urls": [audio_url]
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse({"code": -1, "message": f"处理失败: {str(e)}"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
