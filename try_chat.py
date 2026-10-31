from unittest.mock import patch
import chat

with patch('builtins.input', side_effect=['Ahoy', EOFError]):
    with patch('chat.llm', return_value='Hello!'):
        chat.repl(temperature=0)