from telebot import types
import db_fun
from utils import send_start_buttons

db = db_fun.ApplicationDB()
user_data = {}


def send_long_message(bot, chat_id, text):
    # Telegram has a limit of 4096 characters per message
    max_message_length = 4096
    # If text exceeds the max length, split it into smaller messages
    for i in range(0, len(text), max_message_length):
        bot.send_message(chat_id, text=text[i:i+max_message_length])
def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start_message(message):
        try:
            send_start_buttons(bot, message.chat.id, message.from_user.first_name)
        except Exception as e:
            bot.send_message(message.chat.id, "Something went wrong with /start. Try one more time.")
            print(f"Error in start_message: {e}")

    @bot.message_handler(content_types=['text'])
    def buttons(message):
        try:
            match message.text:
                case "Start":
                    # Add your start logic here
                    pass
                case "Add Application":
                    bot.send_message(message.chat.id, "Write the company name:")
                    bot.register_next_step_handler(message, process_company_name)
                case "Show all Applications":
                    applications = db.view_all_applications()
                    if applications:
                        text = "\n".join([
                            f"ID: {app[0]}, Company: {app[1]}, Position: {app[2]}, Date: {app[3]}, Status: {app[4]}, Link: {app[5]}, Description: {app[6]}, Place: {app[7]}"
                            for app in applications])
                # Send message in chunks if it's too long
                        send_long_message(bot, message.chat.id, text)
                    else:
                        bot.send_message(message.chat.id, "No applications")
                case "Change status of Application":
                    bot.send_message(message.chat.id, "Enter the application ID that you would like to change:")
                    bot.register_next_step_handler(message, process_application_id_change)
                case "Delete Application":
                    bot.send_message(message.chat.id, 'Enter the application ID that you would like to delete:')
                    bot.register_next_step_handler(message, process_application_id_delete)
                case "Delete all Applications":
                    confirm_delete_all(bot, message)
                case "Find Application":
                    bot.send_message(message.chat.id, "Enter the key word you would like to find:")
                    bot.register_next_step_handler(message, process_find_application)
                case _:
                    bot.send_message(message.chat.id, "Unknown command. Please, use the following buttons.")
                    send_start_buttons(bot, message.chat.id)
        except Exception as e:
            bot.send_message(message.chat.id, "Something went wrong. Try one more time.")
            print(f"Error in buttons handler: {e}")

    # All helper functions and callback handlers are defined below

    def process_company_name(message):
        try:
            chat_id = message.chat.id
            user_data[chat_id] = {'company': message.text}
            bot.send_message(chat_id, "Enter the name of position")
            bot.register_next_step_handler(message, process_position)
        except Exception as e:
            bot.send_message(message.chat.id, "Something went wrong. Try one more time.")
            print(f"Error in process_company_name: {e}")

    def process_position(message):
        try:
            chat_id = message.chat.id
            user_data[chat_id]['position'] = message.text
            bot.send_message(chat_id, "Enter the day of application")
            bot.register_next_step_handler(message, process_date)
        except Exception as e:
            bot.send_message(message.chat.id, "Something went wrong. Try one more time.")
            print(f"Error in process_position: {e}")

    def process_date(message):
        try:
            chat_id = message.chat.id
            user_data[chat_id]['date'] = message.text
            bot.send_message(chat_id, "Enter the application status:")
            bot.register_next_step_handler(message, process_status)
        except Exception as e:
            bot.send_message(message.chat.id, "Something went wrong. Try one more time.")
            print(f"Error in process_date: {e}")

    def process_status(message):
        try:
            chat_id = message.chat.id
            user_data[chat_id]['status'] = message.text
            bot.send_message(chat_id, "Enter the application link:")
            bot.register_next_step_handler(message, process_link)
        except Exception as e:
            bot.send_message(message.chat.id, "Something went wrong. Try one more time.")
            print(f"Error in process_status: {e}")

    def process_link(message):
        try:
            chat_id = message.chat.id
            user_data[chat_id]['link'] = message.text
            bot.send_message(chat_id, "Enter the application description:")
            bot.register_next_step_handler(message, process_description)
        except Exception as e:
            bot.send_message(message.chat.id, "Something went wrong. Try one more time.")
            print(f"Error in process_link: {e}")

    def process_description(message):
        try:
            chat_id = message.chat.id
            user_data[chat_id]['description'] = message.text
            bot.send_message(chat_id, "Enter the place of application")
            bot.register_next_step_handler(message, process_place)
        except Exception as e:
            bot.send_message(message.chat.id, "Произошла ошибка при вводе описания. Попробуйте снова.")
            print(f"Error in process_description: {e}")

    def process_place(message):
        try:
            chat_id = message.chat.id
            user_data[chat_id]['place'] = message.text

            summary = (
                f"Company: {user_data[chat_id]['company']}\n"
                f"Position: {user_data[chat_id]['position']}\n"
                f"Data: {user_data[chat_id]['date']}\n"
                f"Status: {user_data[chat_id]['status']}\n"
                f"Link: {user_data[chat_id]['link']}\n"
                f"Description: {user_data[chat_id]['description']}\n"
                f"Place: {user_data[chat_id]['place']}"
            )

            markup = types.InlineKeyboardMarkup()
            button_yes = types.InlineKeyboardButton("Yes", callback_data="confirm_yes")
            button_no = types.InlineKeyboardButton("No", callback_data="confirm_no")
            markup.add(button_yes, button_no)

            bot.send_message(chat_id, f"Check entered data\n\n{summary}\n\nIs it correct?", reply_markup=markup)
        except Exception as e:
            bot.send_message(message.chat.id, "Something went wrong. Try one more time.")
            print(f"Error in process_place: {e}")

    @bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_'))
    def callback_confirm(call):
        try:
            chat_id = call.message.chat.id

            if call.data == "confirm_yes":
                db.add_application(
                    user_data[chat_id]['company'],
                    user_data[chat_id]['position'],
                    user_data[chat_id]['date'],
                    user_data[chat_id]['status'],
                    user_data[chat_id]['link'],
                    user_data[chat_id]['description'],
                    user_data[chat_id]['place']
                )
                bot.send_message(chat_id, "Successfully added!")
                user_data.pop(chat_id)
                send_start_buttons(bot, chat_id)
            elif call.data == "confirm_no":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for key in user_data[chat_id]:
                    markup.add(types.KeyboardButton(key))
                bot.send_message(chat_id, "Which data would you like to change?", reply_markup=markup)
                bot.register_next_step_handler(call.message, process_field_choice)
        except Exception as e:
            bot.send_message(call.message.chat.id, "Something went wrong. Try one more time.")
            print(f"Error in callback_confirm: {e}")

    def process_field_choice(message):
        try:
            chat_id = message.chat.id
            field = message.text

            if field in user_data[chat_id]:
                bot.send_message(chat_id, f"Enter new value for  {field}:")
                bot.register_next_step_handler(message, lambda msg: process_new_value(msg, field))
            else:
                bot.send_message(chat_id, "Wrong choice, try one more time.")
                bot.register_next_step_handler(message, process_field_choice)
        except Exception as e:
            bot.send_message(message.chat.id, "Something went wrong. Try one more time.")
            print(f"Error in process_field_choice: {e}")

    def process_new_value(message, field):
        try:
            chat_id = message.chat.id
            user_data[chat_id][field] = message.text
            process_place(message)
        except Exception as e:
            bot.send_message(message.chat.id, "Something went wrong. Try one more time.")
            print(f"Error in process_new_value: {e}")

    def process_application_id_change(message):
        try:
            chat_id = message.chat.id
            application_id = message.text

            user_data[chat_id] = {'application_id': application_id}

            bot.send_message(chat_id, "Enter new status for application")
            bot.register_next_step_handler(message, process_new_status)
        except Exception as e:
            bot.send_message(message.chat.id, "Something went wrong. Try one more time.")
            print(f"Error in process_application_id_change: {e}")

    def process_new_status(message):
        try:
            chat_id = message.chat.id
            new_status = message.text

            application_id = user_data[chat_id]['application_id']

            db.update_application_status(application_id, new_status)

            bot.send_message(chat_id, f"Status of application with ID {application_id} successfully change to '{new_status}'.")
            user_data.pop(chat_id)
            send_start_buttons(bot, chat_id)
        except Exception as e:
            bot.send_message(message.chat.id, "Something went wrong. Try one more time.")
            print(f"Error in process_new_status: {e}")

    def process_application_id_delete(message):
        try:
            chat_id = message.chat.id
            application_id = message.text
            db.delete_application(application_id)
            bot.send_message(chat_id, f"Application with ID {application_id} successfully deleted.")
            send_start_buttons(bot, chat_id)
        except Exception as e:
            bot.send_message(message.chat.id, "Something went wrong. Try one more time.")
            print(f"Error in process_application_id_delete: {e}")

    def confirm_delete_all(bot, message):
        try:
            chat_id = message.chat.id
            markup = types.InlineKeyboardMarkup()
            button_yes = types.InlineKeyboardButton("Yes", callback_data="delete_all_yes")
            button_no = types.InlineKeyboardButton("No", callback_data="delete_all_no")
            markup.add(button_yes, button_no)
            bot.send_message(chat_id, "Are you sure to delete all application?", reply_markup=markup)
        except Exception as e:
            bot.send_message(message.chat.id,
                             "Something went wrong. Try one more time.")
            print(f"Error in confirm_delete_all: {e}")

    @bot.callback_query_handler(func=lambda call: call.data.startswith('delete_all_'))
    def callback_delete_all(call):
        try:
            chat_id = call.message.chat.id

            if call.data == "delete_all_yes":
                db.delete_all_applications()
                bot.send_message(chat_id, "All applications successfully deleted.")
                send_start_buttons(bot, chat_id)
            elif call.data == "delete_all_no":
                bot.send_message(chat_id, "Deletion canceled.")
                send_start_buttons(bot, chat_id)
        except Exception as e:
            bot.send_message(call.message.chat.id, "Something went wrong. Try one more time.")
            print(f"Error in callback_delete_all: {e}")

    def process_find_application(message):
        try:
            chat_id = message.chat.id
            search_word = message.text

            applications = db.find_application(search_word)
            if applications:
                text = "\n".join([
                    f"ID: {app[0]}, Company: {app[1]}, Position: {app[2]}, Data: {app[3]}, Status: {app[4]}, Link: {app[5]}, Description: {app[6]}, Place: {app[7]}"
                    for app in applications])
            else:
                text = "No applications"

            bot.send_message(chat_id, text=text)
            send_start_buttons(bot, chat_id)
        except Exception as e:
            bot.send_message(message.chat.id, "Something went wrong. Try one more time.")
            print(f"Error in process_find_application: {e}")


