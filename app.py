"""
PrePlay - 预演伙伴
主入口文件：首页 (Landing Page)
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st
from utils.file_handler import parse_uploaded_file
from utils.css_styles import apply_claude_theme

# 页面配置
st.set_page_config(
    page_title="PrePlay - 预演伙伴",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 应用 Claude 风格主题
apply_claude_theme()

# 隐藏侧边栏菜单
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    </style>
    """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# 初始化 session state
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "knowledge_content" not in st.session_state:
    st.session_state.knowledge_content = {}
if "knowledge_file_ids" not in st.session_state:
    st.session_state.knowledge_file_ids = []
if "file_upload_errors" not in st.session_state:
    st.session_state.file_upload_errors = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_round" not in st.session_state:
    st.session_state.current_round = 0
if "training_started" not in st.session_state:
    st.session_state.training_started = False
if "files_to_delete" not in st.session_state:
    st.session_state.files_to_delete = set()
if "training_to_delete" not in st.session_state:
    st.session_state.training_to_delete = None
if "files_uploaded" not in st.session_state:
    st.session_state.files_uploaded = False
if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()


# ============================================
# 文件校验函数
# ============================================

def validate_uploaded_file(file) -> dict:
    """
    校验上传文件

    Args:
        file: Streamlit 上传的文件对象

    Returns:
        {"valid": True/False, "error": "错误信息"}
    """
    # 大小检查：5MB = 5 * 1024 * 1024 bytes
    max_size = 5 * 1024 * 1024
    if file.size > max_size:
        size_mb = file.size / (1024 * 1024)
        return {
            "valid": False,
            "error": f"文件大小超过 5MB（当前：{size_mb:.2f}MB）"
        }

    # 格式检查：只支持 txt 和 docx
    ext = file.name.split('.')[-1].lower()
    if ext not in ['txt', 'docx']:
        return {
            "valid": False,
            "error": f"仅支持 txt 和 docx 格式（当前：.{ext}）"
        }

    return {"valid": True}


def upload_file_to_knowledge(file_path, file_name) -> tuple:
    """
    上传文件到知识库

    Args:
        file_path: 文件路径（临时路径）
        file_name: 原始文件名

    Returns:
        (success: bool, file_id: str or None, error: str or None)
    """
    try:
        from services.knowledge_service import get_knowledge_service

        service = get_knowledge_service()
        result = service.upload_document(file_path, file_name)

        if result["success"]:
            return True, result["file_id"], None
        else:
            return False, None, result.get("error", "上传失败")
    except Exception as e:
        return False, None, f"网络错误：{str(e)}"


def refresh_training_history():
    """从数据库刷新训练记录"""
    try:
        from database import get_db

        db = get_db()
        sessions = db.list_sessions(limit=20)

        history = []
        for session in sessions:
            # 获取会话统计
            stats = db.get_session_stats(session['id'])

            # 格式化时间
            created_at = session['created_at']
            if isinstance(created_at, str):
                date_str = created_at[:16]  # 取到分钟
            else:
                from datetime import datetime
                date_str = created_at.strftime('%Y-%m-%d %H:%M')

            history.append({
                "id": session['id'],
                "title": f"训练-{session['id'][-6:]}",
                "files": [],  # 暂不显示文件
                "date": date_str,
                "rounds": stats.get('user', 0),
                "red_questions": stats.get('red', 0),
                "blue_responses": stats.get('blue', 0),
                "status": "completed"
            })

        st.session_state.training_history = history
    except Exception as e:
        print(f"加载训练记录失败: {str(e)}")
        st.session_state.training_history = []


# 首次加载或刷新训练记录
if "training_history" not in st.session_state:
    refresh_training_history()

# 欢迎区域 - Claude 风格
st.markdown("""
<div style="text-align: center; padding: 16px 0 24px 0;">
    <h1 style="font-size: 1.8rem; font-weight: 500; margin-bottom: 6px; color: #3A3632 !important; font-family: ui-serif, Georgia, 'Times New Roman', 'Songti SC', serif !important;">
        PrePlay
    </h1>
    <p style="color: #8A847C; font-size: 0.9rem; margin: 0; font-family: ui-serif, Georgia, 'Times New Roman', 'Songti SC', serif !important;">
        预演伙伴 — 你的 AI 心理防弹衣
    </p>
</div>
""", unsafe_allow_html=True)

