import os
import discord
import google.generativeai as genai

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not DISCORD_TOKEN or not GEMINI_API_KEY:
    raise RuntimeError("Missing environment variables")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()
        if not prompt:
            return

        async with message.channel.typing():
            try:
                response = model.generate_content(prompt)
                await message.reply(response.text)
            except Exception as e:
                await message.reply("⚠️ Error processing your request.")
                print(e)

client.run(DISCORD_TOKEN)
