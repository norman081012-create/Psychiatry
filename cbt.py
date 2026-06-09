import streamlit as st
import json
from analyzer import process_transcript

def clean_json_string(raw_string):
    """清理 LLM 可能產生的 Markdown 標記，確保能正確解析 JSON"""
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
    
    # 初始化 Session State 來記憶 A、B、C 三個欄位的顯示狀態 (True=顯示, False=隱藏)
    if "show_cols" not in st.session_state:
        st.session_state.show_cols = [True, True, True]
        
    # 初始化 Session State 來記憶 API 回傳的結果，避免按鈕重整後資料消失
    if "cbt_analysis_result" not in st.session_state:
        st.session_state.cbt_analysis_result = None

    if st.button("執行 CBT 分析", type="primary"):
        if st.session_state.transcript:
            with st.spinner("正在萃取認知扭曲與行為模式 (預期 JSON 格式)..."):
                # 安全地取得主訴或病患資訊
                patient_info = st.session_state.get("patient_info", st.session_state.get("chief_complaint", ""))
                
                result = process_transcript(
                    st.session_state.transcript, 
                    "CBT", 
                    patient_info
                )
                
                if result:
                    # 檢查是否為錯誤訊息
                    if result.startswith("⚠️") or "錯誤" in result:
                        st.error(result)
                    else:
                        # 儲存結果並重置所有欄位為顯示狀態
                        st.session_state.cbt_analysis_result = result
                        st.session_state.show_cols = [True, True, True]
                        st.success("分析完成！")
                        st.rerun() # 強制刷新畫面以顯示下方結果
                else:
                    st.error("分析失敗，請確認逐字稿內容。")
        else:
            st.warning("請先在上方輸入逐字稿！")

    # ================= 動態欄位渲染區 =================
    if st.session_state.cbt_analysis_result:
        try:
            # 嘗試解析 JSON
            clean_str = clean_json_string(st.session_state.cbt_analysis_result)
            data = json.loads(clean_str)
            scenarios = data.get("scenarios", [])
        except json.JSONDecodeError:
            st.error("解析資料失敗，請確認 AI 輸出的是正確的 JSON 格式。以下為原始輸出：")
            st.code(st.session_state.cbt_analysis_result)
            return

        st.markdown("### 🧩 CBT 概念化與橫向比較分析")
        
        # 建立 3 個平行的欄位
        cols = st.columns(3)
        scenario_names = ["A", "B", "C"]

        for i in range(3):
            # 防呆：如果 AI 產生的情境少於 3 個，避免 IndexError
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
                        
                        # 內容區 (使用 get() 避免鍵值缺失噴錯)
                        st.markdown(f"**認知扭曲：**<br>{scene.get('cognitive_distortion', '無資料')}", unsafe_allow_html=True)
                        st.markdown(f"**惡性循環 (情境)：**<br>{scene.get('situation', '無資料')}", unsafe_allow_html=True)
                        st.markdown(f"**惡性循環 (想法)：**<br>{scene.get('thought', '無資料')}", unsafe_allow_html=True)
                        st.markdown(f"**惡性循環 (情緒)：**<br>{scene.get('emotion', '無資料')}", unsafe_allow_html=True)
                        st.markdown(f"**惡性循環 (生理)：**<br>{scene.get('physiology', '無資料')}", unsafe_allow_html=True)
                        st.markdown(f"**惡性循環 (行為)：**<br>{scene.get('behavior', '無資料')}", unsafe_allow_html=True)
                        st.divider()
                        st.markdown(f"**介入：認知重構**<br>{scene.get('intervention_cognitive', '無資料')}", unsafe_allow_html=True)
                        st.markdown(f"**介入：放鬆與安撫**<br>{scene.get('intervention_behavioral', '無資料')}", unsafe_allow_html=True)

                # 如果狀態為 False，顯示「新增」大按鈕
                else:
                    with st.container(border=True):
                        st.markdown("<br><br><br><br>", unsafe_allow_html=True) # 撐開高度對齊
                        if st.button("➕ 新增", key=f"add_{i}", use_container_width=True):
                            st.session_state.show_cols[i] = True
                            st.rerun()
                        st.markdown("<br><br><br><br>", unsafe_allow_html=True)

        # 底部：重置按鈕
        st.markdown("---")
        if st.button("🔄 重置所有欄位 (恢復 A、B、C)"):
            st.session_state.show_cols = [True, True, True]
            st.rerun()
