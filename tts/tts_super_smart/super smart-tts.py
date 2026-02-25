# -*- coding:utf-8 -*-

import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import os

# ============== 讯飞语音合成配置 ==============
APPID = '945e2a28'
APISECRET = 'NDI5OTRjMWM4Y2Y0ZjMyY2M2MjY4ZjAw'
APIKEY = 'd5f911b74f1cd73db4b239c7e1c62db9'
WS_URL = 'wss://cbm01.cn-huabei-1.xf-yun.com/v1/private/mcd9m97e6'

# ============== 发音人列表 ==============
VOICES = [
    ("x6_lingxiaoxuan_pro", "聆小璇"),
    ("x6_lingfeiyi_pro", "聆飞逸"),
    ("x5_lingyuzhao_flow", "聆玉昭"),
    ("x6_lingxiaoyue_pro", "聆小玥"),
    ("x6_lingyuyan_pro", "聆玉言"),
    ("x6_shibingnvsheng_mini", "士兵女声"),
    ("x6_ganliannvxing_pro", "干练女性"),
    ("x6_wenrounansheng_mini", "温柔男声"),
    ("x6_cuishounvsheng_pro", "催收女声"),
    ("x6_gaolengnanshen_pro", "高冷男神"),
    ("x6_wennuancixingnansheng_mini", "温暖磁性男声"),
    ("x6_kongbunvsheng_mini", "恐怖女声"),
    ("x6_ruyadashu_pro", "儒雅大叔"),
]

TEST_TEXT = "你好，这是一个测试语音合成的声音，请欣赏我的声音。"


class Ws_Param:
    def __init__(self, text, vcn):
        self.CommonArgs = {"app_id": APPID, "status": 2}
        self.BusinessArgs = {
            "tts": {
                "vcn": vcn,
                "volume": 50,
                "speed": 50,
                "pitch": 50,
                "audio": {
                    "encoding": "lame",
                    "sample_rate": 24000,
                    "channels": 1,
                    "bit_depth": 16,
                }
            }
        }
        self.Data = {
            "text": {
                "encoding": "utf8",
                "compress": "raw",
                "format": "plain",
                "status": 2,
                "seq": 0,
                "text": str(base64.b64encode(text.encode('utf-8')), "UTF8")
            }
        }


class Url:
    def __init__(self, host, path, schema):
        self.host = host
        self.path = path
        self.schema = schema


def parse_url(url):
    stidx = url.index("://")
    host = url[stidx + 3:]
    schema = url[:stidx + 3]
    edidx = host.index("/")
    if edidx <= 0:
        raise Exception("invalid url")
    path = host[edidx:]
    host = host[:edidx]
    return Url(host, path, schema)


def assemble_ws_url():
    u = parse_url(WS_URL)
    host = u.host
    path = u.path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    signature_origin = "host: {}\ndate: {}\nGET {} HTTP/1.1".format(host, date, path)
    signature_sha = hmac.new(APISECRET.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
    authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
        APIKEY, "hmac-sha256", "host date request-line", signature_sha)
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    values = {
        "host": host,
        "date": date,
        "authorization": authorization
    }
    return WS_URL + "?" + urlencode(values)


def create_audio(vcn, filename):
    """生成音频文件"""
    wsUrl = assemble_ws_url()
    result = {"success": False}

    wsParam = Ws_Param(TEST_TEXT, vcn)

    def on_message(ws, message):
        msg = json.loads(message)
        code = msg["header"]["code"]
        if code != 0:
            print(f"  Error: {msg.get('message', msg.get('header', {}).get('message', 'unknown'))}")
            ws.close()
            return
        if "payload" in msg:
            audio = base64.b64decode(msg["payload"]["audio"]["audio"])
            status = msg["payload"]["audio"]["status"]
            with open(filename, 'ab') as f:
                f.write(audio)
            if status == 2:
                result["success"] = True
                ws.close()

    def on_error(ws, error):
        print(f"  Error: {error}")

    def on_close(ws, ts, end):
        pass

    def on_open(ws):
        def run(*args):
            d = {"header": wsParam.CommonArgs,
                 "parameter": wsParam.BusinessArgs,
                 "payload": wsParam.Data}
            ws.send(json.dumps(d))
            if os.path.exists(filename):
                os.remove(filename)
        thread.start_new_thread(run, ())

    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    return result


if __name__ == "__main__":
    print("=" * 60)
    print("讯飞语音合成 - 多发音人测试")
    print("=" * 60)

    for vcn, name in VOICES:
        filename = f"voice_{vcn}.mp3"
        print(f"\n[{name}] ({vcn})")
        result = create_audio(vcn, filename)
        if result["success"]:
            print(f"  SUCCESS -> {filename}")
        else:
            print(f"  FAILED")

    print("\n" + "=" * 60)
    print("All done!")
