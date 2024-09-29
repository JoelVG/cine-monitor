SKYBOX_URL = "https://skyboxcinemas.com.bo/"
SKYBOX_PREM = "https://skyboxcinemas.com.bo/genero/estrenos/"
SKYBOX_NOW = "https://skyboxcinemas.com.bo/genero/en-cartelera/"

PRIME_URL = "https://primecinemas.com.bo/"
PRIME_PREM = "https://primecinemas.com.bo/amy_genre/proximamente/"
PRIME_NOW = "https://primecinemas.com.bo/amy_genre/cartelera/"

NOT_CATEGORIES = ("en cartelera", "estrenos", "próximamente")

SKYBOX_OUTPUT = "skybox.csv"
PRIM_OUTPUT = "prime.csv"

SKYBOX_TITLE_TARGET = {
    "name": "div",
    "class_": "list-content"
}

PRIME_TITLE_TARGET = {
    "name": "article",
    "class_": "entry-item clearfix"
}


# MESSAGE_FORMAT = f"🎬 *{name}*\n" \
#                    f"🕒 Duration: {duration}\n" \
#                    f"📅 Release Date: {date}\n\n"
