import streamlit as st
from analyzer import process_transcript

def render_page():
    st.header("🌊 第三波療法 (ACT/MBCT/DBT) 視角")
    st.markdown("強調心理彈性（Psychological Flexibility）、正念覺察、接納，以及與價值觀一致的行動。")
    
    if st.button("執行第三波療法分析", type="primary"):
        if st.session_state.transcript:
            with st.spinner("正在結合個案資料進行綜合分析..."):
                report, summary = process_transcript(
                    st.session_state.transcript, 
                    "Third-Wave", 
                    st.session_state.patient_info
                )
                
                st.success("分析與匯總完成！")
                
                st.markdown(report)
                st.markdown("---")
                st.markdown(summary)
        else:
            st.warning("請先在上方輸入逐字稿！")
