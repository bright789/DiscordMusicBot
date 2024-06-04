import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import os
import asyncio

# Add ffmpeg directory to PATH
os.environ["PATH"] += os.pathsep + os.path.abspath(r"C:\Users\Surge\Downloads\DiscordMusicBot\ffmpeg-master-latest-win64-gpl\bin")

# Intents and bot prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Remove default help command
bot.remove_command('help')

# YouTube downloader options
ytdl_format_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
}

ffmpeg_options = {
    'options': '-vn',
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
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

queue = []

def play_next(ctx):
    if len(queue) > 0:
        next_song = queue.pop(0)
        ctx.voice_client.play(next_song, after=lambda e: play_next(ctx))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send(f'{ctx.message.author.name} is not connected to a voice channel')
        return
    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='play', help='To play song')
async def play(ctx, url):
    try:
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                return

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
            queue.append(player)

        if not ctx.voice_client.is_playing():
            ctx.voice_client.play(queue.pop(0), after=lambda e: play_next(ctx))

        await ctx.send(f'Added to queue: {player.title}')
    except Exception as e:
        await ctx.send(f'An error occurred: {str(e)}')

@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_playing():
        await ctx.send("Pausing the song")
        voice_client.pause()
    else:
        await ctx.send("The bot is not playing any song.")

@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_paused():
        await ctx.send("Resuming the song")
        voice_client.resume()
    else:
        await ctx.send("The bot was not playing any song.")

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_playing():
        await ctx.send("Stopping the song")
        voice_client.stop()
    else:
        await ctx.send("The bot is not playing any song.")

@bot.command(name='skip', help='Skips the current song')
async def skip(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_playing():
        await ctx.send("Skipping the song")
        voice_client.stop()
    else:
        await ctx.send("The bot is not playing any song.")

@bot.command(name='queue', help='Shows the current queue')
async def show_queue(ctx):
    if len(queue) == 0:
        await ctx.send("The queue is empty.")
    else:
        queue_list = "\n".join([song.title for song in queue])
        await ctx.send(f"Current queue:\n{queue_list}")

@bot.command(name='help', help='Displays help message')
async def help(ctx):
    helptext = """
    **Music Bot Commands:**
    `!join` - Tells the bot to join the voice channel
    `!leave` - Makes the bot leave the voice channel
    `!play <YouTube URL>` - Plays a song from a YouTube URL
    `!pause` - Pauses the current song
    `!resume` - Resumes the paused song
    `!stop` - Stops the current song
    `!skip` - Skips the current song
    `!queue` - Shows the current queue
    """
    await ctx.send(helptext)

# Run the bot with the token
bot.run('MTI0NzMzNjE2MTIxOTk3MzEzMA.GVqtuI.2urcl3Ey0tFlvn_SbAerG_msPgXBGcQSQv1XIc')
