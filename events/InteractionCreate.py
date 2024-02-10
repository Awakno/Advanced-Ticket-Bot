"""
made: awakno
@Contributor: Null
@Version: 1.0

Detect  the click of button

-> No function
"""




import discord
from db.ticket import TicketDB
class InteractionCreate(discord.Cog):
    def __init__(self,bot) -> None:
        super().__init__()
        self.bot = bot
    async def make_panel(self,interaction):
        embed_data=await TicketDB().get_panel_inticket(interaction)
        embed = discord.Embed()
       
        if embed_data.get("title"):
            embed.title = embed_data.get("title")
        if embed_data.get("description"):
            embed.description = embed_data.get("description")
        if embed_data.get("image"):
            embed.set_image(url=embed_data.get("image"))
        if embed_data.get("footer"):
            embed.set_footer(text=embed_data.get("footer"))
        
        return embed
    async def create_close_button(self,interaction):
        
        view = discord.ui.View()
        button = discord.ui.Button(label="Fermer",style=discord.ButtonStyle.danger,custom_id="close_ticket_btn",emoji="🔒")
        view.add_item(button)
        return view
    @discord.Cog.listener()
    async def on_interaction(self,interaction):
        if interaction.type == discord.InteractionType.component:
            if interaction.data['custom_id'] == "ticket_btn":
                categories = await TicketDB().get_categories(interaction)
                if categories:
                    categories = self.bot.get_channel(categories)
                    overwrites= {
                        interaction.user: discord.PermissionOverwrite(read_messages=True,send_messages=True),
                        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False)
                    }
                    for role in await TicketDB().get_support(interaction):
                        overwrites[interaction.guild.get_role(role)] = discord.PermissionOverwrite(read_messages=True,send_messages=True)
                    salon=await categories.create_text_channel(f"ticket-{interaction.user.name}",overwrites=overwrites)
                    await interaction.response.send_message(f"Le ticket a bien été crée !\n> **Salon** : {salon.mention}",ephemeral=True)
                    message = ""
                    for role in await TicketDB().get_support(interaction):
                        message += "<@&"+str(role)+">"
                    message += interaction.user.mention
                    embed = await self.make_panel(interaction)
                    await salon.send(message,embed=embed,view=await self.create_close_button(interaction))
                else:
                    await interaction.response.send_message("Veuillez d'abord configurer la catégorie du ticket !",ephemeral=True)
            if interaction.data['custom_id'] == "close_ticket_btn":
                await interaction.channel.delete()
                
                
def setup(bot):
    bot.add_cog(InteractionCreate(bot))