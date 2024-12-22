from gpt import ask
from gm_prompt import Prompt

# Three types -- General grammar check (Default), Email(Formal),and text chat(Causual)  
def get_input_type() -> str:
    input_type = input("[GrammarGPT] input type: [E/C/G]\n").strip().lower()
    if input_type in ['e', 'c']:
        return input_type
    else:
        input_type = 'g'
        return input_type
    

def main():
    input_type = get_input_type()
    prompt = Prompt()
    system_prompt = prompt.get_system_prompt(input_type)

    # Accept multiple lines of input
    print("[GrammarGPT] User input(End input with Ctrl+Z): ")
    lines = []
    try:
        while True:
            line = input()
            lines.append(line+"\n")
    except EOFError:
        pass
    user_input = '\n'.join(lines)
    print("\n...Connecting with OpenAI...\n")  # Confirm the end of user_input

    # Pass the user_input to OpenAI as a single string
    answer = ask(system_prompt, user_input)
    
    # Match the correct input type 
    type_map = {
        'e': 'Email',
        'c': 'Chat',
        'g': 'General'
    }

    # Return the output from OpenAI
    print(f"[GrammarGPT][{type_map.get(input_type)}]\n{answer}\n\n[End]")

if __name__ == "__main__":

    main()