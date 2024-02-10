"""
made: awakno
@Contributor: Null
@Version: 1.0

This is the on ready event for the bot
"""

import discord
from librairie.color import Color  # Importation de la classe de couleur personnalisée


class OnReady(discord.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @discord.Cog.listener()
    async def on_ready(self):
        # Affichage d'un message indiquant que le bot est prêt lorsque l'événement on_ready est déclenché
        print(f"{Color.green}[{Color.blue}+{Color.green}] {Color.cyan}Bot is ready!{Color.end}")

def setup(bot):
    # Ajout du Cog (component object) à l'instance du bot lors du chargement de l'extension
    bot.add_cog(OnReady(bot))
