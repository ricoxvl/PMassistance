import json
import streamlit as st
from groq import Groq

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

MODEL = "llama-3.3-70b-versatile"


# -----------------------------
# Helper Functions
# -----------------------------

def ask_json(prompt):
    content = ""

    system_prompt = """
You are a JSON generator.

Return ONLY valid JSON.

Rules:
- Output must be valid JSON.
- Do not include markdown.
- Do not include ```json.
- Do not explain anything.
- Every property name MUST be enclosed in double quotes.
- Every array must be properly closed.
- Never omit quotation marks around keys.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.choices[0].message.content

        return json.loads(content)

    except json.JSONDecodeError:
        st.error("The AI returned invalid JSON.")
        st.code(content)
        return {}

    except Exception as e:
        st.error(f"Groq API Error: {e}")
        return {}
def ask_text(prompt):

    try:
        response = client.chat.completions.create(
            model=MODEL,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful Product Management assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        st.error(f"Groq API Error: {e}")
        return ""
# -----------------------------
# Step 1
# -----------------------------

def summarize_feedback(feedback_list):

    feedback = "\n".join(feedback_list)

    prompt = f"""

You are a Senior Product Analyst preparing customer feedback for executive product analysis.

Your objective is to summarize every customer feedback item while preserving its original meaning.

Customer Feedback

{feedback}

====================================================
RULES
====================================================

Summarize EVERY feedback item exactly once.

Never merge multiple feedback items.

Never omit a feedback item.

Preserve the customer's primary issue, request, or compliment.

Do NOT infer information that is not explicitly stated.

Do NOT provide recommendations.

Do NOT classify sentiment.

Do NOT group similar feedback.

====================================================
WRITING REQUIREMENTS
====================================================

Each summary should:

• Be between 8 and 20 words.

• Be one concise sentence.

• Clearly identify the customer's main point.

• Use professional business language.

• Preserve the original intent.

Examples:

Original:
"The application crashes every time I upload a PDF."

Summary:
"Application crashes when uploading PDF files."

Original:
"I'd really like a dark mode because I work at night."

Summary:
"Customer requests a dark mode feature."

Original:
"Searching for invoices takes too long."

Summary:
"Customer reports slow invoice search performance."

====================================================
OUTPUT REQUIREMENTS
====================================================

Return ONLY valid JSON.

Format:

{{
    "summaries":[
        {{
            "summary":"..."
        }}
    ]
}}
"""

    return ask_json(prompt)

# -----------------------------
# Step 2
# -----------------------------

def cluster_feedback(summary_json):

    prompt = f"""

You are a Principal Product Manager responsible for analyzing customer feedback and identifying strategic product themes.

Your objective is to organize customer feedback into executive-level product categories suitable for roadmap planning and portfolio management.

Customer Feedback Summaries

{json.dumps(summary_json, indent=2)}

====================================================
ANALYSIS OBJECTIVE
====================================================

Group similar customer issues into broad strategic themes.

The categories should represent areas of product investment—not individual bugs.

Think like a Product Director preparing a quarterly roadmap.

====================================================
CATEGORY RULES
====================================================

Create BETWEEN 3 AND 5 categories.

Never create more than 5.

Never create fewer than 3 unless the feedback is extremely limited.

Every summary must belong to exactly one category.

Categories should be broad enough to contain multiple customer requests.

Do NOT create categories for individual bugs.

====================================================
GOOD CATEGORY EXAMPLES
====================================================

User Experience

Performance & Reliability

Authentication & Security

Reporting & Analytics

Notifications

Integrations

Search & Navigation

Account Management

Workflow Automation

Collaboration

Administration

Feature Requests

====================================================
BAD CATEGORY EXAMPLES
====================================================

Broken Login

Dark Mode Bug

Upload Error

Button Missing

PDF Crash

Slow Export

====================================================
NAMING RULES
====================================================

Category names should:

• Be professional.

• Contain 2–4 words.

• Be Title Case.

