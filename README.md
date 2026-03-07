---
sdk: streamlit
app_file: app.py
domain: nlp
tags:
- 训练
- 对话
- 知识库
license: Apache License 2.0
---

# PrePlay - 预演伙伴

<div align="center">

你的 AI 心理防弹衣

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-green.svg)](https://www.python.org/)

</div>

---

PrePlay 是一款基于 AI 角色扮演的训练应用，帮助用户提升汇报和面试能力。结合**知识库检索**与**认知行为疗法（CBT）**原理，通过双人角色扮演训练，提前熟悉可能的提问方向，锻炼临场应变能力。

## 功能特点

| 功能 | 说明 |
|------|------|
| 🔴 **红方魔鬼导师** | 基于知识库内容，模拟严厉评审提出挑战性问题 |
| 🔵 **蓝方心理教练** | 运用认知行为疗法提供情绪支持和认知重构 |
| 📚 **知识库集成** | 上传 txt/docx 文档，AI 基于真实材料生成问题 |
| 📊 **训练报告** | 训练结束后自动生成结构化分析报告 |
| 💾 **历史记录** | SQLite 本地存储，支持随时继续训练 |

## 快速开始

### 本地运行

```bash
# 1. 克隆项目
git clone https://github.com/C704master/PrePlay3.git
cd PrePlay3

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填写 API 密钥

# 4. 运行应用
streamlit run app.py
```

访问 http://localhost:8501

### 在线体验

[魔搭创空间](https://modelscope.cn/studios/your-username/PrePlay)

## 环境变量配置

在 `.env` 文件中配置以下变量：

```bash
# === 讯飞星火（红方） ===
XUNFEI_RED_WS_URL=wss://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/{id}
XUNFEI_RED_APP_ID=your_app_id
XUNFEI_RED_API_SECRET=your_api_secret
XUNFEI_RED_API_KEY=your_api_key

# === 讯飞星火（蓝方） ===
XUNFEI_BLUE_WS_URL=wss://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/{id}
XUNFEI_BLUE_APP_ID=your_app_id
XUNFEI_BLUE_API_SECRET=your_api_secret
XUNFEI_BLUE_API_KEY=your_api_key

# === 月之暗面（报告生成） ===
MOONSHOT_API_KEY=your_api_key
MOONSHOT_API_URL=https://api.moonshot.cn/v1
MOONSHOT_MODEL=kimi-k2-turbo-preview

# === 讯飞星火知识库 ===
CHATDOC_APP_ID=your_app_id
CHATDOC_API_SECRET=your_api_secret
```

### API 密钥获取

| 服务 | 获取地址 |
|------|---------|
| 讯飞星火 | [console.xfyun.cn](https://console.xfyun.cn/services/cbm) |
| 月之暗面 | [platform.moonshot.cn](https://platform.moonshot.cn/console) |
| 知识库 | [chatdoc.xfyun.cn](https://chatdoc.xfyun.cn/) |

## 使用指南

1. **上传材料**：将汇报 PPT 的文字内容提取后上传（支持 txt、docx）
2. **开始训练**：红方会基于你的材料提出刁钻问题
3. **应对提问**：用专业知识回答红方的挑战，遇到压力可向蓝方寻求建议
4. **导出报告**：训练结束后自动生成包含分析和改进建议的报告

## 项目结构

```
PrePlay/
├── app.py                 # 首页（文件上传、训练记录）
├── config.py              # 环境配置
├── database.py            # SQLite 数据库
├── requirements.txt        # Python 依赖
├── services/             # AI 服务层
│   ├── red_assistant.py   # 红方魔鬼导师
│   ├── blue_assistant.py  # 蓝方心理教练
│   ├── report_service.py  # 报告生成
│   └── knowledge_service.py # 知识库服务
├── utils/                # 工具函数
│   ├── chat_manager.py    # 对话上下文管理
│   └── file_handler.py   # 文件解析
└── pages/               # Streamlit 页面
    ├── 1_训练.py         # 训练界面
    └── 2_报告.py         # 报告界面
```

## 开源协议

[Apache License 2.0](LICENSE)

---

<div align="center">

**⭐ 如果对你有帮助，请给个 Star 支持！**

</div>
