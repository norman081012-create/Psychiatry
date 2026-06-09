import streamlit as st
import google.generativeai as genai

def process_transcript(transcript, school_type, patient_info=""):
    """將逐字稿與案主資訊組裝成 Prompt，並呼叫 LLM 進行分析"""
    if not transcript or not transcript.strip():
        return None
        
    # 準備各學派的專屬 Prompt
    prompts = {
        "CBT": f"""請扮演一位資深的臨床心理師，專精於認知行為治療（CBT）。
請分析下方的諮商逐字稿與案主資訊，從中擷取出「3 個不同的壓力事件、焦慮情境或困擾面向（分別標為 A、B、C）」。

請務必嚴格依照以下 Markdown 表格的格式輸出，將這三個情境「並排在同一列」進行橫向比較。表格的欄位名稱與結構不可更改：

| 分析向度 | 情境 A | 情境 B | 情境 C |
| :--- | :--- | :--- | :--- |
| **認知扭曲 (如讀心術等)** | [填寫內容] | [填寫內容] | [填寫內容] |
| **惡性循環模型：情境** | [填寫內容] | [填寫內容] | [填寫內容] |
| **惡性循環模型：想法** | [填寫內容] | [填寫內容] | [填寫內容] |
| **惡性循環模型：情緒** | [填寫內容] | [填寫內容] | [填寫內容] |
| **惡性循環模型：生理** | [填寫內容] | [填寫內容] | [填寫內容] |
| **惡性循環模型：行為** | [填寫內容] | [填寫內容] | [填寫內容] |
| **介入策略：認知重構** | [填寫內容] | [填寫內容] | [填寫內容] |
| **介入策略：放鬆訓練與自我安撫** | [填寫內容] | [填寫內容] | [填寫內容] |

【輸入資料】
案主基本資訊：
{patient_info}

逐字稿內容：
{transcript}
""",

        "Psychodynamic": f"""請扮演一位資深的臨床心理師，專精於精神動力學派（Psychodynamic）。
請根據防衛機轉、潛意識衝突、客體關係等理論框架，深度分析下方的諮商逐字稿與案主資訊，並以專業且結構化的方式產出分析報告。

【輸入資料】
案主基本資訊：
{patient_info}

逐字稿內容：
{transcript}
""",

        "Humanistic": f"""請扮演一位資深的臨床心理師，專精於人本與存在主義（Humanistic & Existential）。
請根據自我概念、條件性正向關懷、存在焦慮與意義感等理論框架，深度分析下方的諮商逐字稿與案主資訊，並以溫和且專業的方式產出分析報告。

【輸入資料】
案主基本資訊：
{patient_info}

逐字稿內容：
{transcript}
""",

        "Third-Wave": f"""請扮演一位資深的臨床心理師，專精於第三波療法（ACT/MBCT/DBT）。
請根據認知融合、經驗迴避、正念覺察與價值觀釐清等理論框架，深度分析下方的諮商逐字稿與案主資訊，並以專業且結構化的方式產出分析報告。

【輸入資料】
案主基本資訊：
{patient_info}

逐字稿內容：
{transcript}
"""
    }

    selected_prompt = prompts.get(school_type, "")

    # ==========================================
    # 💡 實際 API 串接區塊 (已解開註解)
    # ==========================================
    
    api_key = st.session_state.get("api_key", "")
    model_name = st.session_state.get("model_choice", "gemini-3.5-flash")
    
    if not api_key:
        return "⚠️ 請先在左側系統設定欄位輸入您的 API Key"
    
    try:
        # 設定 API 金鑰並呼叫 Gemini 模型
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(selected_prompt)
        return response.text
        
    except Exception as e:
        return f"呼叫 API 時發生錯誤，請檢查您的 API Key 是否正確或網路狀態：\n\n{str(e)}"
