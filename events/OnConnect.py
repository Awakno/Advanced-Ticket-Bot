"""
made: awakno
@Contributor: Null
@Version: 1.0

This is the on connect event for the bot
"""

import discord
from librairie.color import Color  # Importation de la classe de couleur personnalisée

class OnConnect(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.Cog.listener()
    async def on_connect(self):
        # Affichage d'un message indiquant que le bot est en train de créer un websocket lors de la connexion
        print(f"{Color.red}[{Color.blue}+{Color.red}] {Color.cyan}Creating a websocket...{Color.end}")

def setup(bot):
    # Ajout du Cog (component object) à l'instance du bot lors du chargement de l'extension
    bot.add_cog(OnConnect(bot))
