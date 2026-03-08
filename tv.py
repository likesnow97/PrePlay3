# -*- coding:utf-8 -*-
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import ssl
from wsgiref.handlers import format_date_time
from time import mktime
from datetime import datetime
import _thread as thread

# appid = "5239fcd0"
# apikey = "c757134db213fbc05e8d58f51f283734"
# apisecret = "OTE4MzE4OWU4ZjE2Njg4MzlhMmNmYzJk"

appid = "945e2a28"
apikey = "d5f911b74f1cd73db4b239c7e1c62db9"
apisecret = "NDI5OTRjMWM4Y2Y0ZjMyY2M2MjY4ZjAw"

text = "全红婵，2007年3月28日出生于广东省湛江市，中国国家跳水队女运动员，主项为女子10米跳台。"


class Ws_Param(object):
    def __init__(self, APPID, APIKey, APISecret, Text):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text

        self.CommonArgs = {"app_id": self.APPID}

        self.BusinessArgs = {
            "aue": "lame",
            "auf": "audio/L16;rate=16000",
            "vcn": "aislingxi",
            "speed": 45,
            "pitch": 50,
            "volume": 80,
            "tte": "utf8"
        }

        self.Data = {
            "status": 2,
            "text": str(base64.b64encode(self.Text.encode("utf-8")), "UTF8")
        }

    def create_url(self):
        url = "wss://tts-api.xfyun.cn/v2/tts"
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        signature_origin = "host: tts-api.xfyun.cn\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET /v2/tts HTTP/1.1"

        signature_sha = hmac.new(
            self.APISecret.encode("utf-8"),
            signature_origin.encode("utf-8"),
            digestmod=hashlib.sha256
        ).digest()

        signature_sha = base64.b64encode(signature_sha).decode()

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha}"'
        authorization = base64.b64encode(authorization_origin.encode()).decode()

        v = {
            "authorization": authorization,
            "date": date,
            "host": "tts-api.xfyun.cn"
        }

        url = url + "?" + urlencode(v)

        return url


def on_message(ws, message):
    message = json.loads(message)

    if message["code"] != 0:
        print("错误:", message["message"])
        ws.close()
        return

    audio = message["data"]["audio"]
    audio = base64.b64decode(audio)

    with open("demo.mp3", "ab") as f:
        f.write(audio)

    if message["data"]["status"] == 2:
        print("合成完成，生成 demo.mp3")
        ws.close()


def on_error(ws, error):
    print("error:", error)


def on_close(ws, *args):
    print("连接关闭")


def on_open(ws):
    def run(*args):
        data = {
            "common": wsParam.CommonArgs,
            "business": wsParam.BusinessArgs,
            "data": wsParam.Data,
        }

        ws.send(json.dumps(data))

    thread.start_new_thread(run, ())


if __name__ == "__main__":

    wsParam = Ws_Param(appid, apikey, apisecret, text)

    websocket.enableTrace(False)

    wsUrl = wsParam.create_url()

    ws = websocket.WebSocketApp(
        wsUrl,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.on_open = on_open

    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})