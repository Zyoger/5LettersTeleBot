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
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_array_words():
    """"""
    with open("words.txt", "r", encoding="utf-8") as file:
        words_array = [row.strip('\n') for row in file]
    return words_array


word = "буква"
counter_worlds = 0
array_words = get_array_words()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    chat_id = update.effective_message.chat_id
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}!"
    )
    await update.message.reply_text(
        f"Сейчас в базе {len(get_array_words())} слов. Введи первое слово. Пример: /w <буква>"
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    global array_words
    global word
    array_words = get_array_words()
    word = "буква"
    await update.message.reply_text(f"Выполнен сброс.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("-----Добавить помощь-----")


async def get_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """"""
    global word
    word = context.args[0]
    await update.message.reply_text(f"Слово {word} из {len(word)} букв.")
    await update.message.reply_text(f"Введи маску. (y) - буква на месте, "
                                    f"(m) - буква правильная, но не на месте, "
                                    f"(n) - такой буквы нет. Шаблон маски, /m <*****>")


async def get_mask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """"""
    mask = context.args[0]
    global word
    global array_words
    array_words = filter_by_length(array_words, mask)
    array_words = filter_wrong_letter(array_words, mask, word)
    array_words = filter_right_letter(array_words, mask, word)
    array_words = filter_include_letter(array_words, mask, word)
    await update.message.reply_text(f"Всего подходящих слов: {len(array_words)} Варианты слов:")
    if len(array_words) >= 5:
        for i in range(0, 5):
            await update.message.reply_text(array_words[i])
    else:
        for i in range(0, len(array_words)):
            await update.message.reply_text(array_words[i])



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
            if words_mask[i] == "n" and current_word[i] in word:
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
            if words_mask[i] == "y":
                if word[i] != current_word[i]:
                    flag = False
        if flag:
            filter_array.append(word)
    return filter_array


def filter_include_letter(array, words_mask, current_word):
    """Фильтрует по букве которая есть в слове"""
    filter_array = []
    for word in array:
        flag = True
        for i in range(len(words_mask)):
            if words_mask[i] == "m":
                if current_word[i] not in word:
                    flag = False
                elif current_word[i] == word[i]:
                    flag = False
        if flag:
            filter_array.append(word)
    return filter_array


def main() -> None:
    application = Application.builder().token("5698474788:AAHVW2OF2hSss7cB8XhE7UjG41sbmjfXBMc").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("w", get_word))
    application.add_handler(CommandHandler("m", get_mask))
    application.add_handler(CommandHandler("r", reset))
    application.run_polling()


if __name__ == "__main__":
    main()