# 快捷导航 - 胶囊按钮样式，使用更紧凑的列
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("开始训练", use_container_width=True):
        st.switch_page("pages/1_训练.py")
with col2:
    if st.button("查看报告", use_container_width=True):
        st.switch_page("pages/2_报告.py")

st.markdown("<div style='height: 1px; background: #E7E2DA; margin: 16px 0;'></div>", unsafe_allow_html=True)

# 训练记录
st.markdown("### 训练记录")

# 处理删除训练记录
if st.session_state.training_to_delete:
    # 同时从数据库删除
    try:
        from database import get_db
        db = get_db()
        db.delete_session(st.session_state.training_to_delete)
    except Exception as e:
        print(f"删除会话失败: {str(e)}")

    # 从 session state 删除
    st.session_state.training_history = [
        r for r in st.session_state.training_history
        if r["id"] != st.session_state.training_to_delete
    ]
    st.session_state.training_to_delete = None
    st.rerun()

if st.session_state.training_history:
    for record in st.session_state.training_history:
        with st.container():
            col1, col2, col3 = st.columns([4, 1, 1.5], gap="small", vertical_alignment="center")
            with col1:
                st.markdown(f"**{record['title']}**")
                st.caption(f"文件: {', '.join(record['files']) if record['files'] else '无'}")
            with col2:
                st.caption(record['date'])
                st.caption(f"{record['rounds']} 轮对话")
            with col3:
                c1, c2 = st.columns(2, gap="small")
                with c1:
                    if st.button("继续", key=f"continue_{record['id']}"):
                        # 恢复历史训练
                        st.session_state.current_training_id = record['id']
                        # 不清空 chat_history，让训练页面加载历史消息
                        st.switch_page("pages/1_训练.py")
                with c2:
                    if st.button("删除", key=f"delete_training_{record['id']}"):
                        st.session_state.training_to_delete = record['id']
        st.markdown("<div style='height: 1px; background: #E7E2DA; margin: 8px 0;'></div>", unsafe_allow_html=True)
else:
    st.info("暂无训练记录，开始第一次训练吧")


# ============================================
# 从知识库 API 获取文件列表
# ============================================

def get_knowledge_files_from_api():
    """从讯飞知识库 API 获取文件列表"""
    try:
        from services.knowledge_service import get_knowledge_service
        service = get_knowledge_service()
        result = service.get_document_list(current_page=1, page_size=100)

        if result["success"]:
            print(f"[DEBUG] 从 API 获取了 {result['total']} 个文件")
            return result["files"]
        else:
            print(f"[DEBUG] API 调用失败: {result.get('error')}")
            st.error(f"获取文件列表失败: {result.get('error')}")
            return []
    except Exception as e:
        print(f"[DEBUG] 获取文件列表异常: {str(e)}")
        st.error(f"获取文件列表异常: {str(e)}")
        return []


# 文件上传区域
st.markdown("### 上传汇报材料")

# 刷新按钮
if st.button("刷新文件列表", key="refresh_kb_files"):
    st.rerun()

# 从 API 获取文件列表
knowledge_files = get_knowledge_files_from_api()

# 将知识库文件 IDs 保存到 session_state
if knowledge_files:
    st.session_state.knowledge_file_ids = [f["fileId"] for f in knowledge_files]
else:
    st.session_state.knowledge_file_ids = []

