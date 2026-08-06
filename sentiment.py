import streamlit as st
import pandas as pd
import plotly.express as px


def show_sentiment(results):

    sentiment = results.get("sentiment", {})

    positive = sentiment.get("positive", 0)
    neutral = sentiment.get("neutral", 0)
    negative = sentiment.get("negative", 0)

    overall = sentiment.get("overall_sentiment", "Unknown")
    reason = sentiment.get("reason", "")

    st.header("Customer Sentiment")

    col1, col2, col3 = st.columns(3)

    col1.metric("Positive", positive)
    col2.metric("Neutral", neutral)
    col3.metric("Negative", negative)

    st.write(f"**Overall Sentiment:** {overall}")

    if reason:
        st.info(reason)

    sentiment_df = pd.DataFrame({
        "Sentiment": ["Positive", "Neutral", "Negative"],
        "Count": [positive, neutral, negative]
    })

    fig = px.pie(
        sentiment_df,
        names="Sentiment",
        values="Count",
        hole=0.55,
        title="Customer Sentiment Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)