import os
import subprocess
import asyncio
import webbrowser
import keyboard
import requests
from dotenv import dotenv_values
from AppOpener import open as appopen, close
from pywhatkit import search, playonyt
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
from typing import List

env_vars = dotenv_values(".env")
GroqAPIkey = env_vars.get("GroqAPIkey", "")
client = Groq(api_key=GroqAPIkey)

useragent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 "
    "(KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
)

messages = []
username = os.environ.get("Username", "Your Assistant")

SystemChatBot = [
    {"role": "system", "content": f"Hello, I am {username}, You're a content writer. You have to write content like a letter."}
]

def GoogleSearch(topic: str):
    search(topic)

def YouTubeSearch(topic: str):
    url = f"https://www.youtube.com/results?search_query={topic}"
    webbrowser.open(url)

def OpenNotepad(filepath: str):
    subprocess.Popen(["notepad.exe", filepath])
def ContentWriteAI(prompt: str):
    messages.append({"role": "user", "content": prompt})
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + messages,
        max_tokens=2048,
        temperature=0.7,
        top_p=1,
        stream=True
    )
    answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            answer += chunk.choices[0].delta.content
    answer = answer.replace("</s>", "")
    messages.append({"role": "assistant", "content": answer})
    return answer


def Content(topic: str):
    topic_clean = topic.replace("content ", "").strip()
    content = ContentWriteAI(topic_clean)
    path = rf"Data\{topic_clean.lower().replace(' ', '')}.txt"
    os.makedirs("Data", exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)
    OpenNotepad(path)
    return True
def OpenApp(app_name: str, sess=requests.session()):
    try:
        appopen(app_name, match_closest=True, output=True, throw_error=True)
        return True
    except:
        def extract_links(html):
            soup = BeautifulSoup(html, "html.parser")
            links = soup.find_all("a", {"jsname": "UWckNb"})
            return [link.get("href") for link in links]

        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
            else:
                print("Failed to retrieve search results.")
                return None

        html = search_google(app_name)
        if html:
            links = extract_links(html)
            if links:
                webbrowser.open(links[0])
                return True
    return False

def CloseApp(app_name: str):
    try:
        if "chrome" in app_name.lower():
            pass  # Do not close Chrome
        else:
            close(app_name, match_closest=True, output=True, throw_error=True)
        return True
    except:
        return False

def System(command: str):
    if command == "mute" or command == "unmute":
        keyboard.press_and_release("volume mute")
    elif command == "volume up":
        keyboard.press_and_release("volume up")
    elif command == "volume down":
        keyboard.press_and_release("volume down")
    return True

async def TranslateAndExecute(commands: List[str]):
    funcs = []
    for command in commands:
        if command.startswith("open "):
            funcs.append(asyncio.to_thread(OpenApp, command.removeprefix("open ").strip()))
        elif command.startswith("close "):
            funcs.append(asyncio.to_thread(CloseApp, command.removeprefix("close ").strip()))
        elif command.startswith("play "):
            funcs.append(asyncio.to_thread(playonyt, command.removeprefix("play ").strip()))
        elif command.startswith("content "):
            funcs.append(asyncio.to_thread(Content, command.removeprefix("content ").strip()))
        elif command.startswith("google search "):
            funcs.append(asyncio.to_thread(GoogleSearch, command.removeprefix("google search ").strip()))
        elif command.startswith("youtube search "):
            funcs.append(asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search ").strip()))
        elif command.startswith("system "):
            funcs.append(asyncio.to_thread(System, command.removeprefix("system ").strip()))
        else:
            print(f"No Function Found For: {command}")
    results = await asyncio.gather(*funcs)
    for result in results:
        yield result

async def Automation(commands: List[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True
