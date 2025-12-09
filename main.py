import os
import discord
from discord.ext import commands

# ==============================
#  SECRET TOKEN VIA ENV (RENDER)
# ==============================
BOT_TOKEN = os.getenv("BOT_TOKEN")          # comes from Render Environment
TARGET_USER_ID = 1345360711664013332        # put her numeric Discord ID

# Example:
# TARGET_USER_ID = 123456789012345678

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

ticket_channel = None  # will store the created ticket channel


@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")


@bot.command()
async def openticket(ctx):
    global ticket_channel

    guild = ctx.guild
    user = await bot.fetch_user(TARGET_USER_ID)

    # create ticket channel
    ticket_channel = await guild.create_text_channel(f"ticket-{user.name}")
    await ticket_channel.send(
        f"💬 Ticket opened to chat with **{user.name}**.\n"
        f"Type messages here and I will DM her."
    )
    await ctx.send("✅ Ticket created!")


@bot.event
async def on_message(message):
    global ticket_channel

    # ignore bot messages
    if message.author == bot.user:
        return

    # 1) message from ticket channel → DM her
    if ticket_channel and message.channel == ticket_channel and not message.author.bot:
        user = await bot.fetch_user(TARGET_USER_ID)
        await user.send(message.content)
        return

    # 2) message from her DM → send to ticket channel
    if message.author.id == TARGET_USER_ID and isinstance(message.channel, discord.DMChannel):
        if ticket_channel:
            await ticket_channel.send(f"**Her:** {message.content}")
        return

    await bot.process_commands(message)


bot.run(BOT_TOKEN)
