import streamlit as st

st.title("Dimensionering av tvåstödsbalk i stål")

# Profildata (förenklat urval)
profiler = {
    "IPE": {
        "100": {"W": 45.6e3, "I": 64.4e6},  # mm3, mm4
        "160": {"W": 106e3, "I": 170e6},
        "200": {"W": 203e3, "I": 407e6},
    },
    "HEA": {
        "100": {"W": 53.5e3, "I": 42.1e6},
        "160": {"W": 125e3, "I": 100e6},
        "200": {"W": 229e3, "I": 229e6},
    },
    "HEB": {
        "100": {"W": 63.4e3, "I": 50.8e6},
        "160": {"W": 149e3, "I": 119e6},
        "200": {"W": 263e3, "I": 263e6},
    },
}

# Användarval
profiltyp = st.selectbox("Profiltyp", list(profiler.keys()))
dimension = st.selectbox("Dimension", list(profiler[profiltyp].keys()))
stal = st.selectbox("Stålkvalitet", ["S235", "S275", "S355"])

# Materialdata
staldata = {"S235": 235, "S275": 275, "S355": 355}
f_y = staldata[stal] * 1e6  # MPa till Pa

# Laster och geometri
L = st.number_input("Spännvidd L (meter)", min_value=0.5, value=5.0)
lasttyp = st.radio("Lasttyp", ["Linjelast", "Punktlast"])
if lasttyp == "Linjelast":
    q = st.number_input("Linjelast q (kN/m)", value=10.0)
    q_Nm = q * 1e3  # kN/m till N/m
else:
    F = st.number_input("Punktlast F (kN)", value=20.0)
    a = st.number_input("Avstånd till punktlastens placering (meter)", value=L/2)
    F_N = F * 1e3  # kN till N

# Visa val
st.subheader("Valda parametrar")
st.write(f"Profil: {profiltyp} {dimension}")
st.write(f"Stålkvalitet: {stal} (f<sub>y</sub> = {f_y/1e6:.0f} MPa)", unsafe_allow_html=True)
st.write(f"Spännvidd: {L:.2f} m")

if lasttyp == "Linjelast":
    st.write(f"Linjelast: {q:.2f} kN/m")
else:
    st.write(f"Punktlast: {F:.2f} kN vid {a:.2f} m från vänstra stöd")

# Visa tvärsnittsegenskaper
W = profiler[profiltyp][dimension]["W"]  # mm3
I = profiler[profiltyp][dimension]["I"]  # mm4
st.write(f"W (böjmotstånd): {W:.0f} mm³")
st.write(f"I (tröghetsmoment): {I:.0f} mm⁴")
