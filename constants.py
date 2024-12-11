from os import environ


BOT_TOKEN = environ.get("BOT_TOKEN")

SKYBOX_URL = "https://skyboxcinemas.com.bo/"
SKYBOX_PREM = "https://skyboxcinemas.com.bo/genero/estrenos/"
SKYBOX_NOW = "https://skyboxcinemas.com.bo/genero/en-cartelera/"

PRIME_URL = "https://primecinemas.com.bo/"
PRIME_PREM = "https://primecinemas.com.bo/amy_genre/proximamente/"
PRIME_NOW = "https://primecinemas.com.bo/amy_genre/cartelera/"

NOT_CATEGORIES = ("en cartelera", "estrenos", "próximamente")

SKYBOX_OUTPUT = "skybox.csv"
PRIM_OUTPUT = "prime.csv"

# header to mimic a browser
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"
COMMANDS = ("test", "add", "remove", "set", "prime", "skybox")

TEST_MESSAGE = """
Hola, soy un bot de cine 🤖\n
Envío notificaciones de pelis nuevas y en cartelera de los cines de:\n
Skybox y Prime\n

Mis comandos disponibles son:\n
test - Prueba el bot\n
add - Te añades a la lista de notificaciones\n
remove - Te eliminas de la lista de notificaciones\n
prime - Ver las peliculas de Prime Cinemas\n
skybox - Ver las peliculas de Skybox\n
"""
