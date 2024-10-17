import openai
import os
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import random
from dotenv import load_dotenv
import threading

# Carregar a chave da API da OpenAI do arquivo .env
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def reconhecer_fala():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Gessilene está ouvindo... pode falar!")
        audio = recognizer.listen(source)

    try:
        texto = recognizer.recognize_google(audio, language='pt-BR')
        print("Você disse:", texto)
        return texto
    except sr.UnknownValueError:
        print("Não entendi o que você disse.")
        return ""
    except sr.RequestError as e:
        print(f"Erro no serviço de reconhecimento de fala; {e}")
        return ""

def obter_resposta_openai(texto):
    messages = [
        {"role": "system", "content": "Você é Gessilene, uma assistente virtual criada por Leomar. Você fala de forma casual e descontraída, e às vezes usa gírias ou palavrões. Nem sempre me respeita muito, mas gosta de mim. Já ouviu falar sobre conchas e acha que elas não existem"},
        {"role": "user", "content": texto}
    ]
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.9
    )
    return response.choices[0].message.content.strip()

def falar_com_pyttsx3(texto):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voz_feminina = next((voice for voice in voices if "female" in voice.name.lower() or "feminina" in voice.name.lower()), None)
    if voz_feminina:
        engine.setProperty('voice', voz_feminina.id)
    engine.setProperty('rate', 150)
    engine.say(texto)
    engine.runAndWait()

def falar_com_gtts(texto):
    tts = gTTS(text=texto, lang='pt', slow=False)
    tts.save("resposta.mp3")
    resposta_audio = AudioSegment.from_mp3("resposta.mp3")
    play(resposta_audio)

def texto_para_voz(texto):
    falar_com_pyttsx3(texto)

def chatbot_de_voz():
    print("Gessilene está ativa! Para encerrar, use Ctrl + C.")
    while True:
        texto_usuario = reconhecer_fala()
        if texto_usuario:
            resposta = obter_resposta_openai(texto_usuario)
            print("Gessilene:", resposta)
            texto_para_voz(resposta)

# Iniciar Gessilene
chatbot_de_voz()
