import asyncio
import os
import discord
import youtube_dl
import ffmpeg

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN2')

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''



ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options, executable='ffmpeg.exe'), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join2(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Relatively simple music bot example')

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')

@bot.event
async def on_message(ctx):
    lm=""
    channel1 = ctx.author.voice.channel
    channel2 = ctx.channel
    async for message in channel2.history(limit=1):
        lm=message.content

    if "$b2jv" in lm:
        await channel1.connect()
        await channel2.send('Connected')
    channel = ctx.author.voice.channel
    if "$b2dc" in lm:
        await channel1.disconnect()

# #    print("test")
# #    voice.play(discord.FFmpegPCMAudio(executable="C:/path/ffmpeg.exe", source="C:/songpath"))
#     # oldestMessage = None
#     # for channel in ctx.guild.text_channels:
#     #     fetchMessage = await channel.history().find(lambda m: m.author.id == users_id)
#     #     if fetchMessage is None:
#     #         continue


#     #     if oldestMessage is None:
#     #         oldestMessage = fetchMessage
#     #     else:
#     #         if fetchMessage.created_at > oldestMessage.created_at:
#     #             oldestMessage = fetchMessage

#     # if (oldestMessage is not None):
#     #     await ctx.send(f"Oldest message is {oldestMessage.content}")
#     # else:
#     #     await ctx.send("No message found.")
#     guild = ctx.guild
#     voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
#     audio_source = discord.FFmpegPCMAudio('boom1.mp3')
#     voice_client.play(audio_source, after=None)
#     print(ctx.author.voice.channel)

@bot.command(aliases=['paly', 'queue', 'que'])
async def jc(ctx):
    #guild = ctx.guild
    #discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
    #audio_source = discord.FFmpegPCMAudio('vuvuzela.mp3')
    #discord.VoiceClient.play(audio_source, after=None)
    print()
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        await channel.connect()
    #ctx.voice_client.move_to(channel)

#@bot.event
#async def on_message(message):
#    bot.process_commands(message)

bot.add_cog(Music(bot))
bot.run(TOKEN)