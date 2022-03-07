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
	message='L etat actuel de votre commande'+" " + commande.produitcommande.product.nom + " " +  'est: ' +" "+ commande.statut_commande +"."
	data={'titre':'Notification sur la commande'+" " + commande.produitcommande.product.nom,'body':message}
	Notification.objects.create(user=user,message=message,nature_notification='etat commande',commande=commande)
	notif(user,data)

def NotificationCommandeAuVendeur(user,commande,nom):
	message='Votre produit'+" " +  nom + " " +  'a été commandé  ' +" "+"rendez vous au point d acces le plus proche pour le déposer." 
	Notification.objects.create(user=user,message=message,nature_notification='vente',commande=commande)
	data={'titre':'Notification de vente du produit'+" " + nom,'body':message}
	notif(user,data)
	

def AvertissementDeNonLivraison(user,commande):
	message='L equipe GaalguiShop vous envoie cette notification d avertissement de non livraison du produit '+" "+ commande.produitcommande.product.nom +". Un total de 3 avertissments equivaut a une desactivation de votre boutique!"
	data={'titre':'Notification d avertissment ','body':message}
	Notification.objects.create(user=user,message=message,nature_notification='avertissement',commande=commande)
	try:
		avertissement=Avertissement.objects.get(user=user).first()
		avertissement.total+=1
		avertissement.save()
	except ObjectsDoesNotExist:
		Avertissement.objects.create(user=user,total=1)
		notif(user,data)

def DesactivationDeBoutique(user):
	message='L équipe GaalguiShop vous envoie cette notification pour vous informer de la désactivation de votre boutique pour non respect de la politique de confidentialité.'
	data={'titre':'Désactivation de votre boutique ','body':message}
	Notification.objects.create(user=user,message=message,nature_notification='desactivation boutique')
	notif(user,data)


def AnnulationAchatCoteClient(user,commande):
	message=' Suite a un contre temps ,l équipe GaalguiShop vous envoie cette notification pour vous informer de l annulation de votre commande'+" "+ commande.produitcommande.product.nom +" "+".Un remboursement vous sera fait dans les plus brefs delais."
	data={'titre':'Annulation de commande ','body':message}
	Notification.objects.create(user=user,message=message,nature_notification='annulation d achat',commande=commande)
	notif(user,data)

def AnnulationVente(user,commande):
	message='L équipe GaalguiShop vous envoie cette notification pour vous informer de l annulation de l achat de votre produit'+" "+ commande.produitcommande.product.nom + " "+ "et vous invite a plus de respect de la politique de confidentialité."
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

#def NotificationProduitVendu(vendeur,produit):
	#message='Votre produit ' + " "+ produit.nom + " " + 'a été recemment vendu,vous pouvez changer la quantité en stock '



#def NotificationNoteApresVente(client,boutique):
	#pass







