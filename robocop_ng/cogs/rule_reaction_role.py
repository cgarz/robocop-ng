from discord.ext.commands import Cog, command, check
import config
from helpers.checks import check_if_staff


class RuleReactionRole(Cog):
    """
    Assigns a set role to users when they react with specific emoji to a chosen message
    """
    def __init__(self, bot):
        self.bot = bot
        self.enroll_reaction_role = None
        self.role_cog_ready = False

    @Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(config.guild_whitelist[0])
        self.enroll_reaction_role = guild.get_role(config.enroll_reaction_role_id)
        self.role_cog_ready = True

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if any((
            not self.role_cog_ready,
            payload.message_id != config.enroll_reaction_message_id,
            payload.emoji.id   != config.enroll_reaction_emoji_id,
            payload.emoji.name != config.enroll_reaction_emoji_name
        )):
            return

        await payload.member.add_roles(self.enroll_reaction_role)

    @check(check_if_staff)
    @command()
    async def unack(self, ctx):
        '''Removes rules_ack role for any mentioned members'''

        for member in ctx.message.mentions:
            await member.remove_roles(self.enroll_reaction_role)


async def setup(bot):
    await bot.add_cog(RuleReactionRole(bot))
