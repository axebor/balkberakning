import streamlit as st

st.title("Dimensionering av tvåstödsbalk i stål")

# Profildata (förenklat urval)
profiler = {
    "IPE": {
        "100": {"W": 45.6e3, "I": 64.4e6},
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

# Materialdata
staldata = {"S235": 235, "S275": 275, "S355": 355}

# Användarval
profiltyp = st.selectbox("Profiltyp", list(profiler.keys()))
dimension = st.selectbox("Dimension", list(profiler[profiltyp].keys()))
stal = st.selectbox("Stålkvalitet", list(staldata.keys()))
f_y = staldata[stal] * 1e6  # MPa till Pa

L = st.number_input("Spännvidd L (meter)", min_value=0.5, value=5.0)

# Laster
q = st.number_input("Linjelast q (kN/m)", value=10.0)
F = st.number_input("Punktlast F (kN)", value=20.0)
a = st.number_input("Avstånd till punktlast F från vänstra stöd (meter)", value=L/2)

# Tvärsnittsegenskaper
W_mm3 = profiler[profiltyp][dimension]["W"]
I_mm4 = profiler[profiltyp][dimension]["I"]

# Omräkning
W = W_mm3 * 1e-9  # mm3 till m3
I = I_mm4 * 1e-12  # mm4 till m4
E = 210e9  # Pa (för stål)
gamma_M = 1.0  # Säkerhetsfaktor

# Beräkningar
Mq = (q * 1e3) * L**2 / 8          # Nm
Mf = (F * 1e3) * a * (L - a) / L   # Nm
Mmax = Mq + Mf

sigma = Mmax / W                  # Pa
sigma_MPa = sigma / 1e6

sigma_grans = f_y / gamma_M / 1e6

# Nedböjning
fq = (5 * q * 1e3 * L**4) / (384 * E * I)   # m
ff = (F * 1e3 * a * (L**3 - a**2 * (3*L - a))) / (6 * E * L)  # m
ftotal = fq + ff

# Redovisning
st.subheader("Resultat")

st.markdown(f"**Maxmoment från linjelast:** {Mq/1e3:.2f} kNm")
st.markdown(f"**Maxmoment från punktlast:** {Mf/1e3:.2f} kNm")
st.markdown(f"**Totalt moment:** {Mmax/1e3:.2f} kNm")

st.markdown(f"**Böjspänning:** {sigma_MPa:.2f} MPa")
st.markdown(f"**Tillåten spänning:** {sigma_grans:.0f} MPa")

if sigma_MPa <= sigma_grans:
    st.success("Balken klarar böjspänningen.")
else:
    st.error("⚠️ Balken klarar INTE böjspänningen.")

st.markdown(f"**Nedböjning från linjelast:** {fq*1000:.2f} mm")
st.markdown(f"**Nedböjning från punktlast:** {ff*1000:.2f} mm")
st.markdown(f"**Total nedböjning:** {ftotal*1000:.2f} mm")

