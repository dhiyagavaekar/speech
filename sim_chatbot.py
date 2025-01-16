import google.generativeai as genai
import json

# Initialize the Google GenAI API with your key
genai.configure(api_key="AIzaSyDFJ_Cz2xvOwz9TaAn62rDn1LkzbARWvYU")

# Set up the generation configuration
generation_config = {
    "temperature": 0.6,
    "top_p": 0.9,
    "top_k": 1,
    "max_output_tokens": 300,
}

# Create the generative model
model = genai.GenerativeModel('gemini-1.0-pro', generation_config=generation_config)


def sim_support_chatbot():
    conversation_context = """
    You are a SIM card support assistant. Your name is Elle. Follow this flow while interacting with the user:
    1. Ask for the user's name.
    2. Ask for the user's SIM provider and  Always provide a list of possible example:  
       - 1. Airtel
       - 2. Jio
       - 3. VI
    3. Ask for the mobile number.
    4. Ask about the issue they are facing and Always provide a list of possible issues example:
       - 1. Network
       - 2. Billing
       - 3. Activation
       and it just example you can add more
    5. Based on the issue, ask follow-up questions to gather more details and provide a solution using options wherever possible.
    6. If the issue cannot be resolved, suggest escalating it to customer support.

    Be professional, friendly, and empathetic during the conversation. Always acknowledge the user's inputs before asking the next question.
    """
   
    conversation_history = []
    asked_questions = set()

    # Initial bot message
    bot_message = "Hello! My name is Elle. I am a SIM card support assistant. Could you please tell me your name?"
    print(f"SIM Support Bot: {bot_message}")
    conversation_history.append({"role": "bot", "message": bot_message})

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['exit', 'quit']:
            farewell_message = "Thank you for reaching out to us. Have a great day!"
            print(f"SIM Support Bot: {farewell_message}")
            conversation_history.append({"role": "bot", "message": farewell_message})
            break

        # Add user input to the conversation history
        conversation_history.append({"role": "user", "message": user_input})

        # Generate prompt dynamically
        prompt = conversation_context
        for turn in conversation_history:
            role = "User" if turn["role"] == "user" else "SIM Support Bot"
            prompt += f"\n{role}: {turn['message']}"

        prompt += "\nSIM Support Bot:"

        # Generate the bot's response
        response = model.generate_content(prompt).text.strip()

        # Post-process response to avoid repetition
        if response in asked_questions:
            response = (
                "Let me assist you with something else. Could you share more details about your issue?"
            )
        else:
            asked_questions.add(response)

        # Display the bot's response
        print(f"SIM Support Bot: {response}")
        conversation_history.append({"role": "bot", "message": response})

    # Save the conversation history to a JSON file
    with open("conversation_history.json", "w") as json_file:
        json.dump(conversation_history, json_file, indent=4)


# Start the chatbot
sim_support_chatbot()