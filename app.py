import streamlit as st

st.title("Balkberäkning")

st.write("Beräknar maxmoment för en balk med jämnt fördelad last.")

L = st.number_input("Spännvidd L (meter)", min_value=0.1, value=5.0)
q = st.number_input("Linjelast q (kN/m)", min_value=0.0, value=10.0)

M = q * L**2 / 8

st.write(f"Maxmoment: {M:.2f} kNm")
