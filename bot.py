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
    "https://cdn.discordapp.com/attachments/1453222739501383780/1541938665062801469/IMG_3343.jpg?ex=6a8f69c9&is=6a8e1849&hm=9c919774f6bd177ad4bea2c508f33272415f2d924be3a2ba5b5f0ef7a3a30bba&",
    "https://cdn.discordapp.com/attachments/1453222739501383780/1530494775323525211/IMG_2183.jpg?ex=6a8f4f15&is=6a8dfd95&hm=490bab817dc03e6907a44eff34cba5d22dae958ca984ab73204ac116232fca1f&",
    "https://cdn.discordapp.com/attachments/1453222739501383780/1530494774740783114/IMG_2181.jpg?ex=6a8f4f15&is=6a8dfd95&hm=35cf0fc8cd7e03f4ce5a45d766f4634e100d8b96a09e756f74f226ad670876a4&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1541967761868324944/2UmjVh4g.jpg?ex=6a8f84e2&is=6a8e3362&hm=49271b022aeb2b6e94264b69dd047b0a348407b4b9cdfd7d71f30b19dd28109f&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1541967762337824899/2xJPsUN3.jpg?ex=6a8f84e2&is=6a8e3362&hm=d1e13d9d0e8caeb1637bea0e509ab208f8638664dc73924f19b9d9dd56e39708&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1541967762815979601/3nbgUAVb.jpg?ex=6a8f84e3&is=6a8e3363&hm=a55e64178de35d6e2014c708613a7728c6934145edb06429147391e53ea51511&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1541967763306971236/4EXEn8yD.jpeg?ex=6a8f84e3&is=6a8e3363&hm=0057833af4d3798afae6ba846fe72bbf972790af4b81a7d6c0c0031b7b4e7e1e&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1541967765047476234/4lZSx0XG.jpeg?ex=6a8f84e3&is=6a8e3363&hm=b05897698886ce43371103af966d1bb44831003078e82f44a7da260d0b73fd6b&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1541967765802586212/5RK0FCoJ.jpg?ex=6a8f84e3&is=6a8e3363&hm=fb8e77694b170b1a62c590099a9636762e175941adf4816623849ad64243685d&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1541967766318354482/0noIeeM4.jpeg?ex=6a8f84e3&is=6a8e3363&hm=44ca2efb163ef63568be5a94da1d6cdffa0c89244b0a573956cac7e6de157d43&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1541967766779723856/0OmsWJBw.jpeg?ex=6a8f84e3&is=6a8e3363&hm=0ef31b4bf313720fa3a835fa05781a17558e48b45ffe9ab9680d4807fda0edac&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1541968553526427779/aZqGLvpa.jpg?ex=6a8f859f&is=6a8e341f&hm=8ae991afa4a661cbf08faff7200eda310c1954a33526a7770f8c7cc890c562ad&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1541968553958187149/Bbln0xO9.jpg?ex=6a8f859f&is=6a8e341f&hm=ac7b3553b8d1164ff2131f0d84a13a672d2e7bc8fc84b080d27c3fde504b6f78&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1541968555019599932/bXGez6gt.jpeg?ex=6a8f859f&is=6a8e341f&hm=32df9aa43b937828f9bba56ad33355462baa3e6001ddfff22a7be091b716ffca&"
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
    CHANNEL_ID = 1541946565344759818  
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
    await daily_announcement()
    await bot.close()


# ⚠️ RECOLEZ ICI VOTRE TOKEN DU DEVELOPER PORTAL
bot.run('MTU0MTk0NDEzNjk2NDUwNTY1MA.GLTIZc.3aE9XTN8jJzZ-oLErakWkryQP227m1wJptpflU')
