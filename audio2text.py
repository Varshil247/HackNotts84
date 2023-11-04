import speech_recognition as sr
import os
import openai
from dotenv import load_dotenv
import requests
import pygame
from io import BytesIO

recognizer = sr.Recognizer()

''' recording the sound '''

try:
    with sr.Microphone() as source:
        print("Adjusting noise ")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Recording ")
        recorded_audio = recognizer.listen(source)
        # print("Done recording")

        print("Recognizing the text")
        text = recognizer.recognize_google(
                recorded_audio, 
                language="en-US"
            )
        print("Decoded Text : {}".format(text))

except sr.UnknownValueError:
    print("unknown error occurred")