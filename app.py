import streamlit as st

# Singly Reinforced (Single Tension Layer)
def calculate_single_layer(b, d, fc, fy, As):
    a = (As * fy) / (0.85 * fc * b)
    Mn = As * fy * (d - a / 2)  # Moment in kip-in
    return Mn / 12  # Convert to kip-ft

# Singly Reinforced (Two Layers of Tension Steel)
def calculate_two_layers(b, d1, d2, fc, fy, As1, As2):
    a1 = (As1 * fy) / (0.85 * fc * b)
    a2 = (As2 * fy) / (0.85 * fc * b)
    Mn1 = As1 * fy * (d1 - a1 / 2)
    Mn2 = As2 * fy * (d2 - a2 / 2)
    return (Mn1 + Mn2) / 12  # Convert to kip-ft

# Doubly Reinforced (Single Layer Tension & Compression)
def calculate_doubly_reinforced_single_layer(b, d, fc, fy, As_t, As_c, d_prime):
    net_tension = As_t * fy - As_c * fy
    a = net_tension / (0.85 * fc * b)
    Mn = As_t * fy * (d - a / 2) + As_c * fy * (d - d_prime)
    return Mn / 12  # Convert to kip-ft

# Doubly Reinforced (Double Tension Layers, Single Compression Layer)
def calculate_doubly_reinforced_double_tension_single_compression(b, fc, fy, 
                                                                 As_t1, As_t2, d1, d2,
                                                                 As_c, d_prime):
    total_net_tension = (As_t1 + As_t2) * fy - As_c * fy
    a = total_net_tension / (0.85 * fc * b)
    Mn_tension = As_t1 * fy * (d1 - a / 2) + As_t2 * fy * (d2 - a / 2)
    Mn_compression = As_c * fy * (d2 - d_prime)
    return (Mn_tension + Mn_compression) / 12  # Convert to kip-ft

# Streamlit UI
st.title("Reduced Nominal Moment Calculator for Rectangular Concrete Beams (English Units)")

beam_type = st.sidebar.selectbox("Select Beam Section Type", [
    "Singly Reinforced - Single Tension Layer",
    "Singly Reinforced - Two Layers (Equal Bars)",
    "Singly Reinforced - Two Layers (Different Bars)",
    "Doubly Reinforced - Single Tension & Compression",
    "Doubly Reinforced - Double Tension, Single Compression"
])

st.header("Enter Beam and Material Properties")

# Common Inputs
b = st.number_input("Beam Width, b (in)", value=12.0)
h = st.number_input("Beam Depth, h (in)", value=24.0)
fc = st.number_input("Concrete Compressive Strength, f'c (psi)", value=4000.0) / 1000  # Convert to ksi
fy = st.number_input("Steel Yield Strength, f_y (ksi)", value=60.0)

if beam_type == "Singly Reinforced - Single Tension Layer":
    As = st.number_input("Tension Reinforcement Area, As (in²)", value=1.5)
    d = h - 2.5  # Automatically computed
    st.write(f"Effective Depth, d = {d} in")
    Mn = calculate_single_layer(b, d, fc, fy, As)
    st.write("Calculated Reduced Nominal Moment: ", round(Mn, 2), "kip-ft")

elif beam_type == "Singly Reinforced - Two Layers (Equal Bars)":
    total_As = st.number_input("Total Tension Reinforcement Area, As (in²)", value=3.0)
    d = h - 3.5  # Automatically computed
    d1 = d - 1.0  # First layer depth
    d2 = d  # Second layer depth
    st.write(f"Effective Depths: d1 = {d1} in, d2 = {d2} in")
    Mn = calculate_two_layers(b, d1, d2, fc, fy, total_As / 2, total_As / 2)
    st.write("Calculated Reduced Nominal Moment: ", round(Mn, 2), "kip-ft")

elif beam_type == "Singly Reinforced - Two Layers (Different Bars)":
    As1 = st.number_input("Tension Reinforcement Area for Layer 1, As1 (in²)", value=1.5)
    As2 = st.number_input("Tension Reinforcement Area for Layer 2, As2 (in²)", value=1.5)
    d = h - 3.5
    d1 = d - 1.0
    d2 = d
    st.write(f"Effective Depths: d1 = {d1} in, d2 = {d2} in")
    Mn = calculate_two_layers(b, d1, d2, fc, fy, As1, As2)
    st.write("Calculated Reduced Nominal Moment: ", round(Mn, 2), "kip-ft")

elif beam_type == "Doubly Reinforced - Single Tension & Compression":
    As_t = st.number_input("Tension Reinforcement Area, As_t (in²)", value=3.0)
    As_c = st.number_input("Compression Reinforcement Area, As_c (in²)", value=1.0)
    d = h - 2.5
    d_prime = st.number_input("Effective Depth for Compression Steel, d' (in)", value=2.0)
    st.write(f"Effective Depth, d = {d} in")
    Mn = calculate_doubly_reinforced_single_layer(b, d, fc, fy, As_t, As_c, d_prime)
    st.write("Calculated Reduced Nominal Moment: ", round(Mn, 2), "kip-ft")

elif beam_type == "Doubly Reinforced - Double Tension, Single Compression":
    As_t1 = st.number_input("Tension Reinforcement Area for Layer 1, As_t1 (in²)", value=1.5)
    As_t2 = st.number_input("Tension Reinforcement Area for Layer 2, As_t2 (in²)", value=1.5)
    d = h - 3.5
    d1 = d - 1.0
    d2 = d
    As_c = st.number_input("Compression Reinforcement Area, As_c (in²)", value=1.0)
    d_prime = st.number_input("Effective Depth for Compression Steel, d' (in)", value=2.0)
    st.write(f"Effective Depths: d1 = {d1} in, d2 = {d2} in")
    Mn = calculate_doubly_reinforced_double_tension_single_compression(b, fc, fy,
                                                                        As_t1, As_t2, d1, d2,
                                                                        As_c, d_prime)
    st.write("Calculated Reduced Nominal Moment: ", round(Mn, 2), "kip-ft")
