from data_analyser import analyse_data

print("================================")
print("       VIRTUAL AI AGENT")
print("================================")

while True:
    user_input = input("You: ").lower()

    # Exit
    if user_input == "exit":
        print("Agent: Goodbye!")
        break

    # Greeting
    elif user_input == "hello" or user_input == "hi" or user_input == "hey":
        print("Agent: Hello! How can I help you?")

    # Calculator
    elif "calculate" in user_input:
        expression = user_input.replace("calculate", "").strip()

        try:
            result = eval(expression)
            print("Agent:", result)
        except:
            print("Agent: Sorry, I couldn't calculate that.")

    # Data Analyzer
    elif "analyze" in user_input or "analyse" in user_input:
        print("Agent: Data Analyzer selected.")

        file_path = input("Agent: Enter the CSV file path: ")
        analyse_data(file_path)

    # Unknown command
    else:
        print("Agent: I don't understand that task yet.")
