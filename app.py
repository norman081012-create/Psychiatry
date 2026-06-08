import streamlit as st
import time
# 如果你之後要串接 API，可以 import openai 或 google.generativeai

# 設定頁面資訊
st.set_page_config(page_title="心理師臨床助理系統", page_icon="🧠", layout="wide")

st.title("🧠 心理師臨床助理：對談摘要系統")
st.markdown("將逐字稿自動轉換為結構化的臨床病人總結。")
st.markdown("---")

# 版面配置：左邊輸入，右邊輸出
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 輸入區域")
    transcript = st.text_area(
        "請貼上心理師與病人的對談逐字稿：", 
        height=400, 
        placeholder="例如：\n心理師：你今天感覺怎麼樣？\n病人：我覺得最近壓力很大，晚上都睡不好，經常在半夜醒來...\n心理師：這種狀況持續多久了？..."
    )
    
    analyze_btn = st.button("生成病人總結", type="primary", use_container_width=True)

with col2:
    st.subheader("2. 分析結果")
    
    if analyze_btn:
        if not transcript.strip():
            st.warning("請先輸入逐字稿內容！")
        else:
            with st.spinner("系統正在進行語義分析與臨床特徵萃取..."):
                # 模擬 API 呼叫的延遲
                time.sleep(1.5) 
                
                # ---------------------------------------------------------
                # 實戰時，這裡會替換成你的 LLM API 呼叫邏輯。
                # Prompt 建議："你是一位專業的臨床心理師。請將以下逐字稿整理成一份專業的病人總結，包含：主訴、現病史、精神狀態觀察。"
                # ---------------------------------------------------------
                
                # 以下為模擬 LLM 結構化輸出的假資料
                mock_summary = """
### 臨床對談摘要

**一、 主訴 (Chief Complaint)**
* 睡眠障礙，近期工作壓力導致焦慮感顯著提升。

**二、 現病史 (History of Present Illness)**
* 個案表示過去兩週內入睡困難，常在半夜醒來且無法再次入睡。
* 伴隨胸悶、心悸，以及反覆擔憂工作表現的強迫性思考。
* 尚未嚴重影響日間基本生活自理，但工作專注度已下降。

**三、 精神狀態觀察 (Mental Status Examination)**
* **外觀與行為：** 意識清醒，對答切題，但眉頭深鎖。
* **情緒與情感：** 情緒略顯焦慮與低落，語速偏快。
* **思考過程：** 邏輯連貫，無明顯知覺失調或妄想症狀。

**四、 初步分析**
* 疑似適應障礙伴隨焦慮症狀。建議留意長期睡眠剝奪對軀體化症狀（胸悶、心悸）的放大效應。
                """
                st.success("摘要生成完畢！")
                st.markdown(mock_summary)
                
                # 預留未來的擴充區塊
                st.info("💡 系統擴充準備：下一步可將此摘要作為輸入，啟動「4軸測驗自動判讀」與「轉介/整體醫師建議」的推論引擎。")
