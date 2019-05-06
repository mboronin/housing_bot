import pytest
from src.bot import *


bot = telegram.Bot(token=config.BOT_TOKEN)
updater = Updater(token=config.BOT_TOKEN)

def test_main():
    result = main()
    assert result == 0



def test_main_menu():
    global bot
    res = main_menu()
    assert  res == 0



def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=main_menu_message())
    update.message.reply_text('Choose the option:', reply_markup=main_menu_keyboard())


# Function to ask user its details to register,initiated on /register command
def login(bot, update):
    query = update.callback_query
    details = read_dao.get_user(query.message.from_user.id)
    if details is None:
        # bot.send_chat_action(chat_id=query.effective_user.id, action=telegram.ChatAction.TYPING)
        bot.send_message(chat_id=query.message.chat_id, text='Enter your details in the following format : '
                                                             'username, password, name')
    else:
        bot.send_message(chat_id=update.message.chat_id, text='We already have your credentials, let\'s move on!')
        logging.debug("Login is " + config.USERNAME)
        logging.debug("Password is " + config.PASSWORD)
        config.USERNAME = details[0]
        config.PASSWORD = details[1]


def saveuserDetails(bot, update):
    userid = update.message.from_user.id
    username, password, name = update.message.text.split(',')
    write_dao.save_user([username, password, name, userid])


def one_by_one(bot, update):
    query = update.callback_query
    next_apt(bot, update)


def create_rental_table(apts):
    text = """| Address | Rent | Size | Number of rooms | Link |\n| --- | --- | --- | --- | --- |\n"""
    for apt in apts:
        text = text + "| " + str(apt.address[0]) + " | " + str(apt.rent[0]) + " sek" + " | " + str(
            apt.msize[0]) + " | " + str(apt.rooms[0]) + " | " + str(apt.link[0]) + " |\n"
    print(text)
    return text + ""


def show_all(bot, update):
    query = update.callback_query
    apts = read_dao.get_all_objects()
    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=create_rental_table(apts),
                          reply_markup=main_menu_keyboard(), parse_mode=telegram.ParseMode.MARKDOWN)


def apply_filters(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=filters_menu_message(),
                          reply_markup=filters_menu_keyboard())


def filters_menu_message():
    return "Select filters you want to apply"


def main_menu_message():
    return "Hey! This is Uppsala Housing bot.\n\n We will help you find your new home"


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def next_apt(bot, update):
    query = update.callback_query
    global apts, current
    print(current)
    apt = apts[current]
    current -= current
    print(current)
    bot.send_photo(chat_id=query.message.chat_id, photo=str(apt.imagelink[0]))
    message = "Adress is " + str(apt.address[0]) + "\n" + "Number of rooms is " + str(
        apt.rooms[0]) + "\n" + "Size is is " + str(apt.msize[0]) + "\n" + "Rent is " + str(
        apt.rent[0]) + "\n" + "View details here " + str(apt.link[0])
    bot.send_message(chat_id=query.message.chat_id,
                     message_id=query.message.message_id,
                     text=message,
                     reply_markup=one_by_one_keyboard())


def previous_apt(bot, update):
    query = update.callback_query
    global apts, current
    print(current)
    apt = apts[current]
    current += current
    print(current)
    bot.send_photo(chat_id=query.message.chat_id, photo=str(apt.imagelink[0]))
    message = "Adress is " + str(apt.address[0]) + "\n" + "Number of rooms is " + str(
        apt.rooms[0]) + "\n" + "Size is is " + str(apt.msize[0]) + "\n" + "Rent is " + str(
        apt.rent[0]) + "\n" + "View details here " + str(apt.link[0])
    bot.send_message(chat_id=query.message.chat_id,
                     message_id=query.message.message_id,
                     text=message,
                     reply_markup=one_by_one_keyboard())


def rent_filter(bot, update):
    bot.send_message("Type in min and max rent price separated by comma")
    config.MIN_RENT, config.MAX_RENT = update.message.text.split(',')


def room_filter(bot, update):
    bot.send_message("Type in number of rooms")
    config.ROOMS = update.message.text


def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Set login details', callback_data='login')],
                [InlineKeyboardButton('Apply filters', callback_data='choose filters')],
                [InlineKeyboardButton('Show one by one', callback_data='one_by_one')],
                [InlineKeyboardButton('Show all', callback_data='show_all')]]
    return InlineKeyboardMarkup(keyboard)


def filters_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Rent', callback_data='rent_filter')],
                [InlineKeyboardButton('Number of Rooms', callback_data='room_filter')]]
    return InlineKeyboardMarkup(keyboard)


def one_by_one_keyboard():
    keyboard = [[InlineKeyboardButton('Previous', callback_data='previous_apt')],
                [InlineKeyboardButton('Next', callback_data='next_apt')]]
    return InlineKeyboardMarkup(keyboard)


def main():
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(login, pattern='login'))
    updater.dispatcher.add_handler(CallbackQueryHandler(show_all, pattern='show_all'))
    updater.dispatcher.add_handler(CallbackQueryHandler(one_by_one, pattern='one_by_one'))
    updater.dispatcher.add_handler(CallbackQueryHandler(apply_filters, pattern='apply_filters'))
    updater.dispatcher.add_handler(CallbackQueryHandler(rent_filter, pattern='rent_filter'))
    updater.dispatcher.add_handler(CallbackQueryHandler(room_filter, pattern='room_filter'))
    updater.dispatcher.add_handler(CallbackQueryHandler(next_apt, pattern='next_apt'))
    updater.dispatcher.add_handler(CallbackQueryHandler(previous_apt, pattern='previous_apt'))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, saveuserDetails), group=0)
    updater.start_polling()


main()
