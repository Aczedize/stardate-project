import time
from gtts import gTTS
import pygame
import os

# Função para formatar o stardate
def format_stardate(stardate):
    if stardate >= 10000:
        stardate = stardate % 10000
    return f"{stardate:06.1f}"

# Função para formatar o shipboard time
def format_shipboard_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02}:{minutes:02}:{secs:02}"

# Função para converter texto em áudio e tocar
def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("stardate.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("stardate.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    pygame.mixer.music.unload()
    pygame.mixer.quit()
    time.sleep(1)  # Pequeno atraso para garantir que o arquivo não esteja mais em uso
    os.remove("stardate.mp3")

# Função para formatar o stardate como string para fala
def stardate_to_speech(stardate):
    parts = format_stardate(stardate).split('.')
    return f"{parts[0]} point {parts[1]}"

# Inicialização das variáveis
stardate = 0.0
shipboard_seconds = 0

# Loop do cronômetro
while True:
    # Formatar e imprimir o stardate e shipboard time
    formatted_stardate = format_stardate(stardate)
    formatted_shipboard_time = format_shipboard_time(shipboard_seconds)
    print(f"Stardate {formatted_stardate}, Shipboard {formatted_shipboard_time}")

    # A cada 10 segundos, falar o stardate e shipboard time
    if shipboard_seconds % 10 == 0:
        # Garantir que o stardate esteja sempre no formato "0000.0"
        stardate_text = f"Stardate {stardate_to_speech(stardate)}"
        
        # Formatar shipboard time
        if shipboard_seconds < 60:
            shipboard_text = f"Shipboard {shipboard_seconds} seconds"
        elif shipboard_seconds < 3600:
            minutes = shipboard_seconds // 60
            seconds = shipboard_seconds % 60
            shipboard_text = f"Shipboard {minutes} minutes and {seconds} seconds"
        else:
            hours = shipboard_seconds // 3600
            minutes = (shipboard_seconds % 3600) // 60
            seconds = shipboard_seconds % 60
            shipboard_text = f"Shipboard {hours} hours, {minutes} minutes and {seconds} seconds"

        text = f"{stardate_text}, {shipboard_text}"
        speak(text)
    
    # Aguardar 1 segundo
    time.sleep(1)

    # Atualizar stardate e shipboard time
    stardate += 0.1
    shipboard_seconds += 1

    # Reset do stardate se necessário
    if stardate >= 10000:
        stardate = 0.0
