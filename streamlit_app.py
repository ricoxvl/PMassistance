import streamlit as st
import pandas as pd

from copilot import ask_copilot
from pdf_report import create_pdf
from dashboard_customer import show_customer_dashboard
from dashboard_competitive import show_competitive_dashboard
from charts import show_charts
from sentiment import show_sentiment
from jira import show_jira
from document_processor import extract_competitor_text
from analysis_modes import (
    run_customer_analysis,
    run_competitive_analysis,
    run_combined_analysis
)

st.set_page_config(
    page_title="Product Intelligence AI",
    page_icon="",
    layout="wide"
)
st.sidebar.title("⚙️ Analysis Controls")
analysis_mode = st.sidebar.radio(
    "Analysis Mode",
    [
        "Customer Feedback",
        "Competitive Analysis",
        "Combined Analysis"
    ]
)

# ----------------------------------------------------
# Header
# ----------------------------------------------------

col1, col2 = st.columns([1, 5])

with col1:
    try:
        st.image("assets/logo.png", width=120)
    except Exception:
        pass

with col2:
    st.title("Product Intelligence AI")
    st.caption(
        "Executive AI platform for customer feedback, competitive intelligence, and product strategy."
    )

st.divider()

# ----------------------------------------------------
# Upload Files
# ----------------------------------------------------

feedback_file = st.file_uploader(
    "Customer Feedback Dataset",
    type=["csv"],
    key="feedback"
)

competitor_file = st.file_uploader(
    "Competitive Intelligence Report (XLSX, XLS, PDF, DOCX, TXT)",
    type=["xlsx", "xls", "pdf", "docx", "txt"],
    key="competitor"
)

# ----------------------------------------------------
# Process Files
# ----------------------------------------------------

df = pd.DataFrame()
feedback_list = []
competitor_text = ""

# -------------------------
# Competitive Analysis
# -------------------------

if competitor_file is not None:

    st.success("✅ Competitive analysis uploaded.")

    try:

        competitor_text = extract_competitor_text(
            competitor_file
        )

        st.subheader("Competitive Analysis Preview")

        with st.expander("View extracted document"):

            st.text_area(
                "Extracted Text",
                competitor_text[:3000],
                height=300
            )
    except Exception as e:
        st.error(f"Unable to read competitor document:\n{e}")
# -------------------------
# Customer Feedback
# -------------------------

if feedback_file is not None:

    df = pd.read_csv(feedback_file)

    st.subheader("Customer Feedback")

    search = st.text_input("🔍 Search customer feedback")

    if search:
        display_df = df[
            df["Feedback"]
            .astype(str)
            .str.contains(search, case=False, na=False)
        ]
    else:
        display_df = df

    st.dataframe(display_df, use_container_width=True)

    st.sidebar.subheader("Analysis Filters")

    total_feedback = len(df)

    if total_feedback > 20:
        max_feedback = st.sidebar.slider(
            "Maximum Feedback to Analyze",
            min_value=20,
            max_value=total_feedback,
            value=total_feedback,
            step=10
        )
    else:
        max_feedback = total_feedback
        st.sidebar.info(f"Analyzing all {total_feedback} feedback items.")

    feedback_list = (
        df["Feedback"]
        .astype(str)
        .head(max_feedback)
        .tolist()
    )

    st.info(
        f"Analyzing **{len(feedback_list)}** of **{total_feedback}** customer comments."
    )
    # ------------------------------------
# Run Analysis
# ------------------------------------

if st.button("🚀 Analyze", type="primary"):

    with st.spinner("🤖 AI is analyzing customer feedback and generating executive insights..."):

        try:

            if analysis_mode == "Customer Feedback":

                if not feedback_list:
                    st.error("Please upload a customer feedback CSV.")
                    st.stop()

                results = run_customer_analysis(feedback_list)

            elif analysis_mode == "Competitive Analysis":

                if not competitor_text:
                    st.error("Please upload a competitive analysis document.")
                    st.stop()

                results = run_competitive_analysis(competitor_text)

            else:

                if not feedback_list:
                    st.error("Please upload a customer feedback CSV.")
                    st.stop()

                if not competitor_text:
                    st.error("Please upload a competitive analysis document.")
                    st.stop()

                results = run_combined_analysis(
                    feedback_list,
                    competitor_text
                )

            st.session_state["analysis"] = results
            st.session_state["analysis_mode"] = analysis_mode
            st.success("✅ Analysis Complete!")

        except Exception as e:
            st.error(f"Workflow Failed:\n\n{e}")
# ----------------------------------------------------
# Dashboard
# ----------------------------------------------------

if "analysis" in st.session_state:

    results = st.session_state["analysis"]
    mode = st.session_state.get("analysis_mode", "Customer Feedback")

    st.divider()

    if mode == "Customer Feedback":
        show_customer_dashboard(results)

    elif mode == "Competitive Analysis":
        show_competitive_dashboard(results)

    elif mode == "Combined Analysis":
        show_combined_dashboard(results)

        with tab2:
            show_charts(results)

        with tab3:
            show_sentiment(results)

        with tab4:
            show_jira(results)

    # ------------------------------------------------
    # AI Product Copilot
    # ------------------------------------------------

    st.divider()

    st.header("🤖 AI Product Copilot")

    st.caption(
        "Ask questions about customer insights, product strategy, competitive intelligence, roadmap planning, and business priorities."
    )

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    question = st.text_input(
        "Ask anything about this analysis..."
    )

    if st.button("Ask AI"):

        if question.strip():

            with st.spinner("Thinking..."):

                answer = ask_copilot(
                    question,
                    results
                )

            st.session_state["chat_history"].append(
                ("You", question)
            )

            st.session_state["chat_history"].append(
                ("AI", answer)
            )

    for speaker, message in st.session_state["chat_history"]:

        if speaker == "You":
            st.chat_message("user").write(message)
        else:
            st.chat_message("assistant").write(message)

    # ------------------------------------------------
    # PDF Export
    # ------------------------------------------------

    st.divider()

    st.header("📄 Executive Report")

    st.caption(
        "Download a professionally formatted executive report."
    )   

    if st.button("Generate PDF"):

        pdf_file = create_pdf(results)

        with open(pdf_file, "rb") as file:

            st.download_button(
                label="⬇️ Download Report",
                data=file,
                file_name="Analyzed_Report.pdf",
                mime="application/pdf"
            )

# ----------------------------------------------------
# Footer
# ----------------------------------------------------

st.divider()

st.caption(
    "Product Intelligence AI • Executive Analytics Dashboard • Powered by Streamlit, Groq & Llama 3.1"
)