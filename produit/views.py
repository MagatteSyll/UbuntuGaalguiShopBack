from .models import*
from django.shortcuts import get_object_or_404
from rest_framework import status
from .serializer import*
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView,DestroyAPIView,GenericAPIView,ListAPIView
from rest_framework.response import Response
from rest_framework import authentication, permissions,generics
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.mixins import ListModelMixin
from rest_framework import filters
from rest_framework.permissions import  BasePermission, SAFE_METHODS
from user.serializer import UserSerializer
from user.models import User
import decimal
from user.notifications import NotificationCommandeAuVendeur,NotificationNewProductToFollower 

  

 
class VendeurPermission(BasePermission):
	message = 'La modification ou suppression d un produit ne peut etre fait que par le vendeur'

	def has_object_permission(self, request, view, obj):
		if request.method in SAFE_METHODS:
			return True
		return obj.vendeur == request.user



#Gestion recherche a revoir
class ProduitSearch(generics.ListAPIView):
	permission_classes = [permissions.AllowAny]
	queryset = Produit.objects.filter(vendu=False,active=True)
	serializer_class = ProductSerializer
	filter_backends = [filters.SearchFilter]
	search_fields = search_fields = ['^nom','^description','^category__category']

#list des categories
class CategoryList(ListAPIView):
	permission_classes = [permissions.AllowAny]
	def get(self,request):
		category=Category.objects.all().order_by('-id')
		serializer=CategorySerializer(category,many=True)
		return Response(serializer.data)


#liste des regions
class RegionList(ListAPIView):
	queryset = Region.objects.all().order_by('-id')
	serializer_class = RegionSerializer
	permission_classes = [permissions.AllowAny]


#liste des adresses de livraison
class AdressList(ListAPIView):
	serializer_class=AdresseSerializer
	queryset=Adress.objects.all().order_by('-id')
	permission_classes = [permissions.AllowAny]


#recuperer le vendeur 
'''class IsVendeur(APIView):
	def post(self,request,*args,**kwargs):
		id =request.data.get('id')
		produit=Produit.objects.get(id=id)
		if request.user==produit.vendeur:
			return Response(True)
		return Response(False)'''

class Getdevise(APIView):
	def get(self,request):
		devise=Devise.objects.all()
		serializer=DeviseSerializer(devise,many=True)
		return Response(serializer.data)
		

#ajout de produit au panier
class AddCartView(APIView):   
	def post(self,request,*args,**kwargs):
		slug=request.data.get('slug')
		if slug is None:
			return Response({'error':'id invalide'})
		else:
			produit=Produit.objects.get(slug=slug)
			cart=Cart.objects.get(proprietaire=request.user)
			if produit.variation==False:
				produit_cart=cart.cartproduct.filter(product=produit)
				if produit_cart.exists():
					cart_product=produit_cart.last()
					if produit.qte>cart_product.quantity:
						cart_product.quantity+=1
						cart_product.subtotal+=produit.prix
						cart_product.save()
						cart.total+=produit.prix
						cart.save()
						return Response({'message':'produit existant reajoute fois'})
				else:
					cart_product=CartProduct.objects.create(product=produit , quantity=1,
					 subtotal=produit.prix,client=request.user)
					cart.cartproduct.add(cart_product)
					cart.total+=produit.prix
					cart.save()
					return Response({'message':'premiere fois'})

			else:
				produitimg_id=request.data.get('prodimg')
				prodimg=ProduitImage.objects.get(id=produitimg_id)
				produitimg_cart=cart.cartproduct.filter(imageproduct=prodimg)
				if produitimg_cart.exists():
					cart_produitimg=produitimg_cart.last()
					if prodimg.quantite>cart_produitimg.quantity:
						cart_produitimg.quantity+=1
						cart_produitimg.subtotal+=produit.prix
						cart_produitimg.save()
						return Response({'message':'premiere fois'})
				else:
					cart_produitimg=CartProduct.objects.create(imageproduct=prodimg , quantity=1,
					 subtotal=produit.prix,client=request.user)
					cart.cartproduct.add(cart_produitimg)
					cart.total+=produit.prix
					cart.save()
					return Response({'message':'cart cree produit ajoute '})

#panier d un utilisateur	
class CartView(RetrieveAPIView):
	serializer_class=CartSerializer
	def get_object(self):
		try:
			cart=Cart.objects.filter(proprietaire=self.request.user,ordered=False).first()
			return cart
		except ObjectsDoesNotExist:
			return Response({'message':'cart non existant'})

