"""
Claude 官网风格主题 - 暖白米灰配色
修复按钮和元素大小适配问题
"""

def apply_claude_theme():
    """应用 Claude 官网风格的浅色暖白主题"""
    import streamlit as st

    claude_css = """
    <style>
    /* ===== Claude 官网风格主题 - 暖白米灰配色 ===== */

    /* 全局背景 - 暖白米白 */
    .stApp {
        background-color: #F7F6F3 !important;
        color: #5B5650 !important;
        font-family: ui-serif, Georgia, "Times New Roman", "Songti SC", "SimSun", serif !important;
    }

    /* 页面容器 */
    [data-testid="stAppViewContainer"] {
        background-color: #F7F6F3 !important;
    }

    /* 侧边栏背景 - 略深的暖灰白 */
    [data-testid="stSidebar"] {
        background-color: #F1EFEB !important;
    }

    /* 标题样式 - 深灰褐色 - 衬线字体 */
    h1, h2, h3, h4, h5, h6 {
        color: #3A3632 !important;
        font-family: ui-serif, Georgia, "Times New Roman", "Songti SC", "SimSun", serif !important;
        font-weight: 500 !important;
    }

    h1 {
        font-size: 1.8rem !important;
        letter-spacing: -0.02em !important;
    }

    h2 {
        font-size: 1.3rem !important;
        letter-spacing: -0.01em !important;
    }

    h3 {
        font-size: 1.05rem !important;
    }

    /* 副标题 */
    .stSubheader {
        color: #3A3632 !important;
        font-size: 1.1rem !important;
    }

    /* 副标题和 caption */
    p, span, div {
        color: #5B5650 !important;
    }

    .stCaption {
        color: #8A847C !important;
        font-size: 0.8rem !important;
    }

    /* 链接 */
    a {
        color: #8A847C !important;
    }

    a:hover {
        color: #3A3632 !important;
    }

    /* ===== 按钮样式 - 透明背景 + 悬停浅橙 + 持续涟漪 ===== */
    .stButton button {
        background-color: transparent !important;
        color: #5B5650 !important;
        border: 1px solid #E7E2DA !important;
        border-radius: 10px !important;
        font-weight: 450 !important;
        font-size: 0.75rem !important;
        padding: 4px 10px !important;
        min-height: auto !important;
        height: auto !important;
        position: relative !important;
        overflow: visible !important;
        white-space: nowrap !important;
        line-height: 1.2 !important;
        box-sizing: border-box !important;
        margin: 0 !important;
    }

    /* Streamlit 按钮外层容器 */
    [data-testid="stBaseButton-secondary"],
    [data-testid="stBaseButton-primary"] {
        background-color: transparent !important;
        border: 1px solid #E7E2DA !important;
        border-radius: 10px !important;
        padding: 4px 10px !important;
    }

    [data-testid="stBaseButton-secondary"]:hover,
    [data-testid="stBaseButton-primary"]:hover {
        border-color: #C97A52 !important;
    }

    /* 按钮内容 */
    [data-testid="stBaseButton-secondary"] p,
    [data-testid="stBaseButton-primary"] p {
        margin: 0 !important;
        padding: 0 !important;
        font-size: 0.75rem !important;
    }

    /* 涟漪效果容器 */
    .stButton > button .ripple {
        position: absolute !important;
        border-radius: 50% !important;
        background: radial-gradient(circle, rgba(232, 200, 175, 0.8) 0%, rgba(201, 122, 82, 0.6) 100%) !important;
        transform: scale(0) !important;
        animation: ripple-effect 1.5s ease-out infinite !important;
        pointer-events: none !important;
    }

    @keyframes ripple-effect {
        0% {
            transform: scale(0);
            opacity: 1;
        }
        100% {
            transform: scale(2.5);
            opacity: 0;
        }
    }

    .stButton > button:hover {
        background-color: #F5E6DE !important;
        border-color: #C97A52 !important;
        color: #3A3632 !important;
    }

    /* 悬停时添加多个涟漪 */
    .stButton > button:hover::before,
    .stButton > button:hover::after {
        content: '' !important;
        position: absolute !important;
        width: 100px !important;
        height: 100px !important;
        left: 50% !important;
        top: 50% !important;
        margin-left: -50px !important;
        margin-top: -50px !important;
        border-radius: 50% !important;
        background: radial-gradient(circle, rgba(232, 200, 175, 0.6) 0%, rgba(201, 122, 82, 0.3) 50%, transparent 70%) !important;
        transform: scale(0) !important;
        animation: ripple-continuous 2s ease-out infinite !important;
        pointer-events: none !important;
    }

    .stButton > button:hover::after {
        animation-delay: 0.6s !important;
    }

    @keyframes ripple-continuous {
        0% {
            transform: scale(0);
            opacity: 0.8;
        }
        100% {
            transform: scale(2);
            opacity: 0;
        }
    }

    .stButton > button:disabled {
        opacity: 0.5 !important;
        cursor: not-allowed !important;
    }

    /* 主要按钮 - 同样风格 */
    .stButton > button[kind="primary"] {
        background-color: transparent !important;
        color: #3A3632 !important;
        border: 1px solid #E7E2DA !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #F5E6DE !important;
        border-color: #C97A52 !important;
    }

    /* 按钮容器宽度 */
    .stButton > button[use_container_width="true"] {
        width: 100% !important;
    }

    /* ===== 输入框样式 ===== */
    .stTextInput > div > div {
        background-color: #FBFAF8 !important;
    }

    .stTextInput > div > div > input {
        background-color: #FBFAF8 !important;
        color: #3A3632 !important;
        border: 1px solid #E7E2DA !important;
        border-radius: 10px !important;
        font-size: 0.95rem !important;
        padding: 0.6rem 0.9rem !important;
        min-height: 42px !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #C97A52 !important;
        outline: none !important;
        box-shadow: none !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #A7A198 !important;
    }

    /* TextArea */
    .stTextArea > div > div {
        background-color: #FBFAF8 !important;
    }

    .stTextArea > div > div > textarea {
        background-color: #FBFAF8 !important;
        color: #3A3632 !important;
        border: 1px solid #E7E2DA !important;
        border-radius: 10px !important;
        font-size: 0.95rem !important;
        padding: 0.6rem 0.9rem !important;
        min-height: 80px !important;
    }

    .stTextArea > div > div > textarea:focus {
        border-color: #C97A52 !important;
        outline: none !important;
        box-shadow: none !important;
    }

    .stTextArea > div > div > textarea::placeholder {
        color: #A7A198 !important;
    }

    /* ===== 文件上传器 ===== */
    [data-testid="stFileUploader"] {
        background-color: #FBFAF8 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        border: 1px dashed #E7E2DA !important;
    }

    [data-testid="stFileUploader"] > div {
        border: none !important;
    }

    /* ===== 分隔线 ===== */
    hr {
        border-color: #E7E2DA !important;
        margin: 20px 0 !important;
    }

    [data-testid="stDivider"] {
        border-color: #E7E2DA !important;
        margin: 16px 0 !important;
    }

    /* ===== 消息提示 ===== */
    .stAlert {
        background-color: #FBFAF8 !important;
        border-radius: 8px !important;
        border: 1px solid #E7E2DA !important;
        color: #5B5650 !important;
        padding: 12px 16px !important;
    }

    [data-testid="stSuccess"],
    [data-testid="stError"],
    [data-testid="stWarning"],
    [data-testid="stInfo"] {
        background-color: #FBFAF8 !important;
        border-color: #E7E2DA !important;
    }

    /* ===== 折叠面板 ===== */
    .streamlit-expanderHeader {
        background-color: #FBFAF8 !important;
        color: #5B5650 !important;
        border-radius: 8px !important;
        border: 1px solid #E7E2DA !important;
        padding: 10px 14px !important;
    }

    .streamlit-expanderContent {
        background-color: #F7F6F3 !important;
    }

    /* ===== 标签页 ===== */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        gap: 8px !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #8A847C !important;
        padding: 8px 16px !important;
    }

    .stTabs [aria-selected="true"] {
        color: #3A3632 !important;
    }

    /* ===== 表格 ===== */
    [data-testid="stDataFrame"] {
        background-color: #FBFAF8 !important;
        border-radius: 10px !important;
        border: 1px solid #E7E2DA !important;
    }

    .stDataFrame td, .stDataFrame th {
        background-color: #FBFAF8 !important;
        color: #5B5650 !important;
        border-color: #E7E2DA !important;
        padding: 10px 14px !important;
    }

    /* ===== 下拉选择框 ===== */
    .stSelectbox > div > div {
        background-color: #FBFAF8 !important;
        color: #5B5650 !important;
        border: 1px solid #E7E2DA !important;
        border-radius: 8px !important;
    }

    /* ===== 指标卡片 ===== */
    [data-testid="stMetric"] {
        background-color: #FBFAF8 !important;
        border: 1px solid #E7E2DA !important;
        border-radius: 10px !important;
        padding: 14px 18px !important;
    }

    [data-testid="stMetricValue"] {
        color: #3A3632 !important;
        font-weight: 500 !important;
        font-size: 1.4rem !important;
    }

    [data-testid="stMetricLabel"] {
        color: #8A847C !important;
        font-size: 0.8rem !important;
    }

    /* ===== 滚动条 ===== */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }

    ::-webkit-scrollbar-track {
        background: #F7F6F3;
    }

    ::-webkit-scrollbar-thumb {
        background: #E7E2DA;
        border-radius: 3px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #C97A52;
    }

    /* ===== 隐藏默认元素 ===== */
    #MainMenu {
        visibility: hidden !important;
    }

    footer {
        visibility: hidden !important;
    }

    /* ===== 自定义消息气泡 ===== */
    .message-container {
        background-color: #FBFAF8 !important;
        border-radius: 10px !important;
        padding: 14px 18px !important;
        margin: 10px 0 !important;
    }

    .message-red {
        border-left: 3px solid #C97A52 !important;
    }

    .message-blue {
        border-left: 3px solid #8A847C !important;
    }

    .message-user {
        background-color: #F1EFEB !important;
        border-left: 3px solid #E7E2DA !important;
    }

    /* ===== 加载动画 ===== */
    .stSpinner > div {
        border-color: #E7E2DA !important;
        border-top-color: #C97A52 !important;
    }

    /* ===== 多选框 ===== */
    .stMultiSelect > div > div {
        background-color: #FBFAF8 !important;
        border: 1px solid #E7E2DA !important;
        border-radius: 8px !important;
    }

    /* ===== 数字/日期/时间输入框 ===== */
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input,
    .stTimeInput > div > div > input {
        background-color: #FBFAF8 !important;
        color: #3A3632 !important;
        border: 1px solid #E7E2DA !important;
        border-radius: 8px !important;
    }

    /* ===== 列间距 ===== */
    div[data-testid="column"] {
        padding: 0 6px !important;
    }

    /* ===== 下载按钮 ===== */
    .stDownloadButton > button {
        background-color: transparent !important;
        color: #5B5650 !important;
        border: 1px solid #E7E2DA !important;
        border-radius: 24px !important;
        font-weight: 450 !important;
        font-size: 0.85rem !important;
        padding: 0.4rem 1.2rem !important;
        min-height: 36px !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .stDownloadButton > button:hover {
        background-color: #F5E6DE !important;
        border-color: #C97A52 !important;
        color: #3A3632 !important;
    }

    .stDownloadButton > button:hover::before,
    .stDownloadButton > button:hover::after {
        content: '' !important;
        position: absolute !important;
        width: 100px !important;
        height: 100px !important;
        left: 50% !important;
        top: 50% !important;
        margin-left: -50px !important;
        margin-top: -50px !important;
        border-radius: 50% !important;
        background: radial-gradient(circle, rgba(232, 200, 175, 0.6) 0%, rgba(201, 122, 82, 0.3) 50%, transparent 70%) !important;
        transform: scale(0) !important;
        animation: ripple-continuous 2s ease-out infinite !important;
        pointer-events: none !important;
    }

    .stDownloadButton > button:hover::after {
        animation-delay: 0.6s !important;
    }

    /* ===== 进度条 ===== */
    .stProgress > div > div > div {
        background-color: #C97A52 !important;
        border-radius: 4px !important;
    }

    /* ===== 滑块 ===== */
    .stSlider [data-baseweb="slider"] {
        background-color: #E7E2DA !important;
    }

    /* ===== 复选框 ===== */
    .stCheckbox > label {
        color: #5B5650 !important;
    }

    /* ===== 工具提示 ===== */
    [data-testid="stTooltipIcon"] {
        color: #A7A198 !important;
    }

    /* ===== 留白优化 ===== */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
    }

    /* ===== 响应式调整 ===== */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        h1 {
            font-size: 1.5rem !important;
        }

        h2 {
            font-size: 1.1rem !important;
        }
    }
    </style>
    """

    st.markdown(claude_css, unsafe_allow_html=True)


