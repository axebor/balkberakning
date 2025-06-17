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
    div[data-testid="stTextInput"][data-key="z_niva"] > div > input,
    div[data-testid="stTextInput"][data-key="z_F"] > div > input {
        max-width: 150px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
        z_niva_str = st.text_input(r"$Z_{v}$ (m) från underkant fundament", value="0.0", key="z_niva")
    else:
        z_niva_str = None

    st.subheader("Laster")
    col_F1, col_F2 = st.columns(2)
    with col_F1:
        F_str = st.text_input(r"Horisontell punktlast $F$ (kN)", value="0.0", key="F")
    with col_F2:
        z_F_str = st.text_input(r"Lastnivå $z_{F}$ (m) från underkant bottenplatta", value="0.0", key="z_F")

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
        z_F = float(z_F_str)
    except ValueError:
        st.error("❌ Ange giltiga numeriska värden för indata.")
        st.stop()

with col_out:
    st.header("Figur")

    fig, ax = plt.subplots(figsize=(6, 6))

    max_diameter = max(D_b, D_s)

    # Vattenlinje och vattenfärg om relevant
    if fundament_i_vatten and z_niva is not None and z_niva > 0:
        ax.fill_between(
            x=[-max_diameter - 1, max_diameter + 1],
            y1=0, y2=z_niva, color='lightblue', alpha=0.5)
        ax.hlines(y=z_niva, xmin=-max_diameter - 1, xmax=max_diameter + 1,
                  colors='blue', linestyles='--', linewidth=2)

        # Måttpil och etikett för Zv
        ax.annotate("", xy=(max_diameter + 0.5, 0), xytext=(max_diameter + 0.5, z_niva),
                    arrowprops=dict(arrowstyle="<->", color='blue'))
        ax.text(max_diameter + 0.7, z_niva / 2, r"$Z_{v}$", va='center', fontsize=12, color='blue')

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

    # Punktstreckad centrumlinje
    ax.vlines(x=0, ymin=0, ymax=h_b + h_s + 1, colors='gray', linestyles='dotted', linewidth=1)

    # Horisontell pil för punktlast F på nivå z_F
    if F != 0 and 0 <= z_F <= h_b + h_s:
        arrow_len = max_diameter / 2
        ax.annotate("",
                    xy=(0, z_F), xytext=(-arrow_len, z_F),
                    arrowprops=dict(arrowstyle="->", color='red', lw=2))
        ax.text(-arrow_len - 0.2, z_F, r"$F$", color='red', fontsize=14, va='center')

    ax.set_xlim(-max_diameter - 1, max_diameter + 1.5)
    ax.set_ylim(-1, max(h_b + h_s, z_niva if z_niva else 0, z_F) + 1)
    ax.set_aspect('equal')
    ax.axis('off')

    st.pyplot(fig)

with col_res:
    st.header("Resultat")

    pi = np.pi

    # Volymer
    vol_bottenplatta = pi * (D_b / 2) ** 2 * h_b
    vol_skaft = pi * (D_s / 2) ** 2 * h_s

    # Volymer under vatten och ovan vatten
    if fundament_i_vatten and z_niva is not None and z_niva > 0:
        under_vatten_botten = max(0, min(z_niva, h_b)) * pi * (D_b / 2) ** 2
        ovan_vatten_botten = vol_bottenplatta - under_vatten_botten

        under_vatten_skaft = max(0, min(z_niva - h_b, h_s)) * pi * (D_s / 2) ** 2
        ovan_vatten_skaft = vol_skaft - under_vatten_skaft
    else:
        under_vatten_botten = 0
        ovan_vatten_botten = vol_bottenplatta
        under_vatten_skaft = 0
        ovan_vatten_skaft = vol_skaft

    # Vikter (kN)
    vikt_ovan = (ovan_vatten_botten + ovan_vatten_skaft) * 25
    vikt_under = (under_vatten_botten + under_vatten_skaft) * 15
    vikt_tot = vikt_ovan + vikt_under

    # Underrubrik Volym
    st.markdown("### Volym")

    # Tabell med volymer (avrundat till 1 decimal)
    df_volymer = pd.DataFrame({
        "Över vatten (m³)": [round(ovan_vatten_botten, 1), round(ovan_vatten_skaft, 1)],
        "Under vatten (m³)": [round(under_vatten_botten, 1), round(under_vatten_skaft, 1)]
    }, index=["Bottenplatta", "Skaft"])
    st.table(df_volymer)

    # Underrubrik Egenvikt
    st.markdown("### Egenvikt")

    # Tabell med vikter (avrundat till 1 decimal)
    df_vikter = pd.DataFrame({
        "Vikt (kN)": [round(vikt_ovan, 1), round(vikt_under, 1), round(vikt_tot, 1)]
    }, index=["Över vatten", "Under vatten", "Total egenvikt (Gk, fund)"])
    st.table(df_vikter)
