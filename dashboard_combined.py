import streamlit as st
import pandas as pd
from theme import inject_theme

inject_theme()


def show_combined_dashboard(results):

    # ==========================================================
    # Custom CSS
    # ==========================================================

    st.markdown("""
    <style>

    .kpi-card{
        background:var(--secondary-background-color);
        border-left:5px solid var(--primary-color);
        border-radius:12px;
        padding:20px;
        box-shadow:0 3px 10px rgba(0,0,0,.08);
    }

    .kpi-title{
        font-size:14px;
        color:var(--text-color);
        opacity:.70;
        font-weight:600;
    }

    .kpi-number{
        font-size:34px;
        font-weight:700;
        color:var(--text-color);
    }

    .kpi-subtitle{
        color:var(--text-color);
        opacity:.75;
        font-size:13px;
        margin-top:6px;
    }

    </style>
    """, unsafe_allow_html=True)

    # ==========================================================
    # Load Data
    # ==========================================================

    customer = results.get("customer_analysis", {})
    competitive = results.get("competitive_analysis", {})

    categories = customer.get("categories", [])
    priorities = customer.get("priorities", [])
    sentiments = customer.get("sentiment", [])

    strengths = competitive.get("competitor_strengths", [])
    weaknesses = competitive.get("competitor_weaknesses", [])
    opportunities = competitive.get("competitive_gaps", [])
    recommendations = competitive.get("recommended_features", [])

    if isinstance(categories, dict):
        categories = categories.get("categories", [])

    if isinstance(priorities, dict):
        priorities = priorities.get("priorities", [])

    if isinstance(sentiments, dict):
        sentiments = sentiments.get("sentiments", [])

    # ==========================================================
    # KPI Calculations
    # ==========================================================

    high = sum(
        1 for p in priorities
        if isinstance(p, dict)
        and p.get("priority","").lower()=="high"
    )

    medium = sum(
        1 for p in priorities
        if isinstance(p, dict)
        and p.get("priority","").lower()=="medium"
    )

    low = sum(
        1 for p in priorities
        if isinstance(p, dict)
        and p.get("priority","").lower()=="low"
    )

    positive = len([
        s for s in sentiments
        if isinstance(s, dict)
        and s.get("sentiment")=="Positive"
    ])

    total_sentiment = len(sentiments)

    sentiment_score = (
        round((positive / total_sentiment) * 100)
        if total_sentiment else 0
    )

    health_score = max(
        0,
        100 - high*15 - medium*7 - low*3
    )

    market_score = max(
        0,
        min(
            100,
            80 + len(strengths)*4 - len(weaknesses)*5
        )
    )

    confidence = min(
        100,
        80 + len(categories)
    )

    # ==========================================================
    # Header
    # ==========================================================

    st.header("Executive Analysis")

    st.caption(
        "Unified customer and competitive insights to support product strategy and executive decision-making."
    )

    # ==========================================================
    # KPI Cards
    # ==========================================================

    def card(title,value,subtitle):

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-number">{value}</div>
            <div class="kpi-subtitle">{subtitle}</div>
        </div>
        """,unsafe_allow_html=True)

    c1,c2,c3,c4,c5,c6 = st.columns(6)

    with c1:
        card(
            "Product Health",
            f"{health_score}/100",
            "Overall"
        )

    with c2:
        card(
            "Market Position",
            f"{market_score}/100",
            "Competitive"
        )

    with c3:
        card(
            "Customer Satisfaction",
            f"{sentiment_score}%",
            "Positive Sentiment"
        )

    with c4:
        card(
            "High Priority",
            high,
            "Customer Issues"
        )

    with c5:
        card(
            "Growth Opportunities",
            len(opportunities),
            "Market"
        )

    with c6:
        card(
            "AI Confidence",
            f"{confidence}%",
            "Analysis"
        )

    st.divider()
        # ==========================================================
    # Executive Summary
    # ==========================================================

    st.subheader("Executive Summary")

    top_issue = "No major issues identified."

    if priorities:
        top_issue = priorities[0].get(
            "issue",
            "No major issues identified."
        )

    strongest_advantage = (
        strengths[0]
        if strengths
        else "No competitive strengths identified."
    )

    largest_gap = (
        weaknesses[0]
        if weaknesses
        else "No significant competitive gaps identified."
    )

    best_opportunity = (
        opportunities[0]
        if opportunities
        else "No major opportunities identified."
    )

    left, right = st.columns([3,1])

    with left:

        with st.container(border=True):

            st.markdown(f"""

### Executive Assessment

The AI analysis combined customer feedback with competitive benchmarking to provide an overall assessment of current product performance.

#### Customer Insights

- Product Health Score: **{health_score}/100**
- Customer Satisfaction: **{sentiment_score}%**
- High Priority Issues: **{high}**

#### Competitive Position

- Market Score: **{market_score}/100**
- Strongest Competitive Advantage: **{strongest_advantage}**
- Largest Competitive Gap: **{largest_gap}**

#### Executive Recommendation

The highest priority should be resolving **{top_issue.lower()}** while investing in **{best_opportunity.lower()}**.

This approach improves customer satisfaction while strengthening long-term competitive positioning.

