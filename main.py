import os
from typesafe_sdk import TypeSafeClient
from dotenv import load_dotenv
from classifier import IntentClassifier
from domain import Turn

load_dotenv()

def main():

    client = TypeSafeClient(
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api",
    )
    
    user_message = "I want to know where is my order"

    intent_classifier = IntentClassifier(client=client)
    result = intent_classifier.classify(user_message)

    print(result)

    history = [
        Turn(role="user", content="My package was supposed to arrive yesterday."),
        Turn(role="assistant", content="Sorry about that! How can I help?"),
    ]
    result = intent_classifier.classify("I just want my money back", history=history)

    print(result)


if __name__ == "__main__":
    main()
