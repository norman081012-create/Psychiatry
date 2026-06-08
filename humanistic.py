import streamlit as st
from analyzer import process_transcript

def render_page():
    st.header("🌱 人本與存在主義 (Humanistic & Existential) 視角")
    st.markdown("關注個案的自我實現、意義感、主觀經驗，以及此時此刻的存在狀態。")
    
    if st.button("執行人本存在分析", type="primary"):
        if st.session_state.transcript:
            with st.spinner("正在結合個案資料進行綜合分析..."):
                report, summary = process_transcript(
                    st.session_state.transcript, 
                    "Humanistic", 
                    st.session_state.patient_info
                )
                
                st.success("分析與匯總完成！")
                
                st.markdown(report)
                st.markdown("---")
                st.markdown(summary)
        else:
            st.warning("請先在上方輸入逐字稿！")
