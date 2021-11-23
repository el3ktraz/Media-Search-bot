import re
from os import environ

id_pattern = re.compile(r'^.\d+$')

# Bot information
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', False))
PICS = (environ.get('PICS', 'https://te.legra.ph/file/cb57b6561bdb5b4c03eb6.mp4 https://te.legra.ph/file/2402c9db959ca76f5fed9.mp4 https://telegra.ph/file/2451d574ac17276c3a0e6.mp4')).split()

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ['ADMINS'].split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ['CHANNELS'].split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else auth_channel
AUTH_GROUPS = [int(admin) for admin in environ.get("AUTH_GROUPS", "").split()]
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))

# MongoDB information
DATABASE_URI_2 = environ['DATABASE_URI']
DATABASE_NAME = environ['DATABASE_NAME']
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

# Messages
default_start_msg = """
𝙷𝙴𝙻𝙻𝙾 {},

𝙼𝚈 𝙽𝙰𝙼𝙴 𝙸𝚂 <a href='https://t.me/tvseriezzz_bot'>𝙰𝚕𝚊𝚗 𝚆𝚊𝚕𝚔𝚎𝚛</a>,
𝙸 𝙲𝙰𝙽 𝙿𝚁𝙾𝚅𝙸𝙳𝙴 𝙼𝙾𝚅𝙸𝙴𝚂 𝙰𝙽𝙳 𝚂𝙴𝚁𝙸𝙴𝚂, 𝙹𝚄𝚂𝚃 𝙰𝙳𝙳 𝙼𝙴 𝚃𝙾 𝚈𝙾𝚄𝚁 𝙶𝚁𝙾𝚄𝙿 𝙰𝙽𝙳 𝙴𝙽𝙹𝙾𝚈 😍

⚠️ 𝙼𝚘𝚛𝚎 𝙷𝚎𝚕𝚙 𝙲𝚑𝚎𝚌𝚔 𝙷𝚎𝚕𝚙 𝙱𝚞𝚝𝚝𝚘𝚗 𝙱𝚎𝚕𝚘𝚠

©️ MᴀɪɴᴛᴀɪɴᴇD Bʏ : <a href='https://t.me/tvseriezzz'>♠️ 𝑨𝒍𝒍 𝑰𝒏 𝑶𝒏𝒆 𝑮𝒓𝒐𝒖𝒑 🎬</a>
"""
START_MSG = environ.get('START_MSG', default_start_msg)

BUTTON = environ.get("BUTTON",True)
FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "")
OMDB_API_KEY = environ.get("OMDB_API_KEY", "")
if FILE_CAPTION.strip() == "":
    CUSTOM_FILE_CAPTION=None
else:
    CUSTOM_FILE_CAPTION=FILE_CAPTION
if OMDB_API_KEY.strip() == "":
    API_KEY=None
else:
    API_KEY=OMDB_API_KEY
