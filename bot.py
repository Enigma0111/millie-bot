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
CHANNEL_EYE_ID = 1542149705038037082     
ROLE_EYE_NAME = "Millie Eye Contact"           # Nom exact du rôle
INDEX_EYE_FILE = "index_eye.txt"        # Fichier mémoire pour Eye Contact
IMAGE_LIST_EYE = [
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542152900216750090/6f6cc66c9bcc5a5ad80df6ae72d3f8c5.jpg?ex=6a90314f&is=6a8edfcf&hm=a0093a78a82ad5ebec794a048ef84570b7ce9010e11b776b59e16c58993acca9&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542152899814227968/7736387b10ccfe9e298d2b008a975f8b.jpg?ex=6a90314f&is=6a8edfcf&hm=d49bab1933e4970e32fd99ee2aa2cace7cf88760961fdc94eabe5f50816caf9a&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542152899449061547/cd92575abe304a4ef132edf99a481727.jpg?ex=6a90314f&is=6a8edfcf&hm=52a6a17758d03b71381b66112ea0659243b8c536898046445444951bb0e35245&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542152899147075714/825e382945e0fde9556072ee644b345e.jpg?ex=6a90314e&is=6a8edfce&hm=804a3eae3e90240fc47c7ebc8bc6381c3d1498c1abe5a648b93a4dcd1580ccb4&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542152898836955206/637a8c1489d08e685c2298ecb48e1e9a.jpg?ex=6a90314e&is=6a8edfce&hm=1b473768e37a16aff015d9174a2bed9296c282bd5d9247c9cd1f2ff7fbd81501&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542152898572460054/725c0d08ab475ab19869a3bc5637e719.jpg?ex=6a90314e&is=6a8edfce&hm=cd1fd74b19d541b4cdf61a06ba4ba208788702d819f26b341842f84cae7ccb98&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542152898157346986/5c4d22a805906cdd84d1614c3dc225a0.jpg?ex=6a90314e&is=6a8edfce&hm=324eb31866e0ba4eb0e52e0a36a74c16e7813bd83dfad67c450e704128d83b1a&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542152897758896148/0004d39ed706a2f2509fc6703e41c5cc.jpg?ex=6a90314e&is=6a8edfce&hm=215eda70ce840076039caa58ad70ae78cb4a05cc99c23845522730c7658327eb&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542153702574653491/ecb7d22f0fe58189d27343bd9fbbaf20.jpg?ex=6a90320e&is=6a8ee08e&hm=247d0fb819072020f5777e221c89fe01aadecc4d3c38b163d04d60d4a836f5fc&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542153702109093918/ad0945d489f20d24a02b5c159a782184.jpg?ex=6a90320e&is=6a8ee08e&hm=eb6c745b45e293a6e765d65c71836f829193088a894b645cee4d60f2b3446233&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542153701756768256/075c725d353e54c258f8d6e6ef0c93bd.jpg?ex=6a90320e&is=6a8ee08e&hm=796a46c79f6f2fcf3642e1ac4a0a1aa65ba8ac661c43d09062802c72a46be198&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542153701408514070/6f8bc91df7ff08aa1ea42b55e36e72b5.jpg?ex=6a90320e&is=6a8ee08e&hm=d7f414dcbc6eef3b67c43ca0d71e033d4210728c60c54142281b4f4cc50329e2&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542153701114781746/b8b787934830270c3b3209fb20eea050.jpg?ex=6a90320e&is=6a8ee08e&hm=01088d9058d6057549c25448c0b4985e1823383cbbe765fb983a997e216e6cae&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542153700724834485/b7fe66217068cba1d37015b503be2fbc.jpg?ex=6a90320e&is=6a8ee08e&hm=bef51a0c2289785a4c61943269a2a0ba90e92ed058043a427374f720a212ee6b&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542153700347351041/32b7eacc6aaab14ebec02a4594175ba8.jpg?ex=6a90320d&is=6a8ee08d&hm=4de396c49f19205566b3c0c02a37f4ecf4f161089b4bfb8d85a43ecfec25d036&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542153700007481445/8a0b33f46f53b89cc4e97ea387508a69.jpg?ex=6a90320d&is=6a8ee08d&hm=386327a464b0f18ef961377f7a6b9029173a68e452c5d44aca9bc2852b079a41&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542153699625934859/download_2.png?ex=6a90320d&is=6a8ee08d&hm=89cda4d6e413d2f6398b76784056fef6a0a73417581347a2c79854b4365c7a20&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542153699227607110/8e04e5baa889b83662fbcf7b42317c20.jpg?ex=6a90320d&is=6a8ee08d&hm=7f3a7aa660b47f4ea6fbf1ce2a9db6acb373fbbeeb25976e090d7720536c5091&"
]