• Never contain punctuation.

• Never contain numbers.

• Never repeat.

====================================================
OUTPUT REQUIREMENTS
====================================================

For each category return:

category

count

Sort categories by count descending.

Return ONLY valid JSON.

Format:

{{
    "categories":[
        {{
            "category":"Performance & Reliability",
            "count":8
        }},
        {{
            "category":"User Experience",
            "count":6
        }},
        {{
            "category":"Reporting & Analytics",
            "count":5
        }}
    ]
}}
"""

    return ask_json(prompt)


# -----------------------------
# Step 3
# -----------------------------

def prioritize_feedback(category_json):

    prompt = f"""

You are a Director of Product Management responsible for prioritizing product investments.

Your objective is to prioritize customer issues based ONLY on the evidence contained in the provided customer feedback categories.

Use ONLY the categories provided below.

Do NOT invent additional issues, customer behavior, market conditions, revenue figures, or technical information that is not present.

====================================================
PRIORITIZATION FRAMEWORK
====================================================

Evaluate every category using these factors:

1. Customer Impact
- Estimate impact based on the frequency and importance of the category.
- Determine whether it affects core customer workflows.
- Do not assume customer counts that are not provided.

2. Business Impact
- Estimate business value based only on the available customer issues.
- Consider potential effects on customer satisfaction, adoption, and retention.
- Do not invent revenue, churn, or financial metrics.

3. Technical Severity
- Categories involving crashes, failures, login, security, reliability, or performance should generally receive higher priority.
- Cosmetic improvements and minor enhancements should receive lower priority.

4. Strategic Importance
- Consider whether solving the issue would improve overall product quality, customer experience, or competitive positioning.
- Base your decision only on the provided evidence.

====================================================
PRIORITY RULES
====================================================

Assign ONLY one priority:

High
Medium
Low

High

Use when:
• Core functionality is affected.
• Reliability or stability issues exist.
• The issue significantly impacts customer experience.
• The issue represents a major business risk.

Medium

Use when:
• Moderate customer impact exists.
• Improves usability or workflow efficiency.
• Important but not immediately business critical.

Low

Use when:
• Cosmetic improvements.
• Nice-to-have enhancements.
• Minor feature requests.
• Limited customer impact.

====================================================
REASONING RULES
====================================================

Prioritize ONLY using evidence contained in the provided categories.

Do NOT invent:
• Customer behavior
• Revenue estimates
• Market conditions
• Competitive information
• Engineering effort
• Technical metrics

If evidence is limited, make the most conservative priority decision.

====================================================
OUTPUT REQUIREMENTS
====================================================

Every category must appear exactly once.

Do not create duplicate categories.

Sort priorities from High to Low.

Return ONLY valid JSON.

Format:

{{
    "priorities":[
        {{
            "issue":"Performance & Stability",
            "priority":"High",
            "reason":"Reliability issues affect core product functionality and customer experience."
        }},
        {{
            "issue":"User Experience",
            "priority":"Medium",
            "reason":"Improving usability will enhance customer satisfaction but is not business critical."
        }},
        {{
            "issue":"Feature Requests",
            "priority":"Low",
            "reason":"Represents future product enhancements with limited immediate impact."
        }}
    ]
}}

Categories:

{json.dumps(category_json, indent=2)}
"""

    return ask_json(prompt)


# -----------------------------
# Step 4
# -----------------------------

def generate_roadmap(priority_json):

    prompt = f"""

You are a Director of Product Management building an executive product roadmap.

Your objective is to transform the prioritized customer issues into a realistic three-phase product roadmap.

Use ONLY the prioritized categories below.

Do not invent new issues.

Roadmap Principles

Sprint 1
• Address critical customer pain points.
• Resolve reliability and stability issues.
• Improve core product functionality.

Sprint 2
• Improve usability and operational efficiency.
• Enhance workflows.
• Increase customer satisfaction.

Sprint 3
• Deliver strategic product innovation.
• Improve competitive differentiation.
• Create long-term business value.

