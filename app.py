# This app is for education purpose to compute reduced nominal moment for different rectangular beam section
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Constants
Es = 29000  # ksi (Steel Modulus of Elasticity)

# Compute beta_1 based on f'c (psi)
def compute_beta1(fc):
    if fc <= 4000:
        return 0.85
    elif fc > 8000:
        return 0.65
    else:
        return 0.85 - 0.05 * (fc - 4000) / 1000

# Compute strength reduction factor based on net tensile strain
def strength_reduction_factor(epsilon_t):
    if epsilon_t >= 0.005:
        return 0.9
    elif epsilon_t <= 0.002:
        return 0.65
    else:
        return 0.65 + (epsilon_t - 0.002) * (0.9 - 0.65) / (0.005 - 0.002)

# Singly Reinforced Beam - Single Layer
def singly_reinforced_single_layer(b, h, fc, fy, As):
    d = h - 2.5  # Effective depth
    beta1 = compute_beta1(fc)
    a = (As * fy) / (0.85 * fc * b)  # Compression block depth
    c = a / beta1  # Neutral axis depth
    epsilon_t = 0.003 * (d - c) / c  # Net tensile strain
    Mn = As * fy * (d - a / 2)  # Nominal moment in kip-in
    phi = strength_reduction_factor(epsilon_t)
    return Mn / 12, epsilon_t, c, phi, (Mn / 12) * phi  # Convert to kip-ft

# Singly Reinforced Beam - Two Layers
def singly_reinforced_two_layers(b, h, fc, fy, As):
    d_t = h - 2.5  # Approximate distance to extreme tension steel layer
    beta1 = compute_beta1(fc)
    a = (As * fy) / (0.85 * fc * b)
    c = a / beta1
    epsilon_t = 0.003 * (d_t - c) / c
    Mn = As * fy * (d_t - a / 2)
    phi = strength_reduction_factor(epsilon_t)
    return Mn / 12, epsilon_t, c, phi, (Mn / 12) * phi

# Iterative approach for doubly reinforced beams
def doubly_reinforced_beam(b, h, fc, fy, As_t, As_c, d_prime):
    d_t = h - 2.5  # Effective depth for extreme tension steel layer
    beta1 = compute_beta1(fc)
    
    # Initial guess for neutral axis depth
    c = d_t / 4
    tolerance = 0.001  # Convergence threshold
    max_iterations = 100
    iteration = 0

    while iteration < max_iterations:
        a = beta1 * c  # Compression block depth
        Cc = 0.85 * fc * b * a  # Concrete compressive force

        # Compute compression steel stress
        epsilon_s = 0.003 * (c - d_prime) / c
        fs_c = min(fy, Es * epsilon_s)  # Ensure compression steel does not exceed fy
        Cs = As_c * (fs_c - 0.85 * fc)  # Compression steel force

        # Compute net tension force
        T = As_t * fy

        # Force balance check
        if abs(T - (Cc + Cs)) < tolerance:
            break  # Converged
        else:
            c = c * (T / (Cc + Cs))  # Adjust trial c

        iteration += 1

    # Compute net tensile strain
    epsilon_t = 0.003 * (d_t - c) / c

    # Compute nominal moment
    Mn = As_t * fy * (d_t - a / 2) + As_c * fs_c * (d_t - d_prime)

    # Compute strength reduction factor
    phi = strength_reduction_factor(epsilon_t)

    return Mn / 12, epsilon_t, phi, (Mn / 12) * phi, c, Cc, Cs, T  # Convert to kip-ft

# Streamlit UI
st.title("Reinforced Concrete Beam Moment Calculator")
st.sidebar.header("Beam Properties")

beam_type = st.sidebar.selectbox("Select Beam Section Type", [
    "Singly - Single Layer Tension",
    "Singly - Double Layer Tension",
    "Doubly - Single Layer Tension & Compression",
    "Doubly - Double Layer Tension & Compression"
])

b = st.sidebar.number_input("Beam Width, b (in)", value=12.0)
h = st.sidebar.number_input("Beam Depth, h (in)", value=24.0)
fc = st.sidebar.number_input("Concrete Strength, f'c (psi)", value=4000.0) / 1000  # Convert psi to ksi
fy = st.sidebar.number_input("Steel Yield Strength, f_y (ksi)", value=60.0)

if beam_type == "Singly - Single Layer Tension":
    As = st.sidebar.number_input("Tension Reinforcement, As (in²)", value=1.5)
    Mn, epsilon_t, c, phi, Mn_red = singly_reinforced_single_layer(b, h, fc, fy, As)

elif beam_type == "Singly - Double Layer Tension":
    As = st.sidebar.number_input("Total Tension Reinforcement, As (in²)", value=3.0)
    Mn, epsilon_t, c, phi, Mn_red = singly_reinforced_two_layers(b, h, fc, fy, As)

elif beam_type == "Doubly - Single Layer Tension & Compression":
    As_t = st.sidebar.number_input("Tension Reinforcement, As_t (in²)", value=3.0)
    As_c = st.sidebar.number_input("Compression Reinforcement, As_c (in²)", value=1.0)
    d_prime = 2.5  # Single layer compression steel
    Mn, epsilon_t, phi, Mn_red, c, Cc, Cs, T = doubly_reinforced_beam(b, h, fc, fy, As_t, As_c, d_prime)

elif beam_type == "Doubly - Double Layer Tension & Compression":
    As_t = st.sidebar.number_input("Total Tension Reinforcement, As_t (in²)", value=3.0)
    As_c = st.sidebar.number_input("Total Compression Reinforcement, As_c (in²)", value=3.0)
    d_prime = 3.5  # Double layer compression steel
    Mn, epsilon_t, phi, Mn_red, c, Cc, Cs, T = doubly_reinforced_beam(b, h, fc, fy, As_t, As_c, d_prime)

# Display Results
st.subheader("Results")
st.write(f"**Compression block depth (a):** {round(a, 2)} in")
st.write(f"**Neutral Axis Depth (c):** {round(c, 2)} in")
st.write(f"**Nominal Moment (Mn):** {round(Mn, 2)} kip-ft")
st.write(f"**Net Tensile Strain (εt):** {round(epsilon_t, 5)}")
st.write(f"**Strength Reduction Factor (φ):** {round(phi, 2)}")
st.write(f"**Reduced Nominal Moment (φMn):** {round(Mn_red, 2)} kip-ft")

# Visualization: Force and Strain Diagram
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Strain Diagram
depths = [0, c, h]  # Positions (top, neutral axis, bottom)
strains = [0, 0.003, epsilon_t]  # Corresponding strains
ax[1].plot(strains, depths, marker='o', color='black', linestyle='-')
ax[1].invert_yaxis()
ax[1].set_xlabel("Strain")
ax[1].set_ylabel("Beam Depth (in)")
ax[1].set_title("Strain Distribution")
ax[1].grid()

st.pyplot(fig)
