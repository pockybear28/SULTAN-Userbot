# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot help command """

import asyncio

from userbot import CMD_HELP, ALIVE_NAME
from userbot.events import register

modules = CMD_HELP
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node


@register(outgoing=True, pattern=r"^\.help(?: |$)(.*)")
async def help(event):
    """For .help command,"""
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit("**Masukan Perintah yang Bener Goblokkkk!!**")
            await asyncio.sleep(200)
            await event.delete()
    else:
        string = ""
        for i in CMD_HELP:
            string += "`" + str(i)
            string += "`\t❉ "
        await event.edit(
            f"**✦ Daftar Perintah Untuk {DEFAULTUSER}-Userbot :\n\n**"
            f"❉{string}❉"
            "\n\n**Support** @sharinguserbot"
        )
        await event.reply(
            f"\n**Ketik Contoh** `.help afk` **Untuk Melihat Informasi Perintah**"
        )
        await asyncio.sleep(1000)
        await event.delete()
