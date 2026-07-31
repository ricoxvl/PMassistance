from llm import (
    summarize_feedback,
    cluster_feedback,
    prioritize_feedback,
    generate_roadmap,
    analyze_sentiment,
    competitive_analysis,
    executive_summary,
    generate_jira_stories
)


def run_workflow(
    feedback_list,
    competitor_text=""
):

    # ---------------------------------
    # Step 1 - Summarize Feedback
    # ---------------------------------

    summary = summarize_feedback(feedback_list)

    if not summary or "summaries" not in summary:
        raise ValueError("Step 1 failed: Invalid summaries returned.")

    # ---------------------------------
    # Step 2 - Cluster Feedback
    # ---------------------------------

    categories = cluster_feedback(summary)

    if not categories or "categories" not in categories:
        raise ValueError("Step 2 failed: Invalid categories returned.")

    # ---------------------------------
    # Step 3 - Prioritize
    # ---------------------------------

    priorities = prioritize_feedback(categories)

    if (
        not isinstance(priorities, dict)
        or "priorities" not in priorities
        or not isinstance(priorities["priorities"], list)
    ):
        raise ValueError(
            f"Step 3 failed: Invalid priorities returned.\nReturned: {priorities}"
        )

    # ---------------------------------
    # Step 4 - Product Roadmap
    # ---------------------------------

    roadmap = generate_roadmap(priorities)

    if not roadmap or "roadmap" not in roadmap:
        raise ValueError("Step 4 failed: Invalid roadmap returned.")

    # ---------------------------------
    # Step 5 - Sentiment Analysis
    # ---------------------------------

    sentiment = analyze_sentiment(feedback_list)

    if not sentiment or "sentiments" not in sentiment:
        raise ValueError("Step 5 failed: Invalid sentiment analysis returned.")

    # ---------------------------------
    # Step 6 - Competitive Analysis
    # ---------------------------------

    # Limit the amount of customer feedback sent to the AI
    feedback_sample = feedback_list[:50]

    # Limit competitor document size
    competitor_summary = competitor_text[:6000]

    competitive = competitive_analysis(
        feedback_sample,
        competitor_summary
)
    print("=" * 60)
    print("COMPETITIVE ANALYSIS RESULT")
    print(competitive)
    print("=" * 60)

    required_keys = [
        "competitor_strengths",
        "competitor_weaknesses",
        "customer_requested_features",
        "competitive_gaps",
        "recommended_features",
        "strategic_recommendations",
    ]

    if (
        not isinstance(competitive, dict)
        or not all(key in competitive for key in required_keys)
    ):
        raise ValueError(
            f"Step 6 failed: Invalid competitive analysis returned.\nReturned: {competitive}"
        )

    # ---------------------------------
    # Step 7 - Executive Summary
    # ---------------------------------

    executive = executive_summary(
        roadmap,
        competitive
    )

    if not executive:
        raise ValueError("Step 7 failed: Executive summary generation failed.")

    # ---------------------------------
    # Step 8 - Jira Stories
    # ---------------------------------

    stories = generate_jira_stories(priorities)

    if not stories or "stories" not in stories:
        raise ValueError("Step 8 failed: Invalid Jira stories returned.")

    # ---------------------------------
    # Return Everything
    # ---------------------------------

    return {
        "summary": summary,
        "categories": categories,
        "priorities": priorities,
        "roadmap": roadmap,
        "sentiment": sentiment,
        "competitive_analysis": competitive,
        "executive_summary": executive,
        "stories": stories,
    }