import streamlit as st
import google.generativeai as genai

def process_transcript(transcript, school_type, patient_info=""):
    """將逐字稿與案主資訊組裝成 Prompt，並呼叫 LLM 進行分析"""
    if not transcript or not transcript.strip():
        return None
        
    # 建立 CBT 的安全字串模板 (不使用 f-string，避免 JSON 大括號造成 SyntaxError)
    cbt_prompt_template = """請扮演一位資深的臨床心理師，專精於認知行為治療（CBT）。
請分析下方的諮商逐字稿與案主資訊，從中擷取出「3 個不同的壓力事件、焦慮情境或困擾面向」。

【強制要求】
請「只」輸出 JSON 格式，不要包含任何其他文字或問候語。JSON 的結構必須精確如下：

{
  "scenarios": [
    {
      "cognitive_distortion": "[在此填寫認知扭曲與讀心術等]",
      "situation": "[在此填寫惡性循環：情境]",
      "thought": "[在此填寫惡性循環：想法]",
      "emotion": "[在此填寫惡性循環：情緒]",
      "physiology": "[在此填寫惡性循環：生理]",
      "behavior": "[在此填寫惡性循環：行為]",
      "intervention_cognitive": "[在此填寫介入策略：認知重構]",
      "intervention_behavioral": "[在此填寫介入策略：放鬆訓練與自我安撫]"
    },
    {
      "cognitive_distortion": "[情境 2 認知扭曲]",
      "situation": "[情境 2 情境]",
      "thought": "[情境 2 想法]",
      "emotion": "[情境 2 情緒]",
      "physiology": "[情境 2 生理]",
      "behavior": "[情境 2 行為]",
      "intervention_cognitive": "[情境 2 認知重構]",
      "intervention_behavioral": "[情境 2 放鬆訓練]"
    },
    {
      "cognitive_distortion": "[情境 3 認知扭曲]",
      "situation": "[情境 3 情境]",
      "thought": "[情境 3 想法]",
      "emotion": "[情境 3 情緒]",
      "physiology": "[情境 3 生理]",
      "behavior": "[情境 3 行為]",
      "intervention_cognitive": "[情境 3 認知重構]",
      "intervention_behavioral": "[情境 3 放鬆訓練]"
    }
  ]
}

【輸入資料】
案主基本資訊：
__PATIENT_INFO__

逐字稿內容：
__TRANSCRIPT__
"""

    # 建立其他學派的模板
    psych_prompt_template = """請扮演一位資深的臨床心理師，專精於精神動力學派（Psychodynamic）。
請根據防衛機轉、潛意識衝突、客體關係等理論框架，深度分析。

【輸入資料】
案主基本資訊：\n__PATIENT_INFO__
\n逐字稿內容：\n__TRANSCRIPT__"""

    hum_prompt_template = """請扮演一位資深的臨床心理師，專精於人本與存在主義（Humanistic & Existential）。
請根據自我概念、存在焦慮等理論框架，深度分析。

【輸入資料】
案主基本資訊：\n__PATIENT_INFO__
\n逐字稿內容：\n__TRANSCRIPT__"""

    third_prompt_template = """請扮演一位資深的臨床心理師，專精於第三波療法（ACT/MBCT/DBT）。
請根據認知融合、經驗迴避等理論框架，深度分析。

【輸入資料】
案主基本資訊：\n__PATIENT_INFO__
\n逐字稿內容：\n__TRANSCRIPT__"""

    # 將選擇的模板轉換為字典
    prompts = {
        "CBT": cbt_prompt_template,
        "Psychodynamic": psych_prompt_template,
        "Humanistic": hum_prompt_template,
        "Third-Wave": third_prompt_template
    }

    selected_prompt = prompts.get(school_type, "")
    
    # 使用 .replace 安全替換變數
    selected_prompt = selected_prompt.replace("__PATIENT_INFO__", patient_info)
    selected_prompt = selected_prompt.replace("__TRANSCRIPT__", transcript)

    # ==========================================
    # 實際 API 串接區塊
    # ==========================================
    api_key = st.session_state.get("api_key", "")
    model_name = st.session_state.get("model_choice", "gemini-3.5-flash")
    
    if not api_key:
        return "⚠️ 請先在左側系統設定欄位輸入您的 API Key"
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(selected_prompt)
        return response.text
        
    except Exception as e:
        return f"呼叫 API 時發生錯誤，請檢查您的 API Key 是否正確或網路狀態：\n\n{str(e)}"

# ================= 新增：正式報告生成函式 =================
def generate_formal_report(patient_info, json_data, paragraphs, words):
    """根據已有的 JSON 資料與案主資訊，生成正式的心理師報告"""
    prompt = f"""請扮演一位資深的臨床心理師。請根據以下的「案主基本資訊」以及剛剛由逐字稿萃取出的「CBT 概念化與惡性循環分析結果」，撰寫一份正式的心理諮商個案概念化與治療計畫報告。

【格式與限制要求】
1. 報告結構必須嚴格分為 {paragraphs} 個段落。
2. 總字數請控制在約 {words} 字左右。
3. 語氣必須具備臨床專業度、客觀且溫和。
4. 報告內容需自然融入案主基本資訊，並綜合提煉 CBT 分析結果中的核心認知扭曲、惡性循環模式及未來建議的介入策略。

【輸入資料】
案主基本資訊：
{patient_info}

CBT 擷取出的核心情境分析 (JSON 格式)：
{json_data}
"""

    api_key = st.session_state.get("api_key", "")
    model_name = st.session_state.get("model_choice", "gemini-3.5-flash")

    if not api_key:
        return "⚠️ 請先在左側系統設定欄位輸入您的 API Key"

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"呼叫 API 時發生錯誤：\n\n{str(e)}"
