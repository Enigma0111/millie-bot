import datetime
import os
import discord
from discord.ext import commands, tasks

# Configuration des permissions globales du bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================================================================
# 1. CONFIGURATION POUR : MILLIE GAMES
# =========================================================================
CHANNEL_MILLIE_ID = 1541946565344759818  # Votre ID unique de salon
ROLE_MILLIE_NAME = "Millie Games"        # Nom exact du rôle
INDEX_MILLIE_FILE = "index_millie.txt"   # Fichier mémoire pour Millie

# 🖼️ Vos 11 images d'origine pour Millie Games
IMAGE_LIST_MILLIE = [
    "https://cdn.discordapp.com/attachments/1389037044466061334/1541967761868324944/2UmjVh4g.jpg?ex=6a8f84e2&is=6a8e3362&hm=49271b022aeb2b6e94264b69dd047b0a348407b4b9cdfd7d71f30b19dd28109f&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1541967762337824899/2xJPsUN3.jpg?ex=6a8f84e2&is=6a8e3362&hm=d1e13d9d0e8caeb1637bea0e509ab208f8638664dc73924f19b9d9dd56e39708&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1541967762815979601/3nbgUAVb.jpg?ex=6a8f84e3&is=6a8e3363&hm=a55e64178de35d6e2014c708613a7728c6934145edb06429147391e53ea51511&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1541967763306971236/4EXEn8yD.jpeg?ex=6a8f84e3&is=6a8e3363&hm=0057833af4d3798afae6ba846fe72bbf972790af4b81a7d6c0c0031b7b4e7e1e&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1541967765047476234/4lZSx0XG.jpeg?ex=6a8f84e3&is=6a8e3363&hm=b05897698886ce43371103af966d1bb44831003078e82f44a7da260d0b73fd6b&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1541967765802586212/5RK0FCoJ.jpg?ex=6a8f84e3&is=6a8e3363&hm=fb8e77694b170b1a62c590099a9636762e175941adf4816623849ad64243685d&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1541967766779723856/0OmsWJBw.jpeg?ex=6a8f84e3&is=6a8e3363&hm=0ef31b4bf313720fa3a835fa05781a17558e48b45ffe9ab9680d4807fda0edac&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1541968553526427779/aZqGLvpa.jpg?ex=6a8f859f&is=6a8e341f&hm=8ae991afa4a661cbf08faff7200eda310c1954a33526a7770f8c7cc890c562ad&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1541968553958187149/Bbln0xO9.jpg?ex=6a8f859f&is=6a8e341f&hm=ac7b3553b8d1164ff2131f0d84a13a672d2e7bc8fc84b080d27c3fde504b6f78&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1541968553958187149/Bbln0xO9.jpg?ex=6a8f859f&is=6a8e341f&hm=ac7b3553b8d1164ff2131f0d84a13a672d2e7bc8fc84b080d27c3fde504b6f78&",
    "https://cdn.discordapp.com/attachments/1453222739501383780/1541938665062801469/IMG_3343.jpg?ex=6a901289&is=6a8ec109&hm=f6ce4477b0aee2875a0ad9db4f7ad01a97138d7ca7f73729d6de7e055c789d81&"
]

# =========================================================================
# 2. CONFIGURATION POUR : EYE CONTACT
# =========================================================================
# 🔴 REMPLACEZ LE NUMÉRO CI-DESSOUS PAR L'ID DE VOTRE SALON EYE CONTACT 
CHANNEL_EYE_ID = 112233445566778899     
ROLE_EYE_NAME = "Eye Contact"           # Nom exact du rôle
INDEX_EYE_FILE = "index_eye.txt"        # Fichier mémoire pour Eye Contact
IMAGE_LIST_EYE = [
    "https://discordapp.com"  # Image exemple à changer !
]

# =========================================================================
# LOGIQUE DE ROTATION AUTOMATIQUE
# =========================================================================
def get_next_image_url(image_list, index_file):
    if not image_list:
        return "https://example.com"
    index = 0
    if os.path.exists(index_file):
        try:
            with open(index_file, "r") as f:
                index = int(f.read().strip())
        except ValueError:
            index = 0
    if index >= len(image_list):
        index = 0
    image_url = image_list[index]
    next_index = (index + 1) % len(image_list)
    with open(index_file, "w") as f:
        f.write(str(next_index))
    return image_url

# =========================================================================
# SYSTEME D'ENVOI SIMULTANÉ (PARFAITEMENT ALIGNÉ)
# =========================================================================
async def send_all_announcements():
    # 📢 Partie 1 : Envoi dans Millie Games
    try:
        channel_millie = await bot.fetch_channel(CHANNEL_MILLIE_ID)
        role_millie = discord.utils.get(channel_millie.guild.roles, name=ROLE_MILLIE_NAME)
        embed_m = discord.Embed(description="did u cum on this pic today?", color=discord.Color.purple())
        embed_m.set_image(url=get_next_image_url(IMAGE_LIST_MILLIE, INDEX_MILLIE_FILE))
        mention_m = f"📢 {role_millie.mention} Daily Offering!" if role_millie else f"📢 **{ROLE_MILLIE_NAME}** Daily Offering!"
        msg_m = await channel_millie.send(content=mention_m, embed=embed_m)
        await msg_m.add_reaction("💦")
        print("Millie Games envoyé avec succès !")
    except Exception as e:
        print(f"Erreur Millie Games: {e}")

    # 📢 Partie 2 : Envoi dans Eye Contact
    try:
        channel_eye = await bot.fetch_channel(CHANNEL_EYE_ID)
        role_eye = discord.utils.get(channel_eye.guild.roles, name=ROLE_EYE_NAME)
        embed_e = discord.Embed(description="will you stand this eye contact with millie ?", color=discord.Color.blue())
        embed_e.set_image(url=get_next_image_url(IMAGE_LIST_EYE, INDEX_EYE_FILE))
        mention_e = f"📢 New update for {role_eye.mention}!" if role_eye else f"📢 New update for **{ROLE_EYE_NAME}**!"
        msg_e = await channel_eye.send(content=mention_e, embed=embed_e)
        await msg_e.add_reaction("💦")
        print("Eye Contact envoyé avec succès !")
    except Exception as e:
        print(f"Erreur Eye Contact: {e}")

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")
    await send_all_announcements()
    await bot.close()

bot.run('MTU0MTk0NDEzNjk2NDUwNTY1MA.GLTIZc.3aE9XTN8jJzZ-oLErakWkryQP227m1wJptpflU')
