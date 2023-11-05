import speech_recognition as sr
import os
import openai
from dotenv import load_dotenv
import pyttsx3
import tkinter as tk
import threading

engine = pyttsx3.init()

def getAudio():
    threading.Thread(target=record_and_process_audio, daemon=True).start()

def record_and_process_audio():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Adjusting noise ")
            recognizer.adjust_for_ambient_noise(source, duration=0.25)
            print("Recording ")
            recorded_audio = recognizer.listen(source)
            print("Recognizing the text")
            text = recognizer.recognize_google(recorded_audio, language="en-US")
            print("Decoded Text : {}".format(text))
            if text:
                getGPTresp(text)
    except sr.UnknownValueError:
        print("unknown error occurred")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")


def getGPTresp(text):
    def generate_response():
        load_dotenv()
        openai.api_key = os.getenv('GPT')
        messages = [{"role": "user", "content": text + "restrict your answer to 50 words or less"}]
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=50  # This limits the response length
            )
            response_text = completion.choices[0].message['content']
            print(response_text)
            makeAudio(response_text)
        except Exception as e:
            print(f"Error in getting response from GPT-3: {e}")

    threading.Thread(target=generate_response, daemon=True).start()

def makeAudio(response_text):
    engine.say(response_text)
# play the speech
    engine.runAndWait()


# Create the main application window
app = tk.Tk()
app.title("ChatAI")
app.geometry("300x500")

#input
inputFrame = tk.Frame(app)
inputFrame.pack(expand=True, fill="both")

inputlabel = tk.Label(inputFrame, text="Input", bg="#EAEFD3")
inputlabel.pack(expand=True, fill="both")

#output
outputFrame = tk.Frame(app)
outputFrame.pack(expand=True, fill="both")

outputlabel = tk.Label(outputFrame, text="Output", bg="#EAEFD3")
outputlabel.pack(expand=True, fill="both")

#controls
controlsFrame = tk.Frame(app)
controlsFrame.pack(expand=True, fill="both")

startButton = tk.Button(controlsFrame, text="Start", bg="#B3C0A4", command=getAudio)
startButton.pack(expand=True, fill="both", side="left")

# stopButton = tk.Button(controlsFrame, text="Stop", bg="#505168")# , command=stopRec)
# stopButton.pack(expand=True, fill="both", side="right")

resetButton = tk.Button(controlsFrame, text="Reset", bg="#505168")# , command=stopRec)
resetButton.pack(expand=True, fill="both", side="right")

app.mainloop() 