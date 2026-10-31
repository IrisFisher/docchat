import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def llm(messages, temperature=1):
    completion = client.chat.completions.create(
        messages=messages,
        model='openai/gpt-oss-20b',
        temperature=temperature,
    )
    return completion.choices[0].message.content

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
        reply = llm(self.messages, temperature=temperature)
        self.messages.append({'role': 'assistant', 'content': reply})
        return reply

def repl(temperature=0.8, chat = Chat(system='You are a helpful assistant. You always speak like a pirate.')):
    """Send a message and retain the reply.
    >>> from unittest.mock import patch
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
    >>> from unittest.mock import patch
    >>> with patch('builtins.input', side_effect=['Hi','What are you?', EOFError]):
    ...     with patch.object(client.chat.completions, 'create') as request:
    ...         test = Chat(system='Be brief.')
    ...         request.return_value.choices[0].message.content = 'Hello!'
    ...         request.return_value.choices[0].message.content = 'I am a chat bot.'
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
            #print(user_input)
            print(chat.send_message(user_input, temperature=temperature))
    except (KeyboardInterrupt, EOFError):
        print()

if __name__ == '__main__':
    repl()