#Operation sur le panier
class CartProductDeleteSingle(ModelViewSet):
	serializer_class=CartSerializer
	queryset=Cart.objects.all()

	@action(methods=["put"], detail=False, url_path='mycart/remove/(?P<pk>\d+)')
	def product_remove_from_cart(self, *args, **kwargs):
		cart = Cart.objects.get(proprietaire=self.request.user)
		id=self.kwargs['pk']
		if id is None:
			return Response({'error':'id invalide'})
		else:
			cartproduct = CartProduct.objects.get(id=id)
			cartproduct.quantity-=1
			if cartproduct.product is None:
				cartproduct.subtotal-=cartproduct.imageproduct.produit.prix
				cartproduct.save()
				cart.total-=cartproduct.imageproduct.produit.prix
				cart.save()
			else:
				cartproduct.subtotal-=cartproduct.product.prix
				cartproduct.save()
				cart.total-=cartproduct.product.prix
				cart.save()
			if cartproduct.quantity==0:
				cart.cartproduct.remove(cartproduct)
				cartproduct.delete()
				cart.save()
			return Response({"message":'produit supprime'})

	@action(methods=["put"], detail=False, url_path='mycart/removesingle/(?P<pk>\d+)')
	def product_remove_all_cartproduct(self, *args, **kwargs):
		cart = Cart.objects.get(proprietaire=self.request.user)
		id=self.kwargs['pk']
		if id is None:
			return Response({'error':'id invalide'})
		else:
			cartprod = CartProduct.objects.get(id=id)
			cart.cartproduct.remove(cartprod)
			cartprod.delete()
			cart.total-=cartprod.subtotal
			cart.save()
			return Response({"message":'produit supprime'})

	@action(methods=["put"], detail=False, url_path='mycart/removeall')
	def remove_all(self,request):
		cart = Cart.objects.get(proprietaire=request.user)
		cart.cartproduct.all().delete()
		cart.total=0
		cart.save()
		return Response({'message':'carte videe'})

#Ajout d un produit avec variation
class AjoutProduit(APIView):
	parser_classes = [MultiPartParser, FormParser]
	def post(self,request,*args,**kwargs):
		if request.user.active==True:
			data=request.data
			cat_id=data['category_id']
			region_id=data['region_id']
			devise_id=data['devise_id']
			devise=Devise.objects.get(id=devise_id)
			region=Region.objects.get(id=region_id)
			boutique=Boutique.objects.get(user=request.user)
			category=Category.objects.get(id=cat_id)
			serializer=ProductSerializer(data=data)
			if serializer.is_valid():
				serializer.save(vendeur=request.user,category=category,region=region,boutique=boutique,devise=devise
					,active=True,variation=True,recycler=False)
				pro_id=serializer.data['id']
				produit=Produit.objects.get(id=pro_id)
				serializerimg1=ProduitImageserializer(data=data)
				if serializerimg1.is_valid():
					serializerimg1.save(produit=produit,image=data['img1'],size=data['taille1'],
					color=data['couleur1'],quantite=data['qte1'])
				serializerimg2=ProduitImageserializer(data=data)
				if serializerimg2.is_valid():
					serializerimg2.save(produit=produit,image=data['img2'],size=data['taille2'],
					color=data['couleur2'],quantite=data['qte2'])
				img3=request.data.get('img3',None)
				if img3 is not None:
					serializerimg3=ProduitImageserializer(data=data)
					if serializerimg3.is_valid():
						serializerimg3.save(produit=produit,image=img3,size=data['taille3'],
							color=data['couleur3'],quantite=data['qte3'])
				img4=request.data.get('img4',None)
				if img4 is not None:
					serializerimg4=ProduitImageserializer(data=data)
					if serializerimg4.is_valid():
						serializerimg4.save(produit=produit,image=img4,size=data['taille4'],
							color=data['couleur4'],quantite=data['qte4'])
				img5=request.data.get('img5',None)
				if img5 is not None:
					serializerimg5=ProduitImageserializer(data=data)
					if serializerimg5.is_valid():
						serializerimg5.save(produit=produit,image=img5,size=data['taille5'],
							color=data['couleur5'],quantite=data['qte5'])
				img6=request.data.get('img6',None)
				if img6 is not None:
					serializerimg6=ProduitImageserializer(data=data)
					if serializerimg6.is_valid():
						serializerimg3.save(produit=produit,image=img6,size=data['taille6'],
							color=data['couleur6'],quantite=data['qte6'])
				img7=request.data.get('img7',None)
				if img7 is not None:
					serializerimg7=ProduitImageserializer(data=data)
					if serializerimg7.is_valid():
						serializerimg7.save(produit=produit,image=img7,size=data['taille7'],
							color=data['couleur7'],quantite=data['qte7'])
				img8=request.data.get('img8',None)
				if img8 is not None:
					serializerimg8=ProduitImageserializer(data=data)
					if serializerimg8.is_valid():
						serializerimg3.save(produit=produit,image=img8,size=data['taille8'],
							color=data['couleur8'],quantite=data['qte8'])
				img9=request.data.get('img9',None)
				if img9 is not None:
					serializerimg9=ProduitImageserializer(data=data)
					if serializerimg9.is_valid():
						serializerimg9.save(produit=produit,image=img9,size=data['taille9'],
							color=data['couleur9'],quantite=data['qte9'])
				img10=request.data.get('img10',None)
				if img10 is not None:
					serializerimg10=ProduitImageserializer(data=data)
					if serializerimg10.is_valid():
						serializerimg3.save(produit=produit,image=img10,size=data['taille10'],
							color=data['couleur10'],quantite=data['qte10'])
				produitimg=ProduitImage.objects.filter(produit__id=serializer.data['id']).order_by('id')[0]
				produitimg.produit.thumbnail=produitimg.image
				produitimg.produit.save()
				NotificationNewProductToFollower(boutique,produit,request.user)
				return Response({'message':'produit bien ajoute'})
			#return Response(serializer.errors)

