import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def show_sentiment(results):

    sentiments = results["sentiment"]["sentiments"]

    sentiment_df = pd.DataFrame(sentiments)

    st.header(" Customer Sentiment")

    st.dataframe(
        sentiment_df,
        use_container_width=True
    )

    counts = sentiment_df["sentiment"].value_counts()

    st.subheader("Sentiment Distribution")

    st.bar_chart(counts)

    fig, ax = plt.subplots()

    ax.pie(
        counts.values,
        labels=counts.index,
        autopct="%1.1f%%"
    )

    ax.set_title("Customer Sentiment")

    st.pyplot(fig)