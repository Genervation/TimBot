
import os
from dotenv import load_dotenv
import json
import sys

from openai import OpenAI

import argparse


from prompts import system_prompt
from functions.call_functions import available_functions
from functions.call_functions import call_function



load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("OPENROUTER_API_KEY not set")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


parser = argparse.ArgumentParser(description="TimBot: a chatbot that uses OpenRouter's free model to respond to user queries.")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
parser.add_argument("user_prompt", type=str, help="User prompt to send to the chatbot")
args = parser.parse_args()

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]
#DON'T TOUCH ABOVE THIS LINE ------------------------------DON'T TOUCH ABOVE THIS LINE -----------------------------------------

for _ in range(20):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions
    )
    message = response.choices[0].message
    if message.content != None or message.content != "":

        messages.append(message)
        if response.usage != None and args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        elif response.usage == None:
            raise RuntimeError("Response usage is None")

        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                result_message = call_function(tool_call, args.verbose)
                if result_message['content'] == "":
                    break
                messages.append(result_message)
        else:
            print(f"\nResponse: {message.content}")
            break

    elif _ == 19:
        sys.exit("No response after 20 attempts")

def main():
    print("Hello from timbot!")


if __name__ == "__main__":
    main()
