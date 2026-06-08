import streamlit as st
from analyzer import process_transcript

def render_page():
    st.header("🛠️ 認知行為治療 (CBT) 視角")
    st.markdown("著重於找出非理性信念（認知扭曲）與行為模式的惡性循環，強調此時此地的問題解決。")
    
    if st.button("執行 CBT 分析", type="primary"):
        if st.session_state.transcript:
            with st.spinner("正在結合個案資料進行綜合分析..."):
                # 傳入 1.逐字稿 2.學派 3.個案基本資料
                report, summary = process_transcript(
                    st.session_state.transcript, 
                    "CBT", 
                    st.session_state.patient_info
                )
                
                st.success("分析與匯總完成！")
                
                # 顯示左半邊分析報告，右半邊顯示心理師匯總 (使用 Columns 讓排版更好看)
                st.markdown(report)
                st.markdown("---")
                st.markdown(summary)
        else:
            st.warning("請先在主畫面輸入逐字稿！")
