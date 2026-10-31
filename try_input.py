from unittest.mock import patch

with patch('builtins.input', side_effect=['Ahoy', EOFError]):
    print(input('chat> '))
    try:
        input('chat> ')
    except EOFError:
        print('done')