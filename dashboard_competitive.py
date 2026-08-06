import streamlit as st
import pandas as pd
from theme import inject_theme

inject_theme()


def show_competitive_dashboard(results):

    # =====================================================
    # Custom CSS
    # =====================================================

    st.markdown("""
    <style>

    .stApp{
        background: var(--background-color);
    }

    .kpi-card{
        background: var(--secondary-background-color);
        border-left:6px solid var(--primary-color);
        border-radius:14px;
        padding:22px;
        box-shadow:0 4px 12px rgba(0,0,0,.08);
    }

    .kpi-title{
        font-size:15px;
        color: var(--text-color);
        opacity:.7;
        font-weight:600;
    }

    .kpi-number{
        font-size:40px;
        font-weight:700;
        color: var(--text-color);
    }

    .kpi-trend{
        color: var(--text-color);
        opacity:.8;
        font-size:13px;
        margin-top:8px;
    }

    </style>
    """, unsafe_allow_html=True)

    # =====================================================
    # Load Competitive Analysis
    # =====================================================

    competitive = results.get("competitive_analysis", {})

    executive_summary = competitive.get("executive_summary", "")

    market_position = competitive.get("market_position", {})

    strengths = competitive.get("competitor_strengths", [])

    weaknesses = competitive.get("competitor_weaknesses", [])

    opportunities = competitive.get("competitive_gaps", [])

    customer_opportunities = competitive.get(
        "customer_opportunities",
        []
    )

    recommended_initiatives = competitive.get(
        "recommended_initiatives",
        []
    )

    strategic_actions = competitive.get(
        "strategic_actions",
        []
    )

    scorecard = competitive.get("scorecard", [])
    # =====================================================
    # Executive Metrics
    # =====================================================

    strength_count = len(strengths)
    weakness_count = len(weaknesses)
    opportunity_count = len(opportunities)

    recommendation_count = len(recommended_initiatives)

    strategy_count = len(strategic_actions)

    market_label = market_position.get(
        "overall_position",
        "Unknown"
    )

    market_reason = market_position.get(
        "reason",
        "No assessment available."
    )


    # Keep a simple score only for dashboard visuals

    market_score = max(
        60,
        min(
            100,
            80
            + strength_count * 4
            - weakness_count * 5
            + opportunity_count * 2
        )
    )

    if weakness_count >= 5:
        competitive_risk = "High"
    elif weakness_count >= 3:
        competitive_risk = "Medium"
    else:
        competitive_risk = "Low"
    # =====================================================
    # Title
    # =====================================================

    st.header("Competitive Intelligence Dashboard")

    st.caption(
        "AI-generated competitive benchmarking, market analysis, and strategic recommendations."
    )

    # =====================================================
    # Executive Overview
    # =====================================================

    st.subheader("Executive Overview")

    overview_left, overview_right = st.columns([3, 1])

    biggest_strength = (
        strengths[0].get("strength", "Unknown")
        if strengths and isinstance(strengths[0], dict)
        else "No major competitive advantages identified."
    )

    biggest_gap = (
        weaknesses[0].get("weakness", "Unknown")
        if weaknesses and isinstance(weaknesses[0], dict)
        else "No significant competitive gaps identified."
    )

    top_opportunity = (
        opportunities[0].get("gap", "Unknown")
        if opportunities and isinstance(opportunities[0], dict)
        else "No major market opportunities identified."
    )

    with overview_left:

        with st.container(border=True):

            st.markdown(f"""
    ### AI Executive Summary

    **Market Position:** **{market_label} ({market_score}/100)**

    **Strongest Competitive Advantage:** **{biggest_strength}**

    **Largest Competitive Gap:** **{biggest_gap}**

    **📈 Highest Growth Opportunity:** **{top_opportunity}**

    **Executive Recommendation**

    Focus product investment on **{top_opportunity.lower()}** while addressing **{biggest_gap.lower()}** to strengthen long-term market differentiation.

    ---

    ### Executive Takeaway

    Competitive benchmarking indicates the organization is currently positioned as **{market_label.lower()}**.

    The analysis identified **{strength_count} competitive strengths**, **{weakness_count} competitive weaknesses**, and **{opportunity_count} market opportunities**.

    Leadership should prioritize closing high-impact competitive gaps while accelerating investment in differentiated product capabilities.
    """)

    with overview_right:

        if market_score >= 85:
            st.success(f"Market Position\n\n{market_score}/100")
        elif market_score >= 70:
            st.warning(f"Market Position\n\n{market_score}/100")
        else:
            st.error(f"Market Position\n\n{market_score}/100")

        if competitive_risk == "Low":
            st.success("Competitive Risk\n\nLow")
        elif competitive_risk == "Medium":
            st.warning("Competitive Risk\n\nMedium")
        else:
            st.error("Competitive Risk\n\nHigh")

        st.info(f"📈 Opportunities\n\n{opportunity_count}")

        st.info(f"AI Opportunities\n\n{recommendation_count}")

    st.divider()

    # =====================================================
    # Competitive Benchmark
    # =====================================================

    st.subheader("Competitive Benchmark")

    col1, col2, col3 = st.columns(3)

    with col1:

        with st.container(border=True):

            st.markdown("## Competitive Advantages")

            if strengths:

                for item in strengths:

                    if not isinstance(item, dict):
                        continue

                    st.success(item.get("strength", "Unknown"))

                    business_value = item.get("business_value", "")

                    if business_value:
                        st.caption(f"Business Value: {business_value}")

                    evidence = item.get("evidence", [])

                    if evidence:
                        with st.expander("View Evidence"):
                            for source in evidence:
                                st.write(f"• {source}")

            else:
                st.info("No competitive advantages identified.")

    with col2:

        with st.container(border=True):

            st.markdown("## Competitive Gaps")

            if weaknesses:

                for item in weaknesses:

                    if not isinstance(item, dict):
                        continue

                    st.error(item.get("weakness", "Unknown"))

                    business_risk = item.get("business_risk", "")

                    if business_risk:
                        st.caption(f"Business Risk: {business_risk}")

                    evidence = item.get("evidence", [])

                    if evidence:
                        with st.expander("View Evidence"):
                            for source in evidence:
                                st.write(f"• {source}")

            else:
                st.info("No competitive weaknesses identified.")

    with col3:

        with st.container(border=True):

            st.markdown("## Investment Opportunities")

            if opportunities:

                for item in opportunities:

                    if not isinstance(item, dict):
                        continue

                    st.markdown(
                        f"**• {item.get('gap', 'Unknown')}**"
                    )

                    reason = item.get("reason", "")

                    if reason:
                        st.caption(reason)

                    evidence = item.get("evidence", [])

                    if evidence:
                        with st.expander("View Evidence"):
                            for source in evidence:
                                st.write(f"• {source}")

            else:

                st.info("No strategic opportunities identified.")

    st.divider()

    # =====================================================
    # Strategic Themes
    # =====================================================

    st.subheader(" Strategic Themes")

    theme1 = customer_opportunities[:2]
    theme2 = weaknesses[:2]
    theme3 = recommended_initiatives[:2]

    col1, col2, col3 = st.columns(3)

    # =============================================
    # Customer Experience
    # =============================================

    with col1:

        with st.container(border=True):

            st.markdown("## Customer Experience")

            if theme1:

                for item in theme1:

                    if isinstance(item, dict):
                        st.success(
                            item.get("opportunity", "Unknown")
                        )

            else:
                st.info("No customer experience initiatives identified.")

            st.markdown("---")

            st.metric(
                "Strategic Priority",
                "High"
            )

            st.metric(
                "Investment Horizon",
                "Near Term"
            )

            st.metric(
                "Business Goal",
                "Retention"
            )


    # =============================================
    # Competitive Differentiation
    # =============================================

    with col2:

        with st.container(border=True):

            st.markdown("## Competitive Differentiation")

            if theme2:

                for item in theme2:

                    if not isinstance(item, dict):
                        continue

                    st.error(item.get("weakness", "Unknown"))

            else:
                st.info("No competitive gaps identified.")

            st.markdown("---")

            st.metric(
                "Strategic Priority",
                "High"
            )

            st.metric(
                "Investment Horizon",
                "Immediate"
            )

            st.metric(
                "Business Goal",
                "Market Share"
            )


    # =============================================
    # Product Innovation
    # =============================================

    with col3:

        with st.container(border=True):

            st.markdown("## Product Innovation")

            if theme3:

                for item in theme3:

                    if not isinstance(item, dict):
                        continue

                    st.info(item.get("initiative", "Unknown"))

            else:
                st.info("No innovation initiatives identified.")

            st.markdown("---")

            st.metric(
                "Strategic Priority",
                "Medium"
            )

            st.metric(
                "Investment Horizon",
                "Long Term"
            )

            st.metric(
                "Business Goal",
                "Differentiation"
            )

    st.divider()
    # =====================================================
    # AI Product Innovation Pipeline
    # =====================================================

    st.subheader("Recommended Innovation Pipeline")

    if recommended_initiatives:

        cols = st.columns(2)

        for i, feature in enumerate(recommended_initiatives):

            if not isinstance(feature, dict):
                continue

            with cols[i % 2]:

                with st.container(border=True):

                    initiative = feature.get(
                        "initiative",
                        "Unknown Initiative"
                    )

                    priority = feature.get(
                        "priority",
                        "Unknown"
                    )

                    reason = feature.get(
                        "reason",
                        ""
                    )

                    evidence = feature.get(
                        "evidence",
                        []
                    )

                    st.markdown(f"## {initiative}")

                    st.markdown("### Innovation Priority")
                    st.info(priority)

                    st.markdown("### Strategic Rationale")
                    st.write(reason)

                    if evidence:

                        st.markdown("### Supporting Evidence")

                        for source in evidence:
                            st.write(f"• {source}")
    else:

        st.info("No AI product recommendations available.")

    st.divider()

    # =====================================================
    # Product Investment Roadmap
    # =====================================================

    st.subheader("Product Investment Roadmap")

    roadmap_items = []

    roadmap_items.extend(
        [
            ("Immediate", item.get("weakness", "Unknown"))
            for item in weaknesses[:2]
            if isinstance(item, dict)
        ]
    )

    roadmap_items.extend(
        [
            ("Next Release", item.get("opportunity", "Unknown"))
            for item in customer_opportunities[:2]
            if isinstance(item, dict)
        ]
    )

    roadmap_items.extend(
        [
            ("Strategic", item.get("initiative", "Unknown"))
            for item in recommended_initiatives[:2]
            if isinstance(item, dict)
        ]
    )

    if roadmap_items:

        cols = st.columns(min(3, len(roadmap_items)))

        for col, (phase, item) in zip(cols, roadmap_items):

            with col:

                with st.container(border=True):

                    if phase == "Immediate":
                        st.error("🔴 Immediate")

                    elif phase == "Next Release":
                        st.warning("🟡 Next Release")

                    else:
                        st.success("🟢 Strategic")

                    st.markdown(f"### {item}")

                    if phase == "Immediate":

                        st.write(
                            "Close competitive gaps impacting market position."
                        )

                    elif phase == "Next Release":

                        st.write(
                            "Deliver requested customer capabilities."
                        )

                    else:

                        st.write(
                            "Invest in long-term product differentiation."
                        )

    else:

        st.info("No roadmap items available.")

    st.divider()

    # =====================================================
    # Executive Brief
    # =====================================================

    st.subheader("Executive Summary")

    with st.container(border=True):

        st.markdown(f"""
## AI Executive Strategy Report

This competitive intelligence assessment combines benchmarking, customer demand,
market opportunities, and AI-generated strategic recommendations to support
executive product planning.

---

### Executive Assessment

**Current Market Position:** **{market_label} ({market_score}/100)**

**Reason:** {market_reason}

**Competitive Risk:** **{competitive_risk}**

**Competitive Strengths Identified:** **{strength_count}**

**Competitive Weaknesses Identified:** **{weakness_count}**

**Growth Opportunities:** **{opportunity_count}**

**Recommended Product Investments:** **{recommendation_count}**

---

### AI Executive Summary

{executive_summary or "No executive summary available."}
""")

        metric1, metric2, metric3, metric4 = st.columns(4)

        with metric1:
            st.metric(
                "Market Score",
                f"{market_score}/100"
            )

        with metric2:
            st.metric(
                "Competitive Gaps",
                weakness_count
            )

        with metric3:
            st.metric(
                "Growth Opportunities",
                opportunity_count
            )

        with metric4:
            st.metric(
                "AI Recommendations",
                recommendation_count
            )

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
    # =====================================================
    # Strategic Decision Support
    # =====================================================

    st.subheader("Investment Recommendations")

    with st.container(border=True):

        st.markdown("""
### Executive Investment Portfolio

The initiatives below have been prioritized using competitive benchmarking,
customer demand, market opportunity, and AI strategic analysis.

These recommendations are intended to support roadmap planning,
capital allocation, and executive decision making.
""")

        portfolio = []

        # Competitive gaps
        for item in weaknesses[:2]:
            if isinstance(item, dict):
                portfolio.append({
                    "Initiative": item.get("weakness", "Unknown"),
                    "Portfolio": "Protect Market Position",
                    "Investment": "Immediate",
                    "Business Value": "High",
                    "Customer Impact": "Medium",
                    "Executive Decision": "Approve Funding"
                })

        # Customer demand
        for item in customer_opportunities[:2]:
            if isinstance(item, dict):
                portfolio.append({
                    "Initiative": item.get("opportunity", "Unknown"),
                    "Portfolio": "Growth",
                    "Investment": "Next Release",
                    "Business Value": "High",
                    "Customer Impact": "High",
                    "Executive Decision": "Roadmap Priority"
                })

        # Innovation
        for item in recommended_initiatives[:2]:
            if isinstance(item, dict):
                portfolio.append({
                    "Initiative": item.get("initiative", "Unknown"),
                    "Portfolio": "Innovation",
                    "Investment": "Future Planning",
                    "Business Value": "Medium",
                    "Customer Impact": "High",
                    "Executive Decision": "Evaluate Business Case"
                })

        if portfolio:

            portfolio_df = pd.DataFrame(portfolio)

            st.dataframe(
                portfolio_df,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("No investment recommendations available.")

        st.markdown("### Executive Recommendation")

        st.info(f"""
**Current Competitive Position:** **{market_label}**

### Recommended Actions

- Fund initiatives that eliminate the most critical competitive gaps.
- Prioritize customer-requested capabilities for the next product release.
- Continue investing in differentiated AI-enabled capabilities to maintain long-term competitive advantage.

### Executive Investment Outlook

Based on the current competitive landscape, the organization has **{opportunity_count} high-value market opportunities** and **{recommendation_count} strategic innovation opportunities**.

The recommended investment strategy balances **short-term competitive improvements** with **long-term product differentiation**, supporting sustainable growth while reducing competitive risk.
""")