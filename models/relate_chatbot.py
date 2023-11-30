import streamlit as st
from secret.getApi import palm_api_key, gpt4_api_key
from models.chatbot.palm import palm_chatbot
from models.chatbot.gpt4 import gpt4_chatbot
from helper.translator import translate

def relate_chatbot():
    st.markdown("## 💬 Tanya TANGGUH")
    st.divider()

    genAi1, genAi2 = st.columns(2)
    model = st.session_state.get("model", "Palm")
    
    if genAi1.button("🌴 PaLM"):
        model = "Palm"
        st.session_state.model = model
        st.success("🎉 Model PaLM telah aktif!")
    
    if genAi2.button("🧠 GPT-4"):
        model = "GPT-4"
        # st.session_state.model = model
        # st.success("Model GPT-4 telah aktif")
        st.session_state.model = "Palm"
        st.error("😞 Maaf, Model GPT-4 belum tersedia.")
        st.success("🔄 Anda akan dialihkan ke model PaLM.")
    
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Halo! Tanyakan TANGGUH tentang masalah gizi dan kesehatan anak."}
        ]

    if prompt := st.chat_input("🔍 Masukkan pertanyaan mu disini..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Tunggu sebentar ya..."):
                prompt_template = f"""
                    Context: 
                    Currently, you are named TANGGUH, a bot designed to answer questions about child nutrition and health issues. 
                    It is knowledgeable about various topics related to child health, including but not limited to, growth milestones, 
                    nutritional needs, common health problems in children, and measures to prevent stunting. 
                    It is also aware of the latest research and guidelines related to child health and nutrition.

                    Topic: 
                    The primary topic that TANGGUH deals with is child nutrition and health. 
                    It can provide information and answer queries about appropriate diet for different age groups, signs of nutritional deficiencies, 
                    vaccination schedules, tips for dealing with common illnesses, 
                    and advice on promoting healthy growth and development. 
                    It can also provide insights on preventing and dealing with stunting in children.

                    Restrict Command:
                    Remember, if TANGGUH is given a command outside the context of child nutrition and health issues, 
                    the app will reply "I'm sorry, TANGGUH cannot answer that question", 
                    along with the reason that TANGGUH will not be able to answer it and will direct the user to ask another question related to child nutrition and health. 
                    This is to ensure that the conversation stays within the intended scope.
                    
                    Question:
                    The command is: {translate("id", "en", prompt)}.
                """
                                    
                if model == "Palm":
                    response = palm_chatbot(translate("id", "en", prompt_template), palm_api_key())
                else:
                    response = gpt4_chatbot(translate("id", "en", prompt_template), gpt4_api_key())
                    
                st.write(response) 
                message = {"role": "assistant", "content": response}
                st.session_state.messages.append(message)

    clear = st.button("🗑️ Bersihkan chat", disabled=len(st.session_state.messages) <= 1)
        
    if clear:
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Halo! Tanyakan TANGGUH tentang masalah gizi dan kesehatan anak."}
        ]