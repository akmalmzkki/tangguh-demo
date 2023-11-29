import streamlit as st
from models.pred_advice import pred_advice
from models.relate_chatbot import relate_chatbot
from homepage.email import send_mail
from homepage.home import home

def main():
    st.set_page_config(page_title="Stunting Dashboard TANGGUH", layout="wide")
    st.sidebar.image("assets/tangguh.png", use_column_width=True)
    st.sidebar.divider()
    # st.sidebar.title("📌 Menu")
    
    menu_options = {
        # "Homepage": home,
        "Interaksi dengan TANGGUH": relate_chatbot,
        "Prediksi Stunting dengan TANGGUH": pred_advice,
        "Kritik dan Saran untuk TANGGUH": send_mail,
    }
    
    st.sidebar.info("Pilih opsi dari menu dibawah untuk melanjutkan ⬇️")
    menu_choice = st.sidebar.radio("Pilih menu", list(menu_options.keys()))
    
    st.sidebar.markdown("---")
    
    menu_options[menu_choice]()
        
if __name__ == "__main__":
    main()
