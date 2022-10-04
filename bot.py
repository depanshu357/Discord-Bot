from webbrowser import get
import discord 
import responses
import re
import long_responses as long
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

def message_probablity(user_message,recognized_words,single_response=False,required_words=[]):
    message_certainty =0
    has_required_words = True

    for word in user_message:
        if word in recognized_words:
            message_certainty+=1
    
    percentage = float(message_certainty)/float(len(recognized_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break
    if has_required_words or single_response:
        return int(percentage*100)
    else:
        return 0

def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response,list_of_words,single_response=False,required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probablity(message,list_of_words,single_response,required_words)
    #response ---------------------------------------
    response('Hello!',['hello','hi','sup','hey','heyo','ola'],single_response=True)
    response('I\'m doing fine,and you?',['how','are','you','u','doing'],required_words=['how'])
    response('Thank you!',['i','love','code','palace'],required_words=['code','palace'])
    response(long.R_Eating,['what','you','eat','like'],required_words=['eat','like'])
    response('I am glad to hear that!😊',['thank','thanks','you','helping'],required_words=['helping']) 
    
    best_match = max(highest_prob_list,key=highest_prob_list.get)
    print(highest_prob_list)
    # return best_match
    return long.unknown() if highest_prob_list[best_match]<1 else best_match

# To take user input and removing all the symbols and converting it to lowercase
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*',user_input.lower())
    response = check_all_messages(split_message)
    return response

async def send_message(message,user_message,is_private):
    try:
        response  = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    # intents = discord.Intents.default()
    # intents.message_content = True
    # client = discord.Client(intents=discord.Intents.default())

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents = intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')
    
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        print(f"{username} said: '{user_message}' ({channel})")

        # if user_message[0] == '?':
        #    user_message = user_message[1:]
        #    await send_message(message,user_message, is_private=True)
        # else:
        #    await send_message(message,user_message, is_private=False)
        await message.channel.send(get_response(user_message))
           
        
    client.run(TOKEN)