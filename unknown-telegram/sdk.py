# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

from telethon import events
from telethon.extensions import html
from telethon.tl.custom.message import Message

from . import command, const, loader

Module = loader.Module
Event = events.NewMessage.Event
Command = command.Command


def escape_html(text: str) -> str:
    """Escape html-dangerous characters"""
    for key, val in {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
    }.items():
        text = text.replace(key, val)
    return text


def format_seconds(sec: int) -> str:
    """Format seconds into pretty string"""
    minute = 60
    hour = minute * 60
    day = hour * 24

    days = int(sec / day)
    hours = int((sec % day) / hour)
    minutes = int((sec % hour) / minute)
    seconds = int(sec % minute)
    string = ""
    if days > 0:
        string += str(days) + " " + (days == 1 and "day" or "days") + ", "
    if hours > 0:
        string += str(hours) + " " + (hours == 1 and "hour" or "hours") + ", "
    if minutes > 0:
        string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes") + ", "
    string += str(seconds) + " " + (seconds == 1 and "second" or "seconds")
    return string


# Very shitty code
async def send(message, content, **kwargs) -> list:
    """Helper for sending messages"""
    res = []

    if isinstance(content, Message):
        res.append(await message.respond(content, **kwargs))
        try:
            await message.delete()
        except:
            pass

    if isinstance(content, str) and not kwargs.get("force_file", False):
        text, entities = html.parse(content)
        if message.sender_id != (await message.client.get_me()).id:
            res.append(await message.reply(html.unparse(text[:4096], entities)))
        else:
            res.append(await message.edit(html.unparse(text[:4096], entities)))

        text = text[4096:]
        while len(text) > 0:
            message.entities = entities
            message.text = html.unparse(text[:4096], message.entities)
            text = text[4096:]
            res.append(await message.respond(message, parse_mode="HTML", **kwargs))
    else:
        if message.media is None:
            await message.edit(const.MESSAGE_SENDING_MEDIA)
            res.append(
                await message.client.send_file(
                    entity=message.chat_id,
                    file=content,
                    reply_to=message.reply_to_msg_id,
                    **kwargs
                )
            )
            try:
                await message.delete()
            except:
                pass
        else:
            res.append(await message.edit(file=content, **kwargs))
    return res
