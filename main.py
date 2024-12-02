# when making the source code public, delete this token :D
import discord
from discord.ext import commands
import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

discordAPI = os.getenv('DISCORD_TOKEN')
openAIKey = os.getenv('OPEN_AI_KEY')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Command to chat with OpenAI@bot.command(name='chat')


@bot.command()
async def gpt(ctx: commands.Context, *, prompt: str):
    # Ensure your API key is securely managed
    # Replace this with your method of retrieving the API key
    openAIKey = os.getenv("OPEN_AI_KEY")

    if not openAIKey:
        await ctx.reply("OpenAI API key is not set. Please configure it.")
        return

    async with aiohttp.ClientSession() as session:
        payload = {
            'model': 'gpt-4o-mini',  # Use the 4o-mini chat-based model
            'messages': [
                # Optional system message for context
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}  # User's input prompt
            ],
            'temperature': 0.9,
            'max_tokens': 60,
            'presence_penalty': 0,
            'frequency_penalty': 0
        }
        headers = {'Authorization': f'Bearer {openAIKey}'}

        try:
            async with session.post('https://api.openai.com/v1/chat/completions', json=payload, headers=headers) as resp:
                if resp.status != 200:
                    # Handle HTTP errors
                    error_details = await resp.text()
                    await ctx.reply(f"API Error: {resp.status}\nDetails: {error_details}")
                    return

                response = await resp.json()

                if 'choices' in response and len(response['choices']) > 0:
                    # Extract and send the response
                    response_text = response['choices'][0]['message']['content'].strip(
                    )
                    embed = discord.Embed(
                        title="Chat GPT's Response:",
                        description=response_text
                    )
                    await ctx.reply(embed=embed)
                else:
                    # Handle unexpected response structure
                    await ctx.reply("No valid response received from the API.")
                    print("Unexpected API Response:", response)

        except Exception as e:
            # Handle any exceptions during the request
            await ctx.reply(f"An error occurred: {str(e)}")
            print(f"Exception: {e}")


@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.name}!')


@bot.command(name='add')
async def add(ctx, x: int, y: int):
    result = x + y
    await ctx.send(f'The result is {result}')

# Run the bot
bot.run(discordAPI)
