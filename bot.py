import os
import re
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_NAME = "bot-test"


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def count(ctx, emoji: str):
    # find the swear-jar channel in this server
    channel = discord.utils.get(ctx.guild.text_channels, name=CHANNEL_NAME)
    if channel is None:
        await ctx.send(f"I can't find a channel named #{CHANNEL_NAME}.")
        return

    total = 0
    async for message in channel.history(limit=None):
        # count the emoji inside messages (skip bots and commands)
        if not message.author.bot and not message.content.startswith("!"):
            total += message.content.count(emoji)

        # count the emoji as a reaction
        for reaction in message.reactions:
            if str(reaction.emoji) == emoji:
                total += reaction.count

    await ctx.send(f"{total} {emoji}")


# Token comes from the DISCORD_TOKEN variable, or from a file called token.txt
token = os.environ.get("DISCORD_TOKEN")
if not token:
    with open("token.txt") as f:
        token = f.read().strip()

bot.run(token)
