import streamlit as st
import pandas as pd
import plotly.express as px
from theme import inject_theme

inject_theme()


def show_customer_dashboard(results):

    # =====================================================
    # Custom CSS
    # =====================================================

    st.markdown("""
    <style>

    .kpi-card{
        background: var(--secondary-background-color);
        border-left:5px solid var(--primary-color);
        border-radius:12px;
        padding:20px;
        box-shadow:0 2px 8px rgba(0,0,0,.08);
        height:140px;
    }

    .kpi-title{
        font-size:14px;
        font-weight:600;
        color:var(--text-color);
        opacity:.70;
    }

    .kpi-number{
        font-size:34px;
        font-weight:700;
        color:var(--text-color);
        margin-top:10px;
    }

    .kpi-subtitle{
        margin-top:10px;
        font-size:13px;
        color:var(--text-color);
        opacity:.75;
    }

    </style>
    """, unsafe_allow_html=True)

    # =====================================================
    # Load AI Results
    # =====================================================

    categories = results.get("categories", [])
    if isinstance(categories, dict):
        categories = categories.get("categories", [])

    priorities = results.get("priorities", [])
    if isinstance(priorities, dict):
        priorities = priorities.get("priorities", [])

    roadmap = results.get("roadmap", [])
    if isinstance(roadmap, dict):
        roadmap = roadmap.get("roadmap", [])

    sentiments = results.get("sentiment", [])
    if isinstance(sentiments, dict):
        sentiments = sentiments.get("sentiments", [])

    executive_summary = results.get(
        "executive_summary",
        "No executive summary available."
    )

    category_df = pd.DataFrame(categories)
    sentiment_df = pd.DataFrame(sentiments)

    # =====================================================
    # Calculate Executive Metrics
    # =====================================================

    high = sum(
        1 for p in priorities
        if isinstance(p, dict)
        and p.get("priority", "").lower() == "high"
    )

    medium = sum(
        1 for p in priorities
        if isinstance(p, dict)
        and p.get("priority", "").lower() == "medium"
    )

    low = sum(
        1 for p in priorities
        if isinstance(p, dict)
        and p.get("priority", "").lower() == "low"
    )

    if not sentiment_df.empty:

        positive = len(
            sentiment_df[
                sentiment_df["sentiment"] == "Positive"
            ]
        )

        neutral = len(
            sentiment_df[
                sentiment_df["sentiment"] == "Neutral"
            ]
        )

        negative = len(
            sentiment_df[
                sentiment_df["sentiment"] == "Negative"
            ]
        )

    else:

        positive = neutral = negative = 0

    total_sentiment = positive + neutral + negative

    sentiment_score = (
        round(positive / total_sentiment * 100)
        if total_sentiment else 0
    )

    health_score = max(
        0,
        100
        - high * 15
        - medium * 7
        - low * 3
    )

    if health_score >= 85:
        health_status = "Excellent"
    elif health_score >= 70:
        health_status = "Healthy"
    elif health_score >= 55:
        health_status = "Needs Attention"
    else:
        health_status = "Critical"

    business_impact = (
        "High"
        if high >= 3
        else "Medium"
        if high >= 1
        else "Low"
    )

    confidence = 100

    if len(category_df) < 3:
        confidence -= 10

    if total_sentiment < 20:
        confidence -= 15

    confidence = max(confidence, 60)

    if confidence >= 90:
        confidence_label = "Very High"
    elif confidence >= 80:
        confidence_label = "High"
    elif confidence >= 70:
        confidence_label = "Moderate"
    else:
        confidence_label = "Low"

    # =====================================================
    # KPI Card Helper
    # =====================================================

    def executive_card(title, value, subtitle):

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-number">{value}</div>
            <div class="kpi-subtitle">{subtitle}</div>
        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # Dashboard Header
    # =====================================================

    st.title("Product Intelligence AI")

    st.caption(
        "Executive analytics platform for customer feedback, product strategy, and roadmap planning."
    )

    # =====================================================
    # Navigation
    # =====================================================

    executive_tab, analytics_tab, roadmap_tab, ai_tab = st.tabs([
        "Executive",
        "Analytics",
        "Roadmap",
        "AI Insights"
    ])
    executive_tab, analytics_tab, roadmap_tab, ai_tab = st.tabs([
    "Executive",
    "Analytics",
    "Roadmap",
    "AI Insights"
    ])
        # =====================================================
    # Executive Overview
    # =====================================================

    st.subheader("Executive Overview")

    overview_left, overview_right = st.columns([3, 1])

    top_issue = (
        priorities[0].get("issue")
        if priorities
        else "No major issues identified."
    )

    top_theme = (
        category_df.sort_values(
            "count",
            ascending=False
        ).iloc[0]["category"]
        if not category_df.empty
        else "No themes identified."
    )

    with overview_left:

        with st.container(border=True):

            st.markdown(f"""
## Executive Assessment

### Current Product Status

**Product Health:** **{health_status}**

**Customer Satisfaction:** **{sentiment_score}% Positive**

**Business Impact:** **{business_impact}**

---

### Key Findings

- Highest Priority Issue: **{top_issue}**

- Most Discussed Theme: **{top_theme}**

- High Priority Initiatives: **{high}**

- Product Themes Identified: **{len(category_df)}**

---

### Recommendation

Prioritize engineering investment toward **{top_issue.lower()}** while
continuing to strengthen **{top_theme.lower()}**.

This strategy is expected to improve customer satisfaction,
reduce operational risk, and increase long-term product value.

---

### AI Confidence

Confidence Score: **{confidence}% ({confidence_label})**
""")

    with overview_right:

        if health_score >= 85:
            st.success(f"Product Health\n\n{health_score}/100")
        elif health_score >= 70:
            st.warning(f"Product Health\n\n{health_score}/100")
        else:
            st.error(f"Product Health\n\n{health_score}/100")

        if sentiment_score >= 75:
            st.success(f"Customer Satisfaction\n\n{sentiment_score}%")
        elif sentiment_score >= 50:
            st.warning(f"Customer Satisfaction\n\n{sentiment_score}%")
        else:
            st.error(f"Customer Satisfaction\n\n{sentiment_score}%")

        if high >= 3:
            st.error(f"High Priority Issues\n\n{high}")
        else:
            st.success(f"High Priority Issues\n\n{high}")

        st.info(f"AI Confidence\n\n{confidence}%")

    st.divider()
    # =====================================================
    # Analytics
    # =====================================================

    with analytics_tab:

        st.subheader("Customer Feedback Analytics")

        left, right = st.columns([2, 1])

    # ============================================
    # Product Themes
    # ============================================

    with left:

        st.markdown("##### Product Themes")

        if not category_df.empty:

            category_df = category_df.sort_values(
                "count",
                ascending=True
            )

            fig = px.bar(
                category_df,
                x="count",
                y="category",
                orientation="h",
                text="count"
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
                ),

                coloraxis_showscale=False,

                template="plotly_white"
            )

            fig.update_traces(
                textposition="outside"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info("No product themes were identified.")

    # ============================================
    # Sentiment Breakdown
    # ============================================

    with right:

        st.markdown("##### Sentiment Distribution")

        if total_sentiment:

            sentiment_summary = pd.DataFrame({

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

                sentiment_summary,

                names="Sentiment",

                values="Count",

                hole=.60

            )

            fig.update_layout(

                height=500,

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

    # ============================================
    # Product Themes Table
    # ============================================

    st.subheader("Product Theme Breakdown")

    if not category_df.empty:

        display_df = category_df.copy()

        display_df.columns = [
            "Theme",
            "Mentions"
        ]

        display_df = display_df.sort_values(
            "Mentions",
            ascending=False
        )

        st.dataframe(

            display_df,

            use_container_width=True,

            hide_index=True

        )

    else:

        st.info("No product themes available.")

    st.divider()

    # ============================================
    # Priority Distribution
    # ============================================

    st.subheader("Priority Distribution")

    priority_df = pd.DataFrame({

        "Priority": [
            "High",
            "Medium",
            "Low"
        ],

        "Count": [
            high,
            medium,
            low
        ]

    })

    fig = px.bar(

        priority_df,

        x="Priority",

        y="Count",

        text="Count"

    )

    fig.update_layout(

        height=400,

        xaxis_title="",

        yaxis_title="Number of Issues",

        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        )

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ============================================
    # Analytics Summary
    # ============================================

    st.subheader("Analytics Summary")

    analytics_summary = pd.DataFrame([

        {
            "Metric": "Themes Identified",
            "Value": len(category_df)
        },

        {
            "Metric": "High Priority Issues",
            "Value": high
        },

        {
            "Metric": "Positive Sentiment",
            "Value": f"{sentiment_score}%"
        },

        {
            "Metric": "AI Confidence",
            "Value": f"{confidence}%"
        }

    ])

    st.dataframe(

        analytics_summary,

        hide_index=True,

        use_container_width=True

    )
    # =====================================================
    # Roadmap
    # =====================================================

    with roadmap_tab:

        st.subheader("Product Roadmap")

    # =============================================
    # Executive Roadmap
    # =============================================

    roadmap_items = []

    for item in priorities:

        if not isinstance(item, dict):
            continue

        issue = item.get("issue", "Unknown")
        priority = item.get("priority", "Medium").lower()

        if priority == "high":

            release = "Immediate"

            investment = "High"

            owner = "Engineering"

        elif priority == "medium":

            release = "Next Release"

            investment = "Medium"

            owner = "Product"

        else:

            release = "Future"

            investment = "Low"

            owner = "Strategy"

        roadmap_items.append({

            "Initiative": issue,

            "Priority": priority.title(),

            "Target Release": release,

            "Investment": investment,

            "Owner": owner

        })

    if roadmap_items:

        roadmap_df = pd.DataFrame(roadmap_items)

        st.dataframe(

            roadmap_df,

            hide_index=True,

            use_container_width=True

        )

    else:

        st.info("No roadmap recommendations available.")

    st.divider()

    # =============================================
    # Executive Investment Portfolio
    # =============================================

    st.subheader("Investment Portfolio")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Immediate",

            high

        )

    with c2:

        st.metric(

            "Next Release",

            medium

        )

    with c3:

        st.metric(

            "Future",

            low

        )

    st.divider()

    # =============================================
    # Priority Cards
    # =============================================

    st.subheader("Recommended Initiatives")

    if priorities:

        for item in priorities:

            issue = item.get("issue", "Unknown")

            priority = item.get("priority", "Medium")

            with st.container(border=True):

                left, right = st.columns([3,1])

                with left:

                    st.markdown(f"### {issue}")

                    st.write(f"""
    Priority Level: **{priority}**

    This initiative was identified by AI as a customer-driven opportunity.

    Expected outcome includes improved customer satisfaction,
    reduced support effort, and stronger product adoption.
    """)

                with right:

                    st.metric(
                        "Priority",
                        priority
                    )

                    st.metric(
                        "ROI",
                        "High" if priority.lower()=="high" else "Medium"
                    )

    else:

        st.info("No initiatives identified.")

    st.divider()

    # =============================================
    # AI Generated Jira Stories
    # =============================================

    st.subheader("Suggested Jira Stories")

    jira_rows = []

    for item in priorities:

        if not isinstance(item, dict):
            continue

        issue = item.get("issue","Unknown")

        jira_rows.append({

            "Epic":"Customer Experience",

            "Story":f"Improve {issue.lower()}",

            "Priority":item.get("priority","Medium"),

            "Status":"Proposed"

        })

    if jira_rows:

        jira_df = pd.DataFrame(jira_rows)

        st.dataframe(

            jira_df,

            use_container_width=True,

            hide_index=True

        )

    else:

        st.info("No Jira stories generated.")

    st.divider()

    # =============================================
    # Executive Recommendation
    # =============================================

    st.subheader("Portfolio Recommendation")

    with st.container(border=True):

        st.write("""

### Recommended Investment Strategy

Allocate engineering resources toward high-priority customer issues before investing in new functionality.

Once critical issues have been addressed, shift investment toward usability improvements and long-term innovation.

This approach balances customer satisfaction, engineering capacity, and strategic growth while maximizing product value.

""")
    # =====================================================
    # AI Insights
    # =====================================================

    with ai_tab:

        st.subheader("Executive AI Report")

        with st.container(border=True):

            st.markdown(f"""

### Executive Summary

{executive_summary}

---

### Overall Assessment

The uploaded customer feedback indicates an overall product health score of **{health_score}/100**.

The AI identified **{len(category_df)} primary product themes**, **{high} high-priority customer issues**, and an estimated customer satisfaction score of **{sentiment_score}%**.

Business impact is currently assessed as **{business_impact}**, with an AI confidence score of **{confidence}% ({confidence_label})**.

The strongest recommendation is to resolve **{top_issue.lower()}** before expanding feature development.

""")

    st.divider()

    # ===============================================
    # AI Recommendations
    # ===============================================

    st.subheader("Recommended Actions")

    recommendations = []

    if high > 0:

        recommendations.append(
            "Prioritize engineering resources toward high-priority customer issues."
        )

    if sentiment_score < 75:

        recommendations.append(
            "Improve customer satisfaction through targeted usability improvements."
        )

    if len(category_df):

        recommendations.append(
            "Continue monitoring recurring product themes after each release."
        )

    recommendations.append(
        "Use customer feedback as a roadmap input for future planning."
    )

    for i, recommendation in enumerate(recommendations, start=1):

        with st.container(border=True):

            st.markdown(f"### Recommendation {i}")

            st.write(recommendation)

    st.divider()

    # ===============================================
    # Executive Scorecard
    # ===============================================

    st.subheader("Executive Scorecard")

    scorecard = pd.DataFrame([
        {
            "Metric": "Product Health",
            "Score": f"{health_score}/100"
        },
        {
            "Metric": "Customer Satisfaction",
            "Score": f"{sentiment_score}%"
        },
        {
            "Metric": "Business Impact",
            "Score": business_impact
        },
        {
            "Metric": "High Priority Issues",
            "Score": high
        },
        {
            "Metric": "AI Confidence",
            "Score": f"{confidence}%"
        }
    ])

    st.dataframe(
        scorecard,
        hide_index=True,
        use_container_width=True
    )

    st.divider()

    # ===============================================
    # Product Copilot
    # ===============================================

    st.subheader("AI Product Copilot")

    user_question = st.text_input(
        "Ask a question about the analysis"
    )

    if user_question:

        st.info(
            "Connect this input to your Llama/Groq endpoint to provide conversational answers based on the uploaded analysis."
        )

    st.divider()

    # ===============================================
    # Executive Report
    # ===============================================

    st.subheader("Executive Report")

    report = f"""
PRODUCT INTELLIGENCE AI

Executive Summary

Product Health: {health_score}/100

Customer Satisfaction: {sentiment_score}%

Business Impact: {business_impact}

High Priority Issues: {high}

AI Confidence: {confidence}%

Key Recommendation:

Focus engineering investment on resolving
{top_issue} while continuing to improve
{top_theme}.

Expected Outcome:

• Higher customer satisfaction

• Better product quality

• Reduced operational risk

• Stronger roadmap prioritization

• Improved executive decision making

"""

    st.download_button(

        "Download Executive Report",

        report,

        file_name="executive_report.txt",

        mime="text/plain"

    )