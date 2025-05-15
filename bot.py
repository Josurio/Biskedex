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
    bot.send_message(msg.chat.id, "Slay")
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
    bot.send_message(message.chat.id, "Antes de empezar con la aventura, me parce importante que sepas que el servidor donde estoy alojado se conecta mediante eduroam 🥔")
    with open('patata.jpg', 'rb') as patata:
        bot.send_photo(message.chat.id, patata, caption="Aquí tienes tu video 🎥")

    bot.send_message(message.chat.id, "Asi que, si no usas la Bikedex durante un rato, puede que al reconectar tarde un rato en buscar la señal")

    bot.send_message(message.chat.id, "Pista")


@bot.message_handler(func=lambda msg: msg.text.lower() == "video")
def enviar_video(msg):
    with open('output_quad.mp4', 'rb') as video:
        bot.send_video(msg.chat.id, video, caption="Aquí tienes tu video 🎥")

if __name__ == "__main__":
    render_url = 'https://biskedex.onrender.com'
    if render_url:
        bot.remove_webhook()
        bot.set_webhook(url=f"{render_url}/{TOKEN}")
        print(f"Webhook seteado en {render_url}/{TOKEN}")
    else:
        print("❌ ERROR: RENDER_EXTERNAL_URL no definido. Saltando webhook setup.")
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))