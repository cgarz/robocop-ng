from discord.ext.commands import Cog
import config
from helpers.checks import check_if_staff

class KeysRequestBlock(Cog):
    """
    handles nintendouche kiddies constantly asking for keys as soon as they join
    """

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        await self.bot.wait_until_ready()

        if message.channel.id not in config.spy_channels:
            return  # ignore non spy/logged channels
        if message.author.bot:
            return  # ignore bots
        if check_if_staff(message):
            return  # ignore staff
        if message.created_at - message.author.joined_at > config.keys_block_counts_as_new_member:
            return  # ignore non new members

        match1 = config.keys_block_re1.findall(message.content)
        match2 = config.keys_block_re2.findall(message.content)
        if match1 and match2:
            await message.reply(config.keys_request_message)

async def setup(bot):
    await bot.add_cog(KeysRequestBlock(bot))
