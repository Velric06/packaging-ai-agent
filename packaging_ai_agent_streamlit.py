import streamlit as st

# Page config
st.set_page_config(page_title="Production AI Agent", layout="wide")

# Styling (Minimal + Calm UI)
st.markdown("""
<style>
body {
    background-color: #0f172a;
}
.block-container {
    padding-top: 2rem;
}
.stNumberInput, .stSelectbox {
    background-color: #1e293b;
    border-radius: 10px;
}
.stMetric {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 12px;
}
h1, h2, h3 {
    color: #e2e8f0;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("📦 Production Planning Agent")
st.caption("AI-powered Non Woven Bag Manufacturing System")

# Layout
col1, col2 = st.columns(2)

# INPUT SECTION
with col1:
    st.subheader("🧾 Bag Inputs")
    fabric_gsm = st.number_input("Fabric GSM", value=80.0)
    loop_gsm = st.number_input("Loop GSM", value=80.0)
    height = st.number_input("Height (inch)", value=10.0)
    width = st.number_input("Width (inch)", value=10.0)
    gusset = st.number_input("Gusset (inch)", value=4.0)
    loop_height = st.number_input("Loop Height (inch)", value=15.0)

with col2:
    st.subheader("🎨 Printing Inputs")
    colors = st.selectbox("Flexo Colors", [0,1,2,3,4])
    ink_type = st.selectbox("Ink Type", ["Normal", "Gold", "Silver"])
    setoff = st.number_input("Set-off", value=1.38)
    fabric_rate = st.number_input("Fabric Cost ₹/kg", value=120.0)

# Divider
st.markdown("---")

# CALCULATIONS
def inch_to_meter(x):
    return x * 0.0254

area = (2 * height * width) + (2 * gusset * height)
area_m2 = (2 * inch_to_meter(height) * inch_to_meter(width)) + (2 * inch_to_meter(gusset) * inch_to_meter(height))

fabric_weight = fabric_gsm * area_m2

loop_width = 2
loop_area = inch_to_meter(loop_width) * inch_to_meter(loop_height) * 2
loop_weight = loop_area * loop_gsm

grams_per_bag = (fabric_weight + loop_weight) * 1000
pieces_per_kg = 1000 / grams_per_bag if grams_per_bag else 0

printing_cost_map = {0:0,1:6,2:9,3:12,4:15}
printing_cost = printing_cost_map.get(colors,0)

if ink_type in ["Gold","Silver"]:
    printing_cost += 5

bag_cost_per_kg = fabric_rate + printing_cost
rate_per_bag = (grams_per_bag/1000) * bag_cost_per_kg

roll_width = width + gusset + 1
cylinder_size = round(height + 4)

# OUTPUT SECTION
st.subheader("📊 Production Output")

col3, col4, col5 = st.columns(3)

col3.metric("Grams / Bag", f"{grams_per_bag:.2f} g")
col4.metric("Rate / Bag", f"₹ {rate_per_bag:.2f}")
col5.metric("Pieces / KG", f"{pieces_per_kg:.1f}")

col6, col7 = st.columns(2)
col6.metric("Cylinder Size", f"{cylinder_size}")
col7.metric("Roll Width", f"{roll_width:.2f} inch")

# AI Insight Box
st.markdown("---")
st.subheader("🧠 AI Insight")

if grams_per_bag > 40:
    st.info("High weight detected. Consider reducing GSM to optimize cost.")
elif grams_per_bag < 25:
    st.success("Optimized lightweight bag. Good for cost efficiency.")
else:
    st.write("Balanced configuration. Suitable for standard production.")
