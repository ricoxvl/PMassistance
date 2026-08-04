from workflow import run_workflow
from llm import competitive_analysis


def run_customer_analysis(feedback_list):
    """
    Customer feedback only.
    """
    return run_workflow(feedback_list, "")


def run_competitive_analysis(competitor_text):
    """
    Competitive analysis only.
    """

    analysis = competitive_analysis([], competitor_text)

    return {
        "executive_summary": analysis.get(
            "executive_summary",
            "No executive summary available."
        ),
        "themes": [],
        "categories": [],
        "priorities": [],
        "sentiment": {},
        "roadmap": [],
        "jira_stories": [],
        "competitive_analysis": analysis
    }


def run_combined_analysis(feedback_list, competitor_text):
    """
    Customer feedback + competitor analysis.
    """
    return run_workflow(feedback_list, competitor_text)