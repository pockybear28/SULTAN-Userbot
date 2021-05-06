# Ported by @vckyou

from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc

from userbot import CMD_HELP
from userbot.events import register


async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call))
    return xx.call


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


@register(outgoing=True, pattern=r"^\.svc (.*)")
async def _(event):
    try:
        await event.client(stopvc(await get_call(event)))
        await event.edit(event, "`Voice Chat Stopped...`")
    except Exception as ex:
        await event.edit(event, f"`{str(ex)}`")


CMD_HELP.update(
    {
        "vcg": "**Plugin : **`vcg`\
        \n\n  •  **Syntax :** `.svc`\
        \n  •  **Function : **Memberhentikan Voice Call Group (membutuhkan Hak akses VCG).\
    "
    }
)
