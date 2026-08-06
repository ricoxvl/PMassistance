import json
import streamlit as st
from groq import Groq

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

MODEL = "llama-3.3-70b-versatile"


# ==========================================================
# Universal JSON Generator
# ==========================================================

SYSTEM_JSON = """
You are an enterprise Product Intelligence AI.

Your ONLY job is to analyze documents and return JSON.

Rules

• Return ONLY valid JSON.

• Never explain your reasoning.

• Never wrap JSON in markdown.

• Never invent facts.

• Base EVERY conclusion ONLY on the supplied documents.

• If evidence is missing,
return null,
an empty string,
or an empty array.

Never guess.

Every executive insight must be traceable to evidence.

Never fabricate customer issues.

Never fabricate business impact.

Never fabricate product health.

Never fabricate confidence.

Never fabricate roadmap items.

Never fabricate Jira stories.

Everything must originate from the uploaded documents.
"""


def ask_json(prompt, required_keys=None):

    try:

        response = client.chat.completions.create(

            model=MODEL,

            temperature=0,

            response_format={"type": "json_object"},

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_JSON
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result = json.loads(
            response.choices[0].message.content
        )

        if required_keys:

            for key in required_keys:

                if key not in result:
                    result[key] = None

        return result

    except Exception as e:

        st.error(e)

        return {}


# ==========================================================
# Executive Text Generator
# ==========================================================

SYSTEM_TEXT = """
You are a Fortune 500 VP of Product.

Write concise executive business reports.

Every statement must come ONLY from the supplied data.

Never invent information.

Never use generic product advice.

Never recommend something unless the supplied analysis supports it.

If evidence is missing, say so.

Do not hallucinate.
"""


def ask_text(prompt):

    try:

        response = client.chat.completions.create(

            model=MODEL,

            temperature=0,

            messages=[

                {
                    "role":"system",
                    "content":SYSTEM_TEXT
                },

                {
                    "role":"user",
                    "content":prompt
                }

            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        st.error(e)

        return ""
# ==========================================================
# MASTER CUSTOMER INTELLIGENCE
# ==========================================================

def customer_intelligence(feedback_list):

    if not feedback_list:

        return {
            "executive_summary": "No customer feedback was provided.",
            "product_health": {},
            "customer_satisfaction": {},
            "confidence": {},
            "business_impact": {},
            "themes": [],
            "sentiment": {},
            "priorities": [],
            "roadmap": [],
            "recommendations": [],
            "jira_stories": [],
            "scorecard": []
        }

    feedback = "\n".join(feedback_list)

    limited_data = ""

    if len(feedback_list) < 3:

        limited_data = """

    Evidence is limited.

    Use conservative conclusions.

    Lower confidence where appropriate.

    Avoid broad assumptions.

    """

    prompt = f"""

You are Product Intelligence AI.

You are acting as an experienced:

• VP of Product
• Director of Product Management
• Customer Success Executive
• Product Analytics Lead

Your responsibility is to analyze the uploaded customer feedback and produce a complete executive product intelligence report.

Everything you produce MUST come ONLY from the uploaded feedback.

Never invent information.

If evidence is weak,
say so.

If evidence does not exist,
return an empty value.

==================================================
CUSTOMER FEEDBACK
==================================================

{feedback}
{limited_data}

==================================================
OBJECTIVE
==================================================

Analyze ALL customer feedback as a whole.

Do NOT perform independent tasks.

Instead perform one holistic executive analysis.

Your conclusions must remain internally consistent.

==================================================
GENERATE
==================================================

1 Executive Summary

• Executive level
• 150-250 words
• Overall product assessment
• Biggest risks
• Biggest opportunities

--------------------------------------------------

2 Product Health

Return

score (0-100)

status

reason

Example

Excellent

Healthy

Needs Attention

Critical

--------------------------------------------------

3 Customer Satisfaction

Return

score

reason

--------------------------------------------------

4 AI Confidence

Return

score

reason

Explain WHY confidence is high or low.

--------------------------------------------------

5 Business Impact

Return

level

reason

--------------------------------------------------

6 Product Themes

Return 3-8 themes.

Each theme must include:

theme

mentions

summary

evidence

Evidence should reference the feedback items or quote short supporting phrases.

Do not invent evidence.

--------------------------------------------------

7 Customer Sentiment

Return

positive

neutral

negative

Then

overall_sentiment

reason

--------------------------------------------------

8 Priority Matrix

For every major issue return

issue

priority

reason

business_impact

customer_impact

--------------------------------------------------

9 Product Roadmap

Generate

Sprint 1

Sprint 2

Sprint 3

Each sprint

goal

deliverables

--------------------------------------------------

10 Recommended Actions

Return 5 executive recommendations.

Recommendations MUST come ONLY from evidence.

--------------------------------------------------

11 Jira Stories

Generate implementation-ready Jira stories.

Return

id

title

priority

description

acceptance

--------------------------------------------------

12 Executive Scorecard

Return

metric

value

reason

==================================================
OUTPUT
==================================================

Return ONLY JSON.

{{
  "executive_summary":"",

  "product_health":{{
      "score":0,
      "status":"",
      "reason":""
  }},

  "customer_satisfaction":{{
      "score":0,
      "reason":""
  }},

  "confidence":{{
      "score":0,
      "reason":""
  }},

  "business_impact":{{
      "level":"",
      "reason":""
  }},

"themes":[
    {{
        "theme":"",
        "mentions":0,
        "summary":"",
        "evidence":[
            ""
        ]
    }}
],

  "sentiment":{{
      "positive":0,
      "neutral":0,
      "negative":0,
      "overall_sentiment":"",
      "reason":""
  }},

  "priorities":[
      {{
          "issue":"",
          "priority":"",
          "reason":"",
          "business_impact":"",
          "customer_impact":""
      }}
  ],

  "roadmap":[
      {{
          "sprint":"",
          "goal":"",
          "deliverables":[]
      }}
  ],

  "recommendations":[
      ""
  ],

  "jira_stories":[
      {{
          "id":"",
          "title":"",
          "priority":"",
          "description":"",
          "acceptance":[]
      }}
  ],

  "scorecard":[
      {{
          "metric":"",
          "value":"",
          "reason":""
      }}
  ]

}}

"""

    return ask_json(

    prompt,

    required_keys=[

        "executive_summary",

        "product_health",

        "customer_satisfaction",

        "confidence",

        "business_impact",

        "themes",

        "sentiment",

        "priorities",

        "roadmap",

        "recommendations",

        "jira_stories",

        "scorecard"

    ]

)

# ==========================================================
# COMPETITIVE INTELLIGENCE
# ==========================================================

def competitive_analysis(feedback_list, competitor_text):

    feedback = "\n".join(feedback_list)

    if not competitor_text.strip():

        return {

            "executive_summary": "",

            "market_position": {},

            "competitor_strengths": [],

            "competitor_weaknesses": [],

            "competitive_gaps": [],

            "customer_opportunities": [],

            "recommended_initiatives": [],

            "strategic_actions": [],

            "scorecard": []

        }

    limited_data = ""

    if len(feedback_list) < 3:

        limited_data = """

Evidence from customer feedback is limited.

Only make conclusions directly supported by the supplied documents.

Lower confidence where evidence is weak.

Avoid broad assumptions.

"""

    prompt = f"""

You are a VP of Product Strategy.

You are preparing an executive competitive intelligence report.

You have TWO sources.

==================================================
SOURCE 1
CUSTOMER FEEDBACK
==================================================

{feedback}

==================================================
SOURCE 2
COMPETITOR DOCUMENT
==================================================

{competitor_text}

==================================================
OBJECTIVE
==================================================

Compare the customer feedback and competitor document as a single executive analysis.

Every conclusion must be directly supported by the supplied documents.

Do not invent:

• competitor capabilities

• competitor weaknesses

• customer requests

• business impact

• strategic opportunities

If evidence is missing,

state that evidence is limited,

or return an empty value.

Use conservative conclusions whenever evidence is weak.

{limited_data}

==================================================
GENERATE
==================================================

1 Executive Summary

Explain the current competitive position.

Discuss major strengths.

Discuss major weaknesses.

Discuss strategic opportunities.

--------------------------------------------------

2 Market Position

Return

overall_position

reason

Example

Leader

Competitive

Emerging

Behind Market

--------------------------------------------------

3 Competitor Strengths

Return

strength

business_value

--------------------------------------------------

4 Competitor Weaknesses

Return

weakness

business_risk

--------------------------------------------------

5 Competitive Opportunities

Return

opportunity

customer_value

--------------------------------------------------

6 Product Investments

Return

initiative

priority

reason

--------------------------------------------------

7 Executive Recommendations

Return five recommendations.

Begin recommendations with action verbs.

Examples

Invest

Expand

Prioritize

Accelerate

Differentiate

Modernize

Never return generic advice.

--------------------------------------------------

8 Executive Scorecard

Return

metric

value

reason

==================================================
RETURN JSON
==================================================

{{
    "executive_summary":"",

    "market_position":{{
        "overall_position":"",
        "reason":""
}},

    "competitor_strengths":[
        {{
            "strength":"",
            "business_value":"",
            "evidence":[
                ""
            ]
        }}
    ],

    "competitor_weaknesses":[
        {{
            "weakness":"",
            "business_risk":"",
            "evidence":[
                ""
            ]
        }}
    ],

    "competitive_gaps":[
        {{
            "gap":"",
            "reason":"",
            "evidence":[
                ""
            ]
        }}
    ],

    "customer_opportunities":[
        {{
            "opportunity":"",
            "customer_value":"",
            "evidence":[
                ""
            ]
        }}
    ],

"recommended_initiatives":[
    {{
        "initiative":"",
        "priority":"",
        "reason":"",
        "evidence":[
            ""
        ]
    }}
],

    "strategic_actions":[
        ""
    ],

    "scorecard":[
        {{
            "metric":"",
            "value":"",
            "reason":""
        }}
    ]
}}

"""

    return ask_json(

    prompt,

    required_keys=[

        "executive_summary",

        "market_position",

        "competitor_strengths",

        "competitor_weaknesses",

        "competitive_gaps",

        "customer_opportunities",

        "recommended_initiatives",

        "strategic_actions",

        "scorecard"

    ]

)