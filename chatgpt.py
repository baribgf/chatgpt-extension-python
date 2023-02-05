#!/bin/python

import os
import openai
from argparse import ArgumentParser
from halo import Halo

progress = Halo(text='Getting response . .')

def get_response(prompt):
    progress.start()

    try:
        completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        progress.stop()

        return completion.choices[0].text.strip() + '\n'
    except:
        exit("\nError: There was a problem authenticating, verify your 'api key'")

def direct(prompt: str, api_key_path: str = None, api_key: str = None):
    if api_key is not None:
        openai.api_key = api_key
    elif api_key_path is not None:
        if os.path.isfile(api_key_path):
            openai.api_key_path = api_key_path
        else:
            raise FileNotFoundError(f'{api_key_path} is not a file')
    else:
        raise ValueError('Neither "api key" or "api key path" has been specified.')

    response = get_response(prompt)
    print(response)

def interactive():
    while True:
        try:
            openai.api_key_path = './res/openai-api-key.txt'
            if not os.path.isfile(openai.api_key_path):
                openai.api_key_path = input("[>] OpenAI API key path: ")

            prompt = input("[>] Write your prompt: ")

            if prompt == '\c':
                os.system('clear')
                continue
            elif prompt == '\q':
                break
            
            response = get_response(prompt)

            print("[>] Response: \n")
            print(response)
        except KeyboardInterrupt:
            print()
            break

if __name__ == '__main__':
    parser = ArgumentParser()

    # direct mode args
    direct_arg_group = parser.add_argument_group()

    direct_arg_group.add_argument('-p', '--prompt', help='The prompt message to send to ChatGPT')
    
    api_key_args_group = direct_arg_group.add_mutually_exclusive_group()
    api_key_args_group.add_argument('-ak', '--api-key', help='The OpenAI API key', default=None)
    api_key_args_group.add_argument('-akp', '--api-key-path', help='The OpenAI API key', default='./res/openai-api-key.txt')

    args = parser.parse_args()

    if args.prompt:
        direct(args.prompt, api_key_path=args.api_key_path, api_key=args.api_key)
    else:
        interactive()

    print('Good bye!')
