import requests
from dotenv import load_dotenv
import os
import aiogram.utils.markdown as md  # type: ignore
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, ReplyKeyboardMarkup  # type: ignore
from aiogram.utils import executor

import db
from history import History

load_dotenv()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add("Help").add("History")


async def on_start(_) -> None:
    await db.db_start()


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message) -> None:
    """
    This handler will send a welcome message to the user
    """
    await message.answer_sticker(
        "CAACAgIAAxkBAANlZB25Zg3-1deT8ZVs7ZHwuFjSuKQAAugcAAL8gylKGPFgwQkabc8vBA"
    )
    welcome_message = md.text(
        "Hello\nSend me the link of an article with a Paywall that you want to read for free. I will do my best to remove it using 12ft.io."
    )
    logging.info("bot has started")
    await message.reply(
        welcome_message, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard
    )


@dp.message_handler(text="Help")
async def provide_help(message: types.Message) -> None:
    help_msg = md.text(
        "What can I do?\nSend me the link of an article with a Paywall that you want to read for free. I will do my best "
        "to remove it using 12ft.io"
    )
    logging.warning(f'message "{message.text}" from user_id {message.from_user.id} \n')
    await message.reply(help_msg, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)


@dp.message_handler(text="History")
async def get_history(message: types.Message) -> None:
    user_history = db.get_history(message.from_user.username)
    logging.info(user_history)
    await message.reply(f"your history {user_history}")


@dp.message_handler()
async def process_article_link(message: types.Message) -> None:
    """
    This handler will process the article link provided by the user and remove paywall
    """
    article_link = message.text.strip()
    logging.warning(
        f"Received message {message.text} from {message.from_user.id}, message: {message}"
    )
    url = "%s%s" % (os.getenv("PAYWALLER"), article_link)
    r = requests.get(url)
    print(r.status_code)
    if r.status_code == 200:
        temp = History(
            user_id=message.from_user.id,
            name=message.from_user.username,
            url=article_link,
            res=r.url,
        )
        db.save_to_db(temp)
        await message.reply(r.url)
    else:
        logging.error(f"invalid link {article_link}")
        await message.reply("Failed to remove paywall. Please try again.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)
