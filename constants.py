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

# MESSAGE_FORMAT = f"🎬 *{name}*\n" \
#                    f"🕒 Duration: {duration}\n" \
#                    f"📅 Release Date: {date}\n\n"
