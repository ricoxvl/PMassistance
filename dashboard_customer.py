import streamlit as st
import pandas as pd
import plotly.express as px

from theme import inject_theme

inject_theme()


def show_customer_dashboard(results):

    # ==========================================================
    # Executive Styling
    # ==========================================================

    st.markdown("""
    <style>

    .metric-card{
        background:#ffffff08;
        border:1px solid #ffffff18;
        border-radius:12px;
        padding:18px;
        margin-bottom:15px;
    }

    .metric-title{
        font-size:14px;
        color:#AAAAAA;
        font-weight:600;
    }

    .metric-value{
        font-size:34px;
        font-weight:700;
        margin-top:8px;
    }

    .metric-sub{
        font-size:13px;
        color:#BBBBBB;
        margin-top:8px;
    }

    </style>
    """, unsafe_allow_html=True)

    # ==========================================================
    # Read AI Results
    # ==========================================================

    executive_summary = results.get(
        "executive_summary",
        "No executive summary available."
    )

    product_health = results.get("product_health", {})

    customer_satisfaction = results.get(
        "customer_satisfaction",
        {}
    )

    business_impact = results.get(
        "business_impact",
        {}
    )

    confidence = results.get(
        "confidence",
        {}
    )

    themes = results.get(
        "themes",
        []
    )

    priorities = results.get(
        "priorities",
        []
    )

    roadmap = results.get(
        "roadmap",
        []
    )

    recommendations = results.get(
        "recommendations",
        []
    )

    jira_stories = results.get(
        "jira_stories",
        []
    )

    scorecard = results.get(
        "scorecard",
        []
    )

    sentiment = results.get(
        "sentiment",
        {}
    )

    # ==========================================================
    # Convert Themes to DataFrame
    # ==========================================================

    theme_df = pd.DataFrame([
        {
            "Theme": item.get("theme", ""),
            "Mentions": item.get("mentions", 0)
        }
        for item in themes
    ])

    # ==========================================================
    # KPI Values
    # ==========================================================

    health_score = product_health.get("score", 0)
    health_status = product_health.get("status", "Unknown")

    satisfaction = customer_satisfaction.get("score", 0)

    impact = business_impact.get("level", "Unknown")

    confidence_score = confidence.get("score", 0)

    positive = sentiment.get("positive", 0)
    neutral = sentiment.get("neutral", 0)
    negative = sentiment.get("negative", 0)

    # ==========================================================
    # Priority Counts
    # ==========================================================

    high = sum(
        1
        for p in priorities
        if isinstance(p, dict)
        and p.get("priority", "").lower() == "high"
    )

    medium = sum(
        1
        for p in priorities
        if isinstance(p, dict)
        and p.get("priority", "").lower() == "medium"
    )

    low = sum(
        1
        for p in priorities
        if isinstance(p, dict)
        and p.get("priority", "").lower() == "low"
    )

    # ==========================================================
    # Dashboard Header
    # ==========================================================

    st.title("Customer Intelligence Dashboard")

    st.caption(
        "Executive Product Intelligence generated from customer feedback."
    )

    # ==========================================================
    # KPI Cards
    # ==========================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Product Health",
            f"{health_score}/100",
            health_status
        )

    with c2:
        st.metric(
            "Customer Satisfaction",
            f"{satisfaction}%",
            ""
        )

    with c3:
        st.metric(
            "Business Impact",
            impact,
            ""
        )

    with c4:
        st.metric(
            "AI Confidence",
            f"{confidence_score}%",
            ""
        )

    st.divider()

    # ==========================================================
    # Dashboard Tabs
    # ==========================================================

    executive_tab, analytics_tab, roadmap_tab, ai_tab = st.tabs([
        "Executive",
        "Analytics",
        "Roadmap",
        "AI Insights"
    ])
    # ==========================================================
    # EXECUTIVE TAB
    # ==========================================================

    with executive_tab:

        st.subheader("Executive Summary")

        left, right = st.columns([3, 1])

        with left:

            with st.container(border=True):

                st.markdown("### Overall Assessment")

                st.write(executive_summary)

        with right:

            st.metric(
                "Health Score",
                f"{health_score}/100"
            )

            st.metric(
                "Customer Satisfaction",
                f"{satisfaction}%"
            )

            st.metric(
                "High Priority Issues",
                high
            )

            st.metric(
                "AI Confidence",
                f"{confidence_score}%"
            )

        st.divider()

        # ======================================================
        # Product Health
        # ======================================================

        st.subheader("Product Health")

        col1, col2 = st.columns(2)

        with col1:

            with st.container(border=True):

                st.markdown("### Current Status")

                st.write(f"**Status:** {health_status}")

                st.progress(min(max(health_score / 100, 0), 1))

                st.write(product_health.get(
                    "reason",
                    "No explanation available."
                ))

        with col2:

            with st.container(border=True):

                st.markdown("### Business Impact")

                st.write(f"**Level:** {impact}")

                st.write(
                    business_impact.get(
                        "reason",
                        "No explanation available."
                    )
                )

        st.divider()

        # ======================================================
        # Customer Satisfaction
        # ======================================================

        st.subheader("Customer Satisfaction")

        sat1, sat2 = st.columns([1,2])

        with sat1:

            st.metric(
                "Overall Score",
                f"{satisfaction}%"
            )

        with sat2:

            st.write(
                customer_satisfaction.get(
                    "reason",
                    "No explanation available."
                )
            )

        st.divider()

        # ======================================================
        # Executive Scorecard
        # ======================================================

        st.subheader("Executive Scorecard")

        if scorecard:

            scorecard_df = pd.DataFrame(scorecard)

            st.dataframe(
                scorecard_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No executive scorecard available.")

        st.divider()

        # ======================================================
        # Priority Overview
        # ======================================================

        st.subheader("Priority Summary")

        p1, p2, p3 = st.columns(3)

        with p1:
            st.metric(
                "High",
                high
            )

        with p2:
            st.metric(
                "Medium",
                medium
            )

        with p3:
            st.metric(
                "Low",
                low
            )
    # ==========================================================
    # ANALYTICS TAB
    # ==========================================================

    with analytics_tab:

        st.subheader("Customer Feedback Analytics")

        left, right = st.columns([2, 1])

        # ======================================================
        # Theme Frequency
        # ======================================================

        with left:

            st.markdown("### Product Themes")

            if not theme_df.empty:

                chart_df = theme_df.sort_values(
                    "Mentions",
                    ascending=True
                )

                fig = px.bar(
                    chart_df,
                    x="Mentions",
                    y="Theme",
                    orientation="h",
                    text="Mentions",
                    template="plotly_white"
                )

                fig.update_layout(
                    height=500,
                    xaxis_title="Customer Mentions",
                    yaxis_title="",
                    margin=dict(
                        l=10,
                        r=10,
                        t=10,
                        b=10
                    )
                )

                fig.update_traces(
                    textposition="outside"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:

                st.info("No themes were identified.")

        # ======================================================
        # Sentiment Breakdown
        # ======================================================

        with right:

            st.markdown("### Sentiment")

            total = positive + neutral + negative

            if total > 0:

                sentiment_df = pd.DataFrame({

                    "Sentiment": [
                        "Positive",
                        "Neutral",
                        "Negative"
                    ],

                    "Count": [
                        positive,
                        neutral,
                        negative
                    ]

                })

                fig = px.pie(

                    sentiment_df,

                    names="Sentiment",

                    values="Count",

                    hole=.65,

                    template="plotly_white"

                )

                fig.update_layout(

                    height=450,

                    margin=dict(
                        l=0,
                        r=0,
                        t=0,
                        b=0
                    )

                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:

                st.info("No sentiment analysis available.")

        st.divider()

        # ======================================================
        # Theme Breakdown
        # ======================================================

        st.subheader("Theme Breakdown")

        if themes:

            for theme in themes:

                with st.container(border=True):

                    st.markdown(
                        f"### {theme.get('theme','Unknown Theme')}"
                    )

                    c1, c2 = st.columns([1,4])

                    with c1:

                        st.metric(
                            "Mentions",
                            theme.get("mentions",0)
                        )

                    with c2:

                        st.write(
                            theme.get(
                                "summary",
                                "No summary available."
                            )
                        )

                        evidence = theme.get(
                            "evidence",
                            []
                        )

                        if evidence:

                            st.markdown("**Supporting Evidence**")

                            for item in evidence:

                                st.markdown(
                                    f"- {item}"
                                )

        else:

            st.info("No themes available.")

        st.divider()

        # ======================================================
        # Priority Distribution
        # ======================================================

        st.subheader("Priority Distribution")

        priority_df = pd.DataFrame({

            "Priority":[
                "High",
                "Medium",
                "Low"
            ],

            "Count":[
                high,
                medium,
                low
            ]

        })

        fig = px.bar(

            priority_df,

            x="Priority",

            y="Count",

            text="Count",

            template="plotly_white"

        )

        fig.update_layout(

            height=400,

            xaxis_title="",

            yaxis_title="Issues"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    # ==========================================================
    # ROADMAP TAB
    # ==========================================================

    with roadmap_tab:

        st.subheader("Product Roadmap")

        if roadmap:

            if isinstance(roadmap, dict):
                roadmap = roadmap.get("roadmap", [])

            roadmap_df = pd.DataFrame(roadmap)

            st.dataframe(
                roadmap_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No roadmap recommendations were generated.")

        st.divider()

        # ======================================================
        # Priority Initiatives
        # ======================================================

        st.subheader("Priority Initiatives")

        if priorities:

            for item in priorities:

                with st.container(border=True):

                    left, right = st.columns([4,1])

                    with left:

                        st.markdown(
                            f"### {item.get('issue','Unknown Issue')}"
                        )

                        st.write(
                            item.get(
                                "reason",
                                "Customer-driven initiative."
                            )
                        )

                    with right:

                        st.metric(
                            "Priority",
                            item.get(
                                "priority",
                                "Medium"
                            )
                        )

        else:

            st.info("No initiatives identified.")

        st.divider()

        # ======================================================
        # Investment Summary
        # ======================================================

        st.subheader("Investment Portfolio")

        c1, c2, c3 = st.columns(3)

        c1.metric("Immediate", high)
        c2.metric("Next Release", medium)
        c3.metric("Future", low)

    # ==========================================================
    # AI INSIGHTS TAB
    # ==========================================================

    with ai_tab:

        st.subheader("AI Recommendations")

        if recommendations:

            for i, recommendation in enumerate(recommendations, start=1):

                with st.container(border=True):

                    st.markdown(
                        f"### Recommendation {i}"
                    )

                    st.write(recommendation)

        else:

            st.info("No recommendations generated.")

        st.divider()

        # ======================================================
        # Jira Stories
        # ======================================================

        st.subheader("Suggested Jira Stories")

        if jira_stories:

            jira_df = pd.DataFrame(jira_stories)

            st.dataframe(
                jira_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No Jira stories available.")

        st.divider()

        # ======================================================
        # Executive Report
        # ======================================================

        st.subheader("Executive Report")

        report = f"""
PRODUCT INTELLIGENCE AI

======================================

Executive Summary

{executive_summary}

======================================

Product Health:
{health_score}/100 ({health_status})

Customer Satisfaction:
{satisfaction}%

Business Impact:
{impact}

AI Confidence:
{confidence_score}%

======================================

Priority Breakdown

High: {high}
Medium: {medium}
Low: {low}

======================================

Top Product Themes

"""

        if not theme_df.empty:

            for _, row in theme_df.sort_values(
                "Mentions",
                ascending=False
            ).iterrows():

                report += f"- {row['Theme']} ({row['Mentions']} mentions)\n"

        report += """

======================================

Recommended Next Step

Prioritize the highest-impact customer issues
while maintaining investment in the most
requested product capabilities.

======================================
"""

        st.code(report, language="text")
