import streamlit as st
import cbt
import psychodynamic
import humanistic
import third_wave

# 設定頁面資訊
st.set_page_config(page_title="心理師臨床助理：多學派分析", page_icon="🧠", layout="wide")

# 初始化一般 Session State
if "transcript" not in st.session_state: st.session_state.transcript = ""
if "api_key" not in st.session_state: st.session_state.api_key = ""
if "model_choice" not in st.session_state: st.session_state.model_choice = "gemini-3.5-flash"
if "patient_info" not in st.session_state: st.session_state.patient_info = ""

# 初始化案主詳細資訊的 Session State
if "p_name" not in st.session_state: st.session_state.p_name = ""
if "p_age" not in st.session_state: st.session_state.p_age = 30
if "p_gender" not in st.session_state: st.session_state.p_gender = "男"
if "p_marriage" not in st.session_state: st.session_state.p_marriage = "未婚"
if "p_job" not in st.session_state: st.session_state.p_job = ""
if "p_economy" not in st.session_state: st.session_state.p_economy = "普通"
if "p_history" not in st.session_state: st.session_state.p_history = ""
if "p_chief_complaint" not in st.session_state: st.session_state.p_chief_complaint = ""

st.sidebar.title("🧠 多學派分析系統")

# ================= API 與模型設定區 =================
st.sidebar.subheader("⚙️ 系統設定")
api_key_input = st.sidebar.text_input(
    "API Key", value=st.session_state.api_key, type="password", placeholder="請輸入 API Key"
)
model_input = st.sidebar.selectbox(
    "選擇模型", ["gemini-3.5-flash", "gemini-1.5-pro", "gemini-1.5-flash"], 
    index=["gemini-3.5-flash", "gemini-1.5-pro", "gemini-1.5-flash"].index(st.session_state.model_choice)
)

if api_key_input != st.session_state.api_key: st.session_state.api_key = api_key_input
if model_input != st.session_state.model_choice: st.session_state.model_choice = model_input

st.sidebar.markdown("---")

# ================= 案主基本資訊填寫區 =================
st.sidebar.subheader("📋 案主基本資訊")

st.session_state.p_name = st.sidebar.text_input("姓名", value=st.session_state.p_name)

col1, col2 = st.sidebar.columns(2)
with col1:
    st.session_state.p_age = st.number_input("年齡", value=st.session_state.p_age, min_value=0, step=1)
    marriage_opts = ["未婚", "已婚", "離婚", "喪偶", "其他"]
    st.session_state.p_marriage = st.selectbox(
        "婚姻狀態", marriage_opts, 
        index=marriage_opts.index(st.session_state.p_marriage) if st.session_state.p_marriage in marriage_opts else 0
    )
    
with col2:
    gender_opts = ["男", "女", "其他"]
    st.session_state.p_gender = st.selectbox(
        "性別", gender_opts, 
        index=gender_opts.index(st.session_state.p_gender) if st.session_state.p_gender in gender_opts else 0
    )
    economy_opts = ["普通", "佳", "小康", "勉強", "困難"]
    st.session_state.p_economy = st.selectbox(
        "經濟狀況", economy_opts, 
        index=economy_opts.index(st.session_state.p_economy) if st.session_state.p_economy in economy_opts else 0
    )

st.session_state.p_job = st.sidebar.text_input("職業", value=st.session_state.p_job)
st.session_state.p_history = st.sidebar.text_input("過去病史", value=st.session_state.p_history, placeholder="無特殊病史")
st.session_state.p_chief_complaint = st.sidebar.text_input("主訴 (Chief Complaint)", value=st.session_state.p_chief_complaint, placeholder="例如：近期焦慮、失眠...")

# 背景自動組裝字串
st.session_state.patient_info = f"""
姓名: {st.session_state.p_name}
年齡: {st.session_state.p_age}
性別: {st.session_state.p_gender}
職業: {st.session_state.p_job}
婚姻: {st.session_state.p_marriage}
經濟: {st.session_state.p_economy}
病史: {st.session_state.p_history}
主訴: {st.session_state.p_chief_complaint}
"""

st.sidebar.markdown("---")

# ================= 學派切換區 =================
st.sidebar.markdown("請選擇要使用的臨床視角：")

school_choice = st.sidebar.radio(
    "治療學派切換",
    ["1. 認知行為治療 (CBT)", 
     "2. 精神動力學派 (Psychodynamic)", 
     "3. 人本與存在主義 (Humanistic/Existential)", 
     "4. 第三波療法 (Third-Wave)"]
)

# ================= 主畫面：逐字稿輸入區 =================
st.title("臨床逐字稿輸入區")
transcript_input = st.text_area(
    "請貼上醫病對談逐字稿：", 
    value=st.session_state.transcript,
    height=200, 
    placeholder="在此貼上逐字稿..."
)

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
