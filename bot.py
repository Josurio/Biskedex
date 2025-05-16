import os
import telebot
import time
from telebot import types
from flask import Flask, request

TOKEN = '8067492976:AAH6-jnBPKIsG8Yb1tjN0jhGgrFvq9ErRWc'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "Bot funcionando!"

# Diccionario para guardar nombres por chat
usuarios = {}
estados = {}

# GENERO
@bot.message_handler(commands=['start', 'hola'])
def saludar(message):
    estados[message.chat.id] = 'genero'
    bot.reply_to(message, "¡Hola entrenadorx Biskymón! Bienvenida a la Biskedex, este dispositivo que se te a entregado tiene múltiples funciones que te ayudarán en tu aventura, pero antes necesito saber como referirme a ti. Escribe el género con el que te sientes mejor identificx:")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👦 Masculino")
    btn2 = types.KeyboardButton("👧 Femenino")
    btn3 = types.KeyboardButton("🪼 No binario")
    btn4 = types.KeyboardButton("🦖 Otro")
    btn5 = types.KeyboardButton("🚁 Helicoptero apache")
    btn6 = types.KeyboardButton("👩‍🔧 Chief")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)

    bot.send_message(message.chat.id, "Elige una opción:", reply_markup=markup)

@bot.message_handler(func=lambda msg: estados.get(msg.chat.id) == 'genero')
def responder_opciones(msg):
    if msg.text == "👦 Masculino":
        if msg.chat.id not in usuarios:
            usuarios[msg.chat.id] = {}  # Creamos un sub-diccionario para ese usuario si no existe
        usuarios[msg.chat.id]['genero'] = '👦'  # Guardamos el género
    elif msg.text == "👧 Femenino":
        if msg.chat.id not in usuarios:
            usuarios[msg.chat.id] = {}  # Creamos un sub-diccionario para ese usuario si no existe
        usuarios[msg.chat.id]['genero'] = '👧'  # Guardamos el género
    elif msg.text == "🪼 No binario":
        if msg.chat.id not in usuarios:
            usuarios[msg.chat.id] = {}  # Creamos un sub-diccionario para ese usuario si no existe
        usuarios[msg.chat.id]['genero'] = '🪼'  # Guardamos el género
    elif msg.text == "🦖 Otro":
        if msg.chat.id not in usuarios:
            usuarios[msg.chat.id] = {}  # Creamos un sub-diccionario para ese usuario si no existe
        usuarios[msg.chat.id]['genero'] = '🦖'  # Guardamos el género
    elif msg.text == "🚁 Helicoptero apache":
        if msg.chat.id not in usuarios:
            usuarios[msg.chat.id] = {}  # Creamos un sub-diccionario para ese usuario si no existe
        usuarios[msg.chat.id]['genero'] = '🚁'  # Guardamos el género
    elif msg.text == "👩‍🔧 Chief":
        if msg.chat.id not in usuarios:
            usuarios[msg.chat.id] = {}  # Creamos un sub-diccionario para ese usuario si no existe
        usuarios[msg.chat.id]['genero'] = '👩‍🔧'  # Guardamos el género
    else:
        bot.send_message(msg.chat.id, "No entendí eso. Escribe /start para volver al menú.")
    markup = types.ReplyKeyboardRemove()
    bot.send_message(msg.chat.id, "Slay", reply_markup=markup)
    time.sleep(0.8)
    bot.send_message(msg.chat.id, "...")
    time.sleep(0.8)
    bot.send_message(msg.chat.id, "Supongo")
    time.sleep(0.8)
    pedir_nombre(msg)

# NOMBRE
def pedir_nombre(message):
    estados[message.chat.id] = 'esperando_nombre'
    bot.send_message(message.chat.id, "¿Y como te llamas?")

@bot.message_handler(func=lambda msg: estados.get(msg.chat.id) == 'esperando_nombre')
def guardar_nombre(message):
    nombre = message.text.strip()
    
    # Si no hay registro para el usuario, creamos uno vacío (por si acaso)
    if message.chat.id not in usuarios:
        usuarios[message.chat.id] = {}
    
    # Guardamos el nombre sin borrar lo anterior
    usuarios[message.chat.id]['nombre'] = nombre
    
    # Obtenemos el género si existe, sino un valor por defecto
    genero = usuarios[message.chat.id].get('genero')
    
    # Cambiamos el estado para que no vuelva a pedir nombre
    estados[message.chat.id] = None
    
    bot.send_message(message.chat.id, f"Genial, *{nombre}* {genero} ", parse_mode='MarkdownV2')
    time.sleep(2)
    bot.send_message(message.chat.id, "Antes de empezar con la aventura, me parece importante que sepas que el servidor donde estoy alojado se conecta mediante eduroam 🥔.")
    time.sleep(4)
    with open('patata.jpg', 'rb') as patata:
        bot.send_photo(message.chat.id, patata)

    time.sleep(4)
    bot.send_message(message.chat.id, "Asi que, si no usas la Biskedex durante un rato, puede que al reconectar tarde un rato en buscar la señal.")

    time.sleep(2)
    bot.send_message(message.chat.id, "La misión que se te encomienda es la de superar todos los gimnasios Biskymón.")
    time.sleep(1)
    bot.send_message(message.chat.id, "...")
    time.sleep(2)
    bot.send_message(message.chat.id, "Veo que no tienes Biskymones, haremos que eso cambie no te preocupes.")
    with open('audio1.mp3', 'rb') as miraculos:
        bot.send_audio(message.chat.id, miraculos)
    time.sleep(5)
    bot.send_message(message.chat.id, "Ademas, yo conozco una forma de superar los gimnasios, digamos que de una forma... distinta, y a la vez conseguir Biskymones más facilmente.")
   
    time.sleep(3)
    bot.send_message(message.chat.id, "De momento, te voy indicando la ubicación del primer, en cuanto llegues mandame la ubi para mandarte instrucciones")
   
    latitude = 43.262970
    longitude = -2.949766
    bot.send_location(message.chat.id, latitude, longitude)
    estados[message.chat.id] = 'ubi1'
    
