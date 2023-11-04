import speech_recognition as sr
import os
import openai
from dotenv import load_dotenv

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


load_dotenv()
openai.api_key = os.getenv('GPT')

completion = openai.ChatCompletion.create(
    model ="gpt-3.5-turbo",
    message=[{"role": "user", "content": (text)}]
)

print(completion.choices[0].message)

