from config_nkit import *

guild_whitelist = [214879210651516929]  # testing guild id

named_roles = {
    'everyone':              214879210651516929,
    'testingadmin':          1300293893555748904,
    'testingoverseer':       1300294215833751675,
    'testingbot-maintainer': 1300294272326696970,
    'testing_nkitten':       1300339737831145492,
    'rules_ack':             1339377049084891197
}

bot_manager_role_id = named_roles['testingbot-maintainer']
staff_role_ids = [
    named_roles['testingadmin'],
    named_roles['testingoverseer'],
    named_roles['testingbot-maintainer']
]

log_channel = 1300295024315076668
botlog_channel = 1300295067596095498
modlog_channel = 1300295108813656114
spylog_channel = 1300295141323575346
welcome_channel = 1300295206641598474

general_channels = [
    welcome_channel,
    1300295288870928416, # general
]

spy_channels = general_channels

enroll_reaction_emoji_id = None
enroll_reaction_emoji_name = '\N{THUMBS UP SIGN}'  # '👍'
enroll_reaction_message_id = 1345936191568220170
enroll_reaction_role_id = named_roles['rules_ack']
