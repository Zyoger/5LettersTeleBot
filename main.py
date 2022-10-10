#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context.

word = "1"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    chat_id = update.effective_message.chat_id
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!"
    )
    await update.message.reply_text(
        f"Это бот для игры 5 букв у Тинькова."
    )
    await update.message.reply_text(
        f"Сейчас в базе {len(get_array_words())} слов. Введи первое слово. /w <слово>"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("-----Добавить помощь-----")


async def get_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """"""
    word = context.args[0]
    await update.effective_message.reply_text(f"Слово из {len(word)} букв.")
    await update.message.reply_text(f"Составь маску. (+) - буква на месте, (=) - буква правильная, но не на месте, (-) - такой буквы нет.")
    await update.message.reply_text(f"Введи маску, /m <*****>")
    return word


async def get_mask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """"""
    mask = context.args[0]
    await update.effective_message.reply_text(f"Маска: '{mask}'.")
    return mask


def get_array_words():
    """"""
    with open("data\\words.txt", "r", encoding="utf-8") as file:
        words_array = [row.strip('\n') for row in file]
    return words_array


def filter_by_length(array, words_mask):
    """Фильтрует массив по количеству букв в исходном слове"""
    new_array = []
    for i in range(0, len(array)):
        if len(array[i]) == len(words_mask):
            new_array.append(array[i])
    return new_array


def main() -> None:
    application = Application.builder().token("5669784334:AAHe_DyzWPnwBU_-7PFCL6qSQw9ujCPd7Gg").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))


    application.add_handler(CommandHandler("w", get_word))
    application.add_handler(CommandHandler("m", get_mask))
    print(word)

    application.run_polling()


if __name__ == "__main__":
    main()
