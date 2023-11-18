import discord
from random import randint

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def get_random_question():
    with open('viktorina.txt', 'r', encoding='utf-8') as f:
        qs = f.read().split('\n')[:-1]

    if qs:
        res = qs[randint(0, len(qs)-1)]
        return res.split('|')
    else:
        return None, None

question = None
answer = None
hidden_answer = None
game_active = False

@client.event
async def on_message(message):
    global question, answer, hidden_answer, game_active
    if message.author == client.user:
        return

    if message.content == 'start':
        if not game_active:
            game_active = True
            question, answer = get_random_question()
            if question and answer:
                hidden_answer = '-' * len(answer)
                await message.channel.send(question)
                await message.channel.send(hidden_answer)
            else:
                await message.channel.send('No questions available.')
        else:
            await message.channel.send('The game is already in progress.')

    elif message.content == 'stop':
        if game_active:
            game_active = False
            await message.channel.send('The game has been stopped.')
        else:
            await message.channel.send('There is no active game to stop.')

    elif game_active:
        if message.content != answer:
            await message.channel.send('Неправильный ответ')
            indx = hidden_answer.index('-')
            hidden_answer = answer[:indx+1] + hidden_answer[indx+1:]
            await message.channel.send(hidden_answer)
        else:
            await message.channel.send(f'Правильно!, {message.author} молодец')
            question, answer = get_random_question()
            if question and answer:
                hidden_answer = '-' * len(answer)
                await message.channel.send(question)
                await message.channel.send(hidden_answer)
            else:
                await message.channel.send('No more questions available.')


client.run('MTE2NTE5MzUyMjY2ODg5NjM1Ng.GQZw4M.JG9--BuSqGmUUy5MAiE6OPn_LjkduNp5--9Nbw')