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

    competitive = results.get(
        "competitive_analysis",
        {}
    )

    strengths = competitive.get(
        "competitor_strengths",
        []
    )

    weaknesses = competitive.get(
        "competitor_weaknesses",
        []
    )

    opportunities = competitive.get(
        "competitive_gaps",
        []
    )

    customer_requests = competitive.get(
        "customer_requested_features",
        []
    )

    recommendations = competitive.get(
        "recommended_features",
        []
    )

    strategic_actions = competitive.get(
        "strategic_recommendations",
        []
    )
        # =====================================================
    # Executive Metrics
    # =====================================================

    strength_count = len(strengths)
    weakness_count = len(weaknesses)
    opportunity_count = len(opportunities)
    recommendation_count = len(recommendations)
    strategy_count = len(strategic_actions)

    market_score = max(
        0,
        min(
            100,
            80
            + strength_count * 4
            - weakness_count * 5
            + opportunity_count * 2
        )
    )

    if market_score >= 85:
        market_position = "Market Leader"

    elif market_score >= 70:
        market_position = "Strong"

    elif market_score >= 55:
        market_position = "Competitive"

    else:
        market_position = "Needs Investment"

    if weakness_count >= 5:
        competitive_risk = "High"

    elif weakness_count >= 3:
        competitive_risk = "Medium"

    else:
        competitive_risk = "Low"
        # =====================================================
    # Title
    # =====================================================

    st.title("Product Intelligence AI")

    st.caption(
        "Executive Competitive Intelligence Dashboard for strategic product planning, market benchmarking, and investment decisions."
    )
        # =====================================================
    # Executive KPI Dashboard
    # =====================================================

    def executive_card(title, value, subtitle):

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-number">{value}</div>
            <div class="kpi-trend">{subtitle}</div>
        </div>
        """, unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        executive_card(
            "🏆 Market Position",
            f"{market_score}/100",
            market_position
        )

    with c2:
        executive_card(
            "⚠️ Competitive Risk",
            competitive_risk,
            "Current market exposure"
        )

    with c3:
        executive_card(
            "📈 Growth Opportunities",
            opportunity_count,
            "Competitive gaps identified"
        )

    with c4:
        executive_card(
            "💡 Innovation Pipeline",
            recommendation_count,
            "AI product ideas"
        )

    with c5:
        executive_card(
            "🎯 Strategic Actions",
            strategy_count,
            "Leadership initiatives"
        )

    st.divider()
        # =====================================================
    # Executive Overview
    # =====================================================

    st.subheader("📊 Executive Overview")

    overview_left, overview_right = st.columns([3, 1])

    biggest_strength = (
        strengths[0]
        if strengths
        else "No major competitive advantages identified."
    )

    biggest_gap = (
        weaknesses[0]
        if weaknesses
        else "No significant competitive gaps identified."
    )

    top_opportunity = (
        opportunities[0]
        if opportunities
        else "No major market opportunities identified."
    )

    with overview_left:

        with st.container(border=True):

            st.markdown(f"""
### 🤖 AI Executive Summary

**🏆 Market Position:** **{market_position} ({market_score}/100)**

**💪 Strongest Competitive Advantage:** **{biggest_strength}**

**⚠️ Largest Competitive Gap:** **{biggest_gap}**

**📈 Highest Growth Opportunity:** **{top_opportunity}**

**💡 Executive Recommendation**

Focus product investment on **{top_opportunity.lower()}** while addressing **{biggest_gap.lower()}** to strengthen long-term market differentiation.

---

### Executive Takeaway

Competitive benchmarking indicates the organization is currently positioned as **{market_position.lower()}**.

The analysis identified **{strength_count} competitive strengths**, **{weakness_count} competitive weaknesses**, and **{opportunity_count} market opportunities**.

