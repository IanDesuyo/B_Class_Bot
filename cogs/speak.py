from typing import List
from discord import Message
from discord.ext import commands
from main import CustomBot
import re
import random


class Speak(commands.Cog):
    def __init__(self, bot: CustomBot):
        self.bot = bot
        self.speaks: List[dict] = self.bot.config.get("speak")
        self.ShibaInuCard: List[str] = self.bot.config.get("ShibaInuCard")

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if re.match(rf"<@(!|){self.bot.user.id}>", message.content):  # @mention detect
            for speak in self.speaks:
                matched = re.search(speak["regex"], message.content.lower())
                if matched:
                    return await message.channel.send(random.choice(speak["response"]).format(matched))

            return await message.channel.send(random.choice(["幹嘛?", "?", "<:cabpog:890533260759810129>"]))

        if "色色" in message.content:
            return await message.reply(random.choice(self.ShibaInuCard))

        if "mumu" in message.content.lower():
            return await message.reply(
                "https://cdn.discordapp.com/attachments/785526318917877761/896805388907843584/unknown.png"
            )


def setup(bot):
    bot.add_cog(Speak(bot))
