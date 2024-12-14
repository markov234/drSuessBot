import discord
from discord.ext import commands
from openai import OpenAI
import os
from dotenv import load_dotenv

# Setup api key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
discord_bot_key = os.getenv("DISCORD_BOT_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Call OpenAI API
def call_llm(prompt):
    try: 
        # Send the prompt to OpenAI
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo", # 20-30x cheaper than 'gpt-4'
            # system content tells the AI how to behave. user prompt is what the end user requests of the bot.
            messages = [
                {"role": "system", "content": "You are an AI that writes like Dr. Suess and responds in 4 line couplets."}, 
                {"role": "user", "content": prompt}
            ]
        )
        # Extract and return the generated response
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in call_llm: {e}")  # Debug: Print the error
        return f"An error occurred: {e}"


# Initialize the bot with default and then your specific intents.
# Intents are what the bot is allowed to respond to (eg, messages, polls, presenece of a user, etc)
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Event listener for when the bot is ready
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

# Event listener for when a message is sent in the chat
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages from the bot itself
    
    if bot.user.mentioned_in(message):  # Check if the bot is mentioned in the message
        user_input = message.content.replace(f"<@!{bot.user.id}>", "").replace(f"<@{bot.user.id}>", "").strip()
        if user_input:
            response = call_llm(user_input)
            await message.channel.send(response)

# Run the bot
bot.run(discord_bot_key)
