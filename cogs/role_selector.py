import logging
from typing import List
from main import CustomBot
from discord import Role, Embed
from discord.ext import commands
from discord.errors import Forbidden
from discord_slash import cog_ext
from discord_slash.context import ComponentContext
from discord_slash.utils.manage_components import create_actionrow, create_button


class RoleSelector(commands.Cog):
    def __init__(self, bot: CustomBot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @commands.command(name="createRoleButton")
    async def create_role_button(self, ctx: commands.Context):
        action_rows = []
        buttons = []

        roles: List[dict] = self.bot.config.get("roles")
        for role in roles:
            buttons.append(
                create_button(
                    label=role.get("name"),
                    style=role.get("style"),
                    custom_id=f"__roleButton__{role.get('id')}",
                )
            )

            if len(buttons) == 5:
                action_rows.append(create_actionrow(*buttons))
                buttons = []

        if len(buttons) > 0:
            action_rows.append(create_actionrow(*buttons))

        await ctx.send("選擇你有玩的遊戲, 找到遊戲好夥伴吧!", components=action_rows)

    @cog_ext.cog_component(components="__roleButton")
    async def button_callback(self, ctx: ComponentContext):
        role_id = int(ctx.custom_id[14:])
        role: Role = ctx.guild.get_role(role_id)

        if not role:
            await ctx.send("找不到此身分組", hidden=True)
            return self.logger.error(f"{ctx.guild.name} | 找不到身分組 {role_id}")

        try:
            if role in ctx.author.roles:
                await ctx.author.remove_roles(role, reason="身分組設定")
                await ctx.send(embed=Embed(description=f"已移除身分組 {role.name}", color=0xFF0000), hidden=True)
                self.logger.info(f"{ctx.guild.name} | 已移除 {ctx.author.display_name} 的身分組 {role.name}")
            else:
                await ctx.author.add_roles(role, reason="身分組設定")
                await ctx.send(embed=Embed(description=f"已新增身分組 {role.name}", color=0x00FF00), hidden=True)
                self.logger.info(f"{ctx.guild.name} | 已新增 {ctx.author.display_name} 至身分組 {role.name}")
        except Forbidden:
            await ctx.send("我沒有權限QQ", hidden=True)
            self.logger.error(f"{ctx.guild.name} | 沒有權限來管理身分組")


def setup(bot):
    bot.add_cog(RoleSelector(bot))
