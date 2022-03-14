from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from datetime import datetime, timedelta
import string
import random
from autoslug import AutoSlugField





def random_string_generator(request):
    return ''.join(random.choices(string.ascii_letters , k=20))
 
NATURE_NOTIFICATION= (
    ("avertissement", "avertissement"), 
    ("etat commande", "etat commande"),
    ("vente", "vente"),
    ("annulation d achat", "annulation d achat"),
    ("annulation de vente", "annulation de vente"),
    ("desactivation boutique", "desactivation boutique"),
    ("pour follower", "pour follower"),
    ("note vendeur","note vendeur"),
    ("reactivation boutique","reactivation boutique"),
    ("probleme technique","probleme technique")
    )

 
#Gestion utilisateur 
class UserManager(BaseUserManager):
	def create_user(self,nom,prenom,phone,password=None,is_staff=False,is_admin=False):
		if not phone:
			raise ValueError('phone obligatoire')
		if not password:
			raise ValueError('password obligatoire')
		if not nom:
			raise ValueError('entrez un nom')
		if not prenom:
			raise ValueError('entrez un prenom')
				
		self.phone=phone		
		user = self.model(phone=phone)	
		user.set_password(password)
		user.nom=nom
		user.prenom= prenom
		user.is_staff=is_staff
		user.is_admin=is_admin
		user.save(using=self._db)
		return user

	def create_superuser(self,nom,prenom,phone,password=None):
		user=self.create_user(
			phone=phone,
			password=password,
			nom=nom,
			prenom =prenom,
			is_staff=True,is_admin=True
			)
		return user

	def create_staff(self,nom,prenom,phone,password=None):
		user=self.create_user(
			phone=phone,
			password=password,
			nom=nom,
			prenom=prenom,
			is_staff=True,is_admin=False
			)
		return user	
#Utilisateur
class User(AbstractBaseUser,PermissionsMixin):
	phone = PhoneNumberField(unique=True)
	active = models.BooleanField(default=True)
	prenom = models.CharField(max_length=100)
	nom =models.CharField(max_length=100)
	conform_phone=models.BooleanField(default=False)
	date_joined=models.DateTimeField(auto_now_add=True)
	is_staff =models.BooleanField(default=False)
	is_admin=models.BooleanField(default=False)
	room=AutoSlugField(populate_from=random_string_generator,unique=True)
	group=AutoSlugField(populate_from=random_string_generator,unique=True)
	channel=AutoSlugField(populate_from=random_string_generator,unique=True)
	isbureaucrate=models.BooleanField(default=False)
	istechnique=models.BooleanField(default=False)

	

	REQUIRED_FIELDS= ['prenom','nom']
	USERNAME_FIELD ='phone'
	objects=UserManager()

	def get_prenom(self):
		return self.prenom
	def get_nom(self):
		return self.nom	

	def has_perm(self,perm,obj=None):
		return True

	def has_module_perms(self,app_label):
		return True
	def __str__(self):
		return self.prenom


class CodeConfirmationPhone(models.Model):
	phone=PhoneNumberField()
	code=models.PositiveIntegerField()
	created=models.DateTimeField(auto_now_add=True)
	active=models.BooleanField(default=False)

class Avertissement(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	total=models.PositiveIntegerField(default=0)

		


class Notification(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	message=models.TextField()
	lu=models.BooleanField(default=False)
	active=models.BooleanField(default=True)
	created=models.DateTimeField(auto_now_add=True)
	nature_notification =models.CharField(max_length=255, choices=NATURE_NOTIFICATION,blank=True)
	commande=models.ForeignKey("produit.Commande",on_delete=models.CASCADE,blank=True,null=True)
	produit=models.ForeignKey("produit.Produit",on_delete=models.CASCADE,blank=True,null=True)

	

	
		



