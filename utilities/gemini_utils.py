import argparse
import os
from google import genai
from dotenv import load_dotenv

def list_models():
    try:
        load_dotenv()

        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            client = genai.Client()
        else:
            print("Error: The GOOGLE_API_KEY environment variable is not set.")
            print("Please define it in a .env file or export it in your shell.")
            return

        print("Available models:")
        for m in client.models.list():
            print(f"- {m.name}")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    """
    Main function to parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="A CLI tool to interact with the Google GenAI API."
    )

    parser.add_argument(
        '--list-models',
        action='store_true',
        help="Lists all available generation models."
    )

    args = parser.parse_args()

    if args.list_models:
        list_models()
    else:
        print("No action specified. Use --help to see available options.")

if __name__ == "__main__":
    main()