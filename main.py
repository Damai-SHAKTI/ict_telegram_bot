import os
import json
from dotenv import load_dotenv
from datetime import datetime
from telegram import Update
from telegram import InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

from database import get_database
from constants import TITLE, PAST_PAPERS_FILE
from buttons import exam_years_buttons, parts_buttons, feed_back_buttons

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

db_telegram = get_database()
stats = db_telegram["stats"]

query_count: int = 1
user_query: dict = {
    "year": "",
    "part": "",
    "question_number": ""
}
past_papers = None


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reset_data()
    load_past_papers()
    chat_id = update.message.chat_id
    await context.bot.send_message(text=f"{TITLE} \nPlease select examination year: ", chat_id=chat_id, reply_markup=prompt_exam_year(), parse_mode="Markdown")


def reset_data() -> None:
    global query_count, user_query

    query_count = 1
    user_query = {
        "year": "",
        "part": "",
        "question_number": ""
    }
    print("===== Reset data =====")


def load_past_papers() -> None:
    global past_papers
    try:
        past_paper_file = open(PAST_PAPERS_FILE, "r")
        past_papers = json.load(past_paper_file)
        print(f"===== {PAST_PAPERS_FILE} loaded =====")
    except FileNotFoundError:
        print(f"File {PAST_PAPERS_FILE} not found.  Aborting")
    except OSError:
        print(f"OS error occurred trying to open {PAST_PAPERS_FILE}")
    except Exception as err:
        print(f"Unexpected error opening {PAST_PAPERS_FILE} is", repr(err))


def is_positive_integer(num: any) -> bool:
    try:
        value = int(num)
        return value > 0
    except ValueError:
        return False


async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"*STATS* \nMost asked: 10", parse_mode="Markdown")


def prompt_exam_year() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(exam_years_buttons)


def prompt_part() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([parts_buttons])


def prompt_feedback() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([feed_back_buttons])


async def user_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global query_count

    query = update.callback_query
    chat_id = update.callback_query.message.chat_id
    message_id = update.callback_query.message.message_id
    await query.answer()

    if "feed_back" in str(query):
        rating = int(query.data[-1])
        new_text: str = f"Thank you for your feedback. \nIf you have any further questions, please feel free to ask by typing /start"
        await context.bot.edit_message_text(text=new_text, parse_mode="Markdown", chat_id=chat_id, message_id=message_id)
        return

    if query_count == 1 and user_query["year"] == "" and len(query.data) == 4:
        query_count += 1
        user_query["year"] = query.data
        new_text: str = f"{TITLE} \nYear: {user_query['year']} \nPlease enter part (A/B): "
        await context.bot.edit_message_text(text=new_text, reply_markup=prompt_part(), parse_mode="Markdown", chat_id=chat_id, message_id=message_id)

    elif query_count == 2 and user_query["part"] == "" and len(query.data) == 1:
        query_count += 1
        user_query["part"] = query.data
        new_text: str = f"{TITLE} \nYear: {user_query['year']} \nPart: {user_query['part']} \nPlease input question number: "
        await context.bot.edit_message_text(text=new_text, parse_mode="Markdown", chat_id=chat_id, message_id=message_id)


async def handle_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if query_count == 3:
        chat_id = update.message.chat_id
        user_info = update.message.from_user
        user_question_number: str = update.message.text
        reply_text: str = f"{TITLE} \nYear: {user_query['year']} \nPart: {user_query['part']} \nQuestion number: {user_question_number} \nYoutube: Not found"

        if is_positive_integer(user_question_number):
            user_query["question_number"] = user_question_number
            for past_paper in past_papers:
                if user_query["year"] == past_paper["year"] and user_query["part"] == past_paper["part"] and user_query["question_number"] == past_paper["question_number"]:
                    user_details = f"By {user_info['first_name']} {user_info['last_name']} at {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}"
                    reply_text = f"{user_details} \n{TITLE} \nYear: {user_query['year']} \nPart: {user_query['part']} \nQuestion number: {user_question_number} \nYoutube: {past_paper['youtube_url']}"
                    # try:
                    #     document = {
                    #         "user_name": (user_info['first_name'] + " " + user_info['last_name']),
                    #         "date": datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                    #         "question_year": user_query["year"],
                    #         "question_part": user_query["part"],
                    #         "question_number": user_query["question_number"]
                    #     }
                    #     stats.insert_one(document)
                    # except Exception as exp:
                    #     print(exp)
        else:
            reply_text = "Please enter valid positive integer"
        await context.bot.send_message(text=reply_text, parse_mode="Markdown", chat_id=chat_id)

        if reply_text != "Please enter valid positive integer":
            await context.bot.send_message(text="Please give us your feedback:", reply_markup=prompt_feedback(), chat_id=chat_id)


def main() -> None:
    print("===== Starting bot... =====")
    # init bot
    bot = Application.builder().token(TOKEN).build()
    # bot commands
    bot.add_handler(CommandHandler('start', start_command))
    bot.add_handler(CommandHandler('stats', show_stats))
    # callback of selected option from the buttons
    bot.add_handler(CallbackQueryHandler(user_answer))
    # handle user input
    bot.add_handler(MessageHandler(filters.TEXT, handle_user_input))
    # check for new message updates
    bot.run_polling(poll_interval=1)


if __name__ == "__main__":
    main()
