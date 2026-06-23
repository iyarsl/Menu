import os
import sys

from google import genai


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        sys.exit("GEMINI_API_KEY environment variable is not set.")

    prompt = " ".join(sys.argv[1:]) or "Explain how AI works in a few words."

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    print(response.text)


if __name__ == "__main__":
    main()
