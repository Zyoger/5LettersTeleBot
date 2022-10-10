#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

import logging
import random
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

def get_array_words():
    """"""
    with open("data\\words.txt", "r", encoding="utf-8") as file:
        words_array = [row.strip('\n') for row in file]
    return words_array


word = "буква"
counter_worlds = 0
array_words = []
array_words = get_array_words()


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
    await update.message.reply_text(f"Слово {word} из {len(word)} букв.")
    await update.message.reply_text(f"Составь маску. (+) - буква на месте, "
                                    f"(=) - буква правильная, но не на месте, "
                                    f"(-) - такой буквы нет.")
    await update.message.reply_text(f"Введи маску, /m <*****>")
    return word


async def get_mask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """"""
    mask = context.args[0]
    global word
    global array_words
    await update.effective_message.reply_text("Варианты слов:")
    print("mask", mask)
    print("word", word)
    array_words = filter_by_length(array_words, mask)
    array_words = filter_wrong_letter(array_words, mask, word)
    array_words = filter_right_letter(array_words, mask, word)
    array_words = filter_include_letter(array_words, mask, word)
    print(len(array_words))
    print(array_words)
    for i in range(0, 10):
        await update.effective_message.reply_text(array_words[random.randint(0, len(array_words))])




def filter_by_length(array, words_mask):
    """Фильтрует массив по количеству букв в исходном слове"""
    new_array = []
    for i in range(0, len(array)):
        if len(array[i]) == len(words_mask):
            new_array.append(array[i])
    return new_array


def filter_wrong_letter(array, words_mask, current_word):
    """Фильтрует по буквам которых нет в слове"""
    filter_array = []
    for word in array:
        flag = True
        for i in range(len(word)):
            if words_mask[i] == "-" and current_word[i] in word:
                flag = False
        if flag:
            filter_array.append(word)
    return filter_array


def filter_right_letter(array, words_mask, current_word):
    """Фильтрует по правильной букве"""
    filter_array = []
    for word in array:
        flag = True
        for i in range(len(word)):
            if words_mask[i] == "+":
                if word[i] != current_word[i]:
                    flag = False
        if flag:
            filter_array.append(word)
    return filter_array


def filter_include_letter(array, words_mask, current_word):
    """Фильтрует по букве которая есть в слове"""
    filter_array = []
    for word in array:
        flag_1 = True
        for i in range(len(words_mask)):
            if words_mask[i] == "=":
                if current_word[i] not in word:
                    flag_1 = False
                elif current_word[i] == word[i]:
                    flag_1 = False
        if flag_1:
            filter_array.append(word)
    return filter_array



def main() -> None:
    application = Application.builder().token("5669784334:AAHe_DyzWPnwBU_-7PFCL6qSQw9ujCPd7Gg").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(CommandHandler("w", get_word))
    application.add_handler(CommandHandler("m", get_mask))

    application.run_polling()


if __name__ == "__main__":
    main()
