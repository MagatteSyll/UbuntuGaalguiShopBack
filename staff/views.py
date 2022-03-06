from django.shortcuts import render
from rest_framework.permissions import  BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from produit.serializer import*
from produit.models import*
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView,DestroyAPIView,GenericAPIView,ListAPIView
from rest_framework import filters
from rest_framework import authentication, permissions,generics
from .models import*
from user.notifications import NotifcationChangementEtatCommande







class IsStaf(APIView):
	permission_classes=[permissions.AllowAny]
	def get(self,request):
		if request.user.is_staff==True:
			return Response(True)
		return Response(False)


class RechercheCommandes(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		id=request.data.get('id')
		commande=Commande.objects.get(id=id,active=True)
		serializer=CommandeSerializer(commande)
		return Response(serializer.data)

class DepotCommande(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		data=request.data
		id=data['id']
		commande=Commande.objects.get(id=id)
		commande.statut_commande="produit en cours de livraison "
		commande.save()
		user=commande.acheteur
		NotifcationChangementEtatCommande(user,commande)
		action='Modification du status de la  commande : '+ " " + str(id)  + " " + 'nouveau status:' + commande.statut_commande
		identifiant=request.user
		ActionStaff.objects.create(identifiant=identifiant,action=action)
		return Response({"message":'produit status change'})


class RetraitCommande(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		data=request.data
		id=data['id']
		commande=Commande.objects.get(id=id)
		commande.statut_commande="produit livré"
		commande.save()
		commande.produitcommande.product.vendu=True
		commande.produitcommande.product.save()
		#Notification au vendeur
		user=commande.acheteur
		action='Modification du status de la  commande : '+ " " +  str(id) + " " + 'nouveau status:' + commande.statut_commande
		identifiant=request.user
		ActionStaff.objects.create(identifiant=identifiant,action=action)
		return Response({"message":'produit status change'})
	
		


class CommandeAnnulation(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		cid=request.data.get('id')
		com=Commande.objects.get(id=cid)
		com.active=False
		com.save()
		action="Annulation de la  commande numero " + " " + str(cid)
		ActionStaff.objects.create(identifiant=request.user,action=action)
		serializer=CommandeSerializer(com)
		return Response(serializer.data)
		

class DesactiverVendeur(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		slug=request.data.get('slug')
		boutique=Boutique.objects.get(slug=slug)
		vendeur=boutique.user
		vendeur.active=False
		vendeur.save()
		produit=Produit.objects.filter(vendeur=vendeur)
		for p in produit:
			p.active=False
			p.save()
		action="desactivation du vendeur " + " " + vendeur.prenom +" "+ vendeur.nom +" " + "id:" + " "  + str(vendeur.id)
		ActionStaff.objects.create(identifiant=request.user,action=action)
		return Response({'message': 'vendeur desactivé'})

class ActivationVendeur(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		slug=request.data.get('slug')
		boutique=Boutique.objects.get(slug=slug)
		vendeur=boutique.user
		vendeur.active=True
		vendeur.save()
		produit=Produit.objects.filter(vendeur=vendeur)
		for p in produit:
			p.active=True
			p.save()
		return Response({'message':'vendeur reactive'})

	
		
class AnnulationCommande(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		id=request.data.get('id')
		commande=Commande.objects.get(id=id)
		commande.active=False
		commande.save()
		action="desactivation commande " + " " + str(id)
		ActionStaff.objects.create(identifiant=request.user,action=action)
		return Response({'message':'commande desactivée'})

		
class RechercheProduit(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		id=request.data.get('id')
		produit=Produit.objects.get(id=id)
		serializer=ProductSerializer(produit)
		return Response(serializer.data)


class DeleteProduit(ModelViewSet):
	queryset=Produit.objects.all()
	serializer_class=ProductSerializer
	permission_classes=[permissions.IsAdminUser]
	@action(methods=["delete"], detail=False, url_path='supprimer/(?P<pk>\d+)')
	def sup_prod(self,*args,**kwargs):
		id=self.kwargs['pk']
		produit=Produit.objects.get(id=id)
		produit.delete()
		action='suppression du produit Numero:' + " " + str(id)
		identifiant=request.user
		ActionStaff.objects.create(action=action,identifiant=identifiant)
		return Response({'message':'produit supprime'})
	
	
		
		
	
		





	
