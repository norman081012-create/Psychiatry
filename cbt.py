import streamlit as st
import json
from analyzer import process_transcript

def clean_json_string(raw_string):
    """清理 LLM 可能產生的 Markdown 標記，確保能正確解析 JSON"""
    if not raw_string:
        return ""
    cleaned = raw_string.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("
```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return cleaned.strip()

def render_page():
    st.header("🛠️ 認知行為治療 (CBT) 視角")
    st.markdown("著重於找出非理性信念（認知扭曲）與行為模式的惡性循環，強調此時此地的問題解決。")
    
    # 1. 初始化 Session State 記憶 A、B、C 三個欄位的顯示狀態 (True=顯示, False=隱藏)
    if "show_cols" not in st.session_state:
        st.session_state.show_cols = [True, True, True]
        
    # 2. 初始化 Session State 記憶 API 回傳的結果
    if "cbt_analysis_result" not in st.session_state:
        st.session_state.cbt_analysis_result = None

    # ================= 自動執行分析邏輯 =================
    # 取消了手動按鈕，改為：只要有逐字稿且尚未產生結果，就自動在背景執行
    if st.session_state.transcript and not st.session_state.cbt_analysis_result:
        with st.spinner("偵測到新逐字稿，AI 正在自動萃取認知扭曲與行為模式..."):
            patient_info = st.session_state.get("patient_info", st.session_state.get("chief_complaint", ""))
            result = process_transcript(st.session_state.transcript, "CBT", patient_info)
            
            if result:
                if result.startswith("⚠️") or "錯誤" in result:
                    st.error(result)
                else:
                    st.session_state.cbt_analysis_result = result
                    st.session_state.show_cols = [True, True, True]
                    st.rerun()

    # ================= 動態欄位渲染區 (直接無條件呈現) =================
    st.markdown("### 🧩 CBT 概念化與橫向比較分析")
    
    scenarios = []
    if st.session_state.cbt_analysis_result:
        try:
            clean_str = clean_json_string(st.session_state.cbt_analysis_result)
            data = json.loads(clean_str)
            scenarios = data.get("scenarios", [])
        except json.JSONDecodeError:
            st.error("解析資料失敗，請確認 AI 輸出的是正確的 JSON 格式。")

    # 建立 3 個平行的欄位
    cols = st.columns(3)
    scenario_names = ["A", "B", "C"]

    for i in range(3):
        # 若無資料，則套用空字典，讓畫面直接呈現預設的空狀態
        scene = scenarios[i] if i < len(scenarios) else {}
        
        with cols[i]:
            # 如果狀態為 True，顯示卡片內容
            if st.session_state.show_cols[i]:
                with st.container(border=True):
                    # 頂部：標題 + 關閉按鈕
                    top_col1, top_col2 = st.columns([8, 2])
                    with top_col1:
                        st.subheader(f"情境 {scenario_names[i]}")
                    with top_col2:
                        if st.button("❌", key=f"close_{i}", help="移除此欄位"):
                            st.session_state.show_cols[i] = False
                            st.rerun()
                    
                    # 內容區 (預設為空白或等待分析)
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

            # 如果狀態為 False，顯示「新增」大按鈕
            else:
                with st.container(border=True):
                    st.markdown("<br><br><br><br>", unsafe_allow_html=True) # 撐開高度對齊
                    if st.button("➕ 新增", key=f"add_{i}", use_container_width=True):
                        st.session_state.show_cols[i] = True
                        st.rerun()
                    st.markdown("<br><br><br><br>", unsafe_allow_html=True)

    # ================= 底部：重置與重新分析按鈕 =================
    st.markdown("---")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔄 重置所有欄位 (恢復顯示 A、B、C)"):
            st.session_state.show_cols = [True, True, True]
            st.rerun()
    with col_btn2:
        if st.button("✨ 重新請 AI 分析逐字稿"):
            # 清除舊結果並強制重新整理，即可觸發上方的自動分析邏輯
            st.session_state.cbt_analysis_result = None
            st.rerun()
