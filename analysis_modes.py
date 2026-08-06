from workflow import run_workflow
from llm import competitive_analysis


def run_customer_analysis(feedback_list):
    """
    Runs customer feedback analysis using AI.
    All insights returned come directly from the LLM.
    """
    return run_workflow(
        feedback_list=feedback_list,
        competitor_text=""
    )


def run_competitive_analysis(competitor_text):
    """
    Runs competitive analysis using AI.
    Returns the AI response without generating
    additional summaries or placeholder content.
    """

    return competitive_analysis(
        feedback_list=[],
        competitor_text=competitor_text
    )


def run_combined_analysis(feedback_list, competitor_text):
    """
    Runs combined customer + competitive analysis.
    All dashboard content should originate from AI.
    """

    return run_workflow(
        feedback_list=feedback_list,
        competitor_text=competitor_text
    )