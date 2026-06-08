import streamlit as st
from analyzer import process_transcript

def render_page():
    st.header("🌊 第三波療法 (ACT/MBCT/DBT) 視角")
    st.markdown("強調心理彈性（Psychological Flexibility）、正念覺察、接納，以及與價值觀一致的行動。")
    
    if st.button("執行第三波療法分析", type="primary"):
        if st.session_state.transcript:
            with st.spinner("正在分析認知融合與經驗迴避狀態..."):
                result = process_transcript(st.session_state.transcript, "Third-Wave")
                st.success("分析完成！")
                st.markdown(result)
        else:
            st.warning("請先在上方輸入逐字稿！")
