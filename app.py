import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="TFII Dashboard", layout="wide")

# ---------------- PREMIUM STYLE ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Card style */
.card {
    background: rgba(255, 255, 255, 0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    transition: 0.3s;
}

.card:hover {
    transform: scale(1.02);
}

/* Section spacing */
.section {
    margin-top: 30px;
}

/* Titles */
h1, h2, h3 {
    color: #ffffff;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("💎 True Financial Inclusion Dashboard")
st.markdown("### From Access to Usage: Measuring Financial Inclusion")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_excel("Financial_Inclusion_Dataset.xlsx")
    df.columns = df.columns.str.strip()
    return df

df = load_data()
df["TFII Score"] = df["TFII Score (0-100)"]

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔍 Input State Data")

state = st.sidebar.text_input("State Name")
branches = st.sidebar.number_input("Bank Branches", min_value=0.0)
cd_ratio = st.sidebar.number_input("Credit-Deposit Ratio (%)", min_value=0.0)
deposits = st.sidebar.number_input("Total Deposits (₹ Crores)", min_value=0.0)

def calculate_tfii(branches, cd_ratio, deposits):
    return (0.0008 * branches) + (0.12 * cd_ratio) + (0.000001 * deposits) + 10

if st.sidebar.button("🚀 Calculate TFII"):
    score = calculate_tfii(branches, cd_ratio, deposits)

    st.markdown(f"""
    <div class="card">
    <h2>📈 TFII Score: {round(score,2)}</h2>
    </div>
    """, unsafe_allow_html=True)

# ---------------- KPI CARDS ----------------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown("## 📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.markdown(f"""
<div class="card">
<h3>📌 Avg TFII</h3>
<h2>{round(df["TFII Score"].mean(),2)}</h2>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="card">
<h3>🏆 Top State</h3>
<h2>{df.sort_values("TFII Score", ascending=False).iloc[0]["State / Union Territory"]}</h2>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="card">
<h3>⚠️ Lowest State</h3>
<h2>{df.sort_values("TFII Score").iloc[0]["State / Union Territory"]}</h2>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- TOP & BOTTOM ----------------
st.markdown("## 🏆 Performance Overview")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Top 5 States")
    st.dataframe(df.sort_values("TFII Score", ascending=False).head(5))

with col2:
    st.markdown("### Bottom 5 States")
    st.dataframe(df.sort_values("TFII Score").head(5))

# ---------------- ADVANCED CHART ----------------
st.markdown("## 📊 TFII Distribution")

fig = px.bar(
    df.sort_values("TFII Score"),
    x="State / Union Territory",
    y="TFII Score",
    color="TFII Score",
    color_continuous_scale=["#00c6ff", "#0072ff"]
)

fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis_tickangle=-45
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- COMPARISON ----------------
st.markdown("## ⚖️ Compare States")

states = df["State / Union Territory"].unique()

s1 = st.selectbox("Select State 1", states)
s2 = st.selectbox("Select State 2", states)

d1 = df[df["State / Union Territory"] == s1].iloc[0]
d2 = df[df["State / Union Territory"] == s2].iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {s1}")
    st.metric("TFII", d1["TFII Score"])
    st.metric("Access", d1["Access Score (0-100)"])
    st.metric("Usage", d1["Usage Score (0-100)"])

with col2:
    st.markdown(f"### {s2}")
    st.metric("TFII", d2["TFII Score"])
    st.metric("Access", d2["Access Score (0-100)"])
    st.metric("Usage", d2["Usage Score (0-100)"])

# ---------------- GAP ANALYSIS ----------------
st.markdown("## 📉 Inclusion Gap Analysis")

gap_df = df.sort_values("Inclusion Gap (Access minus Usage)", ascending=False)

st.dataframe(gap_df.head(5))

st.warning("⚠️ High gap = people have access but are not using financial services")

# ---------------- INSIGHTS ----------------
st.markdown("## 🧠 Key Insights")

top = df.sort_values("TFII Score", ascending=False).iloc[0]["State / Union Territory"]
low = df.sort_values("TFII Score").iloc[0]["State / Union Territory"]

st.markdown(f"""
<div class="card">
✅ <b>Top Performer:</b> {top} <br><br>
⚠️ <b>Needs Attention:</b> {low} <br><br>
💡 <b>Insight:</b> Financial inclusion is not just access — usage matters more.
</div>
""", unsafe_allow_html=True)

# ---------------- DOWNLOAD ----------------
st.markdown("## 📥 Download")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button("Download Dataset", csv, "TFII_Data.csv", "text/csv")