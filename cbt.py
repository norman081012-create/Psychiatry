import streamlit as st
import json
from analyzer import process_transcript, generate_formal_report

def clean_json_string(raw_string):
    """清理 LLM 可能產生的 Markdown 標記，確保能正確解析 JSON"""
    if not raw_string:
        return ""
    cleaned = raw_string.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return cleaned.strip()

def render_page():
    st.header("🛠️ 認知行為治療 (CBT) 視角")
    st.markdown("著重於找出非理性信念（認知扭曲）與行為模式的惡性循環，強調此時此地的問題解決。")
    
    # 初始化 Session State
    if "show_cols" not in st.session_state:
        st.session_state.show_cols = [True, True, True]
    if "cbt_analysis_result" not in st.session_state:
        st.session_state.cbt_analysis_result = None
    if "cbt_formal_report" not in st.session_state:
        st.session_state.cbt_formal_report = None

    # ================= 頂部：手動執行分析按鈕 (防止畫面卡死) =================
    if st.button("✨ 請 AI 擷取逐字稿並填入下方表格", type="primary"):
        if not st.session_state.transcript:
            st.warning("⚠️ 請先在上方輸入逐字稿內容！")
        else:
            with st.spinner("AI 正在深度解析逐字稿，這可能需要幾秒鐘，請稍候..."):
                patient_info = st.session_state.get("patient_info", "")
                result = process_transcript(st.session_state.transcript, "CBT", patient_info)
                
                if result:
                    if result.startswith("⚠️") or "錯誤" in result:
                        st.error(result)
                    else:
                        st.session_state.cbt_analysis_result = result
                        st.session_state.show_cols = [True, True, True]
                        st.session_state.cbt_formal_report = None 
                        st.rerun()

    # ================= 動態欄位渲染區 (預設無條件呈現空表) =================
    st.markdown("### 🧩 CBT 概念化與橫向比較分析")
    
    scenarios = []
    if st.session_state.cbt_analysis_result:
        try:
            clean_str = clean_json_string(st.session_state.cbt_analysis_result)
            data = json.loads(clean_str)
            scenarios = data.get("scenarios", [])
        except json.JSONDecodeError:
            st.error("解析資料失敗，請確認 AI 輸出的是正確的 JSON 格式。")

    cols = st.columns(3)
    scenario_names = ["A", "B", "C"]

    for i in range(3):
        scene = scenarios[i] if i < len(scenarios) else {}
        
        with cols[i]:
            if st.session_state.show_cols[i]:
                with st.container(border=True):
                    top_col1, top_col2 = st.columns([8, 2])
                    with top_col1:
                        st.subheader(f"情境 {scenario_names[i]}")
                    with top_col2:
                        if st.button("❌", key=f"close_{i}", help="移除此欄位"):
                            st.session_state.show_cols[i] = False
                            st.rerun()
                    
                    # 若尚未分析，填入預設提示字；若已分析但無該欄位資料，顯示無
                    default_text = "（等待分析）" if not st.session_state.cbt_analysis_result else "無"
                    
                    st.markdown(f"**認知扭曲：**<br>{scene.get('cognitive_distortion', default_text)}", unsafe_allow_html=True)
                    st.markdown(f"**惡性循環 (情境)：**<br>{scene.get('situation', default_text)}", unsafe_allow_html=True)
                    st.markdown(f"**惡性循環 (想法)：**<br>{scene.get('thought', default_text)}", unsafe_allow_html=True)
                    st.markdown(f"**惡性循環 (情緒)：**<br>{scene.get('emotion', default_text)}", unsafe_allow_html=True)
                    st.markdown(f"**惡性循環 (生理)：**<br>{scene.get('physiology', default_text)}", unsafe_allow_html=True)
                    st.markdown(f"**惡性循環 (行為)：**<br>{scene.get('behavior', default_text)}", unsafe_allow_html=True)
                    st.divider()
                    st.markdown(f"**介入：認知重構**<br>{scene.get('intervention_cognitive', default_text)}", unsafe_allow_html=True)
                    st.markdown(f"**介入：放鬆與安撫**<br>{scene.get('intervention_behavioral', default_text)}", unsafe_allow_html=True)
            else:
                with st.container(border=True):
                    st.markdown("<br><br><br><br>", unsafe_allow_html=True) 
                    if st.button("➕ 新增", key=f"add_{i}", use_container_width=True):
                        st.session_state.show_cols[i] = True
                        st.rerun()
                    st.markdown("<br><br><br><br>", unsafe_allow_html=True)

    # ================= 中段控制：重置按鈕 =================
    st.markdown("---")
    if st.button("🔄 重置所有欄位 (恢復顯示 A、B、C)"):
        st.session_state.show_cols = [True, True, True]
        st.rerun()

    # ================= 底部：正式報告生成區 =================
    st.markdown("---")
    st.markdown("### 📝 綜合臨床概念化報告")
    st.markdown("基於上述 CBT 情境分析與案主基本資訊，一鍵產出正式報告。")

    # 輸入設定區
    report_col1, report_col2, report_col3 = st.columns([2, 2, 4])
    with report_col1:
        paragraphs = st.number_input("設定段落數", min_value=1, max_value=10, value=4, step=1)
    with report_col2:
        words = st.number_input("預期總字數", min_value=100, max_value=3000, value=800, step=100)
    with report_col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 產生正式心理師報告", use_container_width=True, type="primary"):
            if not st.session_state.cbt_analysis_result:
                st.warning("⚠️ 請先點擊上方的「請 AI 擷取逐字稿」按鈕，產生表格資料後再生成報告！")
            else:
                with st.spinner("正在融合基本資訊與 CBT 概念化，撰寫正式報告中..."):
                    patient_info = st.session_state.get("patient_info", "")
                    json_data = st.session_state.cbt_analysis_result
                    
                    report = generate_formal_report(patient_info, json_data, paragraphs, words)
                    
                    if report and not (report.startswith("⚠️") or "錯誤" in report):
                        st.session_state.cbt_formal_report = report
                    else:
                        st.error(report)

    # 顯示生成的報告
    if st.session_state.cbt_formal_report:
        st.success("報告生成完畢！")
        with st.container(border=True):
            st.markdown(st.session_state.cbt_formal_report)
