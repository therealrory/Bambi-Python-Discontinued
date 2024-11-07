# bot.py
# Made by thereal.rory
import os
import discord
import math
import random
from discord import Intents
from discord.ext import commands
from datetime import timedelta, datetime
from dotenv import load_dotenv # type: ignore

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Create intents for the client
intents = Intents.default()
intents.guilds = True  # Enable guild events
intents.members = True  # Enable member events
intents.message_content = True # Enable reading messages


client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    channel = client.get_channel(1263460611216379955)
    
    if channel is not None:
        await channel.send(
            f'Hi {member.name}, welcome to my Discord server!'
        )
    else:
        print("Channel not found.")

boocounter = 0

@client.event
async def on_message(message):
    global boocounter
    if message.author == client.user:
        return

    responseone = "Tac"
    responsetwo = ["AAAAAAAAAAAAAAAAAAHHHHHHHH!!!!", "AHHH!!!", "Ahh!", "Ah", "..."]
    responsethree = ["Woof!", "Bark!", ":3"]
    responsefour = "Oi oi oi..."
    responsefive = "What?"

    print(f"Message received: {message.content}")  # Debugging line

    if message.content == 'Tic':
        print("Response:" + responseone)
        await message.channel.send(responseone)  # Ensure to 'await' the send
    elif message.content == "Boo":
        if boocounter == 0:
            await message.channel.send(responsetwo[0])  # Send first message
        elif boocounter == 1:
            await message.channel.send(responsetwo[1])  # Send second message
        elif boocounter == 2:
            await message.channel.send(responsetwo[2])  # Send third message
        elif boocounter == 3:
            await message.channel.send(responsetwo[3])  # Send fourth message
        elif boocounter >= 4:
            await message.channel.send(responsetwo[4])  # Send fifth message

        boocounter += 1
    elif message.content == "Bambi is a good boy":
        randomresponse = random.choice(responsethree)
        print("Response: " + randomresponse)
        await message.channel.send(randomresponse)
    elif message.content == "Baka":
        print("Response: " + responsefour)
        await message.channel.send(responsefour)
    elif message.content == "@Bambi#0196":
        print("Response: " + responsefive)
    elif message.content == 'raise-exception':
        raise discord.DiscordException

    await client.process_commands(message)

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

@client.command(name='kick')
@commands.has_permissions(kick_members=True)  # Ensures the user has permission to kick members
async def kick(ctx, member: discord.Member, *, reason=None):
    """Kicks a member from the server."""
    try:
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention} for reason: {reason}')
    except discord.Forbidden:
        await ctx.send("I do not have permission to kick this member.")
    except discord.HTTPException:
        await ctx.send("I was unable to kick the member.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@client.command(name="timeout")
@commands.has_permissions(moderate_members=True)
async def kick(ctx, member: discord.Member, duration: int,  *, reason=None):
    """Timeouts a member from the server"""
    try:
        timeout_end = discord.utils.utcnow() + timedelta(seconds=duration)

        await member.edit(timed_out_until=timeout_end, reason=reason)

        await ctx.send(f'{member.mention} has been timeouted for {duration} seconds. Reason: {reason or 'No reason was provided'}')

    except discord.Forbidden:
        await ctx.send("I do not have permission to timeout this member.")
    except discord.HTTPException:
        await ctx.send("There was an error trying to timeout the member.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


client.run(TOKEN)