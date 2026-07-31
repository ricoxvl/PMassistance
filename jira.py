import streamlit as st


def show_jira(results):

    stories = results["stories"]["stories"]

    st.header("🎫 AI Generated Jira Stories")

    for story_index, story in enumerate(stories):

        with st.expander(
            f'{story["id"]} - {story["title"]}',
            expanded=True
        ):

            st.write(f'**Priority:** {story["priority"]}')

            st.write("### Description")
            st.write(story["description"])

            st.write("### Acceptance Criteria")

            for item_index, item in enumerate(story["acceptance"]):

                st.checkbox(
                    item,
                    value=False,
                    key=f"story_{story_index}_item_{item_index}"
                )