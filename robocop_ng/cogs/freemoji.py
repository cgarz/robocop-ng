import discord
import asyncio
from discord.ext.commands import Cog
from discord import app_commands
import config
import re


class Freemoji(Cog):
    JUMP_LINK_RE = re.compile(r'^https?://discord.com/channels/\d+/(?P<channel>\d{15,20})/(?P<message>\d{15,20})$', re.IGNORECASE)
    CHAN_MSG_ID_RE = re.compile(r'^(?P<channel>\d{15,20})-(?P<message>\d{15,20})$')
    MENTION_RE = re.compile(r'^<@!?(?P<user>\d{15,20})>$')
    MSG_ID_RE = re.compile(r'^(?P<message>\d{15,20})$')
    FETCH_MSG_LIMIT = 10
    REACTION_TIMEOUT = 10

    def __init__(self, bot):
        self.bot = bot
        self.react_messages = set()
        self.emojis = {}

    @Cog.listener()
    async def on_ready(self):
        self.emojis = {e.name: e for e in await self.bot.get_guild(config.guild_whitelist[0]).fetch_emojis()}

    @Cog.listener()
    async def on_guild_emojis_update(self, guild, before_emojis, after_emojis):
        self.emojis = {e.name: e for e in after_emojis}

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        for message, user_id, emoji in self.react_messages:
            if all((payload.message_id == message.id,  payload.member.id == user_id,  payload.emoji == emoji)):
                await message.remove_reaction(emoji, self.bot.user)
                self.react_messages.discard((message, user_id, emoji))
                return

    async def add_to_reactions_with_timeout(self, message, user_id, emoji):
        self.react_messages.add((message, user_id, emoji))
        await asyncio.sleep(self.REACTION_TIMEOUT)

        self.react_messages.discard((message, user_id, emoji))
        await message.remove_reaction(emoji, self.bot.user)

    @staticmethod
    async def error_response(interaction, message):
        await interaction.edit_original_response(embed=discord.Embed.from_dict({
            'title': ':x:  '              ':regional_indicator_e:'
                     '\N{Zero Width Joiner}:regional_indicator_r:'
                     '\N{Zero Width Joiner}:regional_indicator_r:'
                     '\N{Zero Width Joiner}:regional_indicator_o:'
                     '\N{Zero Width Joiner}:regional_indicator_r:'
                     '  :x:',
            'description': message,
            'color': discord.Color.red().value
        }))

    @app_commands.guild_only()
    @app_commands.command(description='React with specified emoji to last message or target message.')
    @app_commands.describe(
        emoji='The emoji to react with. Either a proper emoji or just the name of one in the server.',
        target='Target message via: 1-10 [default=1] / channel_id-message_id / message_id / jump_url / @mention')
    async def react(self, interaction, emoji: str, target: str = '1'):
        await interaction.response.defer(thinking=True, ephemeral=True)
        target = target.strip()

        if match := self.JUMP_LINK_RE.search(target):
            msg_id = int(match.group('message'))
            channel_id = int(match.group('channel'))

        elif match := self.CHAN_MSG_ID_RE.search(target):
            msg_id = int(match.group('message'))
            channel_id = int(match.group('channel'))

        elif match := self.MSG_ID_RE.search(target):
            msg_id = int(match.group('message'))
            channel_id = interaction.channel_id

        elif match := self.MENTION_RE.search(target):
            channel_id = interaction.channel_id
            user_id = int(match.group('user'))
            async for message in self.bot.get_channel(channel_id).history(limit=self.FETCH_MSG_LIMIT):
                if message.author.id == user_id:
                    msg_id = message.id
                    break
            else:
                await self.error_response(interaction, 'No target found')
                return

        elif target.isdigit() and int(target) <= self.FETCH_MSG_LIMIT:
            channel_id = interaction.channel_id
            try:
                msg = [m async for m in self.bot.get_channel(channel_id).history(limit=self.FETCH_MSG_LIMIT)][int(target) - 1]
                msg_id = msg.id
            except IndexError:
                await self.error_response(interaction, 'No target found')
                return

        else:
            await self.error_response(interaction, 'No target found')
            return

        if not (channel := self.bot.get_channel(channel_id)):
            await self.error_response(interaction, f'Channel not found.')
            return

        try:
            message = await channel.fetch_message(msg_id)
            emoji = self.emojis[emoji] if emoji in self.emojis else discord.PartialEmoji.from_str(emoji)

            await message.add_reaction(emoji)
        except (discord.errors.HTTPException, discord.errors.NotFound) as e:
            await self.error_response(interaction, f'[{e.code}] {e.text}')
            return

        asyncio.create_task(self.add_to_reactions_with_timeout(message, interaction.user.id, emoji))
        await interaction.edit_original_response(embed=discord.Embed(
            title=f'Added {emoji} Reaction',
            description=f'Add yourself to the reaction within {self.REACTION_TIMEOUT} seconds to complete the process.\n'
                        f'Jump URL: {message.jump_url}',
            color=discord.Color.green()
        ))


async def setup(bot):
    await bot.add_cog(Freemoji(bot))
