"""
Made by awakno 
@Contributor: Null
@Version: 1.0

This is the main file of the bot
"""

# Importation des bibliothèques Discord.py et autres
import discord
import json
import os
from librairie.color import Color  # Importation de la bibliothèque de couleur personnalisée

# Importation de config.json
f = open("config/config.json")
config = json.load(f)
# Configuration du jeton
token = config["token"]

# Configuration du bot
bot = discord.Bot(intents=discord.Intents.all())

# Importation de toutes les commandes et événements
for j in os.listdir("./commands"):
    if j.endswith(".py"):
        bot.load_extension(f"commands.{j[:-3]}")  # Chargement de l'extension de commande
        print(f"{Color.green}[{Color.blue}+{Color.green}] {Color.cyan}Commande chargée {j[:-3]}{Color.end}")

for j in os.listdir("./events"):
    if j.endswith(".py"):   
        bot.load_extension(f"events.{j[:-3]}")  # Chargement de l'extension d'événement
        print(f"{Color.green}[{Color.blue}+{Color.green}] {Color.cyan}Événement chargé {j[:-3]}{Color.end}")

# Exécution du bot
bot.run(token)
