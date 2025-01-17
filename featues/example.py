# this is an example script of an extension, you will put all extensions into the folder "features"

import discord
from discord.ext import tasks, commands

class ActivityUpdater(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_activity.start()

    @tasks.loop(minutes=1)
    async def update_activity(self):
        server_count = len(self.bot.guilds)
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"{server_count} servers!")
        await self.bot.change_presence(activity=activity)

    @update_activity.before_loop
    async def before_update_activity(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(ActivityUpdater(bot))
