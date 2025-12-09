import discord
from discord.ext import commands

# ==============================
# PUT TOKEN + HER USER ID HERE
# ==============================
BOT_TOKEN = os.getenv("BOT_TOKEN")          # <-- paste your token
TARGET_USER_ID = H514343791797338113         # <-- put her Discord ID (numbers only)
# Example: TARGET_USER_ID = 123456789012345678

# ==============================
# BOT SETUP
# ==============================
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

ticket_channel = None  # will store the created ticket channel

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

# =======================================
# OPEN TICKET COMMAND
# =======================================
@bot.command()
async def openticket(ctx):
    global ticket_channel

    guild = ctx.guild
    user = await bot.fetch_user(TARGET_USER_ID)

    # Create ticket channel
    ticket_channel = await guild.create_text_channel(f"ticket-{user.name}")
    await ticket_channel.send(
        f"💬 Ticket opened to chat with **{user.name}**.\n"
        f"Type messages here and I will DM her."
    )
    await ctx.send("✅ Ticket created!")

# =======================================
# DM RELAY SYSTEM
# =======================================
@bot.event
async def on_message(message):
    global ticket_channel

    # Ignore bot messages
    if message.author == bot.user:
        return

    # ========== MESSAGE FROM TICKET → DM HER ==========
    if ticket_channel and message.channel == ticket_channel and not message.author.bot:
        user = await bot.fetch_user(TARGET_USER_ID)
        await user.send(message.content)
        return

    # ========== MESSAGE FROM HER DM → SEND TO TICKET ==========
    if message.author.id == TARGET_USER_ID and isinstance(message.channel, discord.DMChannel):
        if ticket_channel:
            await ticket_channel.send(f"**Her:** {message.content}")
        return

    await bot.process_commands(message)

# RUN BOT
bot.run(BOT_TOKEN)

