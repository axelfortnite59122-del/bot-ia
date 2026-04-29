import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from groq import Groq

# Charger le .env
load_dotenv()

# Debug
print("GROQ =", os.getenv("GROQ_API_KEY"))
print("DISCORD =", os.getenv("DISCORD_TOKEN"))

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not DISCORD_TOKEN:
    raise ValueError("❌ DISCORD_TOKEN manquant dans .env")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY manquant dans .env")

client = Groq(api_key=GROQ_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

REGLEMENT = """
Tu es un assistant IA FiveM RP pour le serveur Nebulix FA.

Réponds en français, simplement et clairement.
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

Si tu n'es pas sûr, dis au joueur de contacter le staff.
"""

@bot.event
async def on_ready():
    print(f"✅ Bot connecté : {bot.user}")

@bot.command(name="ia")
async def ia(ctx, *, question: str):
    await ctx.typing()

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
        await ctx.reply(f"🤖 {reponse[:1900]}")

    except Exception as e:
        await ctx.reply(f"❌ Erreur Groq : {e}")

@bot.command(name="regle")
async def regle(ctx, *, sujet: str):
    await ctx.invoke(ia, question=f"Explique cette règle FiveM RP : {sujet}")

@bot.command(name="rp")
async def rp(ctx, *, situation: str):
    await ctx.invoke(
        ia,
        question=f"Cette situation est-elle autorisée ou interdite en RP ? {situation}"
    )

bot.run(DISCORD_TOKEN)