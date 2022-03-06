from rest_framework import serializers
from .models import*
from user.serializer import UserSerializer
from user.models import Notification



class RegionSerializer(serializers.ModelSerializer):
	class Meta:
		model=Region
		fields='__all__'
	
class LivraisonSerializer(serializers.Serializer):
	livraison=serializers.IntegerField()

	def create(self, validated_data):
		return Snippet.objects.create(**validated_data)
	
		
#Follower Serializer
class FollowerSerializer(serializers.Serializer):
	user=serializers.SerializerMethodField()
	class Meta:
		model=Category
		fields='__all__'

	def get_user(self,obj):
		return UserSerializer(obj.user).data



#serialisation des categories
class CategorySerializer(serializers.ModelSerializer):

	class Meta:
		model=Category
		fields='__all__'

#serialisation des adresses
class AdresseSerializer(serializers.ModelSerializer):
	region=serializers.SerializerMethodField()
	class Meta: 
		model=Adress
		fields='__all__'

	def get_region(self,obj):
		return RegionSerializer(obj.region).data

#boutique serializer		
class BoutiqueSerializer(serializers.ModelSerializer):
	user=serializers.SerializerMethodField()
	follower=FollowerSerializer(read_only=True, many=True)
	class Meta:
		model=Boutique
		fields='__all__'

	def get_user(self,obj):
		return UserSerializer(obj.user).data

class DeviseSerializer(serializers.ModelSerializer):
	class Meta:
		model=Devise
		fields='__all__'
				

#serialisation des produits
class ProductSerializer(serializers.ModelSerializer):
	vendeur=serializers.SerializerMethodField()
	category=serializers.SerializerMethodField()
	region=serializers.SerializerMethodField()
	boutique=serializers.SerializerMethodField()
	devise=serializers.SerializerMethodField()
	class Meta:
		model=Produit
		fields='__all__'

	def get_vendeur(self,obj):
		return UserSerializer(obj.vendeur).data
		
	def get_category(self,obj):
		return CategorySerializer(obj.category).data

	def get_region(self,obj):
		return RegionSerializer(obj.region).data

	def get_boutique(self,obj):
		return  BoutiqueSerializer(obj.boutique).data

	def get_devise(self,obj):
		return  DeviseSerializer(obj.devise).data

class ProduitImageserializer(serializers.ModelSerializer):
	produit=serializers.SerializerMethodField()
	class Meta:
		model=ProduitImage
		fields='__all__'

	def get_produit(self,obj):
		return ProductSerializer(obj.produit).data

	


#serialisaton des produits dans le panier
class CartProductSerializer(serializers.ModelSerializer):
	client=serializers.ReadOnlyField(source='client.nom')
	product=ProductSerializer()
	imageproduct=ProduitImageserializer()
	class Meta:
		model=CartProduct
		fields='__all__'
	def get_product(self,obj):
		return ProductSerializer(obj.product).data
	def get_image(self,obj):
		return ProduitImageserializer(obj.imageproduct).data

#serialisation du panier
class CartSerializer(serializers.ModelSerializer):
	cartproduct=CartProductSerializer(read_only=True, many=True)
	class Meta: 
		model=Cart
		fields='__all__'


#serialisation des commandes
class CommandeSerializer(serializers.ModelSerializer):
	produitcommande=serializers.SerializerMethodField()
	adress=serializers.SerializerMethodField()
	acheteur=serializers.SerializerMethodField()
	livraison=serializers.ReadOnlyField()
	commission=serializers.ReadOnlyField()
	montant_vendeur=serializers.ReadOnlyField()
	active=serializers.ReadOnlyField()
	class Meta:
		model=Commande
		fields='__all__'

	def get_produitcommande(self,obj):
		return CartProductSerializer(obj.produitcommande).data

	def get_adress(self,obj):
		return AdresseSerializer(obj.adress).data

	def get_acheteur(self,obj):
		return UserSerializer(obj.acheteur).data

	def get_adress(self,obj):
		return AdresseSerializer(obj.adress).data


	def update(self, instance, validated_data):
		instance.description = validated_data.get('description', instance.description)
		instance.logo = validated_data.get('logo', instance.logo)
		return instance


class NotificationSerializer(serializers.ModelSerializer):
	user=serializers.SerializerMethodField()
	commande=serializers.SerializerMethodField()
	produit=serializers.SerializerMethodField()
	class Meta:
		model=Notification
		fields="__all__"
	def get_user(self,obj):
		return UserSerializer(obj.user).data

	def get_commande(self,obj):
		return CommandeSerializer(obj.commande).data

	def get_produit(self,obj):
		return ProductSerializer(obj.produit).data
		



		

	

	



	



	

	
		



		
	
		
	
		