""")

    with right:

        st.metric(
            "Product Health",
            f"{health_score}/100"
        )

        st.metric(
            "Market Score",
            f"{market_score}/100"
        )

        st.metric(
            "Customer Satisfaction",
            f"{sentiment_score}%"
        )

        st.metric(
            "Growth Opportunities",
            len(opportunities)
        )

    st.divider()

    # ==========================================================
    # Customer vs Competition
    # ==========================================================

    st.subheader("Customer vs. Competition")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.markdown("### Customer Priorities")

            if priorities:

                for item in priorities[:5]:

                    issue = item.get("issue","Unknown")

                    priority = item.get(
                        "priority",
                        "Medium"
                    )

                    st.write(
                        f"**{issue}**"
                    )

                    st.caption(
                        f"Priority: {priority}"
                    )

            else:

                st.info(
                    "No customer priorities identified."
                )

    with col2:

        with st.container(border=True):

            st.markdown("### Competitive Gaps")

            if weaknesses:

                for item in weaknesses[:5]:

                    st.write(f"**{item}**")

            else:

                st.info(
                    "No competitive gaps identified."
                )

    st.divider()
        # ==========================================================
    # Executive Investment Priorities
    # ==========================================================

    st.subheader("Executive Investment Priorities")

    investments = []

    # Customer Issues
    for item in priorities[:3]:

        if not isinstance(item, dict):
            continue

        investments.append({

            "Initiative": item.get("issue", "Unknown"),

            "Source": "Customer Feedback",

            "Priority": item.get("priority", "Medium"),

            "Business Value": "High",

            "Timeline": "Next Release"

        })

    # Competitive Gaps
    for item in weaknesses[:3]:

        investments.append({

            "Initiative": item,

            "Source": "Competitive Analysis",

            "Priority": "High",

            "Business Value": "High",

            "Timeline": "Immediate"

        })

    # Opportunities
    for item in opportunities[:3]:

        investments.append({

            "Initiative": item,

            "Source": "Growth Opportunity",

            "Priority": "Medium",

            "Business Value": "Medium",

            "Timeline": "Future"

        })

    if investments:

        investment_df = pd.DataFrame(investments)

        st.dataframe(

            investment_df,

            use_container_width=True,

            hide_index=True

        )

    else:

        st.info("No investment opportunities available.")

    st.divider()

    # ==========================================================
    # Product Roadmap
    # ==========================================================

    st.subheader("Product Roadmap")

    immediate, next_release, future = st.columns(3)

    with immediate:

        with st.container(border=True):

            st.markdown("### Immediate")

            if weaknesses:

                for item in weaknesses[:3]:

                    st.write(f"• {item}")

            else:

                st.write("No immediate initiatives.")

    with next_release:

        with st.container(border=True):

            st.markdown("### Next Release")

            if priorities:

                for item in priorities[:3]:

                    if isinstance(item, dict):

                        st.write(
                            f"• {item.get('issue','Unknown')}"
                        )

            else:

                st.write("No roadmap items.")

    with future:

        with st.container(border=True):

            st.markdown("### Future Investment")

            if opportunities:

                for item in opportunities[:3]:

                    st.write(f"• {item}")

            else:

                st.write("No future opportunities.")

    st.divider()

        # ==========================================================
    # Leadership Recommendation
    # ==========================================================

    st.subheader("Leadership Recommendation")

    with st.container(border=True):

        # Overall recommendation
        if health_score >= 85 and market_score >= 85:

            recommendation = (
                "The product is performing well from both a customer and "
                "competitive perspective. Continue investing in innovation "
                "while maintaining the current roadmap."
            )

        elif health_score >= 70 and market_score >= 70:

            recommendation = (
                "The product is well positioned, but several customer pain "
                "points and competitive gaps should be addressed in the next "
                "release to strengthen market position."
            )

        else:

            recommendation = (
                "Leadership should prioritize resolving the highest-impact "
                "customer issues while closing competitive feature gaps before "
                "expanding investment into new capabilities."
            )

        st.markdown("### Executive Recommendation")

        st.write(recommendation)

        st.markdown("---")

        metric1, metric2, metric3 = st.columns(3)

        with metric1:

            st.metric(
                "Product Health",
                f"{health_score}/100"
            )

        with metric2:

            st.metric(
                "Market Position",
                f"{market_score}/100"
            )

        with metric3:

            st.metric(
                "Customer Satisfaction",
                f"{sentiment_score}%"
            )

        st.markdown("---")

        st.markdown("### Key Leadership Actions")

        actions = []

        if priorities:
            actions.append(
                "Resolve the highest-priority customer issues."
            )

        if weaknesses:
            actions.append(
                "Address the largest competitive gaps."
            )

        if opportunities:
            actions.append(
                "Invest in the highest-value growth opportunities."
            )

        actions.append(
            "Monitor customer sentiment after future product releases."
        )

        for action in actions:
            st.write(f"• {action}")

        st.markdown("---")

        st.markdown("### Executive Outlook")

        st.write(
            f"""
The combined AI analysis indicates a **Product Health Score of
{health_score}/100** and a **Competitive Position Score of
{market_score}/100**.

Based on customer feedback and competitive benchmarking, the product
currently has **{high} high-priority customer issues**, **{len(weaknesses)} competitive gaps**, and **{len(opportunities)} strategic growth opportunities**.

The recommended strategy is to balance short-term improvements that
increase customer satisfaction with long-term investments that strengthen
competitive differentiation.
"""
        )