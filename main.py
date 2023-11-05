import speech_recognition as sr
import os
import openai
from dotenv import load_dotenv
import pyttsx3
import tkinter as tk
import customtkinter
import threading
from PIL import Image,ImageTk


#-----------------------------------------------------------------------#
# Backend


engine = pyttsx3.init()

def getAudio():
    threading.Thread(target=record_and_process_audio, daemon=True).start()
   

def record_and_process_audio():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Adjusting noise ")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Recording ")
            recorded_audio = recognizer.listen(source)
            print("Recognizing the text")
            text = recognizer.recognize_google(recorded_audio, language="en-US")
            print(f"User: {text}")
            if text:
                typeWriter(text, 1, inputlabel)
                getGPTresp(text)

    except sr.UnknownValueError:
        print("unknown error occurred")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")


def getGPTresp(text):
    def generate_response():
        load_dotenv()
        typeWriter("The AI is Thinking . . .", 1, outputlabel)
        openai.api_key = os.getenv('GPT')
        messages = [{"role": "user", "content": text + "in no more than 50 words"}]
        typeWriter("The AI is Thinking . . .", 1, outputlabel)
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                #max_tokens=50  # This limits the response length
            )
            response_text = completion.choices[0].message['content']
            print(f"ChatAI: {response_text}")
            typeWriter(response_text, 1, outputlabel)
            makeAudio(response_text)
        except Exception as e:
            print(f"Error in getting response from GPT-3: {e}")
        
    threading.Thread(target=generate_response, daemon=True).start()

def makeAudio(response_text):
    def audio():
        # play the speech
        engine.say(response_text)
        engine.runAndWait()

    threading.Thread(target=audio, daemon=True).start()



#-----------------------------------------------------------------------#
# Frontend


def typeWriter(text, counter, label):
    text=text.capitalize()
    label.configure(text=f"{text[:counter]}...")
    label.configure(text_color="green")
    if counter < len(text):
        app.after(50, lambda: typeWriter(text, counter+1, label))
    if counter == len(text):
        label.configure(text_color="#6874E8")


customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.title("ChatAI")
app.geometry("300x500")
app.resizable(False, False)

mainFrame = customtkinter.CTkFrame(app)
mainFrame.pack(expand=True, fill="both")

#input
inputFrame = customtkinter.CTkFrame(mainFrame)
inputFrame.pack(expand=True, fill="both", padx=10, pady=10)

label = customtkinter.CTkLabel(inputFrame, text="User", anchor="w")
label.pack(fill="x", padx=10, pady=10)

inputlabel = customtkinter.CTkLabel(inputFrame, text="Input...", anchor="n", wraplength=250)
inputlabel.pack(expand=True, fill="both", padx=10, pady=10)

textInput = tk.Entry(inputFrame, text="input", bg="#EAEFD1")
textInput.insert(0, "Enter your question here")
textInput.pack(expand=True, fill="both")

#output
outputFrame = customtkinter.CTkFrame(mainFrame)
outputFrame.pack(expand=True, fill="both", padx=10, pady=10)

label = customtkinter.CTkLabel(outputFrame, text="ChatAI", anchor="w")
label.pack(fill="x", padx=10, pady=10)

outputlabel = customtkinter.CTkLabel(outputFrame, text="Output...", anchor="n", wraplength=250)
outputlabel.pack(expand=True, fill="both", padx=10, pady=10)

#controls
controlsFrame = customtkinter.CTkFrame(mainFrame)
controlsFrame.pack(padx=10, pady=10)

microphone = customtkinter.CTkImage(Image.open(r"microphone.png"))

startButton = customtkinter.CTkButton(controlsFrame, text="", image=microphone, command=getAudio)
startButton.pack(ipady=10)

arrowButton = tk.Button(controlsFrame, text=">", bg="#B3C0A4", command=lambda: getGPTresp(textInput.get()))
arrowButton.pack(expand=True, fill="both", side="left")

resetButton = tk.Button(controlsFrame, text="Reset", bg="#505168")# , command=stopRec)
resetButton.pack(expand=True, fill="both", side="right")

app.mainloop() 