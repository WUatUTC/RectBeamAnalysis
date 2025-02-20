import streamlit as st

def calculate_single_layer(b, d, fc, fy, As):
    # Compute the depth of the equivalent stress block 'a'
    a = (As * fy) / (0.85 * fc * b)
    # Calculate the nominal moment
    Mn = As * fy * (d - a/2)
    return Mn

def calculate_two_layers(b, d1, d2, fc, fy, As1, As2):
    # For simplicity, assume separate stress blocks for each layer.
    a1 = (As1 * fy) / (0.85 * fc * b)
    a2 = (As2 * fy) / (0.85 * fc * b)
    Mn1 = As1 * fy * (d1 - a1/2)
    Mn2 = As2 * fy * (d2 - a2/2)
    return Mn1 + Mn2

# More functions can be defined for doubly reinforced cases

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

# Common inputs
b = st.number_input("Beam Width, b (mm)", value=300)
fc = st.number_input("Concrete Compressive Strength, f'c (MPa)", value=30)
fy = st.number_input("Steel Yield Strength, f_y (MPa)", value=500)
d = st.number_input("Effective Depth, d (mm)", value=500)

if beam_type == "Singly Reinforced - Single Tension Layer":
    As = st.number_input("Tension Reinforcement Area, As (mm²)", value=500)
    Mn = calculate_single_layer(b, d, fc, fy, As)
    st.write("Calculated Reduced Nominal Moment: ", Mn, "N·mm")

elif beam_type == "Singly Reinforced - Two Layers (Equal Bars)":
    # For equal layers, assume the user enters half the area for each layer.
    total_As = st.number_input("Total Tension Reinforcement Area, As (mm²)", value=500)
    # Assume layers are symmetrically placed; let’s say d1 and d2 are offsets from the top.
    d1 = st.number_input("Effective Depth for Layer 1 (mm)", value=d-50)
    d2 = st.number_input("Effective Depth for Layer 2 (mm)", value=d-100)
    Mn = calculate_two_layers(b, d1, d2, fc, fy, total_As/2, total_As/2)
    st.write("Calculated Reduced Nominal Moment: ", Mn, "N·mm")

elif beam_type == "Singly Reinforced - Two Layers (Different Bars)":
    As1 = st.number_input("Tension Reinforcement Area for Layer 1, As1 (mm²)", value=250)
    As2 = st.number_input("Tension Reinforcement Area for Layer 2, As2 (mm²)", value=300)
    d1 = st.number_input("Effective Depth for Layer 1 (mm)", value=d-50)
    d2 = st.number_input("Effective Depth for Layer 2 (mm)", value=d-100)
    Mn = calculate_two_layers(b, d1, d2, fc, fy, As1, As2)
    st.write("Calculated Reduced Nominal Moment: ", Mn, "N·mm")

# Additional sections for doubly reinforced cases would include extra inputs 
# for compression reinforcement and different calculation functions.

