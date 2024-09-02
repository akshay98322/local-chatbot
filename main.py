from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
how Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


def handle_conversation():
    """
    Handles a conversational interaction with the user, using a language model to generate responses.

    The function prompts the user for input, passes it to the language model, and prints the generated response. The conversation history is maintained and provided to the language model for context.

    The function continues until the user enters 'exit' to quit the conversation.
    """
    context = ""
    print("Welcome to the Jarvis ChatBot! Type 'exit' to quit the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        result = chain.invoke({"context": context, "question": user_input})
        print("Jarvis: ",result)
        context += f"\nUser: {user_input}\nAI: {result}"

if __name__ == "__main__":
    handle_conversation()