#AjoutSansVariation
class AjoutSansVariation(APIView):
	parser_classes = [MultiPartParser, FormParser]
	def post(self,request,*args,**kwargs):
		if request.user.active==True:
			data=request.data
			cat_id=data['category_id']
			region_id=data['region_id']
			region=Region.objects.get(id=region_id)
			boutique=Boutique.objects.get(user=request.user)
			category=Category.objects.get(id=cat_id)
			devise_id=data['devise_id']
			devise=Devise.objects.get(id=devise_id)
			serializer=ProductSerializer(data=data)
			if serializer.is_valid():
				serializer.save(vendeur=request.user,category=category,region=region,boutique=boutique,active=True,
					devise=devise,variation=False,recycler=False)
				pro_id=serializer.data['id']
				produit=Produit.objects.get(id=pro_id)
				serializerimg1=ProduitImageserializer(data=data)
				if serializerimg1.is_valid():
					serializerimg1.save(produit=produit,image=data['img1'])
				serializerimg2=ProduitImageserializer(data=data)
				if serializerimg2.is_valid():
					serializerimg2.save(produit=produit,image=data['img2'])
				serializerimg3=ProduitImageserializer(data=data)
				if serializerimg3.is_valid():
					serializerimg3.save(produit=produit,image=data['img3'])
				img4=request.data.get('img4',None)
				if img4 is not None:
					serializerimg4=ProduitImageserializer(data=data)
					if serializerimg4.is_valid():
						serializerimg4.save(produit=produit,image=img4)
				img5=request.data.get('img5',None)
				if img5 is not None:
					serializerimg5=ProduitImageserializer(data=data)
					if serializerimg5.is_valid():
						serializerimg5.save(produit=produit,image=img5)
				img6=request.data.get('img6',None)
				if img6 is not None:
					serializerimg6=ProduitImageserializer(data=data)
					if serializerimg6.is_valid():
						serializerimg3.save(produit=produit,image=img6)
				img7=request.data.get('img7',None)
				if img7 is not None:
					serializerimg7=ProduitImageserializer(data=data)
					if serializerimg7.is_valid():
						serializerimg7.save(produit=produit,image=img7)
				img8=request.data.get('img8',None)
				if img8 is not None:
					serializerimg8=ProduitImageserializer(data=data)
					if serializerimg8.is_valid():
						serializerimg3.save(produit=produit,image=img8)
				img9=request.data.get('img9',None)
				if img9 is not None:
					serializerimg9=ProduitImageserializer(data=data)
					if serializerimg9.is_valid():
						serializerimg9.save(produit=produit,image=img9)
				img10=request.data.get('img10',None)
				if img10 is not None:
					serializerimg10=ProduitImageserializer(data=data)
					if serializerimg10.is_valid():
						serializerimg3.save(produit=produit,image=img10)
				produitimg=ProduitImage.objects.filter(produit__id=serializer.data['id']).order_by('id')[0]
				produitimg.produit.thumbnail=produitimg.image
				produitimg.produit.save()
				NotificationNewProductToFollower(boutique,produit,request.user)

				return Response({'message':'produit bien ajoute'})



	

