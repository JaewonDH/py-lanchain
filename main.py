from langchain_ollama import ChatOllama

import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "LangChain-test"
os.environ["LANGCHAIN_API_KEY"] = "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"

llm = ChatOllama(model="llama3.2:1b", temperature=0, num_gpu=0)


print("Start chatting. Type 'exit' to end the conversation.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Conversation ended.")
        break

    print("Assistant:", end=" ")
    for chunk in llm.stream(user_input):
        print(chunk.content, end="", flush=True)
    print()
