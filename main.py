import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from PIL import Image
from calcul_emprunt import calcul_emprunt
st.title("Calculateur d'emprunt")
image = Image.open("attijari_logo.png")

st.image(image, caption='Attijariwafa Bank', width=200)

profil = st.selectbox("Profil", ["ECHCONST", "LINEAIRE", "INFINE"])
capital = st.number_input("Capital", min_value=0.0, value=1000.0, step=100.0)
taux_interet = st.number_input("Taux d'intérêt (%)", min_value=0.0, value=5.0, step=0.5)
date_maturite = st.date_input("Date de maturité")
value_date = st.date_input("Value date")
periodicite = st.selectbox("Périodicité", ["annuel", "semestriel", "trimestriel", "mensuel"])

if st.button("Calculer"):
    duree, msg_tci, msg_tsr, df_amortissement = calcul_emprunt(
        profil, capital, taux_interet, date_maturite, value_date, periodicite
    )
    st.write(duree)
    st.write(msg_tci)
    st.write(msg_tsr)
    st.write("Tableau d'amortissement :")
    st.write(df_amortissement)
