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

# Will always be at the top and bottom of the hour
@tasks.loop(minutes=30)
async def scheduled_messages():
    current_time = datetime.now()
    pst_hour = (current_time.hour - 7) % 24  # Convert to PST from UTC
    
    # Morning message around 10 AM PST
    if pst_hour == 10:
        channels = bot.get_all_channels()
        morning_msg = await ai_service.get_response(
            "Generate a good morning message and ask what they're up to today", 
            "scheduled_bot"
        )
        for channel in channels:
            if isinstance(channel, discord.TextChannel):
                await channel.send(morning_msg)
    
    # Night message around 1 AM PST
    if pst_hour == 1:
        channels = bot.get_all_channels()
        night_msg = await ai_service.get_response(
            "Generate a good night message and ask what they did today", 
            "scheduled_bot"
        )
        for channel in channels:
            if isinstance(channel, discord.TextChannel):
                await channel.send(night_msg)

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

async def start_bot():
    await bot.start(os.getenv('DISCORD_TOKEN'))