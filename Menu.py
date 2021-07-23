from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Contribuye en la elaboración del bot',
                                      url='https://github.com/peramon/BotsitoPizza')],
                [InlineKeyboardButton(
                    'Menu Pizzas', callback_data='m1')]]
    return InlineKeyboardMarkup(keyboard)

