#Kanged From @TroJanZheX
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import asyncio
import re
import pyrogram
import random
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
from pyrogram.errors import UserNotParticipant, PeerIdInvalid, FloodWait
from utils import get_filter_results, get_file_details, is_subscribed, get_poster, temp
from database.users_chats_db import db
from database.ia_filterdb import Media
BUTTONS = {}
BOT = {}
RATING = ["(5.1/10)", "(6.2/10)", "(7.3/10)", "(8.4/10)", "(9.5/10)", "(7.6/10)", "(6.9/10)", "(6.6/10)", "(7.9/10)", "(5.4/10)", "(5.8/10)", "(8.7/10)", "(7.1/10)", "(9.1/10)", "(8.5/10)",]
GENRES = ["fun, fact",
         "Thriller, Comedy",
         "Drama, Comedy",
         "Family, Drama",
         "Action, Adventure",
         "Film Noir",
         "Documentary",
         "Horror, Thriller",
         "Action, Sci-Fi",
         "Adventure, Fantasy",
         "Crime, Drama, Mystery",
         "Crime, Mystery, Thriller",
         "Biography, Drama"]

@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**Please Join My Updates Channel to use this Bot!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"🎬[{get_size(file.file_size)}]🎥{file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"subinps#{file_id}")]
                    )
        else:
            await client.send_message(chat_id=message.from_user.id,text=f"""**Sorry, No Movie/Series Related to the Given Word Was Found 🥺**\n\n**Please Go to Google and Confirm the Correct Spelling 🙏**""",
            reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("📃 MUST READ | Click Here 📃", url="https://t.me/vayichitt_poyamathii")
                        ],
                        [
                            InlineKeyboardButton("🔍 Click Here & Go To Google 🔎", url="https://www.google.com")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="⚜ Pages 1/1 ⚜",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=result_txt, reply_markup=InlineKeyboardMarkup(buttons))

            else:
                await message.reply_text(result_txt, reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="𝙽𝚎𝚡𝚝»»»",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"⚜ Pages 1/{data['total']} ⚜",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>🎬 Title :- {search}</b>\n<b>🌟 Rating :- 7.5/10 | IMDb</b>\n<b>🎭 Genre :- Action, Drama, Thriller, Entertainment</b>\n<b>💿 Quality :- HDRip</b>\n\n<b>📃 Total Pages :- {data['total']}</b>\n\n<b>© By @tvseriezzz ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(f"<b>🎬 Title :- {search}</b>\n<b>🌟 IMDb Rating :- (7.5/10)</b>\n<b>🎭 Genre :- Action, Drama, Thriller, Entertainment</b>\n\n<b>📃 Total Pages :- {data['total']} </b>\n\n<b>© By @tvseriezzz ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []

        search = message.text
        result_txt = f"<b>🎬 Title :- {search}</b>\n\n<b>🌟 IMDb Rating :- {random.choice(RATING)}</b>\n\n<b>🎭 Genre :- {random.choice(GENRES)}</b>\n\n<b>💿 Quality :- HDRip</b>\n\n<b>🗣️ Requested By :- {message.from_user.mention}</b>\n\n<b>©️ {message.chat.title} </b>"

        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"🎬[{get_size(file.file_size)}]🎥{file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://telegram.dog/{nyva}?start=subinps_-_-_-_{file_id}")]
                )
        else:
            await message.reply(quote=True,
            text=f"""**Sorry, {message.from_user.first_name} 🥺**\n\n**No Movie/Series Related to the Given Word Was Found 🥺**\n\n**Please Go to Google and Confirm the Correct Spelling 🙏**\n\n**Please Click MUST READ Button Below..!!**""",
            reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("📃 MUST READ | Click Here 📃", url="https://t.me/vayichitt_poyamathii")
                        ],
                        [
                            InlineKeyboardButton("🔍 Click Here & Go To Google 🔎", url="https://www.google.com")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            await asyncio.sleep(150)
            await msg.delete()
            return
    
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="⚜ Pages 1/1 ⚜",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=result_txt, reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_text(result_txt, reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="𝙽𝚎𝚡𝚝»»»",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"⚜ Pages 1/{data['total']} ⚜",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=result_txt, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(result_txt, reply_markup=InlineKeyboardMarkup(buttons))

    
def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("«««Back", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"⚜ Pages {int(index)+2}/{data['total']} ⚜", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("«««Back", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("𝙽𝚎𝚡𝚝»»»", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"⚜ Pages {int(index)+2}/{data['total']} ⚜", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("𝙽𝚎𝚡𝚝»»»", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"⚜ Pages {int(index)}/{data['total']} ⚜", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("«««Back", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("𝙽𝚎𝚡𝚝»»»", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"⚜ Pages {int(index)}/{data['total']} ⚜", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data == "start":
            buttons = [
                [
                    InlineKeyboardButton("➕️Add Me To Your Chats ➕️", url="https://t.me/tvseriezzz_bot?startgroup=botstart")
                ],
                [
                    InlineKeyboardButton("♻️ ⒼⓇⓄⓊⓅ ♻️", url="https://t.me/tvseriezzz"),
                    InlineKeyboardButton("⭕️ 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 ⭕️", url="https://t.me/tvseriezzz_update")
                ],
                [
                    InlineKeyboardButton("♻️ ⒼⓇⓄⓊⓅ 2 ♻️", url="https://t.me/MrCVENOM_chat"),
                    InlineKeyboardButton("🔥 Dev 🔥", url="https://t.me/MrC_VENOM")
                ],
                [
                    InlineKeyboardButton('ℹ️ Help', callback_data='help'),
                    InlineKeyboardButton('😊 About', callback_data='about')
                ],
                [
                    InlineKeyboardButton('🔍 Search', switch_inline_query_current_chat='') 
                ]
                ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
                reply_markup=reply_markup,
                parse_mode='html'
            )
        elif query.data == "help":
            buttons = [
                [
                    InlineKeyboardButton('Manual Filter', callback_data='manuelfilter'),
                    InlineKeyboardButton('Auto Filter', callback_data='autofilter')
                ],
                [
                    InlineKeyboardButton('Connection', callback_data='coct'),
                    InlineKeyboardButton('Extra Mods', callback_data='extra')
                ],
                [
                    InlineKeyboardButton('🏠 Home', callback_data='start'),
                    InlineKeyboardButton('🔮 Status', callback_data='stats')
                ],
                [
                    InlineKeyboardButton('🔐 Close', callback_data='close_data')
                ]
                ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=script.HELP_TXT.format(query.from_user.mention),
                reply_markup=reply_markup,
                parse_mode='html'
            )
        elif query.data == "about":
            buttons= [
                [
                   InlineKeyboardButton("⭕️ 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 ⭕️", url="https://t.me/tvseriezzz_update"),
                   InlineKeyboardButton('❣️ 𝙱𝚘𝚝 𝙸𝚗𝚏𝚘 ❣️', callback_data='source')
                ],
                [
                   InlineKeyboardButton('🏠 Home', callback_data='start'),
                   InlineKeyboardButton('ℹ️ Help', callback_data='help')
                ],
                [
                    InlineKeyboardButton('🔐 Close', callback_data='close_data')
                ]
                ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=script.ABOUT_TXT.format(temp.B_NAME),
                reply_markup=reply_markup,
                parse_mode='html'
            )
        elif query.data == "source":
            buttons = [
                [
                    InlineKeyboardButton('👩‍🦯 Back', callback_data='about')
                ],
                [
                    InlineKeyboardButton('🔐 Close', callback_data='close_data')
                ]
                ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=script.SOURCE_TXT,
                reply_markup=reply_markup,
                parse_mode='html'
            )
        elif query.data == "manuelfilter":
            buttons = [
                [
                    InlineKeyboardButton('👩‍🦯 Back', callback_data='help'),
                    InlineKeyboardButton('⏹️ Buttons', callback_data='button')
                ],
                [
                    InlineKeyboardButton('🔐 Close', callback_data='close_data')
                ]
                ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=script.MANUELFILTER_TXT,
                reply_markup=reply_markup,
                parse_mode='html'
            )
        elif query.data == "button":
            buttons = [
                [
                    InlineKeyboardButton('👩‍🦯 Back', callback_data='manuelfilter')
                ],
                [
                    InlineKeyboardButton('🔐 Close', callback_data='close_data')
                ]
                ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=script.BUTTON_TXT,
                reply_markup=reply_markup,
                parse_mode='html'
            )
        elif query.data == "autofilter":
            buttons = [
                [
                    InlineKeyboardButton('👩‍🦯 Back', callback_data='help')
                ],
                [
                    InlineKeyboardButton('🔐 Close', callback_data='close_data')
                ]
                ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=script.AUTOFILTER_TXT,
                reply_markup=reply_markup,
                parse_mode='html'
            )
        elif query.data == "coct":
            buttons = [
                [
                    InlineKeyboardButton('👩‍🦯 Back', callback_data='help')
                ],
                [
                    InlineKeyboardButton('🔐 Close', callback_data='close_data')
                ]
                ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=script.CONNECTION_TXT,
                reply_markup=reply_markup,
                parse_mode='html'
            )
        elif query.data == "extra":
            buttons = [
                [
                    InlineKeyboardButton('👩‍🦯 Back', callback_data='help'),
                    InlineKeyboardButton('🏠 Home', callback_data='start')
                ],
                [
                    InlineKeyboardButton('🔐 Close', callback_data='close_data')
                ]
                ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=script.EXTRAMOD_TXT,
                reply_markup=reply_markup,
                parse_mode='html'
            )
        elif query.data == "admin":
            buttons = [
                [
                    InlineKeyboardButton('👩‍🦯 Back', callback_data='extra')
                ],
                [
                    InlineKeyboardButton('🔐 Close', callback_data='close_data')
                ]
                ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=script.ADMIN_TXT,
                reply_markup=reply_markup,
                parse_mode='html'
            )
        elif query.data == "stats":
            buttons = [
                [
                    InlineKeyboardButton('👩‍🦯 Back', callback_data='help'),
                    InlineKeyboardButton('♻️ Refresh', callback_data='rfrsh')
                ],
                [
                    InlineKeyboardButton('🔐 Close', callback_data='close_data')
                ]
                ]
            reply_markup = InlineKeyboardMarkup(buttons)
            total = await Media.count_documents()
            users = await db.total_users_count()
            chats = await db.total_chat_count()
            monsize = await db.get_db_size()
            free = 536870912 - monsize
            monsize = get_size(monsize)
            free = get_size(free)
            await query.message.edit_text(
                text=script.STATUS_TXT.format(total, users, chats, monsize, free),
                reply_markup=reply_markup,
                parse_mode='html'
            )
        elif query.data == "rfrsh":
            await query.answer("Fetching MongoDb DataBase")
            buttons = [
                [
                    InlineKeyboardButton('👩‍🦯 Back', callback_data='help'),
                    InlineKeyboardButton('♻️ Refresh', callback_data='rfrsh')
                ],
                [
                    InlineKeyboardButton('🔐 Close', callback_data='close_data')
                ]
                ]
            reply_markup = InlineKeyboardMarkup(buttons)
            total = await Media.count_documents()
            users = await db.total_users_count()
            chats = await db.total_chat_count()
            monsize = await db.get_db_size()
            free = 536870912 - monsize
            monsize = get_size(monsize)
            free = get_size(free)
            await query.message.edit_text(
                text=script.STATUS_TXT.format(total, users, chats, monsize, free),
                reply_markup=reply_markup,
                parse_mode='html'
          )


        elif query.data.startswith("subinps"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton('♻️ ⒼⓇⓄⓊⓅ ♻️', url='https://t.me/tvseriezzz'),
                        InlineKeyboardButton('⭕️ 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 ⭕️', url='https://t.me/tvseriezzz_update')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [
                    [
                        InlineKeyboardButton('♻️ ⒼⓇⓄⓊⓅ ♻️', url='https://t.me/tvseriezzz'),
                        InlineKeyboardButton('⭕️ 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 ⭕️', url='https://t.me/tvseriezzz_update')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )


        elif query.data == "pages":
            await query.answer()
    else:
        await query.answer("കൌതുകും ലേശം കൂടുതൽ ആണല്ലേ👀",show_alert=True)
