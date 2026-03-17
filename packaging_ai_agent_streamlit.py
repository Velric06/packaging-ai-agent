import streamlit as st

st.set_page_config(page_title="Packaging Production AI Agent", layout="centered")

st.title("📦 Production Planning Agent")
st.caption("Non Woven Bag Manufacturing Calculator")

st.markdown("### Input Parameters")

col1, col2 = st.columns(2)

with col1:
    fabric_gsm = st.number_input("Fabric GSM", value=80.0)
    loop_gsm = st.number_input("Loop GSM", value=80.0)
    height = st.number_input("Bag Height (inch)", value=10.25)
    width = st.number_input("Bag Width (inch)", value=11.5)

with col2:
    gusset = st.number_input("Gusset (inch)", value=3.75)
    loop_height = st.number_input("Loop Height (inch)", value=15.0)
    setoff = st.number_input("Set-off value", value=1.38)

colors = st.selectbox("Number of Flexographic Colors", [0,1,2,3,4])
ink_type = st.selectbox("Ink Type", ["Normal", "Gold", "Silver"])

st.markdown("---")

def inch_to_meter(x):
    return x * 0.0254

# Fabric area calculation
area_m2 = (2 * inch_to_meter(height) * inch_to_meter(width)) + (2 * inch_to_meter(gusset) * inch_to_meter(height))
fabric_weight = fabric_gsm * area_m2

# Loop calculation
loop_width = 2
loop_area = inch_to_meter(loop_width) * inch_to_meter(loop_height) * 2
loop_weight = loop_area * loop_gsm

grams_per_bag = (fabric_weight + loop_weight) * 1000

pieces_per_kg = 1000 / grams_per_bag if grams_per_bag != 0 else 0

printing_cost_map = {0:0,1:6,2:9,3:12,4:15}
printing_cost = printing_cost_map.get(colors,0)

if ink_type in ["Gold","Silver"]:
    printing_cost += 5

fabric_rate = st.number_input("Fabric Cost ₹/kg", value=120.0)

bag_cost_per_kg = fabric_rate + printing_cost
rate_per_bag = (grams_per_bag/1000) * bag_cost_per_kg

seal_allowance = 1
roll_width = width + gusset + seal_allowance

handle_fold = 3
bottom_fold = 1
cylinder_repeat = height + handle_fold + bottom_fold
cylinder_size = round(cylinder_repeat)

st.markdown("### Output Results")

col3, col4 = st.columns(2)

with col3:
    st.metric("Grams per Bag", round(grams_per_bag,2))
    st.metric("Pieces per KG", round(pieces_per_kg,2))

with col4:
    st.metric("Rate per Bag ₹", round(rate_per_bag,2))
    st.metric("Cylinder Size", cylinder_size)

st.metric("Roll Width (inch)", round(roll_width,2))

st.markdown("---")
st.caption("Minimal AI-assisted calculator for packaging production planning")
