import streamlit as st
import pandas as pd

def home():
    st.title("🌟 Selamat Datang di Dashboard TANGGUH 🌟")
    st.markdown(" #### Ini adalah dashboard demonstrasi dari situs web TANGGUH, yang dirancang untuk mempublikasikan hasil dari model prediksi stunting dan interaksi dengan chatbot TANGGUH.")
    st.image("assets/tangguh.png", width=300)
    st.markdown("## Menu Dashboard")
    st.write("Silakan pilih menu dari panel di samping untuk mengakses model prediksi stunting dan interaksi chatbot.")

    st.markdown("## Anggota Tim")
    data_tim = pd.DataFrame({
        "Nama": ["Akmal Muzakki Bakir", "Namira Salsabilla", "Dominica Febriyanti"],
        "NIM": ["1305210087", "1305210091", "1305213010"]
    })
    st.table(data_tim.style.set_properties(**{'text-align': 'center'}))

    st.markdown("## Catatan")
    st.write("Dasbor ini masih dalam pengembangan dan demo. Versi lebih baik akan segera menyusul. Tetap pantau!")