Requirements

Create EXACTLY three sprints.

Each sprint must contain:

- sprint
- goal
- deliverables

Each sprint must have exactly THREE deliverables.

Deliverables should:

• Be specific product initiatives.
• Be unique.
• Never repeat across sprints.
• Be directly related to the prioritized issues.
• Be suitable for an executive roadmap.

Prioritize work using this order:

1. High priority issues
2. Medium priority issues
3. Low priority issues

Roadmap Quality

Sprint 1 should reduce customer risk.

Sprint 2 should improve customer experience.

Sprint 3 should strengthen long-term market differentiation.

Return ONLY valid JSON.

Format:

{{
    "roadmap":[
        {{
            "sprint":"Sprint 1",
            "goal":"...",
            "deliverables":[
                "...",
                "...",
                "..."
            ]
        }},
        {{
            "sprint":"Sprint 2",
            "goal":"...",
            "deliverables":[
                "...",
                "...",
                "..."
            ]
        }},
        {{
            "sprint":"Sprint 3",
            "goal":"...",
            "deliverables":[
                "...",
                "...",
                "..."
            ]
        }}
    ]
}}

Prioritized Categories:

{json.dumps(priority_json, indent=2)}
"""

    return ask_json(prompt)
# -----------------------------
# Step 5
# -----------------------------

def analyze_sentiment(feedback_list):

    feedback = "\n".join(feedback_list)

    prompt = f"""
You are a Product Analyst.

Analyze the sentiment of each customer feedback item.

Rules:
- Analyze every feedback item exactly once.
- Use ONLY these sentiment labels:
  - Positive
  - Neutral
  - Negative
- Do not explain your reasoning.
- Preserve the original feedback text.

Return ONLY valid JSON.

Format:

{{
    "sentiments":[
        {{
            "feedback":"The app crashes",
            "sentiment":"Negative"
        }},
        {{
            "feedback":"Love the redesign",
            "sentiment":"Positive"
        }}
    ]
}}

Customer Feedback:

