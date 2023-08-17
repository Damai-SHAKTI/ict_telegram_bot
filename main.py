import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "6309347882:AAHo2tN80esIDdmBrLXy_AECq4JvFWjqkLI"

TITLE = "*ICT HKDSE PAST PAPER*"

query_count: int = 1
user_query: dict = {
    "year": "",
    "part": "",
    "question_number": ""
}
past_papers = None
past_papers_file_name: str = "past_papers.json"

exam_years = [
    [
        InlineKeyboardButton("2012", callback_data="2012"),
        InlineKeyboardButton("2013", callback_data="2013"),
        InlineKeyboardButton("2014", callback_data="2014"),
        InlineKeyboardButton("2015", callback_data="2015"),
    ],
    [
        InlineKeyboardButton("2016", callback_data="2016"),
        InlineKeyboardButton("2017", callback_data="2017"),
        InlineKeyboardButton("2018", callback_data="2018"),
        InlineKeyboardButton("2019", callback_data="2019"),
    ],
    [
        InlineKeyboardButton("2020", callback_data="2020"),
        InlineKeyboardButton("2021", callback_data="2021"),
        InlineKeyboardButton("2022", callback_data="2022"),
        InlineKeyboardButton("2023", callback_data="2023"),
    ],
]

parts = [
    InlineKeyboardButton("A", callback_data="A"),
    InlineKeyboardButton("B", callback_data="B"),
]


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reset_data()
    load_past_papers()
    await update.message.reply_text(f"{TITLE} \nPlease select examination year: ", reply_markup=prompt_exam_year(), parse_mode="Markdown")


def reset_data() -> None:
    global query_count, user_query

    query_count = 1
    user_query = {
        "year": "",
        "part": "",
        "question_number": ""
    }


def load_past_papers() -> None:
    global past_papers, past_papers_file_name
    try:
        past_paper_file = open(past_papers_file_name, "r")
        past_papers = json.load(past_paper_file)
    except FileNotFoundError:
        print(f"File {past_papers_file_name} not found.  Aborting")
    except OSError:
        print(f"OS error occurred trying to open {past_papers_file_name}")
    except Exception as err:
        print(f"Unexpected error opening {past_papers_file_name} is", repr(err))


def is_positive_integer(num: any) -> bool:
    try:
        value = int(num)
        return value > 0
    except ValueError:
        return False


def prompt_exam_year() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(exam_years)


def prompt_part() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([parts])


async def user_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global query_count
    query = update.callback_query
    await query.answer()

    if query_count == 1:
        user_query["year"] = query.data
        new_text: str = f"{TITLE} \nYear: {user_query['year']} \nPlease enter part (A/B): "
        await query.edit_message_text(text=new_text, reply_markup=prompt_part(), parse_mode="Markdown")
    elif query_count == 2:
        user_query["part"] = query.data
        new_text: str = f"{TITLE} \nYear: {user_query['year']} \nPart: {user_query['part']} \nPlease input question number: "
        await query.edit_message_text(text=new_text, parse_mode="Markdown")

    query_count += 1


async def handle_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if query_count == 3:
        user_question_number: str = update.message.text
        reply_text: str = f"{TITLE} \nYear: {user_query['year']} \nPart: {user_query['part']} \nQuestion number: {user_question_number} \nYoutube: Not found"
        if is_positive_integer(user_question_number):
            user_query["question_number"] = user_question_number
            for past_paper in past_papers:
                if user_query["year"] == past_paper["year"] and user_query["part"] == past_paper["part"] and user_query["question_number"] == past_paper["question_number"]:
                    reply_text = f"{TITLE} \nYear: {user_query['year']} \nPart: {user_query['part']} \nQuestion number: {user_question_number} \nYoutube: {past_paper['youtube_url']}"
        else:
            reply_text = "Please enter valid positive integer"
        await update.message.reply_text(reply_text, parse_mode="Markdown")


def main() -> None:
    print("===== Starting bot... =====")
    # init Bot
    bot = Application.builder().token(TOKEN).build()
    # commands
    bot.add_handler(CommandHandler('start', start_command))
    # callback of selected option
    bot.add_handler(CallbackQueryHandler(user_answer))
    # handle user input
    bot.add_handler(MessageHandler(filters.TEXT, handle_user_input))
    # check for updates
    bot.run_polling(poll_interval=0)


if __name__ == "__main__":
    main()
