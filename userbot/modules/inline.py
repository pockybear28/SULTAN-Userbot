# Code By @X_ImFine
# Recode by @mrismanaziz

import logging
import math
import time
from datetime import datetime

import aiohttp
import heroku3
import speedtest
from telegraph import Telegraph
from telethon import Button, events

from userbot import (
    BOT_VER,
    HEROKU_API_KEY,
    HEROKU_APP_NAME,
    UPSTREAM_REPO_BRANCH,
    StartTime,
    tgbot,
)

telegraph = Telegraph()
r = telegraph.create_account(short_name="telegraph")
auth_url = r["auth_url"]

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)

rtext = f"""
 **Hey**, __I am using__ 🔥 **Man-Userbot** 🔥

       __Thanks For Using me__

✣ **Userbot Version:** {BOT_VER}@{UPSTREAM_REPO_BRANCH}
✣ **Group Support :** [Sharing Userbot](t.me/sharinguserbot)
✣ **Owner Repo :** [Risman](t.me/mrismanaziz)

__Klik Tombol di Bawah untuk Menggunakan Repo Man-Userbot__
"""


@tgbot.on(events.NewMessage(pattern="!repo"))
async def xrepo(repo):
    await tgbot.send_message(
        repo.chat_id,
        rtext,
        buttons=[
            [
                Button.url(
                    text="⛑ REPO MAN-USERBOT ⛑",
                    url="https://github.com/mrismanaziz/Man-Userbot",
                )
            ]
        ],
    )


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


def speed_convert(size):
    """
    Hi human, you can't read bytes?
    """
    power = 2 ** 10
    zero = 0
    units = {0: "", 1: "Kb/s", 2: "Mb/s", 3: "Gb/s", 4: "Tb/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


@tgbot.on(events.NewMessage(pattern="!speed"))
async def spd(event):
    asu = await event.reply("`Speedtest...`")
    start = datetime.now()
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    response = s.results.dict()
    download_speed = response.get("download")
    upload_speed = response.get("upload")
    ping_time = response.get("ping")
    client_infos = response.get("client")
    i_s_p = client_infos.get("isp")
    i_s_p_rating = client_infos.get("isprating")
    response = s.results.share()
    speedtest_image = response
    output = (
        f"**SpeedTest** completed in {ms}ms\n\n"
        f"**• Download:** `{speed_convert(download_speed)}\n`"
        f"**• Upload:** `{speed_convert(upload_speed)}\n`"
        f"**• Ping:** `{ping_time}\n`"
        f"**• ISP:** `{i_s_p}\n`"
        f"**• ISP Rating:** `{i_s_p_rating}\n\n`"
        "**🔥 POWERED BY MAN-USEBOT 🔥**"
    )
    await asu.delete()
    await tgbot.send_file(
        event.chat_id,
        speedtest_image,
        caption=output,
        force_document=False,
        allow_cache=False,
    )


@tgbot.on(events.NewMessage(pattern="!ping"))
async def pingme(pong):
    """For .ping command, ping the userbot from any chat."""
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    asu = await pong.reply("`Pinging....`")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await asu.edit(
        f"**PONG!!🏓**\n✣ **Pinger** - %sms\n✣ **Bot Uptime** - {uptime}" % (duration)
    )


heroku_api = "https://api.heroku.com"
if HEROKU_APP_NAME is not None and HEROKU_API_KEY is not None:
    Heroku = heroku3.from_key(HEROKU_API_KEY)
    app = Heroku.app(HEROKU_APP_NAME)
    heroku_var = app.config()
else:
    app = None


@tgbot.on(events.NewMessage(pattern="!usage"))
async def dyno_usage(dyno):
    """
    Get your account Dyno Usage
    """
    x = await dyno.reply("`Getting Information...`")
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/81.0.4044.117 Mobile Safari/537.36"
    )
    user_id = Heroku.account().id
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    async with aiohttp.ClientSession() as session:
        async with session.get(heroku_api + path, headers=headers) as r:
            if r.status != 200:
                await tgbo.send_message(dyno.chat_id, f"`{r.reason}`", reply_to=dyno.id)
                await x.edit("`Can't get information...`")
                return False
            result = await r.json()
            quota = result["account_quota"]
            quota_used = result["quota_used"]

            """ - User Quota Limit and Used - """
            remaining_quota = quota - quota_used
            percentage = math.floor(remaining_quota / quota * 100)
            minutes_remaining = remaining_quota / 60
            hours = math.floor(minutes_remaining / 60)
            minutes = math.floor(minutes_remaining % 60)

            """ - User App Used Quota - """
            Apps = result["apps"]
            for apps in Apps:
                if apps.get("app_uuid") == app.id:
                    AppQuotaUsed = apps.get("quota_used") / 60
                    AppPercentage = math.floor(apps.get("quota_used") * 100 / quota)
                    break
            else:
                AppQuotaUsed = 0
                AppPercentage = 0

            AppHours = math.floor(AppQuotaUsed / 60)
            AppMinutes = math.floor(AppQuotaUsed % 60)

            await x.edit(
                "**Dyno Usage**:\n\n╭━━━━━━━━━━━━━━━━━━━━╮\n"
                f" ❁ **Penggunaan Dyno** **{app.name}**:\n"
                f"    •**{AppHours} jam - "
                f"{AppMinutes} menit - {AppPercentage}%**"
                "\n  ≪━━◈≪━─━─࿇─━─━≫◈━━≫\n"
                " ❁ **Sisa Dyno Bulan Ini**:\n"
                f"    •**{hours} jam - {minutes} menit  "
                f"- {percentage}%**\n"
                "╰━━━━━━━━━━━━━━━━━━━━╯"
            )
            return True


async def progress(current, total, event, start, type_of_ps, file_name=None):
    """Generic progress_callback for uploads and downloads."""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join(["●" for i in range(math.floor(percentage / 10))]),
            "".join(["○" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )
        tmp = progress_str + "{0} of {1}\nETA: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            await event.edit(
                "{}\nFile Name: `{}`\n{}".format(type_of_ps, file_name, tmp)
            )
        else:
            await event.edit("{}\n{}".format(type_of_ps, tmp))


def humanbytes(size):
    """Input size in bytes,
    outputs in a human readable format"""
    # https://stackoverflow.com/a/49361727/4723940
    if not size:
        return ""
    # 2 ** 10 = 1024
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " day(s), ") if days else "")
        + ((str(hours) + " hour(s), ") if hours else "")
        + ((str(minutes) + " minute(s), ") if minutes else "")
        + ((str(seconds) + " second(s), ") if seconds else "")
        + ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    )
    return tmp[:-2]