@bot.message_handler(content_types=['location'], func=lambda msg: estados.get(msg.chat.id) == 'ubi1')
def manejar_ubicacion1(message):
    lat = message.location.latitude
    lon = message.location.longitude
    bot.send_message(message.chat.id, lon)
    bot.send_message(message.chat.id, lat)
   
    # Ejemplo simple de respuesta en función de coordenadas
    if 43.26250 < lat< 43.26350 and -2.94500> lon> -2.95500:
        bot.reply_to(message, "¡Perfecto! Te encuentras debajo del gimnasio Cántico de Luz, aqui moran los Biskymon tipo hada. Pero para intentes entrar así por las buenas... no somos bienvenidos.")
        time.sleep(4)
        bot.reply_to(message, "Para robar, digo, conseguir tus primeros Biskymón, tendras que distraer a los luchadores del gimnasio y luego buscar los Biskymón.")
        time.sleep(3)
        bot.reply_to(message, "Creo que se te da bien hablar de Bisky cosas con gente random, eso tendrás que hacer.")
        time.sleep(2)
        with open('cat.mp4', 'rb') as cat:
            bot.send_video(message.chat.id, cat)
        time.sleep(2)
        bot.reply_to(message, "Prueba 🎯: Debes coger a una persona (preferiblemente externa a Bisky) y mantener una conversación seria y técnica durante 1 minuto sobre cohetes.")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("✅ ¡Los tengo!")
        markup.add(btn1)
        bot.send_message(message.chat.id, "Avisame cuando tengas los Biskymón:", reply_markup=markup)
        estados[message.chat.id] = 'bim'
    else:
        bot.reply_to(message, "¡Aún estás lejos!, Avísame cuando hayas llegado")


@bot.message_handler(func=lambda msg: estados.get(msg.chat.id) == 'bim')
def responder_opciones(msg):
    if msg.text == "✅ ¡Los tengo!":
        markup = types.ReplyKeyboardRemove()
        bot.send_message(msg.chat.id, "¡Genial!, ya tienes tus primeros Biskymón, tratalos con cariño, estos pueden manifestar dinero.",  reply_markup=markup)
        time.sleep(5) 
        bot.send_message(msg.chat.id, "Ahora, nos dirigiremos a por los Biskymón del gimnasio Santuario del Cielo, pero ese lugar esta demasiado alto, asi que trataremos de atraer a algunos a nosotros.")
        time.sleep(6)
        bot.send_message(msg.chat.id, "Se que a algunos de los Biskymón de este gimansio se les alimenta con unos Biskymón tipo pez que nadan en aguas con alto contenido en alcohol.")
        time.sleep(2)
        with open('carp.mp4', 'rb') as video:
            bot.send_video(msg.chat.id, video)
        time.sleep(5)
        bot.send_message(msg.chat.id, "Pero tranquila, se donde estan esas aguas.")
        latitude = 43.265772 
        longitude = -2.942158
        bot.send_location(msg.chat.id, latitude, longitude)

        bot.send_message(msg.chat.id, "Mandame tu ubicación cuando estés.")
        estados[msg.chat.id] = 'ubi2'

@bot.message_handler(content_types=['location'], func=lambda msg: estados.get(msg.chat.id) == 'ubi2')
def manejar_ubicacion2(message):
    lat = message.location.latitude
    lon = message.location.longitude
    bot.send_message(message.chat.id, lon)
    bot.send_message(message.chat.id, lat)

    if 43.26550  < lat< 43.26650  and -2.93500> lon >-2.95500:
        bot.reply_to(message, "¡Increible!, ahora creo que uno de tus compañeros entrenadores tiene una caña para pescar, pidesela.")
        time.sleep(2)
        bot.reply_to(message, "Cuando hayas pescado los borrachocarps, los Biskymon se acercarán a ti, avísame cuando los tengas.")
        time.sleep(2)
        bot.reply_to(message, "Prueba 🎯: Debes buscar en el agua un paquete con tu caña imantada.")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("✅ ¡Los tengo!")
        markup.add(btn1)
        bot.send_message(message.chat.id, "Avisame cuando tengas los Biskymón:", reply_markup=markup)
        estados[message.chat.id] = 'aero'
    else:
        bot.reply_to(message, "¡Aún estás lejos!, Avísame cuando hayas llegado")

