import random

def handle_response(message)-> str:
    p_message = message.lower()

    if p_message == 'hello':
     return 'Hey There!'
    if p_message == 'roll':
        return str(random.randrange(1,6))
    if p_message == 'help':
        return "`This is a help message that you can modify.`"