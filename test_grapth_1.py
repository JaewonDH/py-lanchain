from langgraph.graph import StateGraph, START, END
from typing import TypedDict,Literal

print(f"tttttttttttttt")

class State(TypedDict):
    count : int


def plus(state: State) ->State:
    return {"count": state["count"]+1}

workflow=StateGraph(State)

# 노드는 함수나 기능을 추가 하는 곳
workflow.add_node("plus_fun",plus)

workflow.add_edge(START,"plus_fun")
workflow.add_edge("plus_fun",END)

app=workflow.compile()


result=app.invoke({"count":0})
result=app.invoke({"count":1})
result=app.invoke({"count":2})
result=app.invoke({"count":3})

print(f"result={result}")


class InputState(TypedDict):
    user_input : str

def check_user_input(state: InputState) -> Literal["question", "command", "unknown"]:
    user_input = state["user_input"].lower()

    if user_input.endswith("?"):
        return "question"
    elif user_input.startswith("!"):
        return "command"
    else:
        return "unknown"


workflow_two=StateGraph(InputState)
workflow_two.add_conditional_edges("parser_input",check_user_input,{
        "question": "answer_question",
        "command": "execute_command",
        "unknown": "ask_clarification"
    })
