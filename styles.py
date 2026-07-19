import streamlit as st

def load_css():

    st.markdown("""
    <style>

/* =========================
GLOBAL BACKGROUND
========================= */

.stApp{
    background:#FFFFFF;
    color:#14532D;
}


/* =========================
SIDEBAR
========================= */

section[data-testid="stSidebar"]{

    background:#F4FBF3;

    border-right:1px solid #D8ECD8;

}


/* =========================
HEADINGS
========================= */

h1,h2,h3,h4,h5,h6{

    color:#14532D;

    font-weight:800;

}


/* =========================
TEXT
========================= */

p,label,span{

    color:#355E3B;

}


/* =========================
BUTTONS
========================= */

.stButton>button{

    background:linear-gradient(
    135deg,
    #43A047,
    #2E7D32
    );

    color:white;

    border:none;

    border-radius:14px;

    height:50px;

    font-size:16px;

    font-weight:700;

    transition:.25s;

    box-shadow:
    0 8px 18px rgba(46,125,50,.18);

}

.stButton>button:hover{

    background:linear-gradient(
    135deg,
    #2E7D32,
    #1B5E20
    );

    transform:translateY(-2px);

}


/* =========================
TEXT INPUT
========================= */

.stTextInput input{

    background:white;

    border:2px solid #DDF5D8;

    border-radius:14px;

    color:#14532D;

}


/* =========================
SELECT BOX
========================= */

.stSelectbox{

    color:#14532D;

}


/* =========================
METRICS
========================= */

div[data-testid="stMetric"]{

    background:white;

    border-radius:20px;

    padding:18px;

    border-left:6px solid #43A047;

    box-shadow:
    0 10px 24px rgba(46,125,50,.08);

}


/* =========================
FILE UPLOADER
========================= */

.stFileUploader{

    background:#FAFFFA;

    border:2px dashed #81C784;

    border-radius:18px;

    padding:15px;

}


/* =========================
TABLE
========================= */

[data-testid="stDataFrame"]{

    border-radius:18px;

    overflow:hidden;

    border:1px solid #DDF5D8;

}


/* =========================
TABS
========================= */

.stTabs [data-baseweb="tab"]{

    background:#F4FBF3;

    color:#2E7D32;

    border-radius:14px;

    font-weight:700;

}

.stTabs [aria-selected="true"]{

    background:#2E7D32 !important;

    color:white !important;

}


/* =========================
EXPANDER
========================= */

.streamlit-expanderHeader{

    color:#14532D;

}


/* =========================
DIVIDER
========================= */

hr{

    border-color:#E8F5E9;

}


/* =========================
SCROLLBAR
========================= */

::-webkit-scrollbar{

    width:10px;

}

::-webkit-scrollbar-thumb{

    background:#81C784;

    border-radius:10px;

}

    </style>
    """, unsafe_allow_html=True)
