import streamlit as st
import pandas as pd


def show_jira(results):

    stories = results.get("jira_stories", [])

    st.header("Generated Jira Stories")

    if not stories:
        st.info("No Jira stories were generated.")
        return

    for story in stories:

        with st.container(border=True):

            st.subheader(
                f"{story.get('id', 'N/A')} - {story.get('title', 'Untitled')}"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Priority", story.get("priority", "N/A"))

            with col2:
                st.metric("Status", "Proposed")

            st.markdown("**Description**")
            st.write(story.get("description", ""))

            acceptance = story.get("acceptance", [])

            if acceptance:
                st.markdown("**Acceptance Criteria**")
                for item in acceptance:
                    st.markdown(f"- {item}")