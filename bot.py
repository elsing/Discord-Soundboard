import asyncio
import os
import discord
import ffmpeg

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

ffmpeg_options = {
    'options': '-vn'
}

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Relatively simple music bot example')

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')

@bot.event
async def on_message(ctx):
    lm=""
    
    channel2 = ctx.channel
    async for message in channel2.history(limit=1):
        lm=message.content
    if "$bjv" in lm:
        channel1 = ctx.author.voice.channel
        await channel1.connect()
        await channel2.send('Connected')

    if "$comm" in lm:
        await channel2.send(lm[6:])

    if "$b1dc" in lm:
        server = ctx.message.guild.voice_client
        await server.disconnect()

bot.run(TOKEN)