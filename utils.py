from telebot import types

def send_start_buttons(bot, chat_id, first_name=None):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    action_button1 = types.KeyboardButton("Add Application")
    action_button2 = types.KeyboardButton("Show all Applications")
    action_button3 = types.KeyboardButton("Change status of Application")
    action_button4 = types.KeyboardButton("Delete Application")
    action_button5 = types.KeyboardButton("Delete all Applications")
    action_button6 = types.KeyboardButton("Find Application")

    markup.add( action_button1, action_button2, action_button3, action_button4, action_button5, action_button6)

    text = f"You can use the following functions:"

    bot.send_message(chat_id, text=text, reply_markup=markup)
