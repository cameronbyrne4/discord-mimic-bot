import discord
from discord.ext import commands, tasks
import os
from datetime import datetime
from ..services.ai_service import AIService
from ..services.message_service import MessageService

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

ai_service = AIService()
message_service = MessageService()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    scheduled_messages.start()

@bot.command(name='chat')
async def chat(ctx, *, message: str):
    try:
        # Process message with AI
        response = await ai_service.get_response(message, str(ctx.author.id))
        
        # Store in history
        await message_service.save_message(str(ctx.author.id), message, response)
        
        # Send response
        await ctx.send(response)
        
        # Maybe send a GIF
        #gif_url = await ai_service.get_gif(response)
        #if gif_url:
            #await ctx.send(gif_url)
    
    except Exception as e:
        await ctx.send("Sorry, I encountered an error. Please try again later.")
        print(f"Error in chat: {e}")

@tasks.loop(minutes=30)
async def scheduled_messages():
    scheduled = await message_service.get_scheduled_messages()
    for msg in scheduled:
        channel = bot.get_channel(int(msg['channel_id']))
        if channel:
            await channel.send(msg['content'])

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

async def start_bot():
    await bot.start(os.getenv('DISCORD_TOKEN'))