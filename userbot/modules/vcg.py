import json
from json.decoder import JSONDecodeError

from userbot import bot
from aiohttp import web
from aiohttp.http_websocket import WSMsgType

from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import JoinGroupCallRequest as joinvc
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc
from telethon.tl.types import DataJSON

from userbot import CMD_HELP
from userbot.events import register


async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call))
    return xx.call


async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call))
    return xx.call


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


@register(outgoing=True, pattern=r"^\.vcend (.*)")
async def _(event):
    try:
        await event.client(stopvc(await get_call(event)))
        await event.edit(event, "`Voice Chat Stopped...`")
    except Exception as ex:
        await event.edit(event, f"`{str(ex)}`")


@register(outgoing=True, pattern=r"^\.joinvc")
async def join_call(data):
    try:
        chat = await data.client.get_entity(data.chat_id)
    except ValueError:
        stree = (await bot.get_me()).first_name
        return await bot.send_message(
            data.chat_id, f"`Silakan tambahkan {stree} di grup ini.`"
        )
    except Exception as ex:
        return await data.edit("`" + str(ex) + "`")
    try:
        full_chat = await bot(getchat(chat))
    except ValueError:
        stree = (await bot.get_me()).first_name
        return await data.edit(f"`Silakan tambahkan {stree} di grup ini.`"
                               )
    except Exception as ex:
        return await data.edit("`" + str(ex) + "`")
    try:
        call = await bot(getvc(full_chat.full_chat.call))
    except BaseException:
        call = None
    if not call:
        return await data.edit(
            "`Saya tidak dapat mengakses obrolan suara.`",
        )

    try:
        result = await bot(
            joinvc(
                call=call.call,
                muted=False,
                join_as="me",
                params=DataJSON(
                    data=json.dumps(
                        {
                            "ufrag": data["ufrag"],
                            "pwd": data["pwd"],
                            "fingerprints": [
                                {
                                    "hash": data["hash"],
                                    "setup": data["setup"],
                                    "fingerprint": data["fingerprint"],
                                },
                            ],
                            "ssrc": data["source"],
                        },
                    ),
                ),
            ),
        )
        await data.edit(f"`Bergabung dengan Obrolan Suara di {(await bot.get_entity(data.chat_id)).title}`",
                        )
    except Exception as ex:
        return await data.edit("`" + str(ex) + "`")

    transport = json.loads(result.updates[0].call.params.data)["transport"]

    return {
        "_": "get_join",
        "data": {
            "chat_id": data["chat"]["id"],
            "transport": {
                "ufrag": transport["ufrag"],
                "pwd": transport["pwd"],
                "fingerprints": transport["fingerprints"],
                "candidates": transport["candidates"],
            },
        },
    }


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            try:
                data = json.loads(msg.data)
            except JSONDecodeError:
                await ws.close()
                break

            response = None
            if data["_"] == "join":
                response = await join_call(data["data"])

            #                if data["_"] == "leave":
            #                    response = await leave_vc(data["data"])

            if response is not None:
                await ws.send_json(response)

    return ws


CMD_HELP.update(
    {
        "vcg": "**Plugin : **`vcg`\
        \n\n  •  **Syntax :** `.joinvc`\
        \n  •  **Function : **Untuk bergabung ke Voice chat Group.\
        \n\n  •  **Syntax :** `.vcend`\
        \n  •  **Function : **Memberhentikan Voice Call Group (membutuhkan Hak akses VCG).\
    "
    }
)
