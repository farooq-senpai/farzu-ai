from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
import os
from dotenv import dotenv_values

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIkey = env_vars.get("GroqAPIkey")

client = Groq(api_key=GroqAPIkey)

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question. ***
*** Reply in only English, even if the question is in Hindi. ***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""


# Load chat history or initialize it
chatlog_path = "Data/ChatLog.json"
os.makedirs("Data", exist_ok=True)

try:
    with open(chatlog_path, "r") as f:
        messages = load(f)
except FileNotFoundError:
    messages = []
    with open(chatlog_path, "w") as f:
        dump(messages, f, indent=4)


def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5, timeout=15))

    answer = f"The search results for '{query}' are:\n[start]\n"
    for i in results:
        answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
    answer += "[end]"
    
    print (answer)
    return answer


def AnswerModifier(answer):
    lines = answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)


SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]


def information():
    now = datetime.datetime.now()
    return (
        f"Use This Real-time Information if needed:\n"
        f"Day: {now.strftime('%A')}\n"
        f"Date: {now.strftime('%d')}\n"
        f"Month: {now.strftime('%B')}\n"
        f"Year: {now.strftime('%Y')}\n"
        f"Time: {now.strftime('%H')} hours, {now.strftime('%M')} minutes, {now.strftime('%S')} seconds.\n"
    )


def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    with open(chatlog_path, "r") as f:
        messages = load(f)

    messages.append({"role": "system", "content": GoogleSearch(prompt)})

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [{"role": "system", "content": information()}] + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )

    answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            answer += chunk.choices[0].delta.content

    answer = answer.strip().replace("</s>", "")
    messages.append({"role": "system", "content": GoogleSearch(prompt)})


    with open(chatlog_path, "w") as f:
        dump(messages, f, indent=4)

    if SystemChatBot:
       SystemChatBot.pop()

    return AnswerModifier(answer)


if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))
