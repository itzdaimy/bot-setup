# Example script
# Made by daimy!
# https://discord.gg/dS7asSYg6M

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import sys
from discord import Embed
from flask import Flask, jsonify
from flask_cors import CORS
import threading
import asyncio
import logging
import time
import platform
import psutil
from datetime import datetime

if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()
#create a .env file with the bot token and application id

BOT_TOKEN = os.getenv('BOT_TOKEN')
APPLICATION_ID = os.getenv('APPLICATION_ID') 

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, application_id=APPLICATION_ID)

USER_ID = 00000000000 #change to your discord id

app = Flask(__name__)
CORS(app)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

start_time = time.time()

@app.route("/")
def hello():
    return "Polaris!"

@app.route("/uptime")
def uptime():
    uptime_seconds = time.time() - start_time
    days = int(uptime_seconds // (24 * 3600))
    hours = int((uptime_seconds % (24 * 3600)) // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    seconds = int(uptime_seconds % 60)

    uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
    return jsonify({"uptime": uptime_str})

async def main():
    initial_extensions = [
        'features.admin.admin',
        'features.admin.example'
    ]

    print("\n📦 Loading Extensions:")
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"   ✅ {extension}")
        except Exception as e:
            print(f"   ❌ {extension} - {e}")

    @bot.event
    async def on_ready():
        print(f"   ✅ API loaded!")
        print("\n🚀 Bot Ready!")
        print("=============================")
        try:
            synced = await bot.tree.sync()
            print(f"   ✅ {len(synced)} slash commands synced globally.")
        except Exception as e:
            print(f"   ❌ Failed to sync slash commands - {e}")

        print(f"   🤖 Logged in as: {bot.user.name} (ID: {bot.user.id})")
        print(f"   📊 Connected to {len(bot.guilds)} server(s).")
        print("=============================")

        uptime_duration = datetime.now() - datetime.fromtimestamp(start_time)
        total_seconds = int(uptime_duration.total_seconds())
        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        uptime_str = (
            f"{days}d {hours}h {minutes}m {seconds}s"
            if days > 0
            else f"{hours}h {minutes}m {seconds}s"
        )

        total_guilds = len(bot.guilds)
        total_users = sum(guild.member_count for guild in bot.guilds if guild.member_count)
        bot_version = "V1.7"  
        python_version = platform.python_version()
        memory_usage = psutil.Process().memory_info().rss / 1024**2
        latency = round(bot.latency * 1000, 2)

        embed = discord.Embed(
            title="🤖 Bot Statistics",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=bot.user.display_avatar.url)
        embed.add_field(name="⏳ Uptime", value=uptime_str, inline=False)
        embed.add_field(name="📜 Servers", value=f"{total_guilds} servers", inline=True)
        embed.add_field(name="👥 Users", value=f"{total_users} users", inline=True)
        embed.add_field(name="🛠 Version", value=f"{bot_version}", inline=True)
        embed.add_field(name="🐍 Python Version", value=f"{python_version}", inline=True)
        embed.add_field(name="💾 Memory Usage", value=f"{memory_usage:.2f} MB", inline=True)
        embed.add_field(name="📡 Ping", value=f"{latency} ms", inline=True)
        embed.set_footer(text="Requested by Bot", icon_url=bot.user.display_avatar.url)

        try:
            user = await bot.fetch_user(USER_ID)
            await user.send(embed=embed)
        except Exception as e:
            print(f"Failed to send DM to {USER_ID} - {e}")

    await bot.start(BOT_TOKEN)

def run_flask():
    app.run(host='0.0.0.0', port=8101)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
