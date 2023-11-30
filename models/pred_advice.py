import pandas as pd
import streamlit as st
import pickle
from secret.getApi import palm_api_key, gpt4_api_key
from models.chatbot.palm import palm_generate_text
from models.chatbot.gpt4 import gpt4_generate_text
from helper.translator import translate

def predict_prompt(sex, age, birth_weight, birth_length, body_weight, body_length, asi):
    with open('model.pkl', 'rb') as file:
        data = pickle.load(file)
        
    tabel = pd.DataFrame({
        'Sex':[sex],
        'Age':[age],
        'Birth Weight':[birth_weight],
        'Birth Length':[birth_length],
        'Body Weight':[body_weight],
        'Body Length':[body_length],
        'ASI Eksklusif':[asi],
    })
        
    tabel_real = pd.DataFrame({
        'Sex':[sex],
        'ASI Eksklusif':[asi]
    })

    st.divider()

    tabel['Sex'] = data['SexEncoder'].transform(tabel['Sex'])
    tabel['ASI Eksklusif'] = data['AsiEncoder'].transform(tabel['ASI Eksklusif'])

    num_sex = tabel_real['Sex'].values[0]
    num_asi = tabel_real['ASI Eksklusif'].values[0]
    num_age = tabel['Age'].values[0]
    num_birth_weight = tabel['Birth Weight'].values[0]
    num_birth_length = tabel['Birth Length'].values[0]
    num_body_weight = tabel['Body Weight'].values[0]
    num_body_length = tabel['Body Length'].values[0] 
    
    stunting_pred_prob = data['model'].predict_proba(tabel)

    result = ""
    if data['model'].predict(tabel)[0] == 0:
        result = "no indication of stunting"
    else:
        result = "indicated stunting"
    
    prompt_template = f"""
        A nurse has conducted an examination on a baby to determine if there are any indications of stunting. 
        The following data has been collected:
        - Gender: {num_sex}
        - Age: {num_age} months
        - Birth weight: {num_birth_weight} kg
        - Birth length: {num_birth_length} cm
        - Current body weight: {num_body_weight} kg
        - Current body length: {num_body_length} cm
        - Exclusive breastfeeding: {num_asi}

        After analyzing the data, it has been determined that the baby is {result}. 

        If the baby is indeed indicated to be stunted, the AI should provide a comprehensive explanation to the baby's parents about the condition. 
        It should also suggest preventive measures that can be taken and advice tailored to the baby's specific parameters. 
        Additionally, the AI should provide links to relevant articles for further reading on this issue.
    """

    return stunting_pred_prob, result, prompt_template

def models(model, prompt_template):
    if model == "Palm":
        response = palm_generate_text(prompt_template, palm_api_key())
    else:
        # response = gpt4_chatbot(prompt_template, gpt4_api_key())
        response = gpt4_generate_text(prompt_template, gpt4_api_key())
        
    return response

def pred_advice():
    st.markdown("## 🍼 Prediksi Stunting pada Bayi Disertai Dengan Saran")
    
    st.divider()
    # with open('model.pkl', 'rb') as file:
    #     data = pickle.load(file)
    
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

    SEX = ['Laki-laki', 'Perempuan']
    ASI = ['Ya, mendapatkan 😁', 'Tidak 😢']

    asi = st.selectbox("Apakah bayi mendapatkan ASI eksklusif?", ASI)        
    col1, col2 = st.columns(2)

        
    with col1:
        sex = st.selectbox("Pilih gender", SEX)
        age = st.number_input("Masukkan umur bayi dalam bulan", min_value=1, max_value=59)
        birth_weight = st.number_input("Masukkan berat badan saat lahir dalam kilogram", min_value=1.8, max_value=4.0)
        
    with col2:
        birth_length = st.number_input("Masukkan panjang badan saat lahir dalam centimeter", min_value=42.0, max_value=52.0)
        body_weight = st.number_input("Masukkan berat badan bayi dalam kilogram", min_value=2.9, max_value=24.5)
        body_length = st.number_input("Masukkan panjang badan bayi dalam centimeter", min_value=53.0, max_value=111.0)

    stunting_pred_prob, hasil, prompt_template = predict_prompt(
        sex="F" if sex == "Perempuan" else "M",
        age=age,
        birth_weight=birth_weight,
        birth_length=birth_length,
        body_weight=body_weight,
        body_length=body_length,
        asi="Yes" if asi == "Ya, mendapatkan 😁" else "No"
        # data=data
    )
    
    with col1:
        prediksi = st.button("🔎 Lakukan prediksi dan pencarian")
        
    with col2:
        clear = st.button("🗑️ Bersihkan output")
    
    if prediksi:
        with st.spinner('⏳ Tunggu sebentar ya...'):            
            
            response = models(model, prompt_template)
            
            if hasil == "indicated stunting":
                st.write(f"Maaf 😖, terdapat indikasi bahwa anak Anda mengalami stunting 😔. Persentase stunting anak Anda diperkirakan sebesar {round(stunting_pred_prob[0][1]*100, 2)}%.")
            else:
                st.write(f"Selamat! 😊 Tidak terdapat indikasi stunting pada anak Anda 🤗. Persentase stunting anak Anda diperkirakan sebesar {round(stunting_pred_prob[0][1]*100, 2)}%.")
            
            st.write(response)
        
        st.divider()

        st.markdown("### **Rekomendasi pertanyaan berdasarkan jawaban hasil prediksi**")
        with st.spinner('⏳ Tunggu sebentar ya...'):
            question_response(translate("id", "en", response), model)
                
    if clear:
        st.empty()
                
                
def question_response(prompt, model):
    question_recom_prompt = f"""
        Based on the topic '{prompt}', 
        generate three questions related to health and nutrition issues. 
        Each question should be concise and directly related to the topic. 
        The questions are:
        1. ..., (enter)
        2. ..., (enter)
        3. ...,
    """
        
    question_recom_response = models(model, question_recom_prompt)
    
    questions = question_recom_response.split("\n")
    for question in questions:
        with st.expander(f"{question}"):
            answer = models(model, translate("id", "en", question))
            st.write(answer)