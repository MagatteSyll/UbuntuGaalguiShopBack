from django.db import models
from autoslug import AutoSlugField
from  user.models import User
from phonenumber_field.modelfields import PhoneNumberField
from .utils import unique_slug_generator
from django.db.models.signals import pre_save, post_save
import string
import random

def random_string_generator(request):
    return ''.join(random.choices(string.ascii_letters , k=20))

STATUS_COMMANDE= (
    ("produit en attente de livraison ", "produit  en attente de livraison"),
    ("produit en cours de livraison ", "produit en cours de livraison "),
    ("produit livré", "produit  livré"))

class Region(models.Model):
	region=models.CharField(max_length=255)

	def __str__(self):
		return  self.region
		

#Categories des produits 
class Category(models.Model):
	category=models.CharField(max_length=255)
	image=models.ImageField(upload_to='static/images')

	

#Adresses de livraison disponible 
class Adress(models.Model):
	adress=models.CharField(max_length=255)
	region=models.ForeignKey(Region,on_delete=models.PROTECT)


	

class Follower(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
			

class Boutique(models.Model):
		user=models.OneToOneField(User,on_delete=models.CASCADE)
		logo=models.ImageField(upload_to='static/images',default='static/images/profil.PNG')
		description=models.TextField(default='Description de votre boutique')
		note_vendeur=models.DecimalField( max_digits=19, decimal_places=1)
		follower=models.ManyToManyField(Follower)
		nbrefollower=models.PositiveIntegerField(default=0)
		slug = AutoSlugField(populate_from=random_string_generator,unique=True)

		def __str__(self):
		    return self.user.prenom	

class Devise(models.Model):
	devise=models.CharField(max_length=100)

		

#Les produits
class Produit(models.Model):
	nom=models.CharField(max_length=100)
	description=models.TextField()
	active=models.BooleanField(default=True)
	prix=models.DecimalField( max_digits=19, decimal_places=2)
	vendeur=models.ForeignKey(User,on_delete=models.CASCADE)
	boutique=models.ForeignKey(Boutique,on_delete=models.CASCADE)
	category=models.ForeignKey(Category,on_delete=models.PROTECT)
	created_at=models.DateTimeField(auto_now_add=True)
	vendu=models.BooleanField(default=False)
	taille=models.CharField(max_length=255,blank=True,null=True)
	couleur=models.CharField(max_length=255,blank=True,null=True)
	qte=models.PositiveIntegerField(blank=True,null=True)
	variation=models.BooleanField(default=True)
	region=models.ForeignKey(Region,on_delete=models.PROTECT)
	slug = AutoSlugField(populate_from=random_string_generator,unique=True)
	devise=models.ForeignKey(Devise,on_delete=models.PROTECT)	
	recycler=models.BooleanField(default=False)
	thumbnail=models.ImageField(upload_to='static/images',blank=True,null=True)

	

class ProduitImage(models.Model):
	produit=models.ForeignKey(Produit,on_delete=models.CASCADE)
	image=models.ImageField(upload_to='static/images',blank=True,null=True)
	size=models.CharField(max_length=255,blank=True,null=True)
	color=models.CharField(max_length=255,blank=True,null=True)
	quantite=models.PositiveIntegerField(blank=True,null=True)
	active=models.BooleanField(default=True)
	vendu=models.BooleanField(default=False)
	qte_vendu=models.PositiveIntegerField(default=0)

					

#Produit dans le panier 
class CartProduct(models.Model):
    product = models.ForeignKey(Produit, on_delete=models.CASCADE,null=True,blank=True)
    imageproduct=models.ForeignKey(ProduitImage,on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField( max_digits=19, decimal_places=2)
    client=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
	
#Panier	
class Cart(models.Model):
    proprietaire = models.OneToOneField(User, on_delete=models.CASCADE)
    total = models.DecimalField( max_digits=19, decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    cartproduct = models.ManyToManyField(CartProduct)

       

#gestion de la commande
class Commande(models.Model):
	produitcommande= models.ForeignKey(CartProduct,on_delete=models.CASCADE)
	acheteur = models.ForeignKey(User,on_delete=models.CASCADE)
	nom_client=models.CharField(max_length=255)
	adress = models.ForeignKey(Adress,on_delete=models.CASCADE)
	phone = PhoneNumberField()
	total=models.DecimalField( max_digits=19, decimal_places=2)
	active=models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	statut_commande =models.CharField(max_length=100, choices=STATUS_COMMANDE,blank=True)
	livraison=models.DecimalField(max_digits=19, decimal_places=2)
	commission=models.DecimalField(max_digits=19, decimal_places=2)
	montant_vendeur=models.DecimalField(max_digits=19, decimal_places=2)
	phone_gaalguiMoney=PhoneNumberField()

		

	
		






