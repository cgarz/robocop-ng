import hashlib
import datetime
import re

# Basic bot config, insert your token here, update description if you want
prefixes = [".", "!"]

with open('BOT_TOKEN.txt') as f:
    token = f.read().strip()

bot_description = "robocop-ng, the moderation bot of reswitched — nkit fork"

# If you forked robocop-ng, put your repo here
source_url = "https://github.com/cgarz/robocop-ng"
rules_url = ""

# The bot description to be used in .robocop embed
embed_desc = (
    "Robocop-NG is developed by [Ave](https://github.com/aveao)"
    " and [tomGER](https://github.com/tumGER), and is a rewrite "
    "of Robocop.\nRobocop is based on Kurisu by 916253 and ihaveamac."
)

# The cogs the bot will load on startup.
initial_cogs = [
    "cogs.common",
    "cogs.admin",
    "cogs.mod",
    "cogs.mod_note",
    "cogs.mod_reacts",
    "cogs.mod_userlog",
    "cogs.mod_timed",
    "cogs.mod_watch",
    "cogs.basic",
    "cogs.logs",
    "cogs.err",
    "cogs.links",
    "cogs.rule_reaction_role",
    "cogs.robocronp",
    "cogs.nkitmeme",
    "cogs.invites",
    "cogs.keys_request_block",
    "cogs.crypto_scam_block"
]

# The following cogs are also available but aren't loaded by default:
# cogs.imagemanip - Adds a meme command called .cox.
# Requires Pillow to be installed with pip.
# cogs.lists - Allows managing list channels (rules, FAQ) easily through the bot
# PR'd in at: https://github.com/reswitched/robocop-ng/pull/65
# cogs.pin - Lets users pin important messages
# and sends pins above limit to a GitHub gist

# Minimum account age required to join the guild
# If user's account creation is shorter than the time delta given here
# then user will be kicked and informed
min_age = datetime.timedelta(seconds=1)

# The bot will only work in these guilds
guild_whitelist = [959955884694437948]  # nkit guild id

# Named roles to be used with .approve and .revoke
# Example: .approve User hacker
named_roles = {
    'everyone':       959955884694437948,
    'admin':          959969495852679228,
    'overseer':       963141068570898463,
    'bot-maintainer': 981846640681943040,
    'robo':           982510372315627591,
    'rules_ack':      1339406473318633543
}

# The bot manager and staff roles
# Bot manager can run eval, exit and other destructive commands
# Staff can run administrative commands
bot_manager_role_id = named_roles['bot-maintainer']
staff_role_ids = [
    named_roles['admin'],
    named_roles['overseer'],
    named_roles['bot-maintainer'],
]

# Various log channels used to log bot and guild's activity
# You can use same channel for multiple log types
# Spylog channel logs suspicious messages or messages by members under watch
# Invites created with .invite will direct to the welcome channel.
log_channel = 981843880322420786
botlog_channel = 981843909565116426
modlog_channel = 981843937050378270
spylog_channel = 981844126033150022
welcome_channel = 981694878092243064
image_archive_channel = 1441174621792632935

# These channel entries are used to determine which roles will be given
# access when we unmute on them
general_channels = [
    1002352198828707870, # announcements
    981122068718448671,  # releases
    1300299915750150144, # rules-and-faqs
    981115906115633173,  # general
    963143757937651753,  # bug-reports
    963144218514178108,  # support
    963144311237668945,  # feature-requests
    1021728700363972628, # ui-feedback
    1044754539041001532, # scan-tool
    welcome_channel
]  # Channels everyone can access

#Community Channels: Disabled
community_channels = []  # Channels requiring community role

# Controls which roles are blocked during lockdown
lockdown_configs = {
    # Used as a default value for channels without a config
    "default": {"channels": general_channels, "roles": [named_roles["everyone"]]}
}

# Mute role is applied to users when they're muted
# As we no longer have mute role on ReSwitched, I set it to 0 here
mute_role = 0  # Mute role in ReSwitched

# Channels that will be cleaned every minute/hour.
# This feature isn't very good rn.
# See https://github.com/reswitched/robocop-ng/issues/23
minutely_clean_channels = []
hourly_clean_channels = []

# Edited and deletes messages in these channels will be logged
spy_channels = general_channels

# All lower case, no spaces, nothing non-alphanumeric
suspect_words = []

# List of words that will be ignored if they match one of the
# suspect_words (This is used to remove false positives)
suspect_ignored_words = []

# == For cogs.links ==
links_guide_text = """**Some quick links:**
Github repository: <https://github.com/Nanook/NKit/>

Wiki on Github: <https://github.com/Nanook/NKit/wiki>
Usage guide: <https://github.com/Nanook/NKit/wiki/Usage>
Current Roadmap: <https://github.com/Nanook/NKit/wiki/Roadmap>
"""

# == Only if you want to use cogs.verification ==
# https://docs.python.org/3.7/library/hashlib.html#shake-variable-length-digests
_welcome_blacklisted_hashes = {"shake_128", "shake_256"}
# List of hashes that are to be used during verification:
welcome_hashes = tuple(hashlib.algorithms_guaranteed - _welcome_blacklisted_hashes)
welcome_header = ''
welcome_rules = ''
welcome_footer = ''
hidden_term_line = ''  # Line to be hidden in rules

# == Only if you want to use cogs.pin ==
# Used for the pinboard. Leave empty if you don't wish for a gist pinboard.
github_oauth_token = ""

# Channels and roles where users can pin messages
allowed_pin_channels = []
allowed_pin_roles = []

# == Only if you want to use cogs.lists ==
# Channels that are lists that are controlled by the lists cog.
list_channels = []
# Channel to upload text files while editing list items. (They are cleaned up.)
list_files_channel = 0

# == Only if you want to use cogs.sar ==
self_assignable_roles = {}

# == Only if you want to use cogs.mod_reswitched ==
pingmods_allow = [named_roles["everyone"]] + staff_role_ids
pingmods_role = 0
modtoggle_role = 0

# == Only if you want to use cogs.yubicootp ==
# Optional: Get your own from https://upgrade.yubico.com/getapikey/
yubico_otp_client_id = 1
# Note: You can keep client ID on 1, it will function.
yubico_otp_secret = ""
# Optional: If you provide a secret, requests will be signed
# and responses will be verified.

# == Only if you want to use cogs.keys_request_block ==
keys_block_counts_as_new_member = datetime.timedelta(days=1)
keys_block_message = 'Keys cannot be shared in this Discord server. FAQ #5 <#1300299915750150144>.'
keys_block_re1 = re.compile(
    r'(dats?|datfiles?|discs?|disks?|wii|wii u|wiiu|wua|wup|app)', re.IGNORECASE
)
keys_block_re2 = re.compile(
    r'(keys?|keyfiles?)', re.IGNORECASE
)

# == Only if you want to use cogs.rule_reaction_role ==
enroll_reaction_emoji_id = 1004024752119238727    # for custom emoji, None if regular Unicode codepoint
enroll_reaction_emoji_name = 'read'  # pepe read  # Unicode codepoint or assigned custom emoji name
enroll_reaction_message_id = 1300300848240394323  # @johnsanc #rules-and-faqs message
enroll_reaction_role_id = named_roles['rules_ack']
