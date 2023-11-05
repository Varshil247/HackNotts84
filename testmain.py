import speech_recognition as sr
import os
import openai
from dotenv import load_dotenv
import pyttsx3
import tkinter as tk
from tkinter import messagebox
import customtkinter
import threading
from PIL import Image, ImageTk

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to record and process audio input
def getAudio():
    threading.Thread(target=record_and_process_audio, daemon=True).start()

def record_and_process_audio():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            typeWriter("Adjusting noise... ", 1, inputlabel)
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            typeWriter("Recording... ", 1, inputlabel)
            recorded_audio = recognizer.listen(source)
            typeWriter("Recognizing the text... ", 1, inputlabel)
            text = recognizer.recognize_google(recorded_audio, language="en-US")
            typeWriter(f"User: {text}", 1, inputlabel)
            getGPTresp(text)
    except sr.UnknownValueError:
        typeWriter("Unknown error occurred", 1, inputlabel)
    except sr.RequestError as e:
        typeWriter(f"Could not request results; {e}", 1, inputlabel)

# Function to send user's query to OpenAI's GPT model
def getGPTresp(text):
    def generate_response():
        load_dotenv()
        typeWriter("The AI is thinking...", 1, outputlabel)
        openai.api_key = os.getenv('GPT')
        messages = [{"role": "user", "content": text + " in no more than 50 words, act like a human"}]
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            response_text = completion.choices[0].message['content']
            typeWriter(f"ChatAI: {response_text}", 1, outputlabel)
            makeAudio(response_text)
        except Exception as e:
            typeWriter(f"Error in getting response from GPT-3: {e}", 1, outputlabel)
    threading.Thread(target=generate_response, daemon=True).start()

# Function to use the TTS engine to play the response
def makeAudio(response_text):
    def audio():
        engine.say(response_text)
        engine.runAndWait()
    threading.Thread(target=audio, daemon=True).start()

# Function to display typed text in a typewriter effect
def typeWriter(text, counter, label):
    text = text.capitalize()
    label.configure(text=f"{text[:counter]}...")
    if counter < len(text):
        app.after(50, lambda: typeWriter(text, counter+1, label))

# Function to handle appearance mode change
def combobox_callback(choice):
    customtkinter.set_appearance_mode(choice)
    customtkinter.set_default_color_theme("green")

# Function to display information about the app
def show_info():
    info_text = ("ChatAI is a voice-enabled chat application that uses OpenAI's GPT-3 "
                 "for conversational AI. Speak into your microphone or type in your query, "
                 "and ChatAI will respond. This application showcases the capabilities "
                 "of speech recognition and AI-powered conversational interfaces.")
    messagebox.showinfo("About ChatAI", info_text)

# Creating the main application window
app = customtkinter.CTk()
app.title("ChatAI")
app.geometry("300x500")
app.resizable(False, False)

mainFrame = customtkinter.CTkFrame(app)
mainFrame.pack(expand=True, fill="both")

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

# Input Frame
inputFrame = customtkinter.CTkFrame(mainFrame)
inputFrame.pack(expand=True, fill="both", padx=10, pady=10)

# Appearance Mode Combobox
combobox = customtkinter.CTkComboBox(mainFrame, values=["Dark", "Light"], command=combobox_callback)
combobox.pack(expand=False, fill="both", padx=5, pady=5)

# User Label
inputlabel = customtkinter.CTkLabel(inputFrame, text="", anchor="n", wraplength=250)
inputlabel.pack(expand=True, fill="both", padx=10, pady=10)

# Text Entry Frame
textFrame = customtkinter.CTkFrame(mainFrame)
textFrame.pack(expand=True, fill="both", padx=10, pady=10)

# Text Entry
textInput = customtkinter.CTkEntry(textFrame, placeholder_text="Ask your question here..")
textInput.pack(expand=True, fill="both", side="left", pady=5, padx=5)

# Enter Button Image
enter = customtkinter.CTkImage(Image.open(r"enter.png"))

# Enter Button
arrowButton = customtkinter.CTkButton(textFrame, text="", image=enter, command=lambda: getGPTresp(textInput.get()))
arrowButton.pack(fill="y", side="right", pady=5, padx=5)

# Output Frame
outputFrame = customtkinter.CTkFrame(mainFrame)
outputFrame.pack(expand=True, fill="both", padx=10, pady=10)

# Output Label
outputlabel = customtkinter.CTkLabel(outputFrame, text="", anchor="n", wraplength=250)
outputlabel.pack(expand=True, fill="both", padx=10, pady=10)

# Controls Frame
controlsFrame = customtkinter.CTkFrame(mainFrame)
controlsFrame.pack(expand=True, fill="both", padx=10, pady=10)

# Microphone Button Image
microphone = customtkinter.CTkImage(Image.open(r"microphone.png"))

# Microphone Button
startButton = customtkinter.CTkButton(controlsFrame, text="", image=microphone, command=getAudio)
startButton.pack(expand=True, fill="both", side="left", padx=5)

# Reset Button Image
reset = customtkinter.CTkImage(Image.open(r"reset.png"))

# Reset Button
resetButton = customtkinter.CTkButton(controlsFrame, text="", image=reset)  # Add reset functionality if required
resetButton.pack(expand=True, fill="both", side="right", padx=5)

# Info Button Image
info_icon = customtkinter.CTkImage(Image.open(r"info.png"))  # Ensure you have an 'info.png' image in the working directory

# Info Button
infoButton = customtkinter.CTkButton(controlsFrame, text="", image=info_icon, command=show_info)
infoButton.pack(expand=True, fill="both", side="right", padx=5)

app.mainloop()