import os
from typesafe_sdk import TypeSafeClient
from dotenv import load_dotenv


def main():

    load_dotenv()

    client = TypeSafeClient(
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api",
    )
    
    print("Hello from jev-intent-routing!")


if __name__ == "__main__":
    main()
