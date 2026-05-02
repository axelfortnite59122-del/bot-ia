import os
import discord
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not DISCORD_TOKEN:
    raise ValueError("❌ DISCORD_TOKEN manquant")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY manquant")

client = Groq(api_key=GROQ_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

# 🔥 MET TES IDS DE SALONS ICI
CHANNEL_IDS = [
    1498944375613292656,
    1498877010548883576  # Remplace par l'ID du deuxième salon
]

REGLEMENT = """
Tu es un assistant IA FiveM RP pour le serveur Nebulix RP.

Tu réponds en français, simplement et clairement.
Tu aides les joueurs à comprendre les règles RP.

Règles importantes :
- Respect RP obligatoire
- No Fear interdit
- MetaGaming interdit
- PowerGaming interdit
- FreeKill interdit
- Pain RP obligatoire
- Respect du staff obligatoire
- Les scènes doivent rester cohérentes et réalistes
- Le serveur est créer sur la base Seed

Si tu n'es pas sûr, dis au joueur de contacter le staff.
"""

@bot.event
async def on_ready():
    print(f"✅ Bot connecté : {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # ✅ Vérifie si le message est dans un des salons autorisés
    if message.channel.id not in CHANNEL_IDS:
        return

    # ✅ Vérifie mention du bot
    if bot.user not in message.mentions:
        return

    # 🔧 Nettoie la question
    question = message.content
    question = question.replace(f"<@{bot.user.id}>", "")
    question = question.replace(f"<@!{bot.user.id}>", "")
    question = question.strip()

    if not question:
        await message.reply("❌ Pose une question après m'avoir mentionné.")
        return

    async with message.channel.typing():
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": REGLEMENT},
                    {"role": "user", "content": question}
                ],
                temperature=0.3,
                max_tokens=700
            )

            reponse = completion.choices[0].message.content
            await message.reply(f"🤖 {reponse[:1900]}")

        except Exception as e:
            await message.reply(f"❌ Erreur IA : {e}")

bot.run(DISCORD_TOKEN)