#Suivi d une boutique par un utilisateur
class AddFollower(APIView):
	def post(self,request):
		data=request.data
		id_boutique=data['id_boutique']
		boutique=Boutique.objects.get(id=id_boutique)
		follower,created=Follower.objects.get_or_create(user=request.user)
		boutique.follower.add(follower)
		boutique.nbrefollower+=1
		boutique.save()
		return Response({'message':'nouveau follower'})

#unfollow boutique par un utilisateur
class RemoveFollower(ModelViewSet):
	queryset=Boutique.objects.all()
	serializer_class=BoutiqueSerializer
	@action(methods=["delete"], detail=False, url_path='removefollower/(?P<pk>\d+)')
	def remove_follower(self,request,*args,**kwargs):
		id_boutique=self.kwargs['pk']
		boutique=Boutique.objects.get(id=id_boutique)
		follower=Follower.objects.get(user=self.request.user)
		boutique.follower.remove(follower)
		boutique.nbrefollower-=1
		boutique.save()
		return Response({'message':'follower supprime'})

#Verifier si un utilisateur follow une boutique
class VeriFollower(APIView):
	def post(self,request):
		data=request.data
		user_id=data['user_id']
		user=User.objects.get(id=user_id)
		userfollower=Follower.objects.get(user=user)
		boutique_id=data['boutique_id']
		boutique=Boutique.objects.get(id=boutique_id)
		for follower in boutique.follower.all():
			if follower.id==userfollower.id:
				return Response(True)
			
		return Response(False)

#Ajouter des imageproduit
class AjoutProduitImage(APIView):
	def post(self,request):
		data=request.data
		produit=Produit.objects.get(id=data['id'])
		nbreimg=ProduitImage.objects.filter(produit=produit).count()
		if nbreimg <10:
			serializer=ProduitImageserializer(data=data)
			if serializer.is_valid():
				serializer.save(produit=produit)
				return Response({'message':'un nouveauproduit'})


						
class ManageProduitImage(ModelViewSet,VendeurPermission):
	queryset=ProduitImage.objects.all()
	serializer_class=ProductSerializer 
	permission_classes=(VendeurPermission,)

	@action(methods=["delete"], detail=False, url_path='suppression/(?P<pk>\d+)')
		#permission_classes = [IsVendeurOrReadOnly])
	def sup_prodimg(self,*args,**kwargs):
		id=self.kwargs['pk']
		produitimg=ProduitImage.objects.get(id=id)
		produit=produitimg.produit
		allproduitimg=ProduitImage.objects.filter(produit=produit).count()
		if self.request.user==produitimg.produit.vendeur:
			if produit.variation==True:
				if allproduitimg>2:
					produitimg.delete()
			else:
				if allproduitimg>3:
					produitimg.delete()
			return Response({'message':'produitimg supprime'})

	@action(methods=["put"], detail=False, url_path='modifprodimg/(?P<pk>\d+)')
	def modif_prodimg(self,request,*args,**kwargs):
		id=self.kwargs['pk']
		produitimg=ProduitImage.objects.get(id=id)
		if produitimg.produit.vendeur==request.user:
			color=request.data.get('color',None)
			if color is not None:
				produitimg.color=color
				produitimg.save()
			size=request.data.get('size',None)
			if size is not None:
				produitimg.size=size
				produitimg.save()
			quantite=int(request.data.get('quantite',None))
			if quantite is not None:
				produitimg.quantite=quantite
				produitimg.save()
			image=request.data.get('image',None) 
			if image is not None:
				produitimg.image=image
				produitimg.save()
			primg=ProduitImage.objects.filter(produit=produitimg.produit).order_by('id')[0]
			primg.produit.thumbnail=primg.image
			primg.produit.save()
			return Response({'message':"Produit bien modifie"})	


