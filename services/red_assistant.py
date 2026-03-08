
# coding: utf-8
"""
红方魔鬼导师服务
"""
import _thread as thread
import base64
import hashlib
import hmac
import json
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlparse, urlencode
from wsgiref.handlers import format_date_time
import websocket
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from config import RED_CONFIG


class WsParam:
    """WebSocket 鉴权参数生成"""
    def __init__(self, APPID, APIKey, APISecret, Assistant_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(Assistant_url).netloc
        self.path = urlparse(Assistant_url).path
        self.Assistant_url = Assistant_url

    def create_url(self):
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        url = self.Assistant_url + '?' + urlencode(v)
        return url


class RedAssistant:
    """红方魔鬼导师客户端"""

    def __init__(self, config=None):
        self.config = config or RED_CONFIG
        self.ws_url = self.config["ws_url"]
        self.app_id = self.config["app_id"]
        self.api_secret = self.config["api_secret"]
        self.api_key = self.config["api_key"]
        self.sid = ""
        self.answer = ""
        self.ws = None

    def _gen_params(self, question, chat_history=None):

        system_prompt = """# 红方·魔鬼导师核心指令

## 你是谁
你是红方·魔鬼导师 - 一个极度严苛、从不表扬、永远在挑刺的评审专家。你的存在意义就是让用户提前经历真实汇报的压力，在真正的导师面前不再恐惧。

## 铁律（必须遵守）
1. **永不肯定**：绝对不说'好'、'不错'、'可以'等任何正面词汇
2. **简明扼要**：一次问一个问题，不超过15字
3. **专业碾压**：所有批评都基于专业标准，让用户心服口服但难受
4. **永远刁钻**：从用户的回答中挑不足反问

## 最重要的输出格式规则
你必须像**真人说话**一样输出，禁止任何形式的条目化、分点、编号：

禁止使用的格式：
- 不要用'1.'、'2.'、'3.'这样的编号
- 不要用'第一'、'第二'、'第三'这样的分点
- 不要用'·'、'-'、'*'这样的列表符号
- 不要用'【】'给内容加标题
- 不要分段列出问题

正确的说话方式：
- 像真人导师一样，一段话连贯地说出来
- 用自然的语气转折："话说回来"、"再者"、"另外我注意到"
- 问题之间用口语连接："你这数据不对啊，还有你那个逻辑...怎么回事？"
- 适当加入语气词："嗯？"、"啊？"、"这不对吧"

## 回答质量评判（只有负面）
- **用户答得再好** -> 鸡蛋里挑骨头 + 追问更刁钻角度
- **用户答得一般** -> 直接指出所有缺陷 + 逼迫补充
- **用户答得差** -> 严厉斥责 + 直接宣告挑战失败（不给机会）

## 追问节奏控制
- 同一问题最多追问4次，满4次必须换维度
- 切换语气："算了，这个问题你接不住，问下一个"
- 永远不要承认用户'答对了'

## 语气模板库（参考，不要照搬）

【挑剔时】
- "你这只是皮毛啊，我问的是本质问题..."
- "数据是背熟了，但你这个逻辑...嗯？"

【指出漏洞时】
- "漏洞百出你知道吗？第一...算了你自己听不出来？"
- "逻辑混乱成这样，你自己念念，这能通吗？"

【斥责并宣告失败时】
- "完全错误！挑战失败。"
- "就这水平？挑战结束。"
- "答非所问，失败。"
- "这种质量也敢来？挑战终止。"

【切换维度时】
- "基础问题都过不了，换个简单的问问你"
- "算了，这个问题你接不住，我们换个问题"

## 提问维度矩阵（用来思考问什么）
按顺序轮换：
1. 数据层面：来源、分布、预处理、统计效力
2. 方法层面：选型理由、参数调优、对比SOTA
3. 逻辑层面：论证链条、假设合理性、边界条件
4. 价值层面：创新点、贡献度、落地可行性

## 输出示例（参考语气，不要照抄内容）

错误示范（禁止）：
1. 数据缺失质问：你的用户身份标识为什么空白？
2. 逻辑断裂追责：你的触发机制设计在哪层？
3. 可行性拷问：10万并发怎么处理？

正确示范：
"你这用户身份标识怎么是空白的？啊？而且你写的'开始'这两个字，到底是用户点的还是系统自动跳的？把后台日志调出来我看看，第0.5秒内的用户操作热力图有吗？停留时长呢？"

"还有啊，你这架构图第三层，用户就输了个'开始'，你的触发机制设计在哪层？如果这是首屏测试，A/B版本对比数据在哪？"

"话说回来，假设现在真有10万个人同时点这个'开始'，你的分布式系统怎么保证不卡？具体到毫秒级的容错阈值是多少？说不出来现在就给我现场重构！"

记住：越像真人说话越好，加一些动作描述，越严厉越好，一次只问一个问题，不要有分点和符号！"""
    
        messages = []
        
        # 添加 system prompt
        messages.append({"role": "system", "content": system_prompt})
        
        # 添加对话历史
        if chat_history:
            messages.extend(chat_history)
        
        # 添加当前问题
        messages.append({"role": "user", "content": question})

        data = {
            "header": {
                "app_id": self.app_id,
                "uid": "user123"
            },
            "parameter": {
                "chat": {
                    "domain": "generalv3.5",
                    "temperature": 0.8,
                    "max_tokens": 2048,
                    "top_k": 5
                }
            },
            "payload": {
                "message": {
                    "text": messages
                }
            }
        }
        return data
      
    def _on_message(self, ws, message):
        """收到websocket消息的处理"""
        data = json.loads(message)

        code = data['header']['code']
        if code != 0:
            print(f'红方请求错误: {code}, {data}')
            ws.close()
            return

        if 'sid' in data['header']:
            self.sid = data['header']['sid']

        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]

        print(content, end="")
        self.answer += content

        if status == 2:
            ws.close()

    def _on_error(self, ws, error):
        """收到websocket错误的处理"""
        print(f"红方错误: {error}")

    def _on_close(self, ws, one, two):
        """收到websocket关闭的处理"""
        pass

    def _on_open(self, ws):
        """收到websocket连接建立的处理"""
        thread.start_new_thread(self._run, (ws,))

    def _run(self, ws):
        """发送消息"""
        data = json.dumps(self._gen_params(ws.question, ws.chat_history))
        ws.send(data)

    def chat(self, question, chat_history=None):
        """
        与红方对话一次

        Args:
            question: 用户问题
            chat_history: 对话历史（可选）

        Returns:
            (answer, sid): 回答内容和会话ID
        """
        wsParam = WsParam(
            self.app_id,
            self.api_key,
            self.api_secret,
            self.ws_url
        )
        wsUrl = wsParam.create_url()

        self.answer = ""

        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(
            wsUrl,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open
        )

        ws.question = question
        ws.chat_history = chat_history

        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

        return self.answer, self.sid


# 全局实例
_red_assistant = None


def get_red_assistant():
    """获取红方实例（单例）"""
    global _red_assistant
    if _red_assistant is None:
        _red_assistant = RedAssistant()
    return _red_assistant


def chat_with_red(question, chat_history=None):
    """
    与红方魔鬼导师对话一次

    Args:
        question: 用户问题
        chat_history: 对话历史（可选）

    Returns:
        (answer, sid): 回答内容和会话ID
    """
    assistant = get_red_assistant()
    return assistant.chat(question, chat_history)



