import streamlit as st
import cbt
import psychodynamic
import humanistic
import third_wave

# 設定頁面資訊
st.set_page_config(page_title="心理師臨床助理：多學派分析", page_icon="🧠", layout="wide")

# === 初始化 Session State ===
# 保留逐字稿內容
if "transcript" not in st.session_state:
    st.session_state.transcript = ""

# 保留個案基本資料
if "patient_info" not in st.session_state:
    st.session_state.patient_info = {}

# === 側邊欄 (左側) 介面 ===
st.sidebar.title("🧠 多學派分析系統")

# 1. 個案基本資料 (使用折疊面板保持側欄整潔)
st.sidebar.header("👤 個案基本資料")
with st.sidebar.expander("點擊展開/收合個案資料", expanded=False):
    p_name = st.text_input("姓名或代稱", value=st.session_state.patient_info.get("name", ""))
    p_age = st.number_input("年紀", min_value=0, max_value=120, value=st.session_state.patient_info.get("age", 30))
    p_gender = st.selectbox("性別", ["男", "女", "多元性別", "不願透露"], index=0)
    p_job = st.text_input("職業/工作", value=st.session_state.patient_info.get("job", ""))
    p_marriage = st.selectbox("婚姻狀態", ["未婚", "已婚", "離婚", "喪偶", "交往中"], index=0)
    p_economy = st.text_input("經濟狀況", placeholder="例如：穩定、負債、待業中...", value=st.session_state.patient_info.get("economy", ""))
    p_history = st.text_area("病史/過去諮商史", placeholder="簡述身心科就診或諮商紀錄...", value=st.session_state.patient_info.get("history", ""))
    
    # 即時更新 Session State
    st.session_state.patient_info = {
        "name": p_name, "age": p_age, "gender": p_gender,
        "job": p_job, "marriage": p_marriage, "economy": p_economy,
        "history": p_history
    }

st.sidebar.markdown("---")

# 2. 治療學派切換
st.sidebar.header("🔍 臨床視角")
school_choice = st.sidebar.radio(
    "治療學派切換",
    ["1. 認知行為治療 (CBT)", 
     "2. 精神動力學派 (Psychodynamic)", 
     "3. 人本與存在主義 (Humanistic/Existential)", 
     "4. 第三波療法 (Third-Wave)"]
)

st.sidebar.info("💡 系統提示：設定好個案資料後，在主畫面輸入逐字稿即可分析。")

# === 主畫面通用輸入區 ===
st.title("臨床逐字稿輸入區")
transcript_input = st.text_area(
    "請貼上醫病對談逐字稿：", 
    value=st.session_state.transcript,
    height=200, 
    placeholder="在此貼上逐字稿..."
)

# 更新逐字稿 Session State
if transcript_input != st.session_state.transcript:
    st.session_state.transcript = transcript_input

st.markdown("---")

# === 根據側邊欄選擇，載入對應的模組 ===
if school_choice.startswith("1"):
    cbt.render_page()
elif school_choice.startswith("2"):
    psychodynamic.render_page()
elif school_choice.startswith("3"):
    humanistic.render_page()
elif school_choice.startswith("4"):
    third_wave.render_page()
