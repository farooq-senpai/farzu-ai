import tkinter as tk
import threading
import speech_recognition as sr
import pyttsx3
import os
import speech_recognition as sr
import pyttsx3
import webbrowser
import urllib.parse

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print("You said:", command)
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError:
            speak("Speech service error.")
            return ""

def play_youtube_video(query):
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"
    webbrowser.open(url)
    speak(f"Searching YouTube for {query}.") 
    import webbrowser




# MAIN
speak("Say a command.")
command = recognize_command()

if "play" in command and "youtube" in command:
    song = command.replace("play", "").replace("on youtube", "").strip()
    play_youtube_video(song)
else:
    speak("Command not recognized.")
def process_command(command):
    if "play" in command and "youtube" in command:
        song = command.replace("play", "").replace("on youtube", "").strip()
        play_youtube_video(song)
    elif "open youtube" in command or "start youtube" in command:
         open_youtube()
    else:
        speak("Command not recognized.")


engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        chat_log.insert(tk.END, "🎤 Listening...\n")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            chat_log.insert(tk.END, f"You: {command}\n")
            process_command(command)
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            chat_log.insert(tk.END, "Bot: Sorry, I didn't understand that.\n")
        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
            chat_log.insert(tk.END, "Bot: Service unavailable.\n")

def open_spotify():
    try:
        os.system("start spotify:")
        speak("Opening Spotify")
        chat_log.insert(tk.END, "Bot: Opening Spotify...\n")
    except:
        speak("Couldn't open Spotify.")
        chat_log.insert(tk.END, "Bot: Failed to open Spotify.\n")

def process_command(command):
    if "open spotify" in command or "start spotify" in command:
        open_spotify()
    else:
        speak("Command not recognized.")
        chat_log.insert(tk.END, "Bot: Command not recognized.\n")

def start_listening():
    threading.Thread(target=recognize_command).start()

# GUI setup
root = tk.Tk()
root.title("Voice Command Assistant")
root.geometry("400x400")

chat_log = tk.Text(root, height=20, width=50)
chat_log.pack(pady=10)

listen_btn = tk.Button(root, text="🎤 Speak", command=start_listening)
listen_btn.pack()

root.mainloop()
