from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import*




def notif(user,data):
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(user.group, {
    'type': 'notify',
    'value': data
    }) 

def NotifcationChangementEtatCommande(user,commande,nom):
	message='L etat actuel de votre commande'+" " + nom + " " +  'est: ' +" "+ commande.statut_commande +"."
	data={'titre':'Notification sur la commande'+" " + nom,'body':message}
	Notification.objects.create(user=user,message=message,nature_notification='etat commande',
		commande=commande)
	notif(user,data)

def NotificationCommandeAuVendeur(user,commande,nom):
	message='Votre produit'+" " +  nom + " " +  'a été commandé  ' +" "+"rendez vous au point d acces le plus proche pour le déposer." 
	Notification.objects.create(user=user,message=message,nature_notification='vente',commande=commande)
	data={'titre':'Notification de vente du produit'+" " + nom,'body':message}
	notif(user,data)
	

def AvertissementVendeur(user):
	message='L equipe GaalguiShop vous envoie cette notification d avertissment suite a un non respect de la politique de confidentialité.'
	data={'titre':'Notification d avertissment ','body':message}
	Notification.objects.create(user=user,message=message,
		nature_notification='avertissement')
	notif(user,data)

def DesactivationDeBoutique(user):
	message='L équipe GaalguiShop vous envoie cette notification pour vous informer de la désactivation de votre boutique pour non respect de la politique de confidentialité.'
	data={'titre':'Désactivation de votre boutique ','body':message}
	Notification.objects.create(user=user,message=message,nature_notification='desactivation boutique')
	notif(user,data)


def AnnulationAchatCoteClient(user,commande,nom):
	message=' Suite a un contre temps ,l équipe GaalguiShop vous envoie cette notification pour vous informer de l annulation de votre commande'+" "+ nom +" "+".Un remboursement vous sera fait dans les plus brefs delais."
	data={'titre':'Annulation de commande ','body':message}
	Notification.objects.create(user=user,message=message,nature_notification='annulation d achat',commande=commande)
	notif(user,data)

def AnnulationVente(user,commande,nom):
	message='L équipe GaalguiShop vous envoie cette notification pour vous informer de l annulation de l achat de votre produit'+" "+nom + " "+ "et vous invite a plus de respect de la politique de confidentialité."
	data={'titre':'Annulation d achat','body':message}
	Notification.objects.create(user=user,message=message,nature_notification='annulation de vente',commande=commande)
	notif(user,data)


def NotificationNewProductToFollower(boutique,produit,vendeur):
	message=vendeur.prenom + " "+ vendeur.nom +" " + "a ajouté un nouveau produit"+" "+ produit.nom
	data={'titre':'Un nouveau produit ','body':message}
	for follower in boutique.follower.all():
		Notification.objects.create(user=follower.user,message=message,nature_notification='pour follower'
			,produit=produit)
		notif(follower.user,data)

def NotificationActivationBoutique(user):
	message='L équipe GaalguiShop vous envoie cette notification pour vous informer de la réactivation de votre boutique'
	data={'titre':'Reactivation boutique','body':message}
	Notification.objects.create(user=user,message=message,nature_notification="reactivation boutique")
	notif(user,data)

def NotificationProblemeTeechnique(probleme,users):
	for user in users:
		Notification.objects.create(user=user,message=probleme,nature_notification="probleme technique")
		data={'titre':'Signal d un probleme technique','body':probleme}
		notif(user,data)

def NotificationNoteVendeur(user,nom,commande):
	message="Vous avez recemment achete le produit" + " " +  nom + " " + "vous pouvez noter le vendeur sur la qualite du produit"
	data={'titre':'Noter le vendeur','body':message}
	Notification.objects.create(user=user,message=message,nature_notification="note vendeur",commande=commande)
	notif(user,data)





