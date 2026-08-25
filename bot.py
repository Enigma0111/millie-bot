import datetime
import os
import discord
from discord.ext import commands, tasks

# Configuration requirements
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Set the trigger time to 12:00 PM local time
TARGET_TIME = datetime.time(hour=12, minute=0, second=0)

# 1. ⚠️ YOUR IMAGE LINKS
IMAGE_LIST = [
    "https://cdn.discordapp.com/attachments/1453222739501383780/1541938665062801469/IMG_3343.jpg?ex=6a8f69c9&is=6a8e1849&hm=9c919774f6bd177ad4bea2c508f33272415f2d924be3a2ba5b5f0ef7a3a30bba&", "https://cdn.discordapp.com/attachments/1453222739501383780/1530494775323525211/IMG_2183.jpg?ex=6a8f4f15&is=6a8dfd95&hm=490bab817dc03e6907a44eff34cba5d22dae958ca984ab73204ac116232fca1f&", "https://cdn.discordapp.com/attachments/1453222739501383780/1530494774740783114/IMG_2181.jpg?ex=6a8f4f15&is=6a8dfd95&hm=35cf0fc8cd7e03f4ce5a45d766f4634e100d8b96a09e756f74f226ad670876a4&"
]

# File to remember which image index to use next
INDEX_FILE = "image_index.txt"

def get_next_image_url():
    if not IMAGE_LIST:
        return "https://example.com"
        
    index = 0
    if os.path.exists(INDEX_FILE):
        try:
            with open(INDEX_FILE, "r") as f:
                index = int(f.read().strip())
        except ValueError:
            index = 0

    if index >= len(IMAGE_LIST):
        index = 0

    image_url = IMAGE_LIST[index]
    next_index = (index + 1) % len(IMAGE_LIST)
    with open(INDEX_FILE, "w") as f:
        f.write(str(next_index))

    return image_url


@tasks.loop(time=TARGET_TIME)
async def daily_announcement():
    # ⚠️ YOUR DISCORD CHANNEL ID
    CHANNEL_ID = 154194656534475818  
    channel = bot.get_channel(CHANNEL_ID)

    if channel:
        role = discord.utils.get(channel.guild.roles, name="Millie Games")
        
        # Le texte à mettre dans l'embed
        message_text = "did u cum on this pic today?"
        
        image_url = get_next_image_url()
        
        # Création de l'encadré propre (Embed) pour masquer le lien
        embed = discord.Embed(description=message_text, color=discord.Color.purple())
        embed.set_image(url=image_url)

        # Envoi de la mention du rôle à l'extérieur de l'embed pour qu'elle ping bien les membres, suivie de l'embed
        mention_text = f"📢 New update for {role.mention}!" if role else "📢 New update for **Millie Games**!"
        sent_message = await channel.send(content=mention_text, embed=embed)
        await sent_message.add_reaction("💦")


# Commande secrète de test
@bot.command()
async def test(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Millie Games")
    message_text = "did u cum on this pic today?"
    
    image_url = get_next_image_url()
    
    embed = discord.Embed(description=message_text, color=discord.Color.purple())
    embed.set_image(url=image_url)

    mention_text = f"📢 New update for {role.mention}!" if role else "📢 New update for **Millie Games**!"
    sent_message = await ctx.send(content=mention_text, embed=embed)
    await sent_message.add_reaction("💦")


@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")
    if not daily_announcement.is_running():
        daily_announcement.start()


# ⚠️ RECOLEZ ICI VOTRE TOKEN DU DEVELOPER PORTAL
bot.run('MTU0MTk0NDEzNjk2NDUwNTY1MA.GLTIZc.3aE9XTN8jJzZ-oLErakWkryQP227m1wJptpflU')
