import streamlit as st

st.set_page_config(layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
body {background:#0f172a;}
.card {background:#1e293b;padding:20px;border-radius:14px;}
h1,h2,h3{color:#e2e8f0;}
</style>
""", unsafe_allow_html=True)

st.title("📦 Bag Costing Calculator")

tab1, tab2 = st.tabs(["Calculator", "Velric Says:"])

with tab1:

    col1, col2 = st.columns([1.1,1])

    with col1:

        st.subheader("🧾 BAG")

        c1,c2,c3 = st.columns(3)
        width = c1.number_input("Width (in)", value=8.0)
        height = c2.number_input("Height (in)", value=6.0)
        gusset = c3.number_input("Gusset (in)", value=6.0)

        fabric_gsm = st.number_input("Fabric GSM", value=68.0)
        moq = st.number_input("MOQ", value=10000)

        st.subheader("🎨 PRINT")

        color_map = {
            "Plain":0,
            "1 Color":25,
            "2 Color":30,
            "3 Color":35,
            "4 Color":40
        }

        color_choice = st.selectbox("Colors", list(color_map.keys()))
        printing = color_map[color_choice]

        gold = st.toggle("Gold/Silver (+5)", True)

        setoff = st.number_input("Set-off ₹", value=220.0)
        fabric_rate = st.number_input("Fabric ₹/kg", value=130.0)

        st.subheader("🔁 LOOP")

        l1,l2,l3 = st.columns(3)
        loop_width = l1.number_input("Width", value=2.0)
        loop_height = l2.number_input("Height", value=15.0)
        loop_gsm = l3.number_input("Loop GSM", value=80.0)

    # ---------- CALCULATIONS ----------

    # Convert inch to mm
    width_mm = width * 25.4
    height_mm = height * 25.4
    gusset_mm = gusset * 25.4

    # Fabric grams (exact structure)
    fabric_grams = (width_mm * height_mm * fabric_gsm) / 1000000

    # Loop grams
    loop_grams = ((loop_width*25.4 * loop_height*25.4 * loop_gsm) / 1000000) * 2

    grams_per_bag = fabric_grams + loop_grams

    # Total weight
    total_weight = (grams_per_bag * moq) / 1000

    # Printing cost
    if color_choice != "Plain" and gold:
        printing += 5

    # Bill
    bill = (fabric_rate + printing) * total_weight + setoff

    # Rate per bag
    rate_per_bag = bill / moq

    # Rate per kg
    rate_per_kg = bill / total_weight

    # GST
    gst_rate = rate_per_bag * 1.18

    # Roll width
    roll_width = (width_mm + gusset_mm) / 25.4

    # Cylinder
    cylinder = height_mm / 25.4

    # ---------- OUTPUT ----------
    with col2:

        st.subheader("📊 OUTPUT")

        c1,c2 = st.columns(2)
        c1.metric("Grams / Bag", f"{grams_per_bag:.3f}")
        c2.metric("Total Weight", f"{total_weight:.2f} kg")

        c3,c4 = st.columns(2)
        c3.metric("Roll Width", f"{roll_width:.2f} in")
        c4.metric("Cylinder", f"{cylinder:.2f} in")

        st.markdown("---")

        c5,c6,c7 = st.columns(3)
        c5.metric("Rate / Bag", f"₹ {rate_per_bag:.2f}")
        c6.metric("Incl GST", f"₹ {gst_rate:.2f}")
        c7.metric("Rate / KG", f"₹ {rate_per_kg:.2f}")

with tab2:

    st.subheader("🧠 Velric Says:")

    if grams_per_bag > 18:
        st.warning("Weight is high. Reduce GSM to optimize cost.")
    else:
        st.success("Optimized bag weight.")

    if printing > 30:
        st.info("Printing cost is high. Reduce colors if possible.")

    st.write("This will evolve into full AI production planning.")
