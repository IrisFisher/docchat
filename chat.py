import os
from dotenv import load_dotenv
from groq import Groq
import json
from tools.calculate import calculate
from tools.ls import ls
from tools.cat import cat
from tools.grep import grep

load_dotenv()

tools = [{"type": "function",
            "function": {
                "name": "calculate",
                "description": "Evaluate a mathematical expression",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "The mathematical expression to evaluate"
                        }
                    },
                    "required": ["expression"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "ls",
                "description": "Lists all of the files in a folder",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "folder": {
                            "type": "string",
                            "description": "The folder to list the files from"
                        }
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "cat",
                "description": "Open a file and print its contents.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file": {
                            "type": "string",
                            "description": "The file to be opened."
                        }
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "grep",
                "description": "Returns each line from a set of files which contains a regular expression.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "regex": {
                            "type": "string",
                            "description": "The regular expression you are searching for."
                        },
                        "path": {
                            "type": "string",
                            "description": "The path of the files you are searching in."
                        }
                    }
                }
            }
        }]


def llm(messages, tool_choice="auto", temperature=1):
    """Call llm"""
    client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

    completion = client.chat.completions.create(
        model='openai/gpt-oss-20b',
        messages=messages,
        tools = tools,
        tool_choice = tool_choice,
        temperature=temperature,
    )       
    return completion.choices[0].message


def call_tools(messages, tool_call):
    available_functions = {
    "calculate": calculate,
    "ls": ls,
    "cat": cat,
    "grep": grep,
    }

    function_name = tool_call.function.name
    function_to_call = available_functions[function_name]
    function_args = json.loads(tool_call.function.arguments)
    function_response = function_to_call(**function_args)

    messages.append(
        {
            "role": "tool",
            "content": str(function_response),
            "name": tool_call.function.name,
            "tool_call_id": tool_call.id,
        }
    )
    return messages

def execute_tool_calls(messages, tool_calls):
    """Parse and execute tool calls"""

    for tool_call in tool_calls:
        messages = call_tools(messages, tool_call)

    final_response = llm(messages, tool_choice="none", temperature=0)
    messages.append(final_response)
    return messages, final_response.content


class Chat:
    def __init__(self, system='You are a helpful assistant.'):
        self.messages = [{'role': 'system', 'content': system}]

    def send_message(self, message, temperature=0.8):
        """Send a message and retain the reply.

        >>> from unittest.mock import patch
        >>> with patch.object(client.chat.completions, 'create') as request:
        ...     request.return_value.choices[0].message.content = 'Hello!'
        ...     chat = Chat(system='Be brief.')
        ...     print(chat.send_message('Hi', temperature=0))
        Hello!
        >>> expected = [
        ...     {'role': 'system', 'content': 'Be brief.'},
        ...     {'role': 'user', 'content': 'Hi'},
        ...     {'role': 'assistant', 'content': 'Hello!'},
        ... ]
        >>> chat.messages == expected
        True
        """
 
        self.messages.append({'role': 'user', 'content': message})
        if "/calculate" in message:
            start = message.find(' ', message.find('/calculate')+10)+1
            expression = message[start:]
            self.messages.append(
                {
                "role": "tool",
                "content": str(calculate(expression)),
                "name": 'calculate',
                "tool_call_id": 'manual_calculate_call',
                }
            )
            reply = self.messages[-1]['content']
        elif "/ls" in message:
            start = message.find(' ', message.find('/ls')+3)+1
            if start != -1:
                folder = message[start:]
            else:
                folder = ''
            self.messages.append(
                {
                "role": "tool",
                "content": str(ls(folder)),
                "name": 'ls',
                "tool_call_id": 'manual_ls_call',
                }
            )
            reply = self.messages[-1]['content']
        elif "/cat" in message:
            start = message.find(' ', message.find('/cat')+4)+1
            file = message[start:]
            self.messages.append(
                {
                "role": "tool",
                "content": str(cat(file)),
                "name": 'cat',
                "tool_call_id": 'manual_cat_call',
                }
            )
            reply = self.messages[-1]['content']
        elif "/grep" in message:
            start = message.find(' ', message.find('/grep')+5)+1
            end = message.find(' ', start+1)
            regex = message[start:end]
            path = message[end+1:]
            print(regex, path)
            self.messages.append(
                {
                "role": "tool",
                "content": str(grep(regex, path)),
                "name": 'grep',
                "tool_call_id": 'manual_grep_call',
                }
            )
            reply = self.messages[-1]['content']
        else:
            tool_logic = llm(self.messages, temperature=0)
            #print(tool_logic)
            self.tool_calls = tool_logic.tool_calls
            if self.tool_calls:
                self.messages.append({'role': 'assistant', 'content': tool_logic.reasoning, 'tool_calls': self.tool_calls})
                messages, reply = execute_tool_calls(self.messages, self.tool_calls)
                self.messages = messages
            else:
                reply = llm(self.messages, temperature=temperature).content
            self.messages.append({'role': 'assistant', 'content': reply})
            print(self.messages)
        return reply


def repl(temperature=0.8, chat = Chat(system='You are a helpful assistant. Be brief.')):
    """Send a message and retain the reply.
    >>> from unittest.mock import MagicMock, patch
    >>> with patch('builtins.input', side_effect=['Hi', EOFError]):
    ...     with patch.object(client.chat.completions, 'create') as request:
    ...         request.return_value.choices[0].message.content = 'Hello!'
    ...         test = Chat(system='Be brief.')
    ...         repl(temperature=0, chat = test)
    Hello!
    <BLANKLINE>
    >>> expected = [
    ...     {'role': 'system', 'content': 'Be brief.'},
    ...     {'role': 'user', 'content': 'Hi'},
    ...     {'role': 'assistant', 'content': 'Hello!'},
    ... ]
    >>> test.messages == expected
    True
    >>> from chat import client, Chat
    >>> first = MagicMock()
    >>> first.choices[0].message.content = 'Hello!'
    >>> second = MagicMock()
    >>> second.choices[0].message.content = 'I am a chat bot.'
    >>> with patch('builtins.input', side_effect=['Hi', 'What are you?', EOFError]):
    ...     with patch.object(client.chat.completions, 'create') as request:
    ...         request.side_effect=[first, second]
    ...         test = Chat(system='Be brief.')
    ...         repl(temperature=0, chat = test)
    Hello!
    I am a chat bot.
    <BLANKLINE>
    >>> expected = [
    ...     {'role': 'system', 'content': 'Be brief.'},
    ...     {'role': 'user', 'content': 'Hi'},
    ...     {'role': 'assistant', 'content': 'Hello!'},
    ...     {'role': 'user', 'content': 'What are you?'},
    ...     {'role': 'assistant', 'content': 'I am a chat bot.'},
    ... ]
    >>> test.messages == expected
    True
    """

    try:
        while True:
            user_input = input('chat> ')
            print(chat.send_message(str(user_input), temperature=temperature))
    except (KeyboardInterrupt, EOFError):
        print()

if __name__ == '__main__':
    repl()