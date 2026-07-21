import asyncio
from discord.ext.commands import Cog
from datetime import datetime, timezone, timedelta
import config
from helpers.checks import check_if_staff

class CryptoScamBlock(Cog):
    """
    Handles image spam from crypto fannies. Triggers if a user posts TRIGGER AMOUNT images in TRIGGER_AMOUNT or more
    spy channels within CLEAR_AFTER_SEC seconds. Unacks them and deletes previous PURGE_MINUTES minutes worth of their
    messages from all spy channels.
    """

    def __init__(self, bot):
        self.bot = bot
        self.log_channel = None
        self.enroll_reaction_role = None
        self.spy_channels = []
        self.recent_image_data = {}  # {user.id: (image_count, set(channel_ids))}
        self.TRIGGER_AMOUNT = 2
        self.CLEAR_AFTER_SEC = 90
        self.PURGE_MINUTES = 3

    async def increment_with_timeout(self, user_id, channel_id):
        image_count, channel_ids = self.recent_image_data.get(user_id, (0, set()))
        image_count += 1
        channel_ids.add(channel_id)
        self.recent_image_data[user_id] = image_count, channel_ids

        await asyncio.sleep(self.CLEAR_AFTER_SEC)
        image_count, channel_ids = self.recent_image_data[user_id]
        image_count -= 1
        channel_ids.discard(channel_id)
        self.recent_image_data[user_id] = image_count, channel_ids

    @Cog.listener()
    async def on_ready(self):
        self.log_channel = self.bot.get_channel(config.log_channel)
        guild = self.bot.get_guild(config.guild_whitelist[0])
        self.enroll_reaction_role = guild.get_role(config.enroll_reaction_role_id)
        self.spy_channels = [c for c in guild.channels if c.id in config.spy_channels]

    @Cog.listener()
    async def on_message(self, message):
        await self.bot.wait_until_ready()

        if message.channel.id not in config.spy_channels:
            return  # ignore non spy/logged channels
        if message.author.bot:
            return  # ignore bots
        if check_if_staff(message):
            return  # ignore staff

        if any(a.content_type.startswith(('image/', 'video/')) for a in message.attachments):
            asyncio.create_task(self.increment_with_timeout(message.author.id, message.channel.id))
            await asyncio.sleep(0)
        else:
            await asyncio.sleep(2)  # give douchecord enough time to convert a bare image link into an image embed
            if any(e.type in ('image', 'video', 'gifv') for e in message.embeds):
                asyncio.create_task(self.increment_with_timeout(message.author.id, message.channel.id))
                await asyncio.sleep(0)

        image_count, channel_ids = self.recent_image_data.get(message.author.id, (0,set()))
        if image_count >= self.TRIGGER_AMOUNT and len(channel_ids) >= self.TRIGGER_AMOUNT:
            await message.author.remove_roles(self.enroll_reaction_role)
            await self.log_channel.send('🚨 **Crypto scam fanny**')  # log cog does the rest
            delete_after = datetime.now(tz=timezone.utc) - timedelta(minutes=self.PURGE_MINUTES)
            for channel in self.spy_channels:
                async for scam_message in channel.history(after=delete_after):
                    if scam_message.author == message.author:
                        await scam_message.delete()


async def setup(bot):
    await bot.add_cog(CryptoScamBlock(bot))
