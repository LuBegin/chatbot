from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv() 

@tool
def calculadora(a: float, b: float) -> str:
    """Útil para realizar cálculos matemáticos simples com números"""
    print("Tool foi requisitada.")
    return f"O resultado de {a} e {b} é {a + b} , {a - b} , {a * b} e {a / b} respectivamente."

def main():
    modelo = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

    tools = [calculadora]
    agent_executor = create_react_agent(model=modelo, tools=tools)

    print("Bem vindo(a))! Eu sou seu assistente virtual. Digite 'sair' para encerrar a conversa.")
    print("Posso te ajudar com suas atividades. O que você quer hoje?")

    while True:
        user_input = input("\nVocê: ").strip()

        if user_input == "sair":
            break

        print("\nAssistente: ", end="")
        for chunk in agent_executor.stream(
            {"messages":[HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
        print()
if __name__ == "__main__":
    main()
