"""
made: awakno
@Contributor: Null
@Version: 1.0
"""
import discord
from librairie.GetLang import get_lang
from librairie.Staff import is_staff
import json
from view.Admin import AdminView
class Admin(discord.Cog):
    def __init__(self, bot):
        self.bot = bot
    @discord.slash_command(name="admin",description="Admin commands")
    async def admin(self, ctx):
        if is_staff(ctx.author):
            c = json.load(open(f"lang/{get_lang(ctx.author)}.json","r",encoding="utf-8"))
            embed = discord.Embed()
            embed.title = c['Admin']['Main']['title']
            embed.description = c['Admin']['Main']['description']
            embed.set_footer(text=c['Admin']['Main']['footer'])
            await ctx.respond(embed=embed,ephemeral=True,view=AdminView(ctx.author,self.bot))
            
            
def setup(bot):
    bot.add_cog(Admin(bot))
        

    