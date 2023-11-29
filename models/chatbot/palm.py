import google.generativeai as palm
from helper.translator import translate

def palm_generate_text(prompt, api_key):
    palm.configure(api_key=api_key)
    completion = palm.generate_text(prompt=prompt)
    if completion.result:
        response = translate("en", "id", completion.result)
    else:
        response = "Maaf, saya tidak mengerti maksud Anda. Silakan tanyakan pertanyaan lain."
    return response

def palm_chatbot(prompt, api_key):
    palm.configure(api_key=api_key)
    reply = palm.chat(messages=prompt)
    if reply.last:
        response = translate("en", "id", reply.last)
    else:
        response = "Maaf, saya tidak mengerti maksud Anda. Silakan tanyakan pertanyaan lain."
        
    return response