Leadership should prioritize closing high-impact competitive gaps while accelerating investment in differentiated product capabilities.
            """)

    with overview_right:

        if market_score >= 85:
            st.success(f"🏆 Market Position\n\n{market_score}/100")
        elif market_score >= 70:
            st.warning(f"🏆 Market Position\n\n{market_score}/100")
        else:
            st.error(f"🏆 Market Position\n\n{market_score}/100")

        if competitive_risk == "Low":
            st.success("⚠️ Competitive Risk\n\nLow")
        elif competitive_risk == "Medium":
            st.warning("⚠️ Competitive Risk\n\nMedium")
        else:
            st.error("⚠️ Competitive Risk\n\nHigh")

        st.info(f"📈 Opportunities\n\n{opportunity_count}")

        st.info(f"💡 AI Opportunities\n\n{recommendation_count}")

    st.divider()

    # =====================================================
    # Competitive Benchmark
    # =====================================================

    st.subheader("🏆 Competitive Benchmark")

    col1, col2, col3 = st.columns(3)

    with col1:

        with st.container(border=True):

            st.markdown("## 💪 Competitive Advantages")

            if strengths:

                for item in strengths:
                    st.success(item)

            else:
                st.info("No competitive advantages identified.")

    with col2:

        with st.container(border=True):

            st.markdown("## ⚠️ Competitive Gaps")

            if weaknesses:

                for item in weaknesses:
                    st.error(item)

            else:
                st.info("No competitive weaknesses identified.")

    with col3:

        with st.container(border=True):

            st.markdown("## 🚀 Investment Opportunities")

            if opportunities:

                for item in opportunities:

                    st.markdown(f"**• {item}**")

                    st.caption(
                        "Potential for revenue growth, product differentiation, "
                        "or market expansion."
                    )

            else:

                st.info("No strategic opportunities identified.")

    st.divider()

    # =====================================================
    # Market Opportunities
    # =====================================================

    st.subheader("📈 Market Opportunities")

    if opportunities:

        cols = st.columns(min(3, len(opportunities)))

        for col, opportunity in zip(cols, opportunities):

            with col:

                with st.container(border=True):

                    st.markdown(f"## 🚀 Opportunity")

                    st.write(opportunity)

                    st.markdown("---")

                    st.metric("Strategic Impact", "High")

                    st.metric("Customer Demand", "High")

                    st.metric("Investment Horizon", "6-12 Months")
    else:

        st.info("No market opportunities identified.")

    st.divider()

    # =====================================================
    # Voice of Customer
    # =====================================================

    st.subheader("🗣️ Voice of Customer")

    if customer_requests:

        for request in customer_requests:

            with st.container(border=True):

                left, right = st.columns([3,1])

                with left:

                    st.markdown(f"### 💬 {request}")

                    st.write(
                        "This feature has been consistently requested by customers "
                        "and represents an opportunity to improve customer satisfaction "
                        "and product competitiveness."
                    )

                with right:

                    st.metric(
                        "Business Value",
                        "High"
                    )

                    st.metric(
                        "Revenue Impact",
                        "Medium"
                    )

                    st.metric(
                        "Roadmap Priority",
                        "Next Release"
                    )

                    st.success("Leadership Candidate")
                    
    else:

        st.info("No customer feature requests available.")

    st.divider()

    # =====================================================
    # Strategic Themes
    # =====================================================

    st.subheader("🧭 Strategic Themes")

    theme1 = customer_requests[:2]
    theme2 = weaknesses[:2]
    theme3 = recommendations[:2]

    col1, col2, col3 = st.columns(3)

    # =============================================
    # Customer Experience
    # =============================================

    with col1:

        with st.container(border=True):

            st.markdown("## 😊 Customer Experience")

            if theme1:

                for item in theme1:
                    st.success(item)

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

            st.markdown("## 🏆 Competitive Differentiation")

            if theme2:

                for item in theme2:
                    st.error(item)

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

            st.markdown("## 🚀 Product Innovation")

            if theme3:

                for item in theme3:
                    st.info(item)

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

    st.subheader("🚀 AI Product Innovation Pipeline")

    if recommendations:

        cols = st.columns(2)

        for i, feature in enumerate(recommendations):

            with cols[i % 2]:

                with st.container(border=True):

                    st.markdown(f"## 💡 {feature}")

                    st.markdown("### Innovation Priority")
                    st.success("High")

                    st.markdown("### Competitive Differentiation")
                    st.info("Strong")

                    st.markdown("### Expected Customer Impact")
                    st.success("High")

                    st.markdown("### Executive Recommendation")

                    st.write(
                        "Evaluate this capability for inclusion in the next strategic roadmap cycle."
                    )

    else:

        st.info("No AI product recommendations available.")

    st.divider()

    # =====================================================
    # Strategic Initiatives
    # =====================================================

    st.subheader("🎯 Strategic Initiatives")

    if strategic_actions:

        for action in strategic_actions:

            with st.container(border=True):

                st.markdown(f"## 📌 {action}")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Priority",
                        "High"
                    )

                with col2:
                    st.metric(
                        "Timeline",
                        "Next 6 Months"
                    )

                with col3:
                    st.metric(
                        "Business Impact",
                        "High"
                    )

                st.markdown("### Expected Outcome")

                st.write(
                    "Strengthen market positioning while increasing customer value and competitive differentiation."
                )

    else:

        st.info("No strategic initiatives available.")

    st.divider()
        # =====================================================
    # Product Investment Roadmap
    # =====================================================

    st.subheader("🗺️ Product Investment Roadmap")

    roadmap_items = []

    roadmap_items.extend(
        [("Immediate", item) for item in weaknesses[:2]]
    )

    roadmap_items.extend(
        [("Next Release", item) for item in customer_requests[:2]]
    )

    roadmap_items.extend(
        [("Strategic", item) for item in recommendations[:2]]
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

    st.subheader("📄 Executive Brief")

    with st.container(border=True):

        st.markdown(f"""
