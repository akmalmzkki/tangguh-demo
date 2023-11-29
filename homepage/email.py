import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st
from streamlit.components.v1 import html
# from secret.pwApp import get_pw

def send_email(sender, password, receiver, subject, message):
    email_obj = MIMEMultipart()
    email_obj['From'] = sender
    email_obj['To'] = receiver
    email_obj['Subject'] = subject

    email_obj.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, email_obj.as_string())
    server.quit()

def send_mail():
    st.markdown('## 📩 Ada kritik dan saran terhadap TANGGUH?')
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        sender = st.text_input('Masukkan email Anda') 
    password = st.text_input('Masukkan password email Anda (harus menggunakan password aplikasi)', type='password')
    receiver = "tangguhinnovillage@gmail.com"
    
    with col2:
        subject = st.text_input('Masukkan subjek kritik dan saran') 
    message = st.text_area('Masukkan kritik dan saran')
    
    if st.button('📤 Kirim Pesan'): 
        error = st.empty() 
        if not sender or not password or not subject or not message: 
            error.error('Harap isi semua data email Anda') 
        elif not '@' in sender or not '.' in sender:
            error.error('Harap masukkan email yang valid') 
        else:
            error.empty() 
            with st.spinner('Sedang mengirim email...'): 
                try:
                    send_email(sender, password, receiver, subject, message)
                    st.success('✅ Email berhasil dikirim ke tangguhinnovillage@gmail.com') 
                except Exception as e:
                    st.error(f'❌ Email gagal dikirim. Error: {e}') 
