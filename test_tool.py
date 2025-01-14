from langchain_ollama import ChatOllama
from typing_extensions import TypedDict
from langchain.agents import tool
from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser
from langchain_openai import ChatOpenAI
from langchain_community.llms.gpt4all import GPT4All

model = (
    "C:\\Users\\JWLEE\\AppData\\Local\\nomic.ai\\GPT4All\\qwen2-1_5b-instruct-q4_0.gguf"
)

llm = ChatOllama(model="llama3.2:1b", temperature=0, num_gpu=0)


@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)


@tool
def add_function(a: float, b: float) -> float:
    """Adds two numbers together."""
    return a + b


@tool
def divide_function(a: float, b: float) -> float:
    """division two numbers together."""
    return a / b


def tool_call(tool_call_results):
    print(f"tool_call_results={tool_call_results}")
    for result in tool_call_results:
        tool_name = result["type"]
        tool_args = result["args"]
        print(f"tool_name={tool_name}")
        print(f"tool_args={tool_args}")

    for tool in tools:
        if tool.name == tool_name:
            result = tool.invoke(tool_args)
            print(f"[실행도구] {tool_name}\n[실행결과] {result}")
        else:
            print(f"경고: {tool_name}에 해당하는 도구를 찾을 수 없습니다.")


tools = [get_word_length, add_function, divide_function]
llm_with_tools = llm.bind_tools(tools)
chain = llm_with_tools | JsonOutputToolsParser(tools=tools) | tool_call


# chain.invoke("What is the length of the word 'teddynote'?")
chain.invoke("33 division 55")
