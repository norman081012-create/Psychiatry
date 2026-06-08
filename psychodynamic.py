import streamlit as st
from analyzer import process_transcript

def render_page():
    st.header("🌊 精神動力學派 (Psychodynamic) 視角")
    st.markdown("探索潛意識衝突、防衛機轉的運作，以及過去經驗如何影響當前的人際與情緒模式。")
    
    if st.button("執行動力學分析", type="primary"):
        if st.session_state.transcript:
            with st.spinner("正在結合個案資料進行綜合分析..."):
                report, summary = process_transcript(
                    st.session_state.transcript, 
                    "Psychodynamic", 
                    st.session_state.patient_info
                )
                
                st.success("分析與匯總完成！")
                
                st.markdown(report)
                st.markdown("---")
                st.markdown(summary)
        else:
            st.warning("請先在上方輸入逐字稿！")
