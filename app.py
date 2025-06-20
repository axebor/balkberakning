st.cache_data.clear()
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.set_page_config(page_title="Gravitationsfundament", layout="wide")

# CSS för lika breda inputfält
st.markdown(
    """
    <style>
    div[data-testid="stTextInput"] > div > input {
        max-width: 120px;
        width: 100%;
        box-sizing: border-box;
    }
    div[data-testid="stTextInput"][data-key="z_niva"] > div > input {
        max-width: 150px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Alla kolumner lika breda
col_in, col_out, col_res = st.columns([1, 1, 1])

with col_in:
    st.header("Indata")
    st.subheader("Geometri")

    st.markdown("**Bottenplatta**")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        D_b_str = st.text_input("Diameter Dₐ (m)", value="5.0")
    with col_b2:
        h_b_str = st.text_input("Höjd hₐ (m)", value="1.0")

    st.markdown("**Skaft (centrerat ovanpå)**")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        D_s_str = st.text_input("Diameter Dₛ (m)", value="1.0")
    with col_s2:
        h_s_str = st.text_input("Höjd hₛ (m)", value="2.0")

    fundament_i_vatten = st.checkbox("Fundament delvis i vatten", value=False)

    if fundament_i_vatten:
        z_niva_str = st.text_input("Z_v (m) från underkant fundament", value="0.0", key="z_niva")
    else:
        z_niva_str = None

    st.subheader("Laster")
    F_str = st.text_input("Horisontell punktlast F (kN)", value="0.0")
    zF_str = st.text_input("Lastens angripspunkt z_F (m)", value="0.0")

    # Konvertera till float med avrundning till 1 decimal
    try:
        D_b = round(float(D_b_str), 1)
        h_b = round(float(h_b_str), 1)
        D_s = round(float(D_s_str), 1)
        h_s = round(float(h_s_str), 1)
        if fundament_i_vatten:
            z_niva = float(z_niva_str)
        else:
            z_niva = None
        F = float(F_str)
        zF = float(zF_str)
    except ValueError:
        st.error("❌ Ange giltiga numeriska värden för geometri, vattennivå och laster.")
        st.stop()

with col_out:
    st.header("Figur")

    fig, ax = plt.subplots(figsize=(6, 6))

    if fundament_i_vatten and z_niva is not None and z_niva > 0:
        ax.fill_between(
            x=[-max(D_b, D_s) - 1, max(D_b, D_s) + 1],
            y1=0, y2=z_niva, color='lightblue', alpha=0.5)
        ax.hlines(y=z_niva, xmin=-max(D_b, D_s) - 1, xmax=max(D_b, D_s) + 1,
                  colors='blue', linestyles='--', linewidth=2, label='Vattenlinje')

    # Bottenplatta
    ax.plot([-D_b/2, D_b/2], [0, 0], 'k-')
    ax.plot([-D_b/2, -D_b/2], [0, h_b], 'k-')
    ax.plot([D_b/2, D_b/2], [0, h_b], 'k-')
    ax.plot([-D_b/2, D_b/2], [h_b, h_b], 'k-')

    # Skaft
    ax.plot([-D_s/2, D_s/2], [h_b, h_b], 'k-')
    ax.plot([-D_s/2, -D_s/2], [h_b, h_b + h_s], 'k-')
    ax.plot([D_s/2, D_s/2], [h_b, h_b + h_s], 'k-')
    ax.plot([-D_s/2, D_s/2], [h_b + h_s, h_b + h_s], 'k-')

    # Måttpilar och etiketter - diametrar
    ax.annotate("", xy=(D_b/2, -0.5), xytext=(-D_b/2, -0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0, -0.7, r"$D_b$", ha='center', va='top', fontsize=12)

    ax.annotate("", xy=(D_s/2, h_b + h_s + 0.5), xytext=(-D_s/2, h_b + h_s + 0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0, h_b + h_s + 0.7, r"$D_s$", ha='center', va='bottom', fontsize=12)

    # Måttpilar och etiketter - höjder
    ax.annotate("", xy=(D_b/2 + 0.5, 0), xytext=(D_b/2 + 0.5, h_b),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_b/2 + 0.6, h_b/2, r"$h_b$", va='center', fontsize=12)

    ax.annotate("", xy=(D_s/2 + 0.5, h_b), xytext=(D_s/2 + 0.5, h_b + h_s),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_s/2 + 0.6, h_b + h_s/2, r"$h_s$", va='center', fontsize=12)

    # Måttpil och beteckning för Zv
    if fundament_i_vatten and z_niva is not None and z_niva > 0:
        ax.annotate("", xy=(max(D_b, D_s)/2 + 0.5, 0), xytext=(max(D_b, D_s)/2 + 0.5, z_niva),
                    arrowprops=dict(arrowstyle="<->"))
        ax.text(max(D_b, D_s)/2 + 0.7, z_niva/2, r"$Z_v$", va='center', fontsize=12)

    # Punktlast pil och beteckning
    if F != 0:
        ax.annotate(
            '', xy=(max(D_b, D_s)/2 + 0.5, zF), xytext=(max(D_b, D_s)/2 + 2, zF),
            arrowprops=dict(facecolor='red', shrink=0.05, width=3, headwidth=10)
        )
        ax.vlines(x=ma
