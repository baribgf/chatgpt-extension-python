#!/bin/python

import os
import openai
from argparse import ArgumentParser
from halo import Halo
from pyshs import styled

progress = Halo(text='Getting response . .')

def inter_help():
    print(f"""{styled("Bari's ChatGPT Extension", fg='green', style='italic')}\n""" + \
        styled("[\\h]:", fg='cyan') + " View this help\t" + \
        styled("[\\c]:", fg='cyan') + " Clear shell\n" + \
        styled("[\\q]:", fg='cyan') + " Quit shell\t" + \
        styled("[\\uak]:", fg='cyan') + " Update api key\n" + \
        styled("[...]:", fg='cyan') + " Prompt to ChatGPT\t" + \
        "\n")

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

    except Exception as e:
        print(e)
        exit("\n" + styled("Error: There was a problem authenticating, verify your 'api key'", fg='red'))
        
def update_api_key(api_key):
    with open(os.path.join(os.path.dirname(__file__), 'res/openai-api-key.txt'), 'w') as f:
        f.write(str(api_key))
    print(styled("API key updated successfully !", fg='green'))

def direct(prompt: str, api_key_path: str = None, api_key: str = None, **kwargs):
    if api_key is not None:
        openai.api_key = api_key
        
    elif (ak := kwargs.get('new_api_key')) is not None:
        update_api_key(ak)
        openai.api_key_path = api_key_path
        
    elif api_key_path is not None:
        if os.path.isfile(api_key_path):
            openai.api_key_path = api_key_path
        else:
            raise FileNotFoundError(f'{api_key_path} is not a file')
    else:
        raise ValueError('Neither "api key" or "api key path" has been specified.')

    if prompt is not None and len(prompt) > 0:
        response = get_response(prompt)
        print(styled(response, fg='white'))
    else:
        print("No prompt entered, no response . .")

def interactive():
    inter_help()
    while True:
        try:
            openai.api_key_path = os.path.join(os.path.dirname(__file__), 'res/openai-api-key.txt')
            if not os.path.isfile(openai.api_key_path):
                update_api_key(input(styled("[>] OpenAI API key:", bg='blue') + ' '))
                continue

            prompt = input(styled("[>] Write your prompt:", bg='blue') + ' ')

            if prompt == '\\c':
                os.system('clear')
                continue
            elif prompt == '\\q':
                break
            elif prompt == '\\uak':
                update_api_key(input("... Enter your new api key: "))
                continue
            elif prompt == '\\h':
                inter_help()
                continue

            response = get_response(prompt)

            print(styled("[>] Response:", bg='green') + '\n')
            
            print(styled(response, fg='white'))
        except KeyboardInterrupt:
            print()
            break

if __name__ == '__main__':
    parser = ArgumentParser()

    # direct mode args
    direct_arg_group = parser.add_argument_group()

    direct_arg_group.add_argument('-p', '--prompt', help='The prompt message to send to ChatGPT')
    direct_arg_group.add_argument('-nak', '--new-api-key', help='Update saved api key')
    
    api_key_args_group = direct_arg_group.add_mutually_exclusive_group()
    api_key_args_group.add_argument('-ak', '--api-key', help='The OpenAI API key', default=None)
    api_key_args_group.add_argument('-akp', '--api-key-path', help='The OpenAI API key', default=os.path.join(os.path.dirname(__file__), 'res/openai-api-key.txt'))

    args = parser.parse_args()

    if args.prompt or args.new_api_key:
        if not os.path.isfile(args.api_key_path):
            with open(args.api_key_path, 'w') as f:
                f.write("")
        direct(args.prompt, api_key_path=args.api_key_path, api_key=args.api_key, new_api_key=args.new_api_key)
    else:
        interactive()

    print(styled('Good bye!', bg='cyan'))