class Manageproduit(ModelViewSet,VendeurPermission):
	queryset=Produit.objects.all()
	serializer_class=ProductSerializer 
	permission_classes=(VendeurPermission,)
	@action(methods=["delete"], detail=False, url_path='supprimer/(?P<pk>\d+)')
	def sup_prod(self,*args,**kwargs):
		id=self.kwargs['pk']
		produit=Produit.objects.get(id=id)
		if self.request.user==produit.vendeur:
			produit.delete()
			return Response({'message':'produit supprime'})
	@action(methods=["put"], detail=False, url_path='modifsanspic/(?P<slug>[\w-]+)')
	def modif_withoutpic(self,request,*args,**kwargs):
		slug=self.kwargs['slug']
		produit=Produit.objects.get(slug=slug)
		if produit.vendeur==request.user:
			data=request.data
			cat_id=data['category']
			region_id=data['region']
			devise_id=data['devise']
			devise=Devise.objects.get(id=devise_id)
			produit.devise=devise
			prix=request.data.get('prix')
			prideci=(decimal.Decimal(prix))
			category=Category.objects.get(id=cat_id)
			region=Region.objects.get(id=region_id)
			produit.region=region
			produit.prix=prideci
			produit.category=category
			produit.save()
			nom=request.data.get('nom',None)
			if nom is not None:
				produit.nom=nom
				produit.save()
			description=request.data.get('description',None)
			if description is not None:
				produit.description=description
				produit.save()
			couleur=request.data.get('couleur',None)
			if couleur is not None:
				produit.couleur=couleur
				produit.save()
			taille=request.data.get('taille',None)
			if taille is not None:
				produit.taille=taille
				produit.save()
			qte=request.data.get('qte',None)
			if qte is not None:
				produit.qte=int(qte)
				produit.save()
			return Response({'message':"Produit bien modifie"})


class ReactivationProduit(APIView):
	def post(self,request):
		data=request.data
		id=data['id'] 
		produit=Produit.objects.get(id=id)
		if request.user==produit.vendeur:
			produit.active=True
			produit.vendu=True
			produit.save()
			return Response({'message':'reactivation reussie'})
		


