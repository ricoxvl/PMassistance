from llm import (
    customer_intelligence,
    competitive_analysis
)


def run_workflow(feedback_list, competitor_text=""):

    # ---------------------------------
    # Customer Intelligence
    # ---------------------------------

    customer = customer_intelligence(feedback_list)

    if (
        not isinstance(customer, dict)
        or "executive_summary" not in customer
    ):
        raise ValueError(
            "Customer intelligence analysis failed."
        )

    # ---------------------------------
    # Competitive Intelligence
    # ---------------------------------

    competitive = competitive_analysis(
        feedback_list,
        competitor_text
    )

    if (
        not isinstance(competitive, dict)
        or "executive_summary" not in competitive
    ):
        raise ValueError(
            "Competitive intelligence analysis failed."
        )

    # ---------------------------------
    # Combined Result
    # ---------------------------------

    return {

        "executive_summary":
            customer.get("executive_summary", ""),

        "product_health":
            customer.get("product_health", {}),

        "customer_satisfaction":
            customer.get("customer_satisfaction", {}),

        "confidence":
            customer.get("confidence", {}),

        "business_impact":
            customer.get("business_impact", {}),

        "themes":
            customer.get("themes", []),

        "sentiment":
            customer.get("sentiment", {}),

        "priorities":
            customer.get("priorities", []),

        "roadmap":
            customer.get("roadmap", []),

        "recommendations":
            customer.get("recommendations", []),

        "jira_stories":
            customer.get("jira_stories", []),

        "scorecard":
            customer.get("scorecard", []),

        "competitive_analysis":
            competitive
    }