CHANNEL_RANKING_ID = 1542324573826191430  # 🔴 Clic droit sur Discord -> Copier l'ID de #daily-ranking
ROLE_RANKING_NAME = "Daily Ranking"      # Nom exact du rôle
INDEX_RANKING_FILE = "index_ranking.txt"
IMAGE_LIST_RANKING = [
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542327238173659156/66202be24472d906b4fa88be6322e7b8.jpg?ex=6a90d3ac&is=6a8f822c&hm=204204f54ba1410922213230e2658219e8e43fd6d0fdad6a9d5d8ba1be95f707&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542327237494440016/1d4add4a7f01edab34c61592e8cdd3e7.jpg?ex=6a90d3ac&is=6a8f822c&hm=4e7666dc5d75272d4046492dcdf41efa6c5e3a5d1ef10a3b2a1cc87221b4b6a9&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542327237095989338/fde43b7fbf87b89de3f9d39295aaef8b.jpg?ex=6a90d3ac&is=6a8f822c&hm=eccf74418b2b62675c5160196e512ce01fc88f2340a5944c5f70896ef508286d&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542327236668039278/cce539c32bba35539d637ab9bbbd9f88.jpg?ex=6a90d3ac&is=6a8f822c&hm=d57af02e5eb2cb81974ef55bd43d2a9c18cb547c3ca6d1fd91f2082b134034d0&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542327236357521418/e4585c2d0105be9b329ac34a02584d78.jpg?ex=6a90d3ac&is=6a8f822c&hm=04e97f0ec468eca89027ed49f48add21fba3a2ec8a2b876b11ef309a5be46321&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542327236009529424/a4ba003355cc2315a4d3390e720972ff.jpg?ex=6a90d3ac&is=6a8f822c&hm=c447c69bad8c5be998bd8301f3adfaff462b2825415c0bd8632e95b35a9a9c33&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542327235640565871/d3bbe023f2dceba6372966f930b0b656.jpg?ex=6a90d3ac&is=6a8f822c&hm=492380f5c2aed3cd23a125abe786ecbfe846b0ce6a1f502d962e31a80d94b70f&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542327235317338162/972bed0219e1b2b6fe1399ebac779002.jpg?ex=6a90d3ab&is=6a8f822b&hm=60de36d0d06224f0d286deeb9031817f0d0c051143e4bed05d4f2c3c7841c2b5&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542327235036577832/ed50e5b73d0c276fc45e11b3c307a26f.jpg?ex=6a90d3ab&is=6a8f822b&hm=f6c7ee25da7a83bee331b4e57802a7afcdfde48911c7753b91c7830b08fd15d0&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542327234692517908/170983c43721190ac273217ed544e25a.jpg?ex=6a90d3ab&is=6a8f822b&hm=603164401bccdbd9be45047a0a4924d6aa88be627161b0d6669a7e3698f89a79&",
    "https://cdn.discordapp.com/attachments/1389037044466061334/1542334168464105493/500fd7e1070b6cc6651e272b376fe620.jpg?ex=6a90da20&is=6a8f88a0&hm=c65747fbada35d541cda9f929222b2a458a949c8526d28c55b8b19d6ba32e697&"
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
        await msg_e.add_reaction("✅")
        await msg_e.add_reaction("❌")
        print("Eye Contact envoyé avec succès !")
    except Exception as e:
        print(f"Erreur Eye Contact: {e}")

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")
    
    # Calcul de l'heure française actuelle (UTC + 2h en été)
    import datetime
    current_hour = (datetime.datetime.utcnow() + datetime.timedelta(hours=2)).hour
    print(f"Heure actuelle en France : {current_hour}h")

    # ⏰ Déclencheur du Milieu de la Nuit (4h00 du matin) -> Envoie Daily Ranking
    if 3 <= current_hour <= 5:
        try:
            channel_rank = await bot.fetch_channel(CHANNEL_RANKING_ID)
            role_rank = discord.utils.get(channel_rank.guild.roles, name=ROLE_RANKING_NAME)
            embed_r = discord.Embed(description="rate this from 1-10🔟", color=discord.Color.gold())
            embed_r.set_image(url=get_next_image_url(IMAGE_LIST_RANKING, INDEX_RANKING_FILE))
            mention_r = f"📢 {role_rank.mention} Daily Offering!" if role_rank else f"📢 **{ROLE_RANKING_NAME}** Daily Offering!"
            msg_r = await channel_rank.send(content=mention_r, embed=embed_r)
            
            # Ajout automatique des 10 boutons de notation
            await msg_r.add_reaction("1️⃣")
            await msg_r.add_reaction("2️⃣")
            await msg_r.add_reaction("3️⃣")
            await msg_r.add_reaction("4️⃣")
            await msg_r.add_reaction("5️⃣")
            await msg_r.add_reaction("6️⃣")
            await msg_r.add_reaction("7️⃣")
            await msg_r.add_reaction("8️⃣")
            await msg_r.add_reaction("9️⃣")
            await msg_r.add_reaction("🔟")
            print("Daily Ranking envoyé avec succès !")
        except Exception as e:
            print(f"Erreur Daily Ranking: {e}")

    # ⏰ Déclencheur du Matin (6h00) -> Envoie uniquement Millie Games
    elif 5 <= current_hour <= 7:
        await daily_announcement()

    # ⏰ Déclencheur de la Matinée (10h00) -> Envoie uniquement Eye Contact
    elif 9 <= current_hour <= 11:
        try:
            channel_eye = await bot.fetch_channel(CHANNEL_EYE_ID)
            role_eye = discord.utils.get(channel_eye.guild.roles, name=ROLE_EYE_NAME)
            embed_e = discord.Embed(description="will you stand this eye contact with millie ?", color=discord.Color.blue())
            embed_e.set_image(url=get_next_image_url(IMAGE_LIST_EYE, INDEX_EYE_FILE))
            mention_e = f"📢 {role_eye.mention} Daily Offering!" if role_eye else f"📢 **{ROLE_EYE_NAME}** Daily Offering!"
            msg_e = await channel_eye.send(content=mention_e, embed=embed_e)
            await msg_e.add_reaction("💦")
            print("Eye Contact envoyé à 10h !")
        except Exception as e:
            print(f"Erreur Eye Contact: {e}")

    # Fermeture propre de la session
    await bot.close()

bot.run('MTU0MTk0NDEzNjk2NDUwNTY1MA.GLTIZc.3aE9XTN8jJzZ-oLErakWkryQP227m1wJptpflU')
