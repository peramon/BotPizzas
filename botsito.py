from telegram.ext import *
import logging
import DBPedia as dbpedia
import Menu as Op
import OWLmypizza as owl
import Spacy as pln
from telegram import InlineKeyboardButton, InlineKeyboardMarkup



# Set up the logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')

# Message error


def error(update, context):
    logging.error(f'Update {update} caused error {context.error}')

# MENUS

def start_command(update, context):

    update.message.reply_text(
        'Bienvenido :\n\nOfrecemos un menu variado de pizzas \nEspero encuentres lo que '
        'Por favor seleccione o inserte \'/\' más la opción:\n')
    update.message.reply_text(
        text='1. Lista de 5 pizzas recomendadas(Dbpedia)\n2. Lista de pizzas tradicionales(OWL)'
             '\n3. Introducir un mensaje',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='PizzasRecomendadas', callback_data='PizzasRecomendadas')],
            [InlineKeyboardButton(text='PizzasTradicionales', callback_data='PizzasTradicionales')],
            [InlineKeyboardButton(text='Mensaje Personalizado', callback_data='PLN')],
        ])
        )


def types_command_dbpedia(update, context):
    qres = dbpedia.get_response_dbpedia_pizzas()
    for i in range(len(qres['results']['bindings'])):
        result = qres['results']['bindings'][i]
        name, ing,  image_url = result['name']['value'], result['res']['value'], result['image']['value']
        mensaje ='Pizza : ' + name + "\n Ingredientes: " + ing +"\n" + image_url
        update.callback_query.message.reply_text(mensaje)



def types_command_owl(update, context):
    qres = owl.get_response_pizzas()
    for i in range(len(qres['results']['bindings'])):
        result = qres['results']['bindings'][i]
        name = result['name']['value']
        qres2 = owl.get_response_ingredients(name)
        update.callback_query.message.reply_text('Nombre de la pizza : ' + name)
        update.callback_query.message.reply_text('ingredientes : ')
        for j in range(len(qres2['results']['bindings'])):
            result2 = qres2['results']['bindings'][j]
            name2 = result2['name']['value']
            update.callback_query.message.reply_text(name2)


def processText(update, context):
    # update.message.reply_text("Ingresa el mensaje")
    mytxt = update.message.text  # obtener el texto que envio el usuario
    print(mytxt)
    doc = pln.spacy_info(mytxt)
    for w in doc:
        a = w.text + "\nAun estamos trabajando en esto"
        update.message.reply_text(a)


if __name__ == '__main__':
    updater = Updater(token="1781905513:AAEQ-KAY_UPonjsXzT1FtiBMiaodgbYJ2U8", use_context=True)
    dp = updater.dispatcher
    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CallbackQueryHandler(pattern='PizzasRecomendadas', callback=types_command_dbpedia))
    dp.add_handler(CallbackQueryHandler(pattern='PizzasTradicionales', callback=types_command_owl))
    dp.add_handler(MessageHandler(Filters.text, processText))
    # Messages
    # Log all errors
    dp.add_error_handler(error)
    # Run the bot
    updater.start_polling(1.0)
    updater.idle()


