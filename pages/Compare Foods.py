import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from nutrition import nutrition_df
from styles import load_css

load_css()
st.markdown("""
<div style="
background:linear-gradient(135deg,#F3FAF3,#E8F5E9,#DDF5D8);
padding:35px;
border-radius:25px;
box-shadow:0 10px 25px rgba(46,125,50,.10);
margin-bottom:25px;
">

<h1 style="
text-align:center;
color:#14532D;
font-size:42px;
font-weight:900;
">

⚖️ Compare Foods

</h1>

<p style="
text-align:center;
font-size:18px;
color:#355E3B;
">

Compare nutrition values and discover the healthier choice.

</p>

</div>
""", unsafe_allow_html=True)
st.markdown("""
<div style="
background:white;
padding:28px;
border-radius:22px;
box-shadow:0 8px 20px rgba(46,125,50,.08);
border:1px solid #E8F5E9;
">
<h3 style="color:#14532D;">
🥗 Select Foods
</h3>
""", unsafe_allow_html=True)

food_list = sorted(nutrition_df["Food_Name"].tolist())

col1, col2 = st.columns(2)

with col1:
    food1 = st.selectbox(
        "Select First Food",
        food_list,
        key="food1"
    )

with col2:
    food2 = st.selectbox(
        "Select Second Food",
        food_list,
        key="food2"
    )
st.markdown("</div>", unsafe_allow_html=True)
info1 = nutrition_df[nutrition_df["Food_Name"] == food1].iloc[0]
info2 = nutrition_df[nutrition_df["Food_Name"] == food2].iloc[0]
st.divider()

st.subheader("📊 Nutrition Comparison")

metrics = [
    ("🔥 Calories", info1["Calories"], info2["Calories"]),
    ("💪 Protein", f'{info1["Protein"]} g', f'{info2["Protein"]} g'),
    ("🍚 Carbs", f'{info1["Carbs"]} g', f'{info2["Carbs"]} g'),
    ("🥑 Fat", f'{info1["Fat"]} g', f'{info2["Fat"]} g'),
    ("⭐ Health Score", info1["Health_Score"], info2["Health_Score"])
]

for title, value1, value2 in metrics:

    st.markdown(f"### {title}")

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(f"""
        <div style="
        background:white;
        padding:20px;
        border-radius:18px;
        border-left:6px solid #43A047;
        text-align:center;
        box-shadow:0 6px 15px rgba(46,125,50,.08);
        ">
        <h4 style="color:#14532D;">{food1.replace("_"," ").title()}</h4>
        <h2 style="color:#2E7D32;">{value1}</h2>
        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown(f"""
        <div style="
        background:white;
        padding:20px;
        border-radius:18px;
        border-left:6px solid #81C784;
        text-align:center;
        box-shadow:0 6px 15px rgba(46,125,50,.08);
        ">
        <h4 style="color:#14532D;">{food2.replace("_"," ").title()}</h4>
        <h2 style="color:#2E7D32;">{value2}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
if info1["Health_Score"] > info2["Health_Score"]:

    winner = food1.replace("_"," ").title()

elif info2["Health_Score"] > info1["Health_Score"]:

    winner = food2.replace("_"," ").title()

else:

    winner = None


if winner:

    st.markdown(f"""
    <div style="
    background:#E8F5E9;
    padding:25px;
    border-radius:20px;
    text-align:center;
    box-shadow:0 8px 20px rgba(46,125,50,.10);
    ">

    <h2 style="color:#2E7D32;">
    🏆 {winner}
    </h2>

    <p style="
    color:#14532D;
    font-size:18px;
    ">
    is the healthier choice.
    </p>

    </div>
    """, unsafe_allow_html=True)

else:

    st.info("🤝 Both foods have the same Health Score.")