@bot.message_handler(func=lambda msg: estados.get(msg.chat.id) == 'aero')
def responder_opciones(msg):
    if msg.text == "✅ ¡Los tengo!":
        markup = types.ReplyKeyboardRemove()
        bot.send_message(msg.chat.id, "¡Wow los has atrapado!, Estos Biskymon son únicos, desde algunos con conductas extrañas 👉👈 hasta otros lorosmon que son muy utiles para corregir tu lenguaje poco aliade. Pero no te preocues, seguro que a mas de uno le cojes mucho cariño <3.",  reply_markup=markup)
        time.sleep(4)
        with open('mariposa.jpg', 'rb') as mari:
            bot.send_photo(msg.chat.id, mari)
        time.sleep(4)
        bot.send_message(msg.chat.id, "...")
        time.sleep(3)
        bot.send_message(msg.chat.id, "...")
        time.sleep(5)
        bot.send_message(msg.chat.id, "¡Oh no!")
        time.sleep(1)
        with open('susto.mp4', 'rb') as susto:
            bot.send_video(msg.chat.id, susto)
        time.sleep(8)
        bot.send_message(msg.chat.id, "¡Un Biskymón que has capturado ha atraido a uno tipo eléctrico!")
        time.sleep(3)
        bot.send_message(msg.chat.id, "Lo bueno es que ya no tendremos que ir a capturarlos al gimnasio La Torre de los FrikiFaradios.")
        bot.send_message(msg.chat.id, "Lo malo es que habrá que luchar.")
        time.sleep(5)
        bot.send_message(msg.chat.id, "Y honestamente.")
        time.sleep(2)
        bot.send_message(msg.chat.id, "A tus Biskymon se les ve demasiado disociados como para luchar...")
        time.sleep(2)
        bot.send_message(msg.chat.id, "Así que tendras que ser tu la que se meta de puños con ellos.")
        time.sleep(2)
        with open('audio2.mp3', 'rb') as lucha:
            bot.send_audio(msg.chat.id, lucha)
        time.sleep(10)
        bot.reply_to(msg, "Prueba 🎯: JUEGO.")
        time.sleep(5)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("✅ ¡Derrotados!")
        markup.add(btn1)
        bot.send_message(msg.chat.id, "Avisame cuando termines la batalla:", reply_markup=markup)
        estados[msg.chat.id] = 'antena'    

@bot.message_handler(func=lambda msg: estados.get(msg.chat.id) == 'antena')
def responder_opciones(msg):
    if msg.text == "✅ ¡Derrotados!":
        markup = types.ReplyKeyboardRemove()
        bot.send_message(msg.chat.id, "No tenia mucha fe en ti pero... ¡Me alegro!",  reply_markup=markup)
        time.sleep(2) 
        bot.send_message(msg.chat.id, "Estos ejemplares son un poco raretes y escurridizos, pero unos gran compañeros.")
        time.sleep(2)
        with open('linux.mp4', 'rb') as linux:
            bot.send_video(msg.chat.id, linux)
        time.sleep(6)
        bot.send_message(msg.chat.id, "¡ALERTA!")
        bot.send_message(msg.chat.id, "Acabo de recibir que un Biskymon se ha escapado del gimnasio Centro de control del delirio.")
        time.sleep(2)
        bot.send_message(msg.chat.id, "Te mando su última ubicación, ¡Corre a buscarlo!")

        latitude = 43.265772 
        longitude = -2.942158
        bot.send_location(msg.chat.id, latitude, longitude)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("✅ ¡Encontrado!")
        markup.add(btn1)
        bot.send_message(msg.chat.id, "Avisame cuando lo encuentres:", reply_markup=markup)
        estados[msg.chat.id] = 'estruc'  

@bot.message_handler(func=lambda msg: estados.get(msg.chat.id) == 'estruc')
def responder_opciones(msg):
    if msg.text == "✅ ¡Encontrado!":  
        markup = types.ReplyKeyboardRemove()
        bot.send_message(msg.chat.id, "STOP",  reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.text.lower() == "video")
def enviar_video(msg):
    with open('carp.mp4', 'rb') as video:
        bot.send_video(msg.chat.id, video, caption="Aquí tienes tu video 🎥")




# RENDER CONNECTION
if __name__ == "__main__":
    render_url = 'https://biskedex.onrender.com'
    if render_url:
        bot.remove_webhook()
        bot.set_webhook(url=f"{render_url}/{TOKEN}")
        print(f"Webhook seteado en {render_url}/{TOKEN}")
    else:
        print("❌ ERROR: RENDER_EXTERNAL_URL no definido. Saltando webhook setup.")
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))