# 显示文件列表
if knowledge_files:
    st.info(f"共 {len(knowledge_files)} 个文件")

    for file_info in knowledge_files:
        file_id = file_info["fileId"]
        file_name = file_info["fileName"]
        file_type = file_info.get("extName", "")
        file_status = file_info.get("fileStatus", "")
        created_at = file_info.get("createTime", "")

        # 显示文件信息
        col1, col2 = st.columns([4, 1])
        with col1:
            st.success(file_name)
            st.caption(f"类型: {file_type} | 状态: {file_status}")
            st.caption(f"上传时间: {created_at}")
            st.caption("已上传到知识库")
        with col2:
            # 删除按钮
            if st.button("🗑️", key=f"delete_kb_{file_id}", help="从知识库删除"):
                st.session_state.file_to_delete_kb = file_id
    st.divider()

    # 处理删除操作
    if hasattr(st.session_state, 'file_to_delete_kb') and st.session_state.file_to_delete_kb:
        file_id_to_delete = st.session_state.file_to_delete_kb
        from services.knowledge_service import delete_document

        # 从知识库 API 删除
        with st.spinner(f"正在删除文件..."):
            result = delete_document(file_id_to_delete)

        if result["success"]:
            st.success(f"文件已从知识库删除")
            print(f"[DEBUG] 已从知识库删除: {file_id_to_delete}")
        else:
            st.error(f"删除失败: {result.get('error', '未知错误')}")
            print(f"[DEBUG] 删除失败: {result}")

        st.session_state.file_to_delete_kb = None
        st.rerun()
else:
    st.info("暂无文件")
    st.caption("请上传文件到知识库")

# 上传新文件
st.markdown("#### 上传新文件")

uploaded_files = st.file_uploader(
    "选择文件（支持 txt, docx，最大 5MB）",
    type=["txt", "docx"],
    accept_multiple_files=True,
    help="上传你的汇报材料，AI 将基于此内容进行训练",
    key="file_uploader_new"
)

# 如果有新上传的文件，进行校验和上传
if uploaded_files:
    for file in uploaded_files:
        # 检查文件是否已处理过（防止 rerun 后重复上传）
        if file.name in st.session_state.processed_files:
            continue

        # 检查文件是否已经在知识库中（通过文件名）
        file_exists = any(
            f.get("fileName", "") == file.name
            for f in knowledge_files
        )
        if file_exists:
            continue  # 跳过已存在的文件

        # 文件校验
        validation_result = validate_uploaded_file(file)

        if not validation_result["valid"]:
            # 校验失败
            st.error(f"文件 {file.name} 校验失败：{validation_result['error']}")
        else:
            # 上传到知识库
            with st.spinner(f"正在上传 {file.name} 到知识库..."):
                # 保存到临时文件
                import tempfile

                file_type = file.name.split('.')[-1].lower()
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as tmp_file:
                    tmp_file.write(file.getvalue())
                    tmp_path = tmp_file.name

                # 上传到知识库
                success, file_id, error = upload_file_to_knowledge(tmp_path, file.name)

                # 清理临时文件
                import os

                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

                if success:
                    st.success(f"文件 {file.name} 上传成功！")
                    print(f"[DEBUG] 文件上传成功: {file_id}")
                    # 标记为已处理，防止重复上传
                    st.session_state.processed_files.add(file.name)
                    # 添加到知识库文件 IDs 列表
                    st.session_state.knowledge_file_ids.append(file_id)
                else:
                    st.error(f"文件 {file.name} 上传失败：{error}")
                    print(f"[DEBUG] 文件上传失败: {error}")

    # 刷新页面以显示新文件
    st.rerun()

st.markdown("<div style='height: 1px; background: #E7E2DA; margin: 16px 0;'></div>", unsafe_allow_html=True)

# 使用贴士
st.markdown("### 使用贴士")
st.markdown("""
- **上传材料**：将你的汇报 PPT、文档或讲稿上传
- **开始训练**：红方会提出问题，蓝方会给建议
- **应对提问**：用你的专业知识回答挑战
- **导出报告**：训练完成后可导出完整报告
""")

# 开始训练按钮
st.markdown("<div style='height: 1px; background: #E7E2DA; margin: 20px 0;'></div>", unsafe_allow_html=True)

# 检查是否有知识库文件
has_knowledge_files = len(st.session_state.knowledge_file_ids) > 0

if has_knowledge_files:
    if st.button("开始训练", type="primary", use_container_width=True):
        st.session_state.training_started = True
        st.session_state.training_file_ids = st.session_state.knowledge_file_ids.copy()
        st.switch_page("pages/1_训练.py")
else:
    st.button("开始训练", type="primary", use_container_width=True, disabled=True)
