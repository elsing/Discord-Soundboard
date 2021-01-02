import asyncio
import os
import discord
import youtube_dl
import ffmpeg

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN2')

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
    if "$b2dc" in lm:
        await channel1.disconnect()
    if "$b2ps" in lm:
        lm = lm[6:]
        guild = ctx.guild
        voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
        audio_source = discord.FFmpegPCMAudio("/media/Sounds/"+lm+'.mp3')
        voice_client.play(audio_source, after=None)

bot.run(TOKEN)