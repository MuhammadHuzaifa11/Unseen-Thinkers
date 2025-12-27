import streamlit as st
import processor
import ai_tool
import time
import plotly.express as px

# Setup page layout
st.set_page_config(page_title="Unseen Thinkers | AI", layout="wide")

# INITIALIZATION: Prevent KeyErrors
if "summary" not in st.session_state: st.session_state["summary"] = ""
if "anomalies" not in st.session_state: st.session_state["anomalies"] = ""
if "actions" not in st.session_state: st.session_state["actions"] = ""
if "chat_answer" not in st.session_state: st.session_state["chat_answer"] = ""

st.title("AI Workflow & Report Generator")
st.caption("Unseen Thinkers: Strategic Insights in under 5 seconds")

uploaded_file = st.file_uploader("Upload Business CSV", type=["csv"])

if uploaded_file:
    # Process the data
    vital_stats, df, cols = processor.process_csv(uploaded_file)
    sales_c, profit_c, cat_c = cols

    # Display key metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Sales", vital_stats['financials']['sales'])
    m2.metric("Net Profit", vital_stats['financials']['profit'])
    m3.metric("Margin", vital_stats['financials']['margin'])
    m4.metric("Status", "Data Ready")

    st.divider()
    
    # Mandatory 3 Buttons [cite: 30-33]
    col1, col2, col3 = st.columns(3)
    
    for btn_col, label, key in zip([col1, col2, col3], 
                                  ["Summarize Trends", "Identify Anomalies", "Suggest Actions"],
                                  ["summary", "anomalies", "actions"]):
        if btn_col.button(label):
            start_time = time.time()
            with st.spinner(f"Running {label}..."):
                result = ai_tool.get_ai_response(vital_stats, key)
                duration = time.time() - start_time
                st.session_state[key] = result
                st.session_state[f"{key}_time"] = f"Generated in {duration:.2f} seconds"

    # Display results
    res_col, chart_col = st.columns([1, 1])
    with res_col:
        if st.session_state["summary"]:
            st.info(f"Executive Summary:\n{st.session_state['summary']}\n\n{st.session_state.get('summary_time', '')}")
        if st.session_state["anomalies"]:
            st.error(f"Anomaly Report:\n{st.session_state['anomalies']}\n\n{st.session_state.get('anomalies_time', '')}")
        if st.session_state["actions"]:
            st.success(f"Business Actions:\n{st.session_state['actions']}\n\n{st.session_state.get('actions_time', '')}")

    with chart_col:
        st.subheader("Data Visualization")
        group_col = cat_c if cat_c else df.columns[0]
        chart_data = df.groupby(group_col)[sales_c].sum().reset_index()
        fig = px.bar(chart_data, x=group_col, y=sales_c, title="Sales by Category")
        st.plotly_chart(fig, use_container_width=True)

    # Finalize and Export (Appears after 3 tasks are done)
    if st.session_state["summary"] and st.session_state["anomalies"] and st.session_state["actions"]:
        st.divider()
        st.subheader("📥 Finalize and Export")
        
        report_text = f"UNSEEN THINKERS REPORT\nSales: {vital_stats['financials']['sales']}\nSummary: {st.session_state['summary']}"
        
        st.download_button(
            label="Download Complete Business Report",
            data=report_text,
            file_name="Business_Strategic_Report.txt",
            mime="text/plain"
        )

        st.divider()
        st.header("💬 Business  Assistant")
        question = st.text_input("Ask a question about the report")

        if question:
            with st.spinner("Thinking..."):
                answer = ai_tool.get_chat_response(vital_stats, question)
                st.session_state["chat_answer"] = answer
                st.write(answer)

    # Mandatory Ethical Guardrail [cite: 40, 248]
    st.warning("Note: AI outputs are for decision support and should be verified against raw data.")
    st.info("Built by Unseen Thinkers: Empowering business through speed and strategic AI.")