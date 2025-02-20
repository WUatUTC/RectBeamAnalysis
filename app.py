import streamlit as st

# Singly Reinforced (Single Tension Layer)
def calculate_single_layer(b, d, fc, fy, As):
    # Depth of equivalent stress block (simplified)
    a = (As * fy) / (0.85 * fc * b)
    Mn = As * fy * (d - a / 2)
    return Mn

# Singly Reinforced (Two Layers of Tension Steel)
def calculate_two_layers(b, d1, d2, fc, fy, As1, As2):
    # Compute separate contributions for each tension layer.
    # For simplicity, we use the same 'a' factor from each layer’s force contribution.
    a1 = (As1 * fy) / (0.85 * fc * b)
    a2 = (As2 * fy) / (0.85 * fc * b)
    Mn1 = As1 * fy * (d1 - a1 / 2)
    Mn2 = As2 * fy * (d2 - a2 / 2)
    return Mn1 + Mn2

# Doubly Reinforced (Single Layer Tension & Compression)
def calculate_doubly_reinforced_single_layer(b, d, fc, fy, As_t, As_c, d_prime):
    # Net tensile force minus compression force is balanced by the concrete
    net_tension = As_t * fy - As_c * fy
    a = net_tension / (0.85 * fc * b)
    # Nominal moment includes contributions from both tension and compression steel
    Mn = As_t * fy * (d - a / 2) + As_c * fy * (d - d_prime)
    return Mn

# Doubly Reinforced (Double Tension Layers, Single Compression Layer)
def calculate_doubly_reinforced_double_tension_single_compression(b, fc, fy, 
                                                                 As_t1, As_t2, d1, d2,
                                                                 As_c, d_prime):
    # Total net tensile force (from both tension layers) minus the compression force
    total_net_tension = (As_t1 + As_t2) * fy - As_c * fy
    a = total_net_tension / (0.85 * fc * b)
    # Assume each tension layer contributes with its own effective depth,
    # and the compression steel contribution uses the farthest tension depth (d2)
    Mn_tension = As_t1 * fy * (d1 - a / 2) + As_t2 * fy * (d2 - a / 2)
    Mn_compression = As_c * fy * (d2 - d_prime)
    return Mn_tension + Mn_compression

# Doubly Reinforced (Double Tension Layers, Double Compression Layers)
def calculate_doubly_reinforced_double_tension_double_compression(b, fc, fy,
                                                                  As_t1, As_t2, d1, d2,
                                                                  As_c1, As_c2, d1_prime, d2_prime):
    # Total net tensile force minus total compression force
    total_net_tension = (As_t1 + As_t2) * fy - (As_c1 + As_c2) * fy
    a = total_net_tension / (0.85 * fc * b)
    # Tension reinforcement moment contributions (using respective effective depths)
    Mn_tension = As_t1 * fy * (d1 - a / 2) + As_t2 * fy * (d2 - a / 2)
    # Compression reinforcement contributions (using the distance from the far tension layer, d2)
    Mn_compression = As_c1 * fy * (d2 - d1_prime) + As_c2 * fy * (d2 - d2_prime)
    return Mn_tension + Mn_compression

# Streamlit UI
st.title("Reduced Nominal Moment Calculator for Rectangular Concrete Beams")

beam_type = st.sidebar.selectbox("Select Beam Section Type", [
    "Singly Reinforced - Single Tension Layer",
    "Singly Reinforced - Two Layers (Equal Bars)",
    "Singly Reinforced - Two Layers (Different Bars)",
    "Doubly Reinforced - Single Tension & Compression",
    "Doubly Reinforced - Double Tension, Single Compression",
    "Doubly Reinforced - Double Tension, Double Compression"
])

st.header("Enter Beam and Material Properties")

# Common Inputs
b = st.number_input("Beam Width, b (mm)", value=300)
fc = st.number_input("Concrete Compressive Strength, f'c (MPa)", value=30.0)
fy = st.number_input("Steel Yield Strength, f_y (MPa)", value=500.0)
d = st.number_input("Effective Depth, d (mm)", value=500)

# Conditional Inputs and Calculations Based on Selected Beam Type
if beam_type == "Singly Reinforced - Single Tension Layer":
    As = st.number_input("Tension Reinforcement Area, As (mm²)", value=500)
    Mn = calculate_single_layer(b, d, fc, fy, As)
    st.write("Calculated Reduced Nominal Moment: ", Mn, "N·mm")