#recuperer le panier de commande
class GetPanier(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			cart=Cart.objects.get(proprietaire =request.user)
			cartprod=cart.cartproduct.all().order_by('-id')
			serializer=CartProductSerializer(cartprod,many=True)
			return Response(serializer.data)
		return Response(False)

		

		
#Gestion commande
class PostCommande(APIView):
	def post(self,request):
		data=request.data
		produitcommande=CartProduct.objects.get(id=data['cart_id'])
		if produitcommande.product.quantite>=produitcommande.quantity:
			adress_id=data['adress_id']
			vendeur=produitcommande.product.vendeur
			prod=produitcommande.product.nom
			adress=Adress.objects.get(id=adress_id)
			serializer=CommandeSerializer(data=data)
			user=request.user
			livraison=decimal.Decimal(data['livraison'])
			commission=round(2*produitcommande.product.prix/decimal.Decimal(100),2)
			montant_vendeur=produitcommande.product.prix-commission
			if serializer.is_valid():
				serializer.save(produitcommande=produitcommande,
					adress=adress,active=True,livraison=livraison,acheteur=user,
					statut_commande='produit en attente de livraison',commission=commission,
					montant_vendeur=montant_vendeur)
				id_commande=serializer.data['id']
				commande=Commande.objects.get(id=id_commande)
				produitcommande.product.quantite-=1
				produitcommande.product.save()
				if produitcommande.product.quantite==0:
					produitcommande.product.active=False
					produitcommande.product.save()
				NotificationCommandeAuVendeur(vendeur,commande)
				return Response(serializer.data)
		#return Response(serializer.errors)


		

#Recu commande			
class GetCommande(APIView):
	def post(self,request):
		data=request.data
		id=data['id']
		commande=Commande.objects.get(id=id)
		if commande.acheteur==request.user:
			serializer=CommandeSerializer(commande)
			return Response(serializer.data)
	
		
'''class GetCartProduct(APIView):
	def post(self,request):
		id=request.data.get('id')
		cartproduct=CartProduct.objects.get(id=id)
		serializer=CartProductSerializer(cartproduct)
		return Response(serializer.data)'''

class NotificationDetail(APIView):
	def post(self,request):
		data=request.data
		id=data['id']
		notify=Notification.objects.get(id=id)
		if notify.user==request.user:
			serializer=NotificationSerializer(notify)
			return Response(serializer.data)
						

class ActivationCommande(APIView):
	def post(self,request):
		id=request.data.get('pid')
		commande=Commande.objects.get(id=id)
		commande.active=True
		commande.save()
		commande.statut_commande="produit en attente de livraison"
		commande.save()
		return Response({'message':'commande prise en charge '})

		

class RemoveCommande(ModelViewSet):
	queryset=Commande.objects.all()
	serializer_class=CommandeSerializer

	@action(methods=["delete"], detail=False, url_path='supprimer/(?P<pk>\d+)')
	def noter(self,request,*args,**kwargs):
		id=self.kwargs['pk']
		commande=Commande.objects.get(id=id)
		commande.delete()
		return Response({'message':'commande non prise en charge'})
		

class ProduitMemeCategroy(APIView): 
	def post(self,request):
		category_nom=request.data.get('category')
		category=Category.objects.get(category=category_nom)
		produits=Produit.objects.filter(category=category)
		serializer=ProductSerializer(produits,many=True)
		return Response(serializer.data)

class BoutiqueView(APIView):
	def get(self,request):
		boutique=Boutique.objects.get(user=request.user)
		if boutique is not None:
			serializer=BoutiqueSerializer(boutique)
			return Response(serializer.data)


#produit actif d un utilisateur d un utilisateur donne
class MesProduits(APIView):
	def get(self,request):
		produit=Produit.objects.filter(vendeur=request.user,active=True).order_by('-id')
		serializer=ProductSerializer(produit,many=True)
		return Response(serializer.data)

#Produit vendu d un utilisateur
class MesProduitsVendu(APIView):
	def get(self,request):
		produit=Produit.objects.filter(vendeur=request.user,vendu=True)
		serializer=ProductSerializer(produit,many=True)
		return Response(serializer.data)

		
#Image thumbnail
class ImageDunProduit(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		data=request.data
		id=data['id']
		produitimg=ProduitImage.objects.filter(produit__id=id).order_by('id')[0]
		serializer=ProduitImageserializer(produitimg)
		return Response(serializer.data)

#Toutes les images
class AllImageProduit(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		data=request.data
		slug=data['slug']
		produitimg=ProduitImage.objects.filter(produit__slug=slug).order_by('-id')
		serializer=ProduitImageserializer(produitimg,many=True)
		return Response(serializer.data)

		
#Changement logo boutique
class EditBoutiquePic(APIView):
	parser_classes = [MultiPartParser, FormParser]
	def post(self,request,format=None):
		boutique=Boutique.objects.get(user=request.user)
		data=request.data
		boutique.logo=data['logo']
		boutique.save()
		serializer=BoutiqueSerializer(boutique)
		return Response(serializer.data)

#Changement desription boutique
class EditBoutiqueDes(APIView):
	def post(self,request,*args,**kwargs):
		boutique=Boutique.objects.get(user=request.user)
		data=request.data
		boutique.description=data['description']
		boutique.save()
		serializer=BoutiqueSerializer(boutique)
		return Response({'message':'description bien editee'})

#Toutes les categories
class DisplayPerCategory(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		data=request.data
		cat=data['category']
		category=Category.objects.get(category=cat)
		produit=Produit.objects.filter(category=category,vendu=False,active=True).order_by('-id')
		serializer=ProductSerializer(produit,many=True)
		return Response(serializer.data)
				
#Recuperation d un produit	
class GetProduit(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		data=request.data
		slug=data['slug']
		produit=Produit.objects.get(slug=slug)
		serializer=ProductSerializer(produit)
		return Response(serializer.data)
####
#Reuperation produit et cartproduit
class GetCartCommande(APIView):
	def post(self,request):
		data=request.data
		slug=data['slug']
		id=data['id']
		cartproduit=CartProduct.objects.get(id=id)
		cartserial=CartProductSerializer(cartproduit)
		adress=Adress.objects.all().order_by('-id')
		adressserial=AdresseSerializer(adress,many=True)
		return Response({'cartproduit':cartserial.data,'adress':adressserial.data})

#Calcul de la livraison
class CalculLivraison(APIView):
	def post(self,request):
		data=request.data
		adress_id=data['adress_id']
		slug=data['slug']
		cart_id=data['cartproduit_id']
		cartproduit=CartProduct.objects.get(id=cart_id)
		adress=Adress.objects.get(id=adress_id)
		produit=Produit.objects.get(slug=slug)
		if produit.region.id==adress.region.id:
			livraison=decimal.Decimal(500)
			total=livraison + cartproduit.subtotal
			return Response({'livraison':livraison,'total':total})
		else:
			livraison=decimal.Decimal(1000)
			total=livraison + cartproduit.subtotal
			return Response({'livraison':livraison ,'total':total})



#Produitvendu de l utilisateur				
class ProdutVendu(APIView): 
	def get(self,request):
		vendeur=request.user
		produits=Produit.objects.filter(vendeur=vendeur,vendu=True,recycler=False).order_by('-id')
		serializer=ProductSerializer(produits,many=True)
		return Response(serializer.data)

#Historique d achat 
class ProduitAchete(APIView): 
	def get(self,request):
		produits=Commande.objects.filter(statut_commande="produit livré").order_by('-id')
		serializer=CommandeSerializer(produits,many=True) 
		return Response(serializer.data)

#Commandes pas encore livrees
class CommandeEnCours(APIView):
	def get(self,request):
		commandes=Commande.objects.filter(acheteur=request.user,active=True).exclude(statut_commande="produit livré")
		serializer=CommandeSerializer(commandes,many=True)
		return Response(serializer.data)


#ProduitActif  vu client
class ProduitActifVendeur(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		data=request.data
		id=data['id']
		boutique=Boutique.objects.get(id=id)
		vendeur=boutique.user
		items=Produit.objects.filter(vendeur=vendeur,active=True)
		serializer=ProductSerializer(items,many=True)
		return Response(serializer.data)

#Produitvendu vu client		
class ProduitVenduVendeur(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		data=request.data
		id=data['id']
		boutique=Boutique.objects.get(id=id)
		vendeur=boutique.user
		items=Produit.objects.filter(vendu=True)
		serializer=ProductSerializer(items,many=True)
		return Response(serializer.data)

#Profil boutique vu client	
class BoutiqueVuClient(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		data=request.data
		id=data['id']
		boutique=Boutique.objects.get(id=id)
		serializer=BoutiqueSerializer(boutique)
		return Response(serializer.data)

#Profil boutique vu client	
class ProfileVendeur(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		slug=request.data.get('slug')
		produit=Produit.objects.get(slug=slug)
		user=produit.vendeur
		boutique=Boutique.objects.get(user=user)
		serializer=BoutiqueSerializer(boutique)
		return Response(serializer.data)


#Profil vendeur sur mobile
'''class VueVendeur(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		id=request.data.get('id')
		user=User.objects.get(id=id)
		boutique=Boutique.objects.get(user=user)
		serializer=BoutiqueSerializer(boutique)
		return Response(serializer.data)'''

#produits de la boutique sur mobile
'''class ShopVendeur(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		id=request.data.get('id')
		vendeur=User.objects.get(id=id)
		items=Produit.objects.filter(vendeur=vendeur,active=True)
		serializer=ProductSerializer(items,many=True)
		return Response(serializer.data)'''


class ActifVendeur(APIView):
	def post(self,request):
		slug=request.data.get('slug')
		boutique=Boutique.objects.get(slug=slug)
		user=boutique.user
		if user.active==True:
			return Response(True)
		return Response(False)


class GetVendeur(APIView):
	def post(self,request):
		slug=request.data.get('slug')
		produit=Produit.objects.get(slug=slug)
		user=produit.vendeur
		serializer=UserSerializer(user)
		return Response(serializer.data)

###
class NoteVendeur(ModelViewSet):
	queryset=Boutique.objects.all()
	serializer_class=BoutiqueSerializer
	#permission_classes=(VendeurPermission,)
	@action(methods=["put"], detail=False, url_path='note')
	def noter(self,request,*args,**kwargs):
		id=request.data['id']
		note=int(request.data['note'])
		user=User.objects.get(id=id)
		boutique=Boutique.objects.get(user=user)
		boutique.note_vendeur=(boutique.note_vendeur+note)//2
		boutique.save()
		return Response({'message':'vendeur bien noté'})

###
class NosVendeurs(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self,request):
		boutique=Boutique.objects.order_by('-note_vendeur')[:5]
		serializer=BoutiqueSerializer(boutique,many=True)
		return Response(serializer.data)
		
class Occasions(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self,request):
		occasion=Produit.objects.filter(category__category='Occasions').order_by('-id')[:8]
		serializer=ProductSerializer(occasion,many=True)
		return Response(serializer.data)
				
		



	
		
		




  


		

		
	

	

		
		
		
	



	
		


	



	
	


	

	
	


			

		

		
		



























