import streamlit as st
import pandas as pd
import plotly.express as px


def show_dashboard(results):

    st.write(results)

    # =====================================================
    # Custom CSS
    # =====================================================

    st.markdown("""
    <style>

    .stApp{
        background:#F6F8FB;
    }

    .kpi-card{
        background:white;
        border-left:6px solid #005A9C;
        border-radius:14px;
        padding:22px;
        box-shadow:0 4px 12px rgba(0,0,0,.08);
    }

    .kpi-title{
        font-size:15px;
        color:#64748B;
        font-weight:600;
    }

    .kpi-number{
        font-size:40px;
        font-weight:700;
        color:#003B6F;
    }

    .kpi-trend{
        color:#059669;
        font-size:13px;
        margin-top:8px;
    }

    .priority-card{
        background:white;
        border-radius:10px;
        padding:16px;
        margin-bottom:12px;
        box-shadow:0 2px 8px rgba(0,0,0,.08);
    }

    .high{
        border-left:6px solid #DC2626;
    }

    .medium{
        border-left:6px solid #F59E0B;
    }

    .low{
        border-left:6px solid #16A34A;
    }

    .risk-card{
        background:#FFF7ED;
        border-left:6px solid #EA580C;
        border-radius:10px;
        padding:18px;
        margin-bottom:12px;
    }

    </style>
    """, unsafe_allow_html=True)

    # =====================================================
    # Data
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
    has_customer_analysis = (
        len(categories) > 0 or
        len(priorities) > 0 or
        len(roadmap) > 0 or
        len(sentiments) > 0
)
    category_df = pd.DataFrame(categories)
    sentiment_df = pd.DataFrame(sentiments)

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

    # =====================================================
    # Title
    # =====================================================

    st.header("Executive Dashboard")
    st.caption("AI-generated overview of customer feedback analysis.")

    # =====================================================
    # Customer Feedback Dashboard
    # =====================================================

    if has_customer_analysis:

        # ---------------- KPI Cards ----------------

        total_priorities = high + medium + low

        high_pct = (high / total_priorities * 100) if total_priorities else 0
        medium_pct = (medium / total_priorities * 100) if total_priorities else 0
        low_pct = (low / total_priorities * 100) if total_priorities else 0

        def kpi_card(title, value, subtitle):
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">{title}</div>
                <div class="kpi-number">{value}</div>
                <div class="kpi-trend">{subtitle}</div>
            </div>
            """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)

        cards = [
            ("📂 Categories", len(category_df), f"{len(category_df)} active themes"),
            ("🔥 High Priority", high, f"{high_pct:.0f}% of all priorities"),
            ("🟡 Medium Priority", medium, f"{medium_pct:.0f}% of all priorities"),
            ("🟢 Low Priority", low, f"{low_pct:.0f}% of all priorities"),
        ]

        for col, (title, value, subtitle) in zip([c1, c2, c3, c4], cards):
            with col:
                kpi_card(title, value, subtitle)

        st.divider()

        # ---------------- Categories & Sentiment ----------------

        left, right = st.columns([2, 1])

        with left:

            st.subheader("Customer Feedback Categories")

            if not category_df.empty:

                fig = px.bar(
                    category_df,
                    x="count",
                    y="category",
                    orientation="h",
                    text="count",
                    color="count",
                    color_continuous_scale="Blues"
                )

                fig.update_layout(
                    height=420,
                    xaxis_title="Feedback Count",
                    yaxis_title="",
                    coloraxis_showscale=False,
                    margin=dict(l=20, r=20, t=30, b=20)
                )

                fig.update_traces(textposition="outside")
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.info("No categories available.")

        with right:

            st.subheader("Sentiment Distribution")

            if not sentiment_df.empty:

                sentiment_counts = (
                    sentiment_df["sentiment"]
                    .value_counts()
                    .reset_index()
                )

                sentiment_counts.columns = ["Sentiment", "Count"]

                donut = px.pie(
                    sentiment_counts,
                    names="Sentiment",
                    values="Count",
                    hole=.65,
                    color="Sentiment",
                    color_discrete_map={
                        "Positive": "#22C55E",
                        "Neutral": "#FACC15",
                        "Negative": "#EF4444"
                    }
                )

                donut.update_layout(
                    showlegend=True,
                    margin=dict(l=10, r=10, t=20, b=20)
                )

                st.plotly_chart(donut, use_container_width=True)

            else:
                st.info("No sentiment data.")

        st.divider()

        # ---------------- Top Priorities ----------------

        st.subheader("Top Product Priorities")

        if priorities:

            for item in priorities:
                priority = item.get("priority", "").lower()
                issue = item.get("issue", "Unknown")

                st.markdown(f"""
                <div class="priority-card {priority}">
                    <b>{issue}</b><br>
                    <span style="color:#64748B;">
                        Priority: {priority.title()}
                    </span>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.info("No priorities available.")

        st.divider()

        # ---------------- Roadmap ----------------

        st.subheader("Three-Sprint Roadmap")

        if roadmap:

            c1, c2, c3 = st.columns(3)

            for col, sprint in zip([c1, c2, c3], roadmap):

                if not isinstance(sprint, dict):
                    continue

                with col:
                    with st.container(border=True):
                        st.markdown(f"### {sprint.get('sprint', 'Sprint')}")
                        st.write(sprint.get("goal", "No goal available."))

        else:
            st.info("No roadmap available.")

        st.divider()

    else:
        st.info("No customer feedback analysis available.")

    # =====================================================
    # Competitive Analysis
    # =====================================================

    st.subheader("Competitive Analysis")

    competitive = results.get("competitive_analysis", {})

    if competitive:

        left, right = st.columns(2)

        with left:

            with st.container(border=True):
                st.markdown("### 💪 Competitor Strengths")

                for item in competitive.get("competitor_strengths", []):
                    st.write(f"• {item}")

            with st.container(border=True):
                st.markdown("### ⚠️ Competitor Weaknesses")

                for item in competitive.get("competitor_weaknesses", []):
                    st.write(f"• {item}")

            with st.container(border=True):
                st.markdown("### 📉 Competitive Gaps")

                for item in competitive.get("competitive_gaps", []):
                    st.write(f"• {item}")

        with right:

            with st.container(border=True):
                st.markdown("### ⭐ Customer Requested Features")

                for item in competitive.get("customer_requested_features", []):
                    st.write(f"• {item}")

            with st.container(border=True):
                st.markdown("### 🚀 Recommended Features")

                for item in competitive.get("recommended_features", []):
                    st.write(f"• {item}")

            with st.container(border=True):
                st.markdown("### 🎯 Strategic Recommendations")

                for item in competitive.get("strategic_recommendations", []):
                    st.write(f"• {item}")

    else:

        st.info("No competitive analysis available.")

    st.divider()

    # =====================================================
    # Executive Summary
    # =====================================================

    st.subheader("Executive Summary")

    st.markdown(
        results.get(
            "executive_summary",
            "No executive summary available."
        )
    )