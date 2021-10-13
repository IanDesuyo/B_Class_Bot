import json
import os
import logging
import sys
from discord import Message
from discord.ext.commands import Bot
from utils.custom_slash_command import CustomSlashCommand


class CustomBot(Bot):
    def __init__(self):
        self.logger = logging.getLogger("CustomBot")
        self.logger.info("Starting...")
        self.load_config()
        super().__init__(command_prefix="!", help_command=None)

    def load_config(self):
        self.logger.info("Loading config...")
        try:
            with open("./config.json") as f:
                self.config: dict = json.load(f)

        except:
            self.logger.error("Failed to load config.json")
            raise SystemExit

    def load_extensions(self):
        self.logger.info("Loading extensions...")
        for cog in ["cogs.role_selector", "cogs.speak"]:
            self.load_extension(cog)

    def run(self, token: str):
        self.logger.info("Starting...")
        super().run(token)

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user.name} ({self.user.id})")

    async def on_message(self, message: Message):
        """
        Overwrite :function:`on_message` to ignore command not found error.
        """
        if message.author.bot:
            return

        ctx = await self.get_context(message)
        if ctx.command:
            await self.invoke(ctx)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)s][%(asctime)s][%(name)s] %(message)s", stream=sys.stdout
    )
    bot = CustomBot()
    slash = CustomSlashCommand(bot)
    bot.load_extensions()
    bot.run(os.environ.get("TOKEN"))
