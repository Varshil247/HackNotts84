reset = customtkinter.CTkImage(Image.open(r"reset.png"))

resetButton = customtkinter.CTkButton(controlsFrame, text="", image=reset, command=resetText)  # Use app.quit to properly exit the application
resetButton.pack(expand=True, fill="both", side="right", padx=5)