{feedback}
"""

    return ask_json(prompt)

# -----------------------------
# Step 6 - Competitive Analysis
# -----------------------------

def competitive_analysis(feedback_list, competitor_text):

    feedback = "\n".join(feedback_list)

    if not competitor_text.strip():
        return {
            "competitor_strengths": [],
            "competitor_weaknesses": [],
            "customer_requested_features": [],
            "competitive_gaps": [],
            "recommended_features": [],
            "strategic_recommendations": []
        }

    prompt = f"""

    You are a Senior Product Manager at a Fortune 500 technology company preparing an executive competitive assessment for leadership.

    You have TWO independent sources of information.

    ====================================================
    SOURCE 1 — CUSTOMER FEEDBACK
    ====================================================

    {feedback}

    ====================================================
    SOURCE 2 — COMPETITOR DOCUMENT
    ====================================================

    {competitor_text}

    ====================================================
    OBJECTIVE
    ====================================================

    Compare both sources to identify competitive positioning, customer needs, market opportunities, and strategic product investments.

    Base every conclusion on evidence found in the supplied data.

    Do NOT invent competitor capabilities, customer requests, or recommendations.

    If there is insufficient evidence for an item, omit it rather than guessing.

    ====================================================
    ANALYSIS PROCESS
    ====================================================

    Before generating your final answer, internally perform the following reasoning process.

    Do NOT include this reasoning in the output.

    Step 1
    Read the entire competitor document and identify the competitor's major product capabilities.

    Step 2
    Read all customer feedback and identify recurring pain points, requests, and compliments.

    Step 3
    Compare both sources and identify where:
    • Customers request capabilities competitors already provide.
    • Competitors are weak where customers express demand.
    • Both sources indicate the same strategic opportunity.

    Step 4
    Rank findings by:
    • Frequency
    • Business impact
    • Customer impact
    • Competitive differentiation

    Step 5
    Remove duplicate findings.

    Step 6
    Only after completing the above steps, generate the final JSON response.
    ====================================================
    EVIDENCE RULES
    ====================================================

    • Use competitor information ONLY from the competitor document.

    • Use customer requests ONLY from customer feedback.

    • If both sources support the same conclusion, prioritize it.

    • Never duplicate the same idea in multiple sections.

    • If evidence is weak or missing, leave the item out.

    ====================================================
    REASONING PROCESS
    ====================================================

    Before assigning priorities:

    1. Review every product category.
    2. Estimate customer impact.
    3. Estimate business impact.
    4. Estimate technical severity.
    5. Estimate strategic importance.
    6. Compare all categories against each other.
    7. Assign High, Medium, or Low.
    8. Generate the JSON response.

    ====================================================
    REASONING PROCESS
    ====================================================

    Before assigning priorities:

    1. Review every product category.
    2. Estimate customer impact.
    3. Estimate business impact.
    4. Estimate technical severity.
    5. Estimate strategic importance.
    6. Compare all categories against each other.
    7. Assign High, Medium, or Low.
    8. Generate the JSON response.

    ====================================================
    REASONING PROCESS
    ====================================================

    Before building the roadmap:

    1. Review all prioritized issues.
    2. Schedule High priority work first.
    3. Schedule Medium priority work second.
    4. Schedule Low priority work last.
    5. Ensure no deliverable is duplicated.
    6. Build a realistic progression from stabilization to innovation.
    7. Generate the JSON roadmap.

    ====================================================
    REASONING PROCESS
    ====================================================

    Before creating Jira stories:

    1. Review each prioritized issue.
    2. Determine the customer problem.
    3. Identify the desired business outcome.
    4. Create a clear implementation objective.
    5. Write measurable acceptance criteria.
    6. Ensure every story is unique.
    7. Generate the JSON output.
    ====================================================
    OUTPUT REQUIREMENTS
    ====================================================

    Return:

    Exactly 3-5 items for each list.

    Every item should:

    • Be one concise executive sentence.
    • Be under 20 words.
    • Be unique.
    • Avoid repeating ideas.
    • Be written professionally.

    ====================================================
    SECTION DEFINITIONS
    ====================================================

    competitor_strengths

    Strengths the competitor clearly demonstrates.

    Examples:
    - Comprehensive analytics dashboard
    - Strong mobile experience
    - Fast onboarding workflow

    ----------------------------------------------------

    competitor_weaknesses

    Weaknesses, limitations, or missing capabilities identified in the competitor document.

    Examples:
    - Limited customization
    - Weak reporting capabilities
    - No workflow automation

    ----------------------------------------------------

    customer_requested_features

    Recurring customer requests appearing in feedback.

    Examples:
    - Dark mode
    - Mobile support
    - Better reporting

    ----------------------------------------------------

    competitive_gaps

    High-value opportunities where customer demand exists but competitors do not fully satisfy it.

    These should represent potential market opportunities.

    ----------------------------------------------------

    recommended_features

    Recommend realistic product investments that:

    • Solve customer pain points
    • Address competitive gaps
    • Improve business value
    • Fit a practical software product roadmap

    Examples:

    - AI-powered reporting assistant
    - Real-time collaboration
    - Predictive analytics dashboard
    - Workflow automation
    - Custom KPI dashboards

    ----------------------------------------------------

    strategic_recommendations

    Provide executive-level business actions.

    Use action-oriented recommendations such as:

    • Invest
    • Prioritize
    • Accelerate
    • Differentiate
    • Expand
    • Modernize
    • Consolidate
    • Partner

    Avoid generic recommendations such as:

    - Improve the product
    - Add more features
    - Enhance quality

    Recommendations should be suitable for executive leadership.

    ====================================================
    RETURN ONLY VALID JSON
    ====================================================

    {{
        "competitor_strengths": [
            "...",
            "...",
            "..."
        ],
        "competitor_weaknesses": [
            "...",
            "...",
            "..."
        ],
        "customer_requested_features": [
            "...",
            "...",
            "..."
        ],
        "competitive_gaps": [
            "...",
            "...",
            "..."
        ],
        "recommended_features": [
            "...",
            "...",
            "..."
        ],
        "strategic_recommendations": [
            "...",
            "...",
            "..."
        ]
    }}
    """

    return ask_json(prompt)
# -----------------------------
# Step 7
# -----------------------------

def executive_summary(roadmap_json, competitive_json):

    prompt = f"""

