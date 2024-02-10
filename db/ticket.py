"""
made: awakno
@Contributor: Null
@Version: 1.0
"""
"""
Classe TicketDB :
    Cette classe fournit des méthodes pour interagir avec la base de données des tickets.

Méthodes :
    - set_text_button(self, interaction, label, emoji=""): Définit le texte et éventuellement l'emoji pour le bouton affiché dans le panneau des tickets.
        Paramètres :
            - interaction : Le contexte de l'interaction.
            - label (str) : Le texte du libellé pour le bouton.
            - emoji (str) : Emoji optionnel pour le bouton.

    - edit_message(self, interaction, message="", title="", description="", image="", footer=""): Modifie le contenu du message du panneau des tickets.
        Paramètres :
            - interaction : Le contexte de l'interaction.
            - message (str) : Nouveau contenu du message.
            - title (str) : Nouveau titre pour le panneau des tickets.
            - description (str) : Nouvelle description pour le panneau des tickets.
            - image (str) : Nouvelle URL de l'image pour le panneau des tickets.
            - footer (str) : Nouveau texte de bas de page pour le panneau des tickets.

    - set_color_button(self, interaction, color): Définit la couleur du bouton affiché dans le panneau des tickets.
        Paramètres :
            - interaction : Le contexte de l'interaction.
            - color (str) : La valeur de couleur pour le bouton.

    - get_panel(self, interaction): Récupère la configuration du panneau des tickets.
        Paramètres :
            - interaction : Le contexte de l'interaction.
        Retourne :
            - dict : Un dictionnaire contenant la configuration du panneau.

    - set_channel(self, interaction, channel): Définit l'identifiant du canal où les messages des tickets seront envoyés.
        Paramètres :
            - interaction : Le contexte de l'interaction.
            - channel : Le canal où les messages des tickets seront envoyés.

    - get_channel(self, interaction): Récupère l'identifiant du canal où les messages des tickets seront envoyés.
        Paramètres :
            - interaction : Le contexte de l'interaction.
        Retourne :
            - str : L'identifiant du canal.

    - get_button(self, interaction): Récupère la configuration du bouton affiché dans le panneau des tickets.
        Paramètres :
            - interaction : Le contexte de l'interaction.
        Retourne :
            - dict : Un dictionnaire contenant la configuration du bouton.

    - set_categories(self, interaction, category): Définit l'identifiant de la catégorie où les canaux de tickets seront créés.
        Paramètres :
            - interaction : Le contexte de l'interaction.
            - category : La catégorie où les canaux de tickets seront créés.

    - get_categories(self, interaction): Récupère l'identifiant de la catégorie où les canaux de tickets seront créés.
        Paramètres :
            - interaction : Le contexte de l'interaction.
        Retourne :
            - str : L'identifiant de la catégorie.

    - add_support(self, interaction, role): Ajoute l'identifiant d'un rôle de support à la liste des rôles ayant accès aux tickets.
        Paramètres :
            - interaction : Le contexte de l'interaction.
            - role : L'identifiant du rôle à ajouter.

    - remove_support(self, interaction, role): Supprime l'identifiant d'un rôle de support de la liste des rôles ayant accès aux tickets.
        Paramètres :
            - interaction : Le contexte de l'interaction.
            - role : L'identifiant du rôle à supprimer.

    - get_support(self, interaction): Récupère la liste des identifiants de rôles de support ayant accès aux tickets.
        Paramètres :
            - interaction : Le contexte de l'interaction.
        Retourne :
            - list : Une liste d'identifiants de rôles.

    - get_panel_inticket(self, interaction): Récupère la configuration du panneau des tickets à l'intérieur du canal de ticket.
        Paramètres :
            - interaction : Le contexte de l'interaction.
        Retourne :
            - dict : Un dictionnaire contenant la configuration du panneau.

    - edit_message_inticket(self, interaction, title="", description="", image="", footer=""): Modifie le contenu du message du panneau des tickets à l'intérieur du canal de ticket.
        Paramètres :
            - interaction : Le contexte de l'interaction.
            - title (str) : Nouveau titre pour le panneau des tickets.
            - description (str) : Nouvelle description pour le panneau des tickets.
            - image (str) : Nouvelle URL de l'image pour le panneau des tickets.
            - footer (str) : Nouveau texte de bas de page pour le panneau des tickets.
"""



from db.connection import ticket_db
 
class TicketDB:
    async def set_text_button(self,interaction,label,emoji=""):
        ticket_db.update_one({"guild": interaction.guild.id}, {"$set": {"button.label": label, "button.emoji": emoji}},upsert=True)
        return True
    
    async def edit_message(self,interaction,message="",title="",description="",image="",footer=""):
        ticket_db.update_one({"guild": interaction.guild.id}, {"$set": {"panel.message": message, "panel.title": title, "panel.description": description, "panel.image": image, "panel.footer": footer}},upsert=True)
        return True
    
    async def set_color_button(self,interaction,color):
        ticket_db.update_one({"guild": interaction.guild.id}, {"$set": {"button.color": color}},upsert=True)
    
    async def get_panel(self,interaction):
        find = ticket_db.find_one({"guild": interaction.guild.id})
        return find.get("panel")
    
    async def set_channel(self,interaction,channel):
        ticket_db.update_one({"guild": interaction.guild.id}, {"$set": {"channel": channel.id}},upsert=True)
        return True
    
    async def get_channel(self,interaction):
        find = ticket_db.find_one({"guild": interaction.guild.id})
        return find.get("channel")
    
    async def get_button(self,interaction):
        find= ticket_db.find_one({"guild": interaction.guild.id})
        return find.get("button")
    
    async def set_categories(self,interaction,category):
        ticket_db.update_one({"guild": interaction.guild.id}, {"$set": {"category": category.id}},upsert=True)
        return True
    
    async def get_categories(self,interaction):
        find = ticket_db.find_one({"guild": interaction.guild.id})
        return find.get("category")
    
    async def add_support(self,interaction,role):
        ticket_db.update_one({"guild": interaction.guild.id}, {"$push": {"support": role.id}},upsert=True)
        return True
    
    async def remove_support(self,interaction,role):
        ticket_db.update_one({"guild": interaction.guild.id}, {"$pull": {"support": role.id}},upsert=True)
        return True
    
    async def get_support(self,interaction):
        find = ticket_db.find_one({"guild": interaction.guild.id})
        return find.get("support")
    
    async def get_panel_inticket(self,interaction):
        find = ticket_db.find_one({"guild": interaction.guild.id})
        return find.get("inticket")
    
    async def edit_message_inticket(self,interaction,title="",description="",image="",footer=""):
        ticket_db.update_one({"guild": interaction.guild.id}, {"$set": {"inticket.title": title, "inticket.description": description, "inticket.image": image, "inticket.footer": footer}},upsert=True)
        return True
    
        