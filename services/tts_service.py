# coding: utf-8
"""
讯飞 TTS 服务
支持：
- 双角色语音
- 长文本自动分句
- 自动拼接音频
"""

import websocket
import datetime
import hashlib
import base64
import hmac
import json
import os
import re
import ssl
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime


# ==============================
# 音色配置
# ==============================

RED_VCN = "xiaoyu"     # 红方：男声
BLUE_VCN = "xiaoyan"   # 蓝方：女声


# ==============================
# 讯飞配置
# ==============================

from config import (
    XUNFEI_TTS_APP_ID,
    XUNFEI_TTS_API_KEY,
    XUNFEI_TTS_API_SECRET
)


# ==============================
# 文本处理
# ==============================

def optimize_text_for_tts(text):
    """优化文本停顿"""
    text = text.replace("。", "。 ")
    text = text.replace("，", "， ")
    text = text.replace("？", "？ ")
    text = text.replace("！", "！ ")
    return text.strip()


def split_text(text, max_len=120):
    """长文本分句"""
    sentences = re.split(r"[。！？]", text)

    result = []
    buffer = ""

    for s in sentences:

        if len(buffer) + len(s) < max_len:
            buffer += s + "。"
        else:
            result.append(buffer)
            buffer = s + "。"

    if buffer:
        result.append(buffer)

    return result


def merge_audio(files, output):
    """拼接音频"""
    with open(output, "wb") as outfile:

        for f in files:

            with open(f, "rb") as infile:
                outfile.write(infile.read())

            os.remove(f)


# ==============================
# TTS客户端
# ==============================

class TTSClient:

    def __init__(self):

        self.appid = XUNFEI_TTS_APP_ID
        self.apikey = XUNFEI_TTS_API_KEY
        self.apisecret = XUNFEI_TTS_API_SECRET

        self.host = "tts-api.xfyun.cn"
        self.path = "/v2/tts"
        self.url = f"wss://{self.host}{self.path}"

    # 生成鉴权URL
    def create_url(self):

        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        signature_origin = f"host: {self.host}\n"
        signature_origin += f"date: {date}\n"
        signature_origin += f"GET {self.path} HTTP/1.1"

        signature_sha = hmac.new(
            self.apisecret.encode(),
            signature_origin.encode(),
            hashlib.sha256
        ).digest()

        signature_sha = base64.b64encode(signature_sha).decode()

        authorization_origin = (
            f'api_key="{self.apikey}", '
            f'algorithm="hmac-sha256", '
            f'headers="host date request-line", '
            f'signature="{signature_sha}"'
        )

        authorization = base64.b64encode(
            authorization_origin.encode()
        ).decode()

        params = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }

        return self.url + "?" + urlencode(params)

    # 单段TTS
    def synthesize_once(self, text, output_path, vcn):

        ws_url = self.create_url()

        audio_chunks = []

        def on_message(ws, message):

            data = json.loads(message)

            code = data["code"]

            if code != 0:
                print("TTS错误:", data)
                ws.close()
                return

            audio = base64.b64decode(data["data"]["audio"])
            audio_chunks.append(audio)

            if data["data"]["status"] == 2:
                ws.close()

        def on_open(ws):

            text_base64 = base64.b64encode(text.encode()).decode()

            payload = {
                "common": {
                    "app_id": self.appid
                },
                "business": {
                    "aue": "lame",
                    "vcn": vcn,
                    "tte": "utf8",
                    "speed": 50,
                    "volume": 50,
                    "pitch": 50
                },
                "data": {
                    "status": 2,
                    "text": text_base64
                }
            }

            ws.send(json.dumps(payload))

        ws = websocket.WebSocketApp(
            ws_url,
            on_message=on_message
        )

        ws.on_open = on_open
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

        if not audio_chunks:
            return False

        with open(output_path, "wb") as f:
            for chunk in audio_chunks:
                f.write(chunk)

        return True

    # 长文本TTS
    def synthesize_long(self, text, output_path, vcn):

        text = optimize_text_for_tts(text)

        parts = split_text(text)

        temp_files = []

        for i, part in enumerate(parts):

            temp_path = output_path.replace(".mp3", f"_{i}.mp3")

            ok = self.synthesize_once(part, temp_path, vcn)

            if ok:
                temp_files.append(temp_path)

        merge_audio(temp_files, output_path)

        return True


# ==============================
# 全局实例
# ==============================

tts_client = TTSClient()


# ==============================
# 对外接口
# ==============================

def synthesize_speech(text, role, session_id, round_num):

    if role == "red":
        vcn = RED_VCN
    else:
        vcn = BLUE_VCN

    project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    audio_dir = os.path.join(project_root, "static", "audios")
    os.makedirs(audio_dir, exist_ok=True)

    filename = f"{role}_{session_id}_{round_num}.mp3"
    audio_path = os.path.join(audio_dir, filename)

    print(f"TTS合成: {role} | {vcn}")

    success = tts_client.synthesize_long(text, audio_path, vcn)

    if success:
        print("TTS成功:", audio_path)
        return audio_path
    else:
        print("TTS失败")
        return None