You are the Director of Product Management presenting findings to the executive leadership team.

Your audience consists of:
- VP of Product
- Engineering Leadership
- Executive Stakeholders
- Business Leadership

Use ONLY the information contained in the Competitive Analysis and Roadmap below.

Do NOT invent facts.

Do NOT mention information that is not supported by the analysis.

If something is missing, simply omit it.

Your goal is to summarize the business implications of the analysis—not repeat lists.

Write in a concise executive style.

Return plain text only.

Do NOT use Markdown.
Do NOT use bullet points.
Do NOT use tables.
Do NOT use code fences.

Maximum length: 250 words.

Use EXACTLY this structure:

Overview:
Provide a concise assessment of the current competitive position.

Key Findings:
Write exactly three short sentences summarizing the most important findings.

Recommended Roadmap:
Sprint 1: ...
Sprint 2: ...
Sprint 3: ...

Business Impact:
Explain how these recommendations could affect customer satisfaction, product differentiation, market position, and business growth.

Recommendation:
Provide one concise executive recommendation for leadership.

Competitive Analysis:
{json.dumps(competitive_json, indent=2)}

Roadmap:
{json.dumps(roadmap_json, indent=2)}
"""
    return ask_text(prompt)

# -----------------------------
# Step 8
# -----------------------------

def generate_jira_stories(priority_json):

    prompt = f"""

You are a Senior Product Manager creating Jira stories for an Agile product development team.

Your objective is to convert prioritized product categories into implementation-ready Jira stories.

Use ONLY the prioritized categories below.

Do NOT invent additional issues.

====================================================
STORY CREATION GUIDELINES
====================================================

Generate ONE Jira story for every High and Medium priority category.

If fewer than three stories are produced, include the highest-value Low priority category.

Each story should represent a meaningful product initiative rather than a small bug fix.

====================================================
STORY REQUIREMENTS
====================================================

Each story must include:

id

title

priority

description

acceptance

====================================================
TITLE RULES
====================================================

Titles should:

• Begin with a verb.

• Be concise.

• Describe a product initiative.

Examples:

Improve User Authentication

Optimize Dashboard Performance

Enhance Search Experience

Reduce System Latency

Expand Reporting Capabilities

====================================================
DESCRIPTION RULES
====================================================

Descriptions should explain:

• the customer problem

• why it matters

• the expected business benefit

Use professional product management language.

====================================================
ACCEPTANCE CRITERIA
====================================================

Each story must include EXACTLY THREE measurable acceptance criteria.

Acceptance criteria should be testable.

Examples:

User can complete login successfully.

Dashboard loads in under two seconds.

Search returns relevant results.

Reports export successfully.

====================================================
OUTPUT REQUIREMENTS
====================================================

IDs should begin with:

PROD-101

PROD-102

PROD-103

...

Increment sequentially.

Do not repeat IDs.

Return ONLY valid JSON.

Format:

{{
    "stories":[
        {{
            "id":"PROD-101",
            "title":"Improve Authentication",
            "priority":"High",
            "description":"Users experience authentication failures that prevent access to core functionality. Improving authentication reliability will reduce customer frustration and increase platform stability.",
            "acceptance":[
                "Login succeeds on the first attempt.",
                "Authentication errors are logged.",
                "Password reset completes successfully."
            ]
        }}
    ]
}}

Prioritized Categories:

{json.dumps(priority_json, indent=2)}
"""

    return ask_json(prompt)  