def apply_message_style(role: str, content: str, timestamp: str) -> str:
    """生成 Claude 风格的消息样式 HTML"""

    if role == "red":
        bg_color = "#FBFAF8"
        border_color = "#C97A52"  # 赤陶橙强调色
        role_name = "红方"
    elif role == "blue":
        bg_color = "#FBFAF8"
        border_color = "#8A847C"
        role_name = "蓝方"
    else:  # user
        bg_color = "#F1EFEB"
        border_color = "#E7E2DA"
        role_name = "你"

    html = f"""
    <div style="
        background-color: {bg_color};
        padding: 14px 18px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 3px solid {border_color};
    ">
        <div style="
            font-weight: 500;
            color: #3A3632;
            margin-bottom: 6px;
            font-size: 0.85rem;
        ">
            {role_name}
            <span style="color: #A7A198; font-weight: 400; margin-left: 8px; font-size: 0.75rem;">
                {timestamp}
            </span>
        </div>
        <div style="color: #5B5650; line-height: 1.65; white-space: pre-wrap; font-size: 0.9rem;">
            {content}
        </div>
    </div>
    """
    return html


def apply_card_style(title: str, content: str, icon: str = "") -> str:
    """生成 Claude 风格的卡片样式 HTML"""

    html = f"""
    <div style="
        background-color: #FBFAF8;
        border: 1px solid #E7E2DA;
        border-radius: 10px;
        padding: 16px;
        margin: 10px 0;
    ">
        <div style="
            font-weight: 500;
            color: #3A3632;
            font-size: 0.95rem;
            margin-bottom: 10px;
        ">
            {icon} {title}
        </div>
        <div style="color: #5B5650; line-height: 1.6; font-size: 0.9rem;">
            {content}
        </div>
    </div>
    """
    return html
