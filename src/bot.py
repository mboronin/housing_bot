import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ParseMode
import logging
from src.dao import base, read_dao
from src import config
from tabulate import tabulate

bot = telegram.Bot(token=config.BOT_TOKEN)
updater = Updater(token=config.BOT_TOKEN)
connection = base.get_connection()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# Function to start the bot,initiated on /start command
def start(bot, update):
    message = "*Hello and welcome to Uppsala Housing bot! We will help you find your new home !!!*"
    keyboard = [['Login'], ['Get all housing'], ['Set up filters'], ['Show one by one'], ['Help']]
    reply_markup = ReplyKeyboardMarkup(keyboard,
                                       one_time_keyboard=False,
                                       resize_keyboard=True)
    update.message.reply_text(message, reply_markup=reply_markup,parse_mode=ParseMode.MARKDOWN)
    return MENU

def login(bot, update):
    bot.send_chat_action(chat_id=update.effective_user.id, action=telegram.ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id, text='Enter your details in the following format : '
                                                          'Name, Address, Phone number')


def database(user_id, customer_name, address, phone_number):
    print(user_id, customer_name, address, phone_number)
    connection.execute(
        '''CREATE TABLE IF NOT EXISTS userdetails(user_id int,customer_name text,address text,phone_number int )''')
    connection.execute("INSERT INTO userdetails VALUES (?,?,?,?)", (user_id, customer_name, address, phone_number))
    connection.commit()


# Function to save user details in the database
def saveuserDetails(bot, update):
    user_id = update.message.from_user.id
    customer_name, address, phone_number = update.message.text.split(',')
    database(user_id, customer_name, address, phone_number)


# Function to ask user about type of pizza he wants to order
def selection(bot, update):
    reply_markup = telegram.ReplyKeyboardRemove()

    print("message sent by user", update.message.text)
    if update.message.text == 'Get all available housing':
        result = read_dao.get_object(100026009613)
        bot.send_message(chat_id=update.message.chat_id, text=result)
    elif update.message.text == 'Non Veg':
        nonvegpizzaoptions(bot, update)


def show_all(bot, update, result):
    for row in result:
        bot.send_message(chat_id=update.message.chat_id, text=row[1])


def vegpizzaoptions(bot, update):
    print("inside vegpizaa method")
    # button_labels = connection.execute("SELECT name from pizza_details where type=='VEG'")
    for row in connection.execute("SELECT name from pizza_details where type=='VEG'"):
        print(row)
    # print("Button labesl ",button_labels)
    # button_list=[InlineKeyboardButton(button_labels,callback_data=1)]
    # reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=len(button_labels)))
    # update.message.reply_text("Please choose from the following : ",reply_markup=reply_markup)
    # bot.send_message(chat_id=update.message.chat_id, text='Choose from the following',reply_markup=reply_markup)


def nonvegpizzaoptions(bot, update):
    for row in connection.execute("SELECT name from pizza_details where type=='NonVeg'"):
        button_labels = row
    print("Button Labels", button_labels)
    button_list = [
        InlineKeyboardButton('Cheese Chicken ', callback_data=1),
        InlineKeyboardButton('Mushroom Chicken ', callback_data=2)]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    # update.message.reply_text("Please choose from the following : ",reply_markup=reply_markup)
    bot.send_message(chat_id=update.message.chat_id, text='Choose from the following', reply_markup=reply_markup)


# Function to check the userdetails initiated by user on /checkdetails command
def checkDetails(bot, update):
    value = update.message.from_user.id
    print("VALUE : ", value)
    for row in connection.execute("SELECT *from userdetails WHERE user_id=?", (value,)):
        print(row)
        user_id, customer_name, address, phone_number = row
    labels = ["Customer Name : ", "Address : ", "Phone Number : "]
    data = [customer_name, address, phone_number]
    table = zip(labels, data)
    list = tabulate(table, tablefmt="fancy_grid")
    bot.send_message(chat_id=update.message.chat_id, text=list)


# FUNCTION FOR ORDERING PIZZA
def show_menu(bot, update):
    button_labels = [['Login'], ['Get all available housing'], ['Set up filters'], ['Get houses one-by-one'], ['Help']]
    reply_keyboard = telegram.ReplyKeyboardMarkup(button_labels)
    bot.send_chat_action(chat_id=update.effective_user.id, action=telegram.ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id, text='Select your action', reply_markup=reply_keyboard)


def button(bot, update):
    query = update.callback_query
    bot.send_chat_action(chat_id=update.effective_user.id, action=telegram.ChatAction.TYPING)
    bot.edit_message_text(text="Your order is received and will be delivered within 30 mins",
                          chat_id=query.message.chat_id, message_id=query.message.message_id)


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def offers():
    cursor = connection.cursor()
    return cursor.execute('SELECT * from housing.rentals;')


def main():
    updater.dispatcher.add_handler(CommandHandler('start', start))

    updater.dispatcher.add_handler(CommandHandler('checkdetails', checkDetails))
    updater.dispatcher.add_handler(CommandHandler('offers', offers))

    updater.dispatcher.add_handler(MessageHandler(Filters.text, saveuserDetails), group=0)
    updater.dispatcher.add_handler(MessageHandler(Filters.text, selection), group=1)
    updater.dispatcher.add_handler((CallbackQueryHandler(button)))
    updater.start_polling()


main()
