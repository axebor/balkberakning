import streamlit as st

st.set_page_config(page_title="Balkdimensionering", layout="centered")
st.title("Dimensionering av tvåstödsbalk i stål")

# Profildata (förenklat urval – utbyggbar)
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

staldata = {"S235": 235, "S275": 275, "S355": 355}  # MPa

# --- INDATA ---
st.header("1. Indata")

col1, col2 = st.columns(2)
with col1:
    profiltyp = st.selectbox("Profiltyp", list(profiler.keys()))
    dimension = st.selectbox("Dimension", list(profiler[profiltyp].keys()))
with col2:
    stal = st.selectbox("Stålkvalitet", list(staldata.keys()))
    L = st.number_input("Spännvidd L (meter)", min_value=0.5, value=5.0)

# Last
st.subheader("Laster")
q = st.number_input("Linjelast q (kN/m)", value=10.0)
F = st.number_input("Punktlast F (kN)", value=20.0)
a = st.number_input("Avstånd till punktlastens placering (meter)", value=L/2, min_value=0.0, max_value=L)

# Tillåten nedböjning
tillaten_nedbojning = L / 300

# --- MATERIAL & TVÄRSNITT ---
f_y = staldata[stal] * 1e6  # MPa till Pa
E = 210e9  # Pa
gamma_M = 1.0

W_mm3 = profiler[profiltyp][dimension]["W"]
I_mm4 = profiler[profiltyp][dimension]["I"]
W = W_mm3 * 1e-9  # m3
I = I_mm4 * 1e-12  # m4

# --- BERÄKNINGAR ---

# Moment
Mq = (q * 1e3) * L**2 / 8
Mf = (F * 1e3) * a * (L - a) / L
Mmax = Mq + Mf

# Spänning
sigma = Mmax / W
sigma_MPa = sigma / 1e6
sigma_grans = f_y / gamma_M / 1e6

# Nedböjning
fq = (5 * q * 1e3 * L**4) / (384 * E * I)
ff = (F * 1e3 * a * (L**3 - a**2 * (3*L - a))) / (6 * E * L)
ftotal = fq + ff

# --- RESULTAT ---
st.header("2. Resultat")

st.subheader("Böjmoment")
st.latex(r"M_q = \frac{q \cdot L^2}{8}")
st.latex(r"M_F = \frac{F \cdot a \cdot (L - a)}{L}")
st.write(f"Moment från linjelast: **{Mq/1e3:.2f} kNm**")
st.write(f"Moment från punktlast: **{Mf/1e3:.2f} kNm**")
st.write(f"Totalt moment: **{Mmax/1e3:.2f} kNm**")

st.subheader("Böjspänning")
st.latex(r"\sigma = \frac{M}{W}")
st.write(f"Böjspänning: **{sigma_MPa:.2f} MPa**")
st.write(f"Tillåten spänning: **{sigma_grans:.0f} MPa**")

if sigma_MPa <= sigma_grans:
    st.success("✔️ Bärförmågan klarar lasten.")
else:
    st.error("❌ Bärförmågan överskrids.")

st.subheader("Nedböjning")
st.latex(r"f_q = \frac{5qL^4}{384EI} \quad,\quad f_F = \frac{F a (L^3 - a^2(3L - a))}{6EL}")
st.write(f"Nedböjning från linjelast: **{fq*1000:.2f} mm**")
st.write(f"Nedböjning från punktlast: **{ff*1000:.2f} mm**")
st.write(f"Total nedböjning: **{ftotal*1000:.2f} mm**")
st.write(f"Tillåten nedböjning (L/300): **{tillaten_nedbojning*1000:.2f} mm**")

if ftotal <= tillaten_nedbojning:
    st.success("✔️ Nedböjningskravet är uppfyllt.")
else:
    st.error("❌ Nedböjningen är för stor.")

# Avslutning
st.markdown("---")
st.caption("Utökad version – fler profiler och funktioner kan läggas till!")
