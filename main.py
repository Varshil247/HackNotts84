import speech_recognition as sr
import os
import openai
from dotenv import load_dotenv
from tkinter import messagebox
import pyttsx3
import customtkinter
import threading
from PIL import Image, ImageTk

#-----------------------------------------------------------------------#
# Backend

# Global variable to maintain the conversation history
conversation_history = []

engine = pyttsx3.init()

def getAudio():
    threading.Thread(target=record_and_process_audio, daemon=True).start()
   
def record_and_process_audio():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Adjusting noise ")
            typeWriter("Recording ", 1, inputlabel)
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Recording ")
            recorded_audio = recognizer.listen(source)
            print("Recognizing the text")
            typeWriter("Recognizing the text", 1, inputlabel)
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
        global conversation_history
        load_dotenv()
        typeWriter("The AI is Thinking...", 1, outputlabel)
        openai.api_key = os.getenv('GPT')
        messages = conversation_history + [{"role": "user", "content": text + "in no more than 50 words,Act like a human"}]
        typeWriter("The AI is Thinking...", 1, outputlabel)
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            response_text = completion.choices[0].message['content']
            print(f"ChatAI: {response_text}")
            conversation_history.append({"role": "user", "content": text})
            conversation_history.append({"role": "assistant", "content": response_text})
            typeWriter(response_text, 1, outputlabel)
            makeAudio(response_text)
        except Exception as e:
            print(f"Error in getting response from GPT-3: {e}")
        
    threading.Thread(target=generate_response, daemon=True).start()

def makeAudio(response_text):
    def audio():
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

def combobox_callback(choice):
    customtkinter.set_appearance_mode(choice)
    customtkinter.set_default_color_theme("green")

def show_info():
    info_text = ("ChatAI is a voice-enabled chat application that uses OpenAI's GPT-3 "
                 "for conversational AI. Speak into your microphone or type in your query, "
                 "and ChatAI will respond. This application showcases the capabilities "
                 "of speech recognition and AI-powered conversational interfaces.")
    messagebox.showinfo("About ChatAI", info_text)


def resetText():
    global conversation_history
    inputlabel.configure(text="")
    outputlabel.configure(text="")
    conversation_history = []


app = customtkinter.CTk()
app.title("ChatAI")
app.geometry("300x600")
app.resizable(False, True)

mainFrame = customtkinter.CTkFrame(app)
mainFrame.pack(expand=True, fill="both")

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")




#settings
infoFrame = customtkinter.CTkFrame(mainFrame)
infoFrame.pack(fill="x", padx=10, pady=10)

combobox = customtkinter.CTkComboBox(infoFrame, values=["Dark","Light"], command=combobox_callback, state="readonly")
combobox.pack(expand=True, fill="x", side="left")
combobox.set("Dark")




# Info Button Image
info_icon = customtkinter.CTkImage(Image.open(r"info.png"))  # Ensure you have an 'info.png' image in the working directory
infoButton = customtkinter.CTkButton(infoFrame, text="", image=info_icon, width=0, command=show_info)
infoButton.pack(side="right")




#input
inputFrame = customtkinter.CTkFrame(mainFrame)
inputFrame.pack(expand=True, fill="both", padx=10, pady=10)

label = customtkinter.CTkLabel(inputFrame, text="User", anchor="w")
label.pack(fill="x", padx=10, pady=10)

inputlabel = customtkinter.CTkLabel(inputFrame, text="", anchor="n", wraplength=250)
inputlabel.configure(height =20)
inputlabel.pack(expand=True, fill="both", padx=10, pady=10)




#manual input
textFrame = customtkinter.CTkFrame(mainFrame)
textFrame.pack(expand=True, fill="both", padx=10, pady=10)

textInput = customtkinter.CTkEntry(textFrame, placeholder_text="Ask your question here..")
textInput.configure(width=200)
textInput.pack(expand=True, fill="both",side="left", pady=5,padx=5)

enter = customtkinter.CTkImage(Image.open(r"enter.png"))
arrowButton = customtkinter.CTkButton(textFrame, text="", image=enter, command=lambda: getGPTresp(textInput.get()))
arrowButton.pack( fill="y",side="right",pady=5,padx=5)




#output
outputFrame = customtkinter.CTkFrame(mainFrame)
outputFrame.pack(expand=True, fill="both", padx=10, pady=10)

label = customtkinter.CTkLabel(outputFrame, text="ChatAI", anchor="w")
label.pack(fill="x", padx=10, pady=10)

scroll = customtkinter.CTkScrollableFrame(outputFrame)
scroll.pack(expand=True, fill="both", padx=10, pady=10)

outputlabel = customtkinter.CTkLabel(scroll, text="", anchor="n", wraplength=220)
outputlabel.pack(expand=True, fill="both", padx=10, pady=10)



#controls
controlsFrame = customtkinter.CTkFrame(mainFrame)
controlsFrame.pack(expand=True, fill="both", padx=10, pady=10)

microphone = customtkinter.CTkImage(Image.open(r"microphone.png"))
startButton = customtkinter.CTkButton(controlsFrame, text="", image=microphone, command=getAudio)
startButton.pack(expand=True, fill="both", side="left", padx=5)

reset = customtkinter.CTkImage(Image.open(r"reset.png"))
resetButton = customtkinter.CTkButton(controlsFrame, text="", image=reset, command=resetText)  # Use app.quit to properly exit the application
resetButton.pack(expand=True, fill="both", side="right", padx=5)

app.mainloop()