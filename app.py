import tkinter as tk

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

startButton = tk.Button(controlsFrame, text="Start", bg="#B3C0A4")# , command=startRec)
startButton.pack(expand=True, fill="both", side="left")

# stopButton = tk.Button(controlsFrame, text="Stop", bg="#505168")# , command=stopRec)
# stopButton.pack(expand=True, fill="both", side="right")

resetButton = tk.Button(controlsFrame, text="Reset", bg="#505168")# , command=stopRec)
resetButton.pack(expand=True, fill="both", side="right")

app.mainloop() 
