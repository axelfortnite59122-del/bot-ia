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

CHANNEL_IDS = [
    1498944375613292656,
    1498877010548883576
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
- Le serveur est créé sur la base Seed

Informations spécifiques :
- Le Fondateur de Nebulix RP est Zenkyo.
- La base Seed est utilisée sur plusieurs serveurs GTA RP, comme Unity RP.
- Nebulix RP est créé sur la base Seed, mais chaque serveur peut la modifier avec ses propres scripts, règles, mappings et systèmes.

Si tu n'es pas sûr, dis au joueur de contacter le staff.
"""


def nettoyer_question(question: str) -> str:
    question = question.strip()
    return question


def contient_un_mot(question: str, mots: list[str]) -> bool:
    question = question.lower()
    return any(mot in question for mot in mots)


@bot.event
async def on_ready():
    print(f"✅ Bot connecté : {bot.user}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id not in CHANNEL_IDS:
        return

    if bot.user not in message.mentions:
        return

    question = message.content
    question = question.replace(f"<@{bot.user.id}>", "")
    question = question.replace(f"<@!{bot.user.id}>", "")
    question = nettoyer_question(question)

    if not question:
        await message.reply("❌ Pose une question après m'avoir mentionné.")
        return

    # 👑 Réponse automatique fondateur
    if contient_un_mot(question, ["fondateur", "créateur", "createur", "owner"]):
        await message.reply("👑 Le Fondateur de Nebulix RP est Zenkyo.")
        return

    # 🌱 Réponse automatique base Seed
    if contient_un_mot(question, ["base seed", "seed", "base du serveur"]):
        await message.reply(
            "🌱 D'après mes connaissances, la base Seed est utilisée sur plusieurs serveurs GTA RP, "
            "comme par exemple Unity RP.\n\n"
            "Nebulix RP est également créé sur la base Seed, mais chaque serveur peut la modifier "
            "avec ses propres scripts, règles, mappings et systèmes.\n\n"
            "Pour des informations plus précises sur la base Seed de Nebulix RP, contacte le staff."
        )
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

            reponse = completion.choices[0].message.content.strip()

            if not reponse:
                await message.reply("❌ Je n'ai pas réussi à générer une réponse.")
                return

            await message.reply(f"🤖 {reponse[:1900]}")

        except Exception as e:
            await message.reply(f"❌ Erreur IA : {e}")


bot.run(DISCORD_TOKEN)
