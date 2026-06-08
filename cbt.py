import streamlit as st
from analyzer import process_transcript

def render_page():
    st.header("🛠️ 認知行為治療 (CBT) 視角")
    st.markdown("著重於找出非理性信念（認知扭曲）與行為模式的惡性循環，強調此時此地的問題解決。")
    
    if st.button("執行 CBT 分析", type="primary"):
        if st.session_state.transcript:
            with st.spinner("正在萃取認知扭曲與行為模式..."):
                # 安全地取得主訴或病患資訊 (相容 patient_info 或 chief_complaint)
                patient_info = st.session_state.get("patient_info", st.session_state.get("chief_complaint", ""))
                
                # 改用單一變數 result 接收，避免 Unpacking Error
                result = process_transcript(
                    st.session_state.transcript, 
                    "CBT", 
                    patient_info
                )
                
                if result:
                    st.success("分析完成！")
                    st.markdown(result)
                else:
                    st.error("分析失敗，請確認逐字稿內容。")
        else:
            st.warning("請先在上方輸入逐字稿！")