## 🤖 AI Executive Strategy Report

This competitive intelligence assessment combines benchmarking, customer demand,
market opportunities, and AI-generated strategic recommendations to support
executive product planning.

---

### Executive Assessment

**Current Market Position:** **{market_position} ({market_score}/100)**

**Competitive Risk:** **{competitive_risk}**

**Competitive Strengths Identified:** **{strength_count}**

**Competitive Weaknesses Identified:** **{weakness_count}**

**Growth Opportunities:** **{opportunity_count}**

**Recommended Product Investments:** **{recommendation_count}**

---

### AI Executive Summary

{results.get("executive_summary", "No executive summary available.")}

---
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

    st.divider()

    # =====================================================
    # Strategic Decision Support
    # =====================================================

    st.subheader("🎯 Strategic Decision Support")

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
            portfolio.append({
                "Initiative": item,
                "Portfolio": "Protect Market Position",
                "Investment": "Immediate",
                "Business Value": "High",
                "Customer Impact": "Medium",
                "Executive Decision": "Approve Funding"
            })

        # Customer demand
        for item in customer_requests[:2]:
            portfolio.append({
                "Initiative": item,
                "Portfolio": "Growth",
                "Investment": "Next Release",
                "Business Value": "High",
                "Customer Impact": "High",
                "Executive Decision": "Roadmap Priority"
            })

        # Innovation
        for item in recommendations[:2]:
            portfolio.append({
                "Initiative": item,
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

        st.markdown("---")

        st.markdown("### Executive Portfolio Summary")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Immediate Investments",
                len(weaknesses[:2])
            )

        with col2:
            st.metric(
                "Roadmap Candidates",
                len(customer_requests[:2])
            )

        with col3:
            st.metric(
                "Innovation Bets",
                len(recommendations[:2])
            )

        with col4:
            st.metric(
                "Estimated Strategic Value",
                "High"
            )

        st.markdown("---")

        st.markdown("### Executive Recommendation")

        st.info(f"""
    **Current Competitive Position:** **{market_position}**

    ### Recommended Actions

    ✅ Fund initiatives that eliminate the most critical competitive gaps.

    ✅ Prioritize customer-requested capabilities for the next product release.

    ✅ Continue investing in differentiated AI-enabled capabilities to maintain long-term competitive advantage.

    ### Executive Investment Outlook

    Based on the current competitive landscape, the organization has **{opportunity_count} high-value market opportunities** and **{recommendation_count} strategic innovation opportunities**.

    The recommended investment strategy balances **short-term competitive improvements** with **long-term product differentiation**, supporting sustainable growth while reducing competitive risk.
    """)