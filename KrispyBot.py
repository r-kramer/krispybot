import asyncio
import discord
from discord.utils import get
from discord.ext import commands
import youtube_dl
import os

global voice
bot = commands.Bot(command_prefix="/")


def main():
    try:
        readfile = open("token.txt", "r")
    except(IOError, EOFError) as e:
        print("File opening error!!!")
        print('------')
    try:
        token = readfile.readline()
    except(IOError, EOFError) as e:
        print("Cannot assign token!!!")
        print('------')
    str(token)
    bot.run(token)


@bot.event
async def on_ready():
    print('Logged in as ' + str(bot.user))
    print('------')


@bot.command(pass_context=True)
async def HELP(ctx):
    bot_help = discord.Embed(
        colour=discord.Colour.green(),
        title="KrispyBot",
        description="/help"
    )
    # embed.set_author(name="Author", icon_url="https://i.redd.it/ub40fqv7q3221.png")
    # embed.set_image(url="https://i.redd.it/ub40fqv7q3221.png")
    bot_help.set_thumbnail(url="https://i.redd.it/ub40fqv7q3221.png")
    bot_help.add_field(name="/join", value="This joins the bot to your voice channel", inline=True)
    bot_help.add_field(name="/leave", value="This disconnects the bot from your voice channel", inline=True)
    bot_help.add_field(name="/play", value="This plays the audio file  per linked URL in the voice channel\n"
                                       "/play [URL]", inline=True)
    bot_help.add_field(name="/pause", value="This pauses the audio in the voice channel", inline=True)
    bot_help.add_field(name="/resume", value="This resumes the audio in the voice channel", inline=True)
    bot_help.add_field(name="/stop", value="This stops the audio in the voice channel", inline=True)
    bot_help.add_field(name="/meme", value="This will post an embed into the discord\n"
                                       "/meme [user] [desc] [URL]", inline=True)
    # embed.set_footer()
    await ctx.send(embed=bot_help)


@bot.command(pass_contect=True, aliases=['y', 'ytd'])
async def ytdownload(ctx, url: str):
    await ctx.send("Getting everything ready now")
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        # 'verbose': True,
        # 'forcetitle': True,
        'postprocessors':
            [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now")
        print('------')
        ydl.download([url])
        print(f"Downloaded File")
        print('------')

    # Uncomment to send over channel
    # for file in os.listdir("./"):
    #     if file.endswith(".mp3"):
    #         name = file
    #
    #         try:
    #             await ctx.channel.send(file=discord.File(file))
    #         except discord.errors.HTTPException as HTTP:
    #             print("File too large to send")
    #             print('------')


# @bot.command(pass_context=True, aliases=['j', 'joi'])
# async def join(ctx):
#     channel = ctx.message.author.voice.channel
#     voice = get(bot.voice_clients, guild=ctx.guild)
#     if voice and voice.is_connected():
#         await voice.move_to(channel)
#     else:
#         voice = await channel.connect()
#     print(f"The bot has connected to {channel}")
#     print('------')
#     await ctx.send(f"{bot.user.name} joined {channel}")


@bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        print('------')
        await ctx.send(f"{bot.user.name} has left {channel}")
    else:
        print(f"The bot is not in {channel}")
        print('------')
        await ctx.send(f"{bot.user.name} is not in {channel}")


@bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):
    try:
        song_there = os.path.isfile("song.mp3")
        if song_there:
            os.remove("song.mp3")
            print("removed old song file")
    except PermissionError:
        print("Trying to delete song file, but its being played")
        await ctx.send("ERROR: Music playing")
        return

    try:
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild=ctx.guild)
    except AttributeError as voiceError:
        print("Bot can't connect to voice channel!!!")
        # await ctx.send("You have to be in a voice channel you idiot :)")
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    print(f"The bot has connected to {channel}")
    print('------')
    # await ctx.send("Getting everything ready now")
    voice = get(bot.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now")
        print('------')
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} has finished playing"))
    print('------')
    voice.source = discord.PCMVolumeTransformer(voice.source)
    # make this a bit louder
    voice.source.volume = 0.2

    nname = name.rsplit("~", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print(f"Playing: {nname[0]}")
    print('------')


@bot.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        print("Music paused")
        print('------')
        voice.pause()
        await ctx.send("Music paused")
    else:
        print("Music can't be paused")
        print('------')
        await ctx.send("Music can't be paused")


@bot.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_paused():
        print("Music resumed")
        print('------')
        voice.resume()
        await ctx.send("Music resumed")
    else:
        print("Music not paused")
        print('------')
        await ctx.send("Music is not paused")


@bot.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        print("Music stopped")
        print('------')
        voice.stop()
        await ctx.send("Music stopped")
    else:
        print("Music is not playing")
        print('------')
        await ctx.send("Music is not playing")

if __name__ == "__main__":
    main()