elif beam_type == "Singly Reinforced - Two Layers (Equal Bars)":
    total_As = st.number_input("Total Tension Reinforcement Area, As (mm²)", value=500)
    d1 = st.number_input("Effective Depth for Layer 1 (mm)", value=d - 50)
    d2 = st.number_input("Effective Depth for Layer 2 (mm)", value=d - 100)
    Mn = calculate_two_layers(b, d1, d2, fc, fy, total_As / 2, total_As / 2)
    st.write("Calculated Reduced Nominal Moment: ", Mn, "N·mm")

elif beam_type == "Singly Reinforced - Two Layers (Different Bars)":
    As1 = st.number_input("Tension Reinforcement Area for Layer 1, As1 (mm²)", value=250)
    As2 = st.number_input("Tension Reinforcement Area for Layer 2, As2 (mm²)", value=300)
    d1 = st.number_input("Effective Depth for Layer 1 (mm)", value=d - 50)
    d2 = st.number_input("Effective Depth for Layer 2 (mm)", value=d - 100)
    Mn = calculate_two_layers(b, d1, d2, fc, fy, As1, As2)
    st.write("Calculated Reduced Nominal Moment: ", Mn, "N·mm")

elif beam_type == "Doubly Reinforced - Single Tension & Compression":
    st.subheader("Single Layer Tension & Compression")
    As_t = st.number_input("Tension Reinforcement Area, As_t (mm²)", value=500)
    As_c = st.number_input("Compression Reinforcement Area, As_c (mm²)", value=100)
    d_prime = st.number_input("Effective Depth for Compression Steel, d' (mm)", value=50)
    Mn = calculate_doubly_reinforced_single_layer(b, d, fc, fy, As_t, As_c, d_prime)
    st.write("Calculated Reduced Nominal Moment: ", Mn, "N·mm")

elif beam_type == "Doubly Reinforced - Double Tension, Single Compression":
    st.subheader("Double Tension Layers & Single Compression Layer")
    As_t1 = st.number_input("Tension Reinforcement Area for Layer 1, As_t1 (mm²)", value=250)
    As_t2 = st.number_input("Tension Reinforcement Area for Layer 2, As_t2 (mm²)", value=250)
    d1 = st.number_input("Effective Depth for Tension Layer 1 (mm)", value=d - 60)
    d2 = st.number_input("Effective Depth for Tension Layer 2 (mm)", value=d - 20)
    As_c = st.number_input("Compression Reinforcement Area, As_c (mm²)", value=100)
    d_prime = st.number_input("Effective Depth for Compression Steel, d' (mm)", value=50)
    Mn = calculate_doubly_reinforced_double_tension_single_compression(b, fc, fy,
                                                                        As_t1, As_t2, d1, d2,
                                                                        As_c, d_prime)
    st.write("Calculated Reduced Nominal Moment: ", Mn, "N·mm")

elif beam_type == "Doubly Reinforced - Double Tension, Double Compression":
    st.subheader("Double Tension Layers & Double Compression Layers")
    As_t1 = st.number_input("Tension Reinforcement Area for Layer 1, As_t1 (mm²)", value=250)
    As_t2 = st.number_input("Tension Reinforcement Area for Layer 2, As_t2 (mm²)", value=250)
    d1 = st.number_input("Effective Depth for Tension Layer 1 (mm)", value=d - 60)
    d2 = st.number_input("Effective Depth for Tension Layer 2 (mm)", value=d - 20)
    As_c1 = st.number_input("Compression Reinforcement Area for Layer 1, As_c1 (mm²)", value=50)
    As_c2 = st.number_input("Compression Reinforcement Area for Layer 2, As_c2 (mm²)", value=50)
    d1_prime = st.number_input("Effective Depth for Compression Layer 1 (mm)", value=40)
    d2_prime = st.number_input("Effective Depth for Compression Layer 2 (mm)", value=20)
    Mn = calculate_doubly_reinforced_double_tension_double_compression(b, fc, fy,
                                                                        As_t1, As_t2, d1, d2,
                                                                        As_c1, As_c2, d1_prime, d2_prime)
    st.write("Calculated Reduced Nominal Moment: ", Mn, "N·mm")
