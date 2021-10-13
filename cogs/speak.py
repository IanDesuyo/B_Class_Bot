from discord import Message
from discord.ext import commands
from main import CustomBot
import re
from re import RegexFlag
import random


class Speak(commands.Cog):
    def __init__(self, bot: CustomBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if re.match(rf"<@(!|){self.bot.user.id}>", message.content):  # @mention detect
            aisatsu = re.search(r"([早午晚])安", message.content)
            if aisatsu:
                return await message.channel.send(f"{aisatsu.group(1)}安啊")

            hello = re.search(r"(HELLO|哈囉|[你妳]好|嗨)", message.content, flags=RegexFlag.I)
            if hello:
                return await message.channel.send(f"{hello.group(1)}")

            if re.match(r".*(嗎|ㄇ)(\?|)$", message.content):
                return await message.channel.send(random.choice(["嗯", "對", "好啊", "可以", "我覺得可以", "不要", "不行", "不可以"]))

            return await message.channel.send(random.choice(["幹嘛?", "?", "<:cabpog:890533260759810129>"]))


def setup(bot):
    bot.add_cog(Speak(bot))
