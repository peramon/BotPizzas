# Pizza Recomender
## Estructura
- botsito.py
- DBpedia.py
- Menu.py
- OWLmypizza
- Spacy.py

## Configurando la owl
Primeramente nos dirigimnos al sitio oficial de [Fuseki](https://jena.apache.org/download/), luego al apartado de Apache Jena Fuseki, lo descargamos y lo instalamos.
Lo configuramos, puede revisar la configuración en este[enlace](https://programmerclick.com/article/88961947895/).
Luego creamos un [dataset](https://www.youtube.com/watch?v=W-g6oyjBkWk&t=297s) y subimos la nuestro archivo mypizza.owl de nuestro repositorio.
Podemos probar consulta de nestro dataset en la parte de query de Fuseki.
Luego nos vamos a info y copiamos la URL del repoitorio ya ponemos en el archivo OWLmypizza y podemos ir probando las consultas SPARQL.

## botsito.py
Esta clase contiene funcionalidades importantes, a continuación veremos la configureación del método que lanzara al comando start, el cuál es el encargado de iniciar el bot.
```python
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
```

Lo siguiente importante a rsaltar es el uso de de un metodo if para actualizar cada vez que hay una ionteracción nueva, además en esta parte podemos denfinir el **Token** de nuestro bot y las funciones o interacciones iniciales.

```python
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
```

## DBPedia.py
Esta clase contiene funcionalidades para consumir las pizzas recomendadas desde DBPedia. A continuación se muestra la funcionalidad necesaria para consumir los datos.

**URL del repositorio de la ontología en DBpedia**
```python
sparql = SPARQLWrapper('https://dbpedia.org/sparql')
```
**Función que contiene la consulta SPARQL para traer las pizzas desde DBpedia**
```python
def get_response_dbpedia_pizzas():
    sparql.setQuery(f'''
       SELECT ?name ?res  ?image 
         WHERE {{
            ?object dbo:type dbr:Pizza .
            ?object  dbp:mainIngredient ?res .
            ?object rdfs:label ?name .
            ?object dbo:thumbnail ?image 
            FILTER (lang(?name) = 'es')     
        }}
    ''')
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()
    return qres
```
## Menu.py
Esta clase contiene la funcionalidad del menu inicial del bot.
```python
def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Contribuye en la elaboración del bot',
                                      url='https://github.com/peramon/BotsitoPizza')],
                [InlineKeyboardButton(
                    'Menu Pizzas', callback_data='m1')]]
    return InlineKeyboardMarkup(keyboard)
```

## OWLmypizza.py
Esta clase contiene funcionalidades para consumir las pizzas tradicionales desde nuestra owl. A continuación se muestra la funcionalidad necesaria para consumir los datos.

**URL del repositorio de la ontología.**
```python
sparql = SPARQLWrapper(
    'http://localhost:3030/pizzasApi/sparql')
```
**Función que contiene la consulta SPARQL para traer las pizzas**
```python
def get_response_pizzas():
    # Consulta para sacar las pizzas
    sparql.setQuery('''
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX pizza:<http://www.semanticweb.org/paul/ontologies/2021/5/mypizza#>
        SELECT DISTINCT ?name 
        WHERE { 
            ?s rdfs:subClassOf pizza:Named_pizza .
            ?s rdfs:label ?name
            FILTER (lang(?name) = 'es')
        }
    ''')
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()
    return qres
```
## Spacy.py
Esta clase contiene funcionalidades para procesar el texto.

```python
import spacy
nlp = spacy.load("en_core_web_sm")

def spacy_info(text):
    doc = nlp(text)
    print([(w.text, w.pos_) for w in doc])
    return doc
```

