import streamlit as st
import cbt
import psychodynamic
import humanistic
import third_wave

# 設定頁面資訊
st.set_page_config(page_title="心理師臨床助理：多學派分析", page_icon="🧠", layout="wide")

# 初始化 Session State，保留輸入內容，切換頁面時不會消失
if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "patient_info" not in st.session_state:
    st.session_state.patient_info = ""
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "model_choice" not in st.session_state:
    st.session_state.model_choice = "gemini-3.5-flash"

st.sidebar.title("🧠 多學派分析系統")

# ================= API 與模型設定區 =================
st.sidebar.subheader("⚙️ 系統設定")
api_key_input = st.sidebar.text_input(
    "API Key", 
    value=st.session_state.api_key, 
    type="password", 
    placeholder="請輸入您的 API Key"
)
model_input = st.sidebar.selectbox(
    "選擇模型", 
    ["gemini-3.5-flash", "gemini-1.5-pro", "gemini-1.5-flash"], 
    index=0
)

# 更新 Session State
if api_key_input != st.session_state.api_key:
    st.session_state.api_key = api_key_input
if model_input != st.session_state.model_choice:
    st.session_state.model_choice = model_input

st.sidebar.markdown("---")

# ================= 主訴填寫區（已修正變數為 patient_info） =================
st.sidebar.subheader("📋 案主基本資訊")
patient_info_input = st.sidebar.text_area(
    "主訴 (Chief Complaint)", 
    value=st.session_state.patient_info, 
    height=150, 
    placeholder="請在此簡述個案的主訴或背景資訊..."
)

# 更新 Session State
if patient_info_input != st.session_state.patient_info:
    st.session_state.patient_info = patient_info_input

st.sidebar.markdown("---")

# ================= 學派切換區 =================
st.sidebar.markdown("請選擇要使用的臨床視角：")

# 側邊欄切換按鈕
school_choice = st.sidebar.radio(
    "治療學派切換",
    ["1. 認知行為治療 (CBT)", 
     "2. 精神動力學派 (Psychodynamic)", 
     "3. 人本與存在主義 (Humanistic/Existential)", 
     "4. 第三波療法 (Third-Wave)"]
)

st.sidebar.info("💡 系統提示：請在左側填寫 API 與主訴，在主畫面輸入逐字稿後，點選上方按鈕切換不同學派的判讀視角。")

# ================= 主畫面：逐字稿輸入區 =================
st.title("臨床逐字稿輸入區")
transcript_input = st.text_area(
    "請貼上醫病對談逐字稿：", 
    value=st.session_state.transcript,
    height=200, 
    placeholder="在此貼上逐字稿..."
)

# 更新 Session State
if transcript_input != st.session_state.transcript:
    st.session_state.transcript = transcript_input

st.markdown("---")

# 根據側邊欄選擇，載入對應的模組
if school_choice.startswith("1"):
    cbt.render_page()
elif school_choice.startswith("2"):
    psychodynamic.render_page()
elif school_choice.startswith("3"):
    humanistic.render_page()
elif school_choice.startswith("4"):
    third_wave.render_page()
