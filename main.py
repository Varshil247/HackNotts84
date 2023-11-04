import speech_recognition as sr
import os
import openai
from dotenv import load_dotenv
import requests
import pygame
from io import BytesIO

recognizer = sr.Recognizer()

''' recording the sound '''

with sr.Microphone() as source:
    print("Adjusting noise ")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    print("Recording for 4 seconds")
    recorded_audio = recognizer.listen(source, timeout=4)
    print("Done recording")

''' Recorgnizing the Audio '''
try:
    print("Recognizing the text")
    text = recognizer.recognize_google(
            recorded_audio, 
            language="en-US"
        )
    print("Decoded Text : {}".format(text))

except Exception as ex:
    print(ex)

#-------------------------------ai chat gpt---------------------------------------------------------#
#load_dotenv()
#openai.api_key = os.getenv('GPT')

#completion = openai.ChatCompletion.create(
 #   model ="gpt-3.5-turbo",
  #  message=[{"role": "user", "content": (text)}]
#)

#print(completion.choices[0].message)

#-------------------------------speak-----------------------------------------------------------------#

url = "https://api.play.ht/api/v2/tts/stream"

payload = {
    "text": format(text),
    "voice": "s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json",
    "output_format": "mp3",
    "voice_engine": "PlayHT2.0-turbo"
}
headers = {
    #"accept": "text/event-stream",
    "accept": "audio/mpeg",
    "content-type": "application/json",
    "AUTHORIZATION": "22cf5809f001411e808c64bb6f8b5bec",
    "X-USER-ID": "8R48EcHJo3MMHiwT0F6Kp0ULVxq2"
}

requests.head("https://api.play.ht/api/v2/tts")

pygame.mixer.init()
response = requests.post(url, json=payload, headers=headers )

if response.status_code == 200:
    # Convert the response content to a bytes stream
    audio_data = BytesIO(response.content)

    # Load the audio data into Pygame mixer
    pygame.mixer.music.load(audio_data)

    # Play the audio
    pygame.mixer.music.play()

    # Wait for the audio to finish (you can add other logic here)
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

else:
    print('Failed to retrieve the audio file.')