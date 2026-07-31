import json
import streamlit as st
from groq import Groq

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

MODEL = "llama-3.1-8b-instant"


# -----------------------------
# Helper Functions
# -----------------------------

def ask_json(prompt):
    content = ""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.choices[0].message.content

        print("\n========== JSON ==========")
        print(content)
        print("==========================\n")

        return json.loads(content)

    except json.JSONDecodeError:
        st.error("The AI returned invalid JSON.")
        if content:
            st.code(content)
        return {}

    except Exception as e:
        st.error(f"Groq API Error: {e}")
        return {}


def ask_text(prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
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

Summarize each customer feedback item into one concise sentence while preserving its main issue or request.

Rules:
- Create exactly one summary for each feedback item.
- Do not merge multiple feedback items.
- Keep summaries under 20 words.
- Preserve the original meaning.
- Do not include opinions or recommendations.

Return ONLY valid JSON.

Format:

{{
    "summaries":[
        {{
            "summary":"..."
        }}
    ]
}}

Customer Feedback:

{feedback}
"""

    return ask_json(prompt)

# -----------------------------
# Step 2
# -----------------------------

def cluster_feedback(summary_json):

    prompt = f"""
You are a Senior Product Manager.

Group the customer feedback summaries into high-level product themes suitable for an executive dashboard.

Rules:
- Create between 3 and 5 categories.
- Never create more than 5 categories.
- Group similar issues together.
- Use broad product categories instead of one category per issue.
- Never return blank or null category names.
- Never create duplicate categories.
- Every customer feedback summary must belong to exactly one category.
- Use concise, professional names.

Examples of GOOD categories:
- User Experience
- Performance & Stability
- Notifications
- Authentication
- File Management
- Feature Requests
- Account Management
- Search & Navigation

Examples of BAD categories:
- Upload Issues
- Login Button Broken
- Notification Bug
- Crash on Startup
- Dark Mode Bug

Return ONLY valid JSON in this format:

{{
    "categories":[
        {{
            "category":"Performance & Stability",
            "count":5
        }},
        {{
            "category":"User Experience",
            "count":4
        }},
        {{
            "category":"Feature Requests",
            "count":3
        }}
    ]
}}

Customer Feedback Summaries:

{json.dumps(summary_json, indent=2)}
"""

    return ask_json(prompt)


# -----------------------------
# Step 3
# -----------------------------

def prioritize_feedback(category_json):

    prompt = f"""
You are a Senior Product Manager.

Prioritize each product category based on customer impact and business value.

Rules:
- Assign ONLY one of these priorities:
  - High
  - Medium
  - Low
- Do NOT use Critical, Urgent, Highest, or other values.
- Higher priority should be given to categories that:
    - Affect many users
    - Cause crashes or instability
    - Prevent core functionality
- Lower priority should be given to cosmetic issues and feature requests.

Return ONLY valid JSON.

Format:

{{
    "priorities":[
        {{
            "issue":"Performance & Stability",
            "priority":"High"
        }},
        {{
            "issue":"User Experience",
            "priority":"Medium"
        }},
        {{
            "issue":"Feature Requests",
            "priority":"Low"
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
You are a Director of Product Management preparing a roadmap for executive leadership.

Using the prioritized customer issues, create a realistic three-sprint roadmap.

Rules:

- Create exactly three sprints.
- Sprint 1 should focus on critical reliability and customer-impact issues.
- Sprint 2 should improve usability, performance, and operational efficiency.
- Sprint 3 should deliver strategic enhancements and innovation.
- Each sprint must include:
    • sprint
    • goal
    • 3 deliverables
- Deliverables should be specific product initiatives.
- Do not repeat the same work across multiple sprints.
- Write in executive language suitable for leadership.

Return ONLY valid JSON.

Format:

{{
    "roadmap":[
        {{
            "sprint":"Sprint 1",
            "goal":"Improve platform reliability and customer satisfaction",
            "deliverables":[
                "Resolve application crashes",
                "Improve login reliability",
                "Optimize system performance"
            ]
        }},
        {{
            "sprint":"Sprint 2",
            "goal":"Enhance user experience",
            "deliverables":[
                "Improve navigation",
                "Redesign dashboard",
                "Enhance notifications"
            ]
        }},
        {{
            "sprint":"Sprint 3",
            "goal":"Deliver strategic product enhancements",
            "deliverables":[
                "Launch requested features",
                "Expand reporting capabilities",
                "Improve mobile experience"
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
You are a Senior Product Manager preparing an executive competitive assessment for leadership.

You have TWO independent data sources.

====================================================
CUSTOMER FEEDBACK
====================================================

{feedback}

====================================================
COMPETITOR DOCUMENT
====================================================

{competitor_text}

====================================================
TASK
====================================================

Read BOTH sources carefully.

The competitor document may contain:

• tables
• spreadsheets
• feature matrices
• SWOT analyses
• paragraphs
• bullet lists
• meeting notes
• strategy documents
• product brochures

Do NOT assume any particular format.

Extract the important business information regardless of whether it appears
inside tables, bullets, paragraphs or headings.

Compare the competitor information against customer feedback.

Identify:

1. Competitor strengths
2. Competitor weaknesses
3. Features customers are requesting
4. Competitive gaps between our product and competitors
5. Recommended product features
6. Strategic recommendations for leadership

Guidelines:

• Base every recommendation on evidence.
• Avoid repeating the same point.
• Keep every bullet concise.
• Use executive-level language.
• Focus on product strategy.
• If the competitor document lacks enough information for a section,
  return an empty list for that section.

Return ONLY valid JSON.

Format:

{{
  "competitor_strengths":[
    "...",
    "...",
    "..."
  ],

  "competitor_weaknesses":[
    "...",
    "...",
    "..."
  ],

  "customer_requested_features":[
    "...",
    "...",
    "..."
  ],

  "competitive_gaps":[
    "...",
    "...",
    "..."
  ],

  "recommended_features":[
    "...",
    "...",
    "..."
  ],

  "strategic_recommendations":[
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
Competitive Analysis:
{json.dumps(competitive_json, indent=2)}
You are preparing an executive report for product leadership.

Write a concise executive summary.

Requirements:
- Maximum 250 words.
- Return plain text only.
- Do NOT use Markdown.
- Do NOT use #, ##, **, -, *, or numbered lists.
- Do NOT include greetings or sign-offs.
- Do NOT use first-person language.
- Do NOT wrap section titles in Markdown.
- Keep each section separated by one blank line.

Use exactly this format:

Overview:
<paragraph>

Key Findings:
One short sentence.
One short sentence.
One short sentence.

Recommended Roadmap:
Sprint 1: ...
Sprint 2: ...
Sprint 3: ...

Business Impact:
<paragraph>

Recommendation:
<one sentence>

Use the following roadmap to write the summary. Do NOT repeat or copy it verbatim.

Roadmap Data:
{json.dumps(roadmap_json, indent=2)}
"""


    return ask_text(prompt)

# -----------------------------
# Step 8
# -----------------------------

def generate_jira_stories(priority_json):

    prompt = f"""
You are an experienced Product Manager.

Generate Jira user stories from the prioritized product categories.

Rules:
- Generate one story for every High or Medium priority category.
- If there are fewer than three stories, include the most important Low priority category.
- IDs must be unique (PROD-101, PROD-102, PROD-103, ...).
- Titles should begin with a verb (Fix, Improve, Add, Optimize, Reduce).
- Descriptions should clearly explain the user problem.
- Include exactly three measurable acceptance criteria for each story.

Return ONLY valid JSON.

Format:

{{
    "stories":[
        {{
            "id":"PROD-101",
            "title":"Improve Upload Reliability",
            "priority":"High",
            "description":"Users experience upload failures that prevent successful completion of core tasks.",
            "acceptance":[
                "Uploads complete successfully",
                "No application crashes occur",
                "Errors are logged for failed uploads"
            ]
        }}
    ]
}}

Prioritized Issues:

{json.dumps(priority_json, indent=2)}
"""

    return ask_json(prompt)  