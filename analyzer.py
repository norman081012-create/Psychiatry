import streamlit as st
import google.generativeai as genai

def process_transcript(transcript, school_type, patient_info=""):
    """將逐字稿與案主資訊組裝成 Prompt，並呼叫 LLM 進行分析"""
    if not transcript or not transcript.strip():
        return None
        
    # 準備各學派的專屬 Prompt
    prompts = {
        "CBT": f"""請扮演一位資深的臨床心理師，專精於認知行為治療（CBT）。
請分析下方的諮商逐字稿與案主資訊，從中擷取出「3 個不同的壓力事件、焦慮情境或困擾面向」。

【強制要求】
請「只」輸出 JSON 格式，不要包含任何其他文字或問候語。JSON 的結構必須精確如下：

{{
  "scenarios": [
    {{
      "cognitive_distortion": "[在此填寫認知扭曲與讀心術等]",
      "situation": "[在此填寫惡性循環：情境]",
      "thought": "[在此填寫惡性循環：想法]",
      "emotion": "[在此填寫惡性循環：情緒]",
      "physiology": "[在此填寫惡性循環：生理]",
      "behavior": "[在此填寫惡性循環：行為]",
      "intervention_cognitive": "[在此填寫介入策略：認知重構]",
      "intervention_behavioral": "[在此填寫介入策略：放鬆訓練與自我安撫]"
    }},
    {{
      // 請依照上述格式，產生第 2 個情境的資料
    }},
    {{
      // 請依照上述格式，產生第 3 個情境的資料
    }}
  ]
}}

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
    # 💡 實際 API 串接區塊
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
