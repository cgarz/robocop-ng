import asyncio
import re
from discord.ext.commands import Cog
from discord.utils import remove_markdown
import config
from helpers.checks import check_if_staff

class CryptoScamBlock(Cog):
    """
    Handles image spam from crypto fannies. Matches when msg has exactly 4 images/links and no visible text content.
    Also counts multiple messages together if posted in quick succession.
    Everyone and here mentions are also not counted as visible text.
    """

    def __init__(self, bot):
        self.url_extract_re = re.compile(r'((\[[^]]*]\()?https?://\S+\.\S+/\S+)\)?', re.IGNORECASE)
        self.replace_restricted_mentions_re = re.compile(r'@(everyone|here)', re.IGNORECASE)
        self.bot = bot
        self.recent_message_cache = {}  # {user.id: {channel.id: [(image_count, message)]} } (list is actually a set)
        self.log_channel = None
        self.MESSAGE_CACHE_TIMEOUT = 8.0

    async def add_to_cache_with_timeout(self, image_link_count, message):
        if message.author.id not in self.recent_message_cache:
            self.recent_message_cache[message.author.id] = {}
        if message.channel.id not in self.recent_message_cache[message.author.id]:
            self.recent_message_cache[message.author.id][message.channel.id] = set()

        self.recent_message_cache[message.author.id][message.channel.id].add((image_link_count, message))
        await asyncio.sleep(self.MESSAGE_CACHE_TIMEOUT)
        self.recent_message_cache[message.author.id][message.channel.id].discard((image_link_count, message))

    @Cog.listener()
    async def on_ready(self):
        self.log_channel = self.bot.get_channel(config.log_channel)

    @Cog.listener()
    async def on_message(self, message):
        await self.bot.wait_until_ready()

        if message.channel.id not in config.spy_channels:
            return  # ignore non spy/logged channels
        if message.author.bot:
            return  # ignore bots
        if check_if_staff(message):
            return  # ignore staff

        msg_has_no_content = False
        image_count = sum(1 for a in message.attachments if a.content_type.startswith('image/'))

        if not message.content:
            msg_has_no_content = True
        else:
            stripped_content = self.replace_restricted_mentions_re.sub(repl='', string=message.content)
            url_count = 0
            for url in self.url_extract_re.findall(message.content):
                if isinstance(url, tuple):
                    url = url[0]
                stripped_content = stripped_content.replace(url, '')
                url_count += 1

            stripped_content = remove_markdown(stripped_content)
            stripped_content = ''.join(c for c in stripped_content if c.isprintable()).strip()
            if not stripped_content:
                image_count += url_count # Assumes link is an image, checking everything would be too slow/expensive.
                msg_has_no_content = True

        if msg_has_no_content:
            asyncio.create_task(self.add_to_cache_with_timeout(image_count, message))
            await asyncio.sleep(0)

        message_cache = self.recent_message_cache.copy()
        if message_cache_user := message_cache.get(message.author.id):
            message_cache_messages = [(c,m) for c,m in message_cache_user.get(message.channel.id)]
        else:
            message_cache_messages = []

        if message_cache_messages:
            image_count = sum(c for c,m in message_cache_messages)

        if image_count == 4:
            if message.attachments:
                await asyncio.sleep(8)  # give log cog enough time to archive 4 images
            await self.log_channel.send('🚨 **Crypto scam fanny**')  # log cog does the rest
            for _, message in message_cache_messages:
                await message.delete()


async def setup(bot):
    await bot.add_cog(CryptoScamBlock(bot))
