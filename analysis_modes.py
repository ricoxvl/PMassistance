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
    return {
        "executive_summary": "Competitive analysis completed successfully.",
        "themes": [],
        "sentiment": {},
        "roadmap": [],
        "jira_stories": [],
        "competitive_analysis": competitive_analysis([], competitor_text)
    }


def run_combined_analysis(feedback_list, competitor_text):
    """
    Customer feedback + competitor analysis.
    """
    return run_workflow(feedback_list, competitor_text)