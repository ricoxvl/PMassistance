import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def show_charts(results):

    categories = results["categories"]["categories"]

    category_df = pd.DataFrame(categories)

    st.header("📈 Analytics")

    st.subheader("Issue Frequency")

    st.bar_chart(
        category_df.set_index("category")["count"]
    )

    st.subheader("Issue Distribution")

    fig, ax = plt.subplots()

    ax.pie(
        category_df["count"],
        labels=category_df["category"],
        autopct="%1.1f%%"
    )

    ax.set_title("Customer Issues")

    st.pyplot(fig)