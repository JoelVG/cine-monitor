# cine-monitor
Scraper para los cines [Skybox](https://skyboxcinemas.com.bo/) y [Prime](https://primecinemas.com.bo/)
Proyecto base donde puedes implementar tus propios comandos con tu propio bot :)

# bot
[@isdin_bot](https://t.me/isdin_bot)

Bot de Telegram que te envía notificaciones cuando hay pelis nuevas.

**¿Cómo funciona?**
Envías un mensaje al bot con los comandos disponibles para interactuar con él.
Cada que hay una peli nueva en cartelera o próximamente el bot te notificará con la actualización.

# comandos
Comandos disponibles que escucha el bot
- `add` Agrega un user cuando envía la palabra *add* al bot
- `remove` Remueve al user cuando envía la palabra *remove* al bot


# Docker
`docker build -t cine-monitor .`  
`docker run -d --name cine-monitor-container cine-monitor`  
`docker exec -it cine-monitor-container /bin/bash`  
> Los archivos generados por `monitor.py`se guardan en *./root/*  


# Crontab
`crontab -l` # listas los cronjobs activos  
`crontab -e` # editas el archivo de cronjobs  


# Docs
[Telegram Bot API](https://core.telegram.org/bots/api)
[pre-commit](https://pre-commit.com/)
