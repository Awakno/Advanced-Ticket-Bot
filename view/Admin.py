"""
made: awakno
@Contributor: Null
@Version: 1.0

Classe ayant toute les vues de la commande /admin
"""
import discord
import json
from librairie.GetLang import get_lang
from db.ticket import TicketDB

# Classe pour configurer le texte d'un bouton
class SetText(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Configure le bouton")
        self.add_item(discord.ui.InputText(label="Texte",placeholder="Texte du bouton",max_length=80,required=True))
        self.add_item(discord.ui.InputText(label="Emoji",placeholder="Emoji du bouton",max_length=80,required=False))
    
    async def callback(self,interaction):
        if await TicketDB().set_text_button(interaction,self.children[0].value,self.children[1].value):
            await interaction.response.send_message("Le bouton a bien été mis à jour !\n> **Texte** : "+self.children[0].value+"\n> **Emoji** : "+self.children[1].value if self.children[1].value != "" else "Aucun",ephemeral=True)
        else:
            await interaction.response.send_message("Une erreur est survenue !",ephemeral=True)

class ColorButton(discord.ui.View):
    def __init__(self,author):
        super().__init__()
        self.author = author
        self.color= {
            "blue": "Bleu",
            "red": "Rouge",
            "green": "Vert",
            "grey": "Gris",
        }
        for value,key in self.color.items():
            btn=discord.ui.Button(label=key,style=discord.ButtonStyle.primary,custom_id=f"{value}")
            btn.callback = self.callback
            self.add_item(btn)
    async def callback(self,interaction):
        await TicketDB().set_color_button(interaction,interaction.data['custom_id'])
        await interaction.response.edit_message(view=ConfigButton(self.author))
        await interaction.followup.send("La couleur du bouton a bien été mise à jour !\n > **Couleur** : "+self.color[interaction.data['custom_id']],ephemeral=True)
        

# Classe pour configurer un bouton
class ConfigButton(discord.ui.View):
    def __init__(self, author):
        super().__init__()
        self.c = json.load(open(f"lang/{get_lang(author.id)}.json","r",encoding="utf-8"))
        # Ajout d'un bouton pour configurer le texte
        text_btn=discord.ui.Button(label="Texte",style=discord.ButtonStyle.primary,custom_id="admin_config_text",emoji="📝")
        text_btn.callback = self.text_callback
        self.add_item(text_btn)
        # Ajout d'un bouton pour configurer la couleur
        color_btn = discord.ui.Button(label="Couleur",style=discord.ButtonStyle.primary,custom_id="admin_config_ticket",emoji="🎨")
        color_btn.callback = self.color_callback
        self.add_item(color_btn)
    async def text_callback(self, interaction):
        await interaction.response.send_modal(modal=SetText())
    async def color_callback(self, interaction):
        await interaction.response.edit_message(view=ColorButton(interaction.user))


class ConfigMessage(discord.ui.Modal):
    def __init__(self,author):
        super().__init__(title="Configure le panneau")
        self.add_item(discord.ui.InputText(label="Message",placeholder="Texte du panneau",style=discord.InputTextStyle.paragraph,max_length=4000,required=False))
        self.add_item(discord.ui.InputText(label="Titre",placeholder="Titre du panneau",max_length=80,required=False))
        self.add_item(discord.ui.InputText(label="Description",placeholder="Description du panneau",style=discord.InputTextStyle.paragraph,max_length=2048,required=False))
        self.add_item(discord.ui.InputText(label="Image",placeholder="URL de l'image",max_length=2048,required=False))
        self.add_item(discord.ui.InputText(label="Footer",placeholder="Texte du footer",max_length=80,required=False))
    async def callback(self,interaction):
        if await TicketDB().edit_message(interaction,self.children[0].value,self.children[1].value,self.children[2].value,self.children[3].value,self.children[4].value):
            await interaction.response.send_message(f"Le panneau a bien été mis à jour !\n> **Message:** {self.children[0].value if self.children[0].value else 'Aucun'}\n **Titre:** {self.children[1].value if self.children[1].value else 'Aucune'}\n **Description: ** {self.children[2].value if self.children[2].value else 'Aucune'}\n **Image: ** {self.children[3].value if self.children[3].value else 'Aucune'}\n **Footer: ** {self.children[4].value if self.children[4].value else 'Aucune'}",ephemeral=True)
        else:
            await interaction.response.send_message("Une erreur est survenue !",ephemeral=True)

class ConfigMessageInTicket(discord.ui.Modal):
    def __init__(self,author):
        super().__init__(title="Configure le panneau")
        
        self.add_item(discord.ui.InputText(label="Titre",placeholder="Titre du panneau",max_length=80,required=False))
        self.add_item(discord.ui.InputText(label="Description",placeholder="Description du panneau",style=discord.InputTextStyle.paragraph,max_length=2048,required=False))
        self.add_item(discord.ui.InputText(label="Image",placeholder="URL de l'image",max_length=2048,required=False))
        self.add_item(discord.ui.InputText(label="Footer",placeholder="Texte du footer",max_length=80,required=False))
    async def callback(self,interaction):
        if await TicketDB().edit_message_inticket(interaction,self.children[0].value,self.children[1].value,self.children[2].value,self.children[3].value):
            await interaction.response.send_message(f"Le panneau a bien été mis à jour !\n> **Titre:** {self.children[0].value if self.children[0].value else 'Aucun'}\n **Description:** {self.children[1].value if self.children[1].value else 'Aucune'}\n **Image: ** {self.children[2].value if self.children[2].value else 'Aucune'}\n **Footer: ** {self.children[3].value if self.children[3].value else 'Aucune'}",ephemeral=True)
        else:
            await interaction.response.send_message("Une erreur est survenue !",ephemeral=True)


class SetChannel(discord.ui.View):
    def __init__(self,author):
        super().__init__()
        self.author = author
    @discord.ui.select(placeholder="Choisi un salon",select_type=discord.ComponentType.channel_select,channel_types=[discord.ChannelType.text],custom_id="admin_config_channel")
    async def callback(self,select,interaction):
        await TicketDB().set_channel(interaction,select.values[0])
        await interaction.response.send_message("Le salon a bien été mis à jour !\n> **Salon** : "+select.values[0].mention,ephemeral=True)

class SetCategory(discord.ui.View):
    def __init__(self,author,bot):
        super().__init__()
        self.author = author
        self.bot = bot
    @discord.ui.select(placeholder="Choisi une catégories",select_type=discord.ComponentType.channel_select,channel_types=[discord.ChannelType.category],custom_id="admin_config_channel")
    async def callback(self,select,interaction):
        await TicketDB().set_categories(interaction,select.values[0])
        await interaction.response.edit_message(view=TicketConfig(self.author,self.bot))
        await interaction.followup.send("La catégories a bien été mis à jour !\n> **Catégories** : "+select.values[0].mention,ephemeral=True)

class AddSupport(discord.ui.View):
    def __init__(self,author,bot):
        super().__init__()
        self.author = author
        self.bot = bot
    @discord.ui.select(placeholder="Choisi un support",select_type=discord.ComponentType.role_select,custom_id="admin_config_support")
    async def callback(self,select,interaction):
        await TicketDB().add_support(interaction,select.values[0])
        await interaction.response.edit_message(view=TicketConfig(self.author,self.bot))
        await interaction.followup.send("Le support a bien été mis à jour !\n> **Support** : "+select.values[0].mention,ephemeral=True)

class RemoveSupport(discord.ui.View):
    def __init__(self,author,bot):
        super().__init__()
        self.author = author
        self.bot = bot
    @discord.ui.select(placeholder="Choisi un support",select_type=discord.ComponentType.role_select,custom_id="admin_config_support")
    async def callback(self,select,interaction):
        await TicketDB().remove_support(interaction,select.values[0])
        await interaction.response.edit_message(view=TicketConfig(self.author,self.bot))
        await interaction.followup.send("Le support a bien été mis à jour !\n> **Support** : - "+select.values[0].mention,ephemeral=True)


class ChoiceSupport(discord.ui.View):
    def __init__(self,author,bot):
        super().__init__()
        self.author = author
        self.bot = bot
    @discord.ui.button(label="Ajouter un support",style=discord.ButtonStyle.success,custom_id="choice_support")
    async def callback(self,button,interaction):
        await interaction.response.edit_message(view=AddSupport(self.author,self.bot))
    @discord.ui.button(label="Supprimer un support",style=discord.ButtonStyle.danger,custom_id="choice_unsupport")
    async def callback2(self,button,interaction):
        await interaction.response.edit_message(view=RemoveSupport(self.author,self.bot))
    
    
# Classe pour configurer un ticket
class TicketConfig(discord.ui.View):
    def __init__(self, author,bot):
        super().__init__()
        self.bot = bot
        self.c = json.load(open(f"lang/{get_lang(author.id)}.json","r",encoding="utf-8"))
        opt = []
        for i in self.c['Admin']['Plugins']['Ticket']['Select']['Option']:
            opt.append(discord.SelectOption(label=i['label'],description=i['value'],emoji=i['emoji']))
        # Création d'un composant Select pour configurer le ticket
        select=discord.ui.Select(placeholder=self.c['Admin']['Plugins']['Ticket']['Select']['placeholder'],options=opt,custom_id="admin_config_select")
        select.callback = self.callback
        self.add_item(select)
    async def make_panel(self,interaction):
        embed_data=await TicketDB().get_panel(interaction)
        embed = discord.Embed()
        message = None
        if embed_data.get("title"):
            embed.title = embed_data.get("title")
        if embed_data.get("description"):
            embed.description = embed_data.get("description")
        if embed_data.get("image"):
            embed.set_image(url=embed_data.get("image"))
        if embed_data.get("footer"):
            embed.set_footer(text=embed_data.get("footer"))
        if embed_data.get("message"):
            message = embed_data.get("message")
        return message,embed
    async def create_button(self,interaction):
        btn = await TicketDB().get_button(interaction)
        color = {
            "red": discord.ButtonStyle.danger,
            "green": discord.ButtonStyle.success,
            "grey": discord.ButtonStyle.gray,
            "blue": discord.ButtonStyle.blurple
        }
        view = discord.ui.View()
        button = discord.ui.Button(label=btn.get("label"),style=color[btn.get("color")],custom_id="ticket_btn",emoji=btn.get("emoji"))
        view.add_item(button)
        return view
    async def callback(self, interaction):
        selected = interaction.data['values'][0]
        if selected == self.c['Admin']['Plugins']['Ticket']['Select']['Option'][0]['label']:
            await interaction.response.edit_message(view=ConfigButton(interaction.user))
        if selected == self.c['Admin']['Plugins']['Ticket']['Select']['Option'][1]['label']:
            await interaction.response.send_modal(modal=ConfigMessage(author=interaction.user))
        if selected == self.c['Admin']['Plugins']['Ticket']['Select']['Option'][2]['label']:
            await interaction.response.edit_message(view=SetChannel(interaction.user))
        if selected == self.c['Admin']['Plugins']['Ticket']['Select']['Option'][3]['label']:
            message,embed = await self.make_panel(interaction)
            channel = self.bot.get_channel(await TicketDB().get_channel(interaction))
            btn = await self.create_button(interaction)
            await channel.send(content=message,embed=embed,view=btn)
            await interaction.response.send_message("Envoie du panneau reussi",ephemeral=True)
        if selected == self.c['Admin']['Plugins']['Ticket']['Select']['Option'][4]['label']:
            await interaction.response.edit_message(view=SetCategory(interaction.user,self.bot))
        if selected == self.c['Admin']['Plugins']['Ticket']['Select']['Option'][5]['label']:
            await interaction.response.edit_message(view=ChoiceSupport(interaction.user,self.bot))
        if selected == self.c['Admin']['Plugins']['Ticket']['Select']['Option'][6]['label']:
            await interaction.response.send_modal(modal=ConfigMessageInTicket(author=interaction.user))
            


# Classe pour configurer les paramètres d'administration
class AdminConfigView(discord.ui.View):
    def __init__(self, author,bot):
        super().__init__()
        self.bot = bot
        self.c = json.load(open(f"lang/{get_lang(author.id)}.json","r",encoding="utf-8"))
        opt = []
        for i in self.c['Admin']['Config']['Select']['Option']:
            opt.append(discord.SelectOption(label=i['label'],description=i['value'],emoji=i['emoji']))
        # Création d'un composant Select pour configurer les paramètres d'administration
        select=discord.ui.Select(placeholder=self.c['Admin']['Config']['Select']['placeholder'],options=opt,custom_id="admin_config_select")
        select.callback = self.callback
        self.add_item(select)
    
    async def callback(self, interaction):
        selected = interaction.data['values'][0]
        if selected == self.c['Admin']['Config']['Select']['Option'][0]['label']:
            embed = discord.Embed()
            embed.title = self.c['Admin']['Plugins']['Ticket']['title']
            embed.description = self.c['Admin']['Plugins']['Ticket']['description']
            embed.set_footer(text=self.c['Admin']['Plugins']['Ticket']['footer'])
            await interaction.response.edit_message(embed=embed,view=TicketConfig(interaction.user,self.bot))
            

# Classe pour l'interface d'administration principale
class AdminView(discord.ui.View):
    def __init__(self, author,bot):
        super().__init__()
        self.bot = bot
        self.c = json.load(open(f"lang/{get_lang(author.id)}.json","r",encoding="utf-8"))
        opt = []
        for i in self.c['Admin']['Main']['Select']['Option']:
            opt.append(discord.SelectOption(label=i['label'],description=i['value'],emoji=i['emoji']))
        # Création d'un composant Select pour l'interface d'administration principale
        self.select=discord.ui.Select(placeholder=self.c['Admin']['Config']['Select']['placeholder'],options=opt,custom_id="admin_select")
        self.select.callback = self.callback
        self.add_item(self.select)
    
    async def callback(self, interaction):
        selected = interaction.data['values'][0]
        if selected == self.c['Admin']['Main']['Select']['Option'][0]['label']:
            embed = discord.Embed()
            embed.title = self.c['Admin']['Config']['title']
            embed.description = self.c['Admin']['Config']['description']
            embed.set_footer(text=self.c['Admin']['Config']['footer'])
            await interaction.response.edit_message(embed=embed,view=AdminConfigView(interaction.user,self.bot))
