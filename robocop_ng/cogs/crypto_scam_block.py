import asyncio
import re
from discord.ext.commands import Cog
from discord.utils import remove_markdown
import config
from helpers.checks import check_if_staff

class CryptoScamBlock(Cog):
    """
    Handles image spam from crypto fannies. Matches when msg has exactly 4 images/links and no visible text content.
    """

    def __init__(self, bot):
        self.url_extract_re = re.compile(r'(https?://\S+\.\S+/\S+)', re.IGNORECASE)
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

        msg_has_no_content = False
        image_links = [ia.url for ia in message.attachments if ia.content_type.startswith('image/')]

        if not message.content:
            msg_has_no_content = True
        else:
            stripped_content = message.content
            for url in self.url_extract_re.findall(message.content):
                stripped_content = stripped_content.replace(url, '')
                image_links.append(url)  # Assumes link is an image, checking everything would be too slow/expensive.

            stripped_content = remove_markdown(stripped_content).strip()
            stripped_content = ''.join(c for c in stripped_content if c.isprintable())
            if not stripped_content:
                msg_has_no_content = True

        if len(image_links) == 4 and msg_has_no_content:
            log_channel = self.bot.get_channel(config.log_channel)
            if message.attachments:
                await asyncio.sleep(5)  # give log cog enough time to archive 4 images
            await log_channel.send('🚨 **Crypto scam fanny**')  # log cog does the rest
            await message.delete()


async def setup(bot):
    await bot.add_cog(CryptoScamBlock(bot))
