import os
from dotenv import load_dotenv
from groq import Groq
import json
from tools.calculate import calculate
from tools.ls import ls
from tools.cat import cat

load_dotenv()

def llm(messages, tool_choice="auto", temperature=1):
    """Call llm"""
    client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

    with open('tools/tools.json', encoding='utf-8') as f:
        tools = json.load(f)

    completion = client.chat.completions.create(
        model='openai/gpt-oss-20b',
        messages=messages,
        tools = tools,
        tool_choice = tool_choice,
        temperature=temperature,
    )       
    return completion.choices[0].message


def execute_tool_calls(messages, tool_calls):
    """Parse and execute tool calls"""

    available_functions = {
    "calculate": calculate,
    "ls": ls,
    "cat": cat,
    # Add more tools here as you build them
    # "get_weather": get_weather,
    # "search_database": search_database,
    }

    for tool_call in tool_calls:
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
    #print(messages)
    final_response = llm(messages, tool_choice="none", temperature=0.5)
    return final_response.content


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
        self.tool_calls = llm(self.messages, temperature=0.5).tool_calls
        if llm(self.messages,temperature=0.5).tool_calls:
            reply = execute_tool_calls(self.messages, self.tool_calls)
        else:
            reply = llm(self.messages, temperature=temperature).content
        self.messages.append({'role': 'assistant', 'content': reply})
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