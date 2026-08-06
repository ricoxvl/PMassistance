import streamlit as st


def inject_theme():

    st.markdown("""
<style>

/* ----------------------------------------------------
   Executive Dashboard Theme
---------------------------------------------------- */

:root{
    --primary:#2563EB;
    --success:#16A34A;
    --warning:#D97706;
    --danger:#DC2626;

    --radius:14px;
}

/* Main App */

.stApp{
    background:#F5F7FA;
}

/* Sidebar */

section[data-testid="stSidebar"]{
    background:#FFFFFF;
    border-right:1px solid #E5E7EB;
}

/* Typography */

h1{
    font-size:2.2rem;
    font-weight:700;
    color:#111827;
}

h2{
    font-size:1.7rem;
    font-weight:700;
    color:#111827;
}

h3{
    font-size:1.35rem;
    font-weight:600;
    color:#111827;
}

p,label,span{
    color:#4B5563;
    font-size:15px;
}

/* Containers */

div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stVerticalBlock"]){
    border-radius:14px;
}

/* Metrics */

div[data-testid="metric-container"]{

    background:white;

    border:1px solid #E5E7EB;

    border-radius:14px;

    padding:18px;

    box-shadow:0 3px 10px rgba(0,0,0,.05);
}

/* DataFrames */

div[data-testid="stDataFrame"]{

    border-radius:14px;

    overflow:hidden;

    border:1px solid #E5E7EB;
}

/* Tabs */

button[data-baseweb="tab"]{

    font-size:15px;

    font-weight:600;

    color:#6B7280;
}

button[data-baseweb="tab"][aria-selected="true"]{

    color:#2563EB;

    border-bottom:3px solid #2563EB;
}

/* Buttons */

.stButton button{

    background:#2563EB;

    color:white;

    border:none;

    border-radius:10px;

    padding:.55rem 1.2rem;

    font-weight:600;

    transition:.2s;
}

.stButton button:hover{

    background:#1D4ED8;

    transform:translateY(-1px);
}

/* Expanders */

details{

    border-radius:12px;

    border:1px solid #E5E7EB;

    background:white;

    margin-bottom:12px;
}

/* Containers */

div[data-testid="stContainer"]{

    border-radius:14px;
}

/* Success / Warning / Error */

div[data-testid="stAlert"]{

    border-radius:12px;
}

/* Charts */

.js-plotly-plot{

    border-radius:14px;

    background:white;
}

/* Scrollbars */

::-webkit-scrollbar{
    width:10px;
}

::-webkit-scrollbar-thumb{
    background:#C7CBD1;
    border-radius:20px;
}

</style>
""", unsafe_allow_html=True)