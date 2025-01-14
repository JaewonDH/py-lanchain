from typing import Annotated
from langchain_ollama import ChatOllama
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from IPython.display import Image, display
import matplotlib.pyplot as plt
from test_tool import tools


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0,
)
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State):
    # llm.invoke(state["messages"])
    answer = llm_with_tools.invoke(tools)
    return {"messages": [answer]}


graph_builder = StateGraph(State)
# 기능을 추가
graph_builder.add_node("chatbot", chatbot)
# 길을 지정 시작
graph_builder.add_edge(START, "chatbot")
# 길을 지정 종료
graph_builder.add_edge("chatbot", END)

# graph 컴파일
graph = graph_builder.compile()


def display_image(graph, image_path):
    graph.get_graph().draw_mermaid_png(output_file_path=image_path)
    img = plt.imread(image_path)
    plt.imshow(img)
    plt.axis("off")
    plt.show()


image_path = "graph.png"
# display_image(graph, image_path)


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break
