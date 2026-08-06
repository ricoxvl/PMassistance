import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def show_charts(results):

    # -------------------------------------
    # Load Themes
    # -------------------------------------

    themes = results.get("themes", [])

    if not themes:
        st.header("📈 Analytics")
        st.info("No analytics available.")
        return

    category_df = pd.DataFrame(themes)

    st.header("📈 Analytics")

    # -------------------------------------
    # Issue Frequency
    # -------------------------------------

    st.subheader("Issue Frequency")

    st.bar_chart(
        category_df.set_index("theme")["mentions"]
    )

    # -------------------------------------
    # Issue Distribution
    # -------------------------------------

    st.subheader("Issue Distribution")

    fig, ax = plt.subplots(figsize=(7, 7))

    ax.pie(
        category_df["mentions"],
        labels=category_df["theme"],
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Customer Product Themes")

    st.pyplot(fig)

    # -------------------------------------
    # Theme Details
    # -------------------------------------

    st.subheader("Theme Details")

    for theme in themes:

        with st.expander(theme.get("theme", "Unknown Theme")):

            st.write(f"**Mentions:** {theme.get('mentions', 0)}")

            st.write(theme.get("summary", ""))

            evidence = theme.get("evidence", [])

            if evidence:

                st.markdown("**Supporting Evidence**")

                for item in evidence:
                    st.markdown(f"- {item}")