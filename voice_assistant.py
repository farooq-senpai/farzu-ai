import tkinter as tk
import threading
import speech_recognition as sr
import pyttsx3
import subprocess
import os

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        chat_log.insert(tk.END, "Listening...\n")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            chat_log.insert(tk.END, f"You: {{command}}\n")
            process_command(command)
        except sr.UnknownValueError:
            chat_log.insert(tk.END, "Bot: Sorry, I didn't catch that.\n")
            speak("Sorry, I didn't catch that.")

def process_command(command):
    response = "Sorry, I don't understand that."
    if "open chrome" in command:
        response = "Opening Chrome."
        speak(response)
        try:
            subprocess.Popen("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        except FileNotFoundError:
    # Fallback to Store URI
            os.system("start spotify:")
        except:
            response = "Failed to open Chrome."
    elif "open spotify" in command:
        response = "Opening Spotify."
        speak(response)
        try:
            subprocess.Popen("C:\\Users\\Public\\Spotify\\Spotify.exe")
        except:
            response = "Failed to open Spotify."
    elif "exit" in command:
        response = "Goodbye!"
        speak(response)
        root.quit()
    chat_log.insert(tk.END, f"Bot: {{response}}\n")

def start_listening():
    threading.Thread(target=recognize_voice).start()

# GUI setup
root = tk.Tk()
root.title("AI Voice Assistant")
root.geometry("400x400")

chat_log = tk.Text(root, height=20, width=50)
chat_log.pack(pady=10)

listen_btn = tk.Button(root, text="🎤 Speak", command=start_listening)
listen_btn.pack()

root.mainloop()
