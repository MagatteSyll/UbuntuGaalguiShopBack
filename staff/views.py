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
from user.notifications import NotifcationChangementEtatCommande,AnnulationAchatCoteClient,AnnulationVente,AvertissementVendeur,DesactivationDeBoutique,NotificationActivationBoutique,NotificationProblemeTeechnique







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
		commande=Commande.objects.get(id=id,active=True,payer=True)
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
		if commande.produitcommande.product is None:
			nom=commande.produitcommande.imageproduct.produit.nom
			NotifcationChangementEtatCommande(user,commande,nom)
		else:
			nom=commande.produitcommande.product.nom
			NotifcationChangementEtatCommande(user,commande,nom)
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
		if commande.produitcommande.product is None:
			commande.produitcommande.imageproduct.vendu=True
			commande.produitcommande.imageproduct.qte_vendu+=commande.produitcommande.quantity
			commande.produitcommande.imageproduct.save()
		else:
			commande.produitcommande.product.vendu=True
			commande.produitcommande.product.vendu_qte+=commande.produitcommande.quantity
			commande.produitcommande.product.save()
		user=commande.acheteur
		#NotificationDe Note
		action='Modification du status de la  commande : '+ " " +  str(id) + " " + 'nouveau status:' + commande.statut_commande
		identifiant=request.user
		ActionStaff.objects.create(identifiant=identifiant,action=action)
		return Response({"message":'produit status change'})
	
		
#Modification commande par le personnel de bureau
class ModificationEtatCommande(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		id=request.data.get('id')
		com=Commande.objects.get(id=id)
		etat=request.data.get('etat')
		com.statut_commande=etat
		com.save()
		action="modification du status de la commande au bureau " + " "+ str(id) + " " + " en " + " "+ etat
		identifiant=request.user
		ActionStaff.objects.create(action=action,identifiant=identifiant)
		return Response ({'success':'modification commande'})
		





	
		
class AnnulationCommande(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		id=request.data.get('id')
		motif=request.data.get('motif')
		commande=Commande.objects.get(id=id)
		commande.active=False
		commande.save()
		action="Annulation de la  commande " + " " + str(id) + " " + " pour motif" + " " + motif
		ActionStaff.objects.create(identifiant=request.user,action=action)
		if commande.produitcommande.product is None:
			nom=commande.produitcommande.imageproduct.produit.nom
			AnnulationAchatCoteClient(commande.acheteur,commande,nom)
			AnnulationVente(commande.produitcommande.imageproduct.produit.vendeur,commande,nom)
		else:
			nom=commande.produitcommande.product.nom
			AnnulationAchatCoteClient(commande.acheteur,commande,nom)
			AnnulationVente(commande.produitcommande.product.vendeur,commande,nom)
		serializer=CommandeSerializer(commande)
		return Response(serializer.data)


		

class AvertirVendeur(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		id=request.data.get('id')
		motif=request.data.get('motif')
		boutique=Boutique.objects.get(id=id)
		boutique.avertissement+=1
		boutique.save()
		if boutique.avertissement<4:
			AvertissementVendeur(boutique.user)
		if boutique.avertissement==4:
			boutique.active=False
			boutique.save()
			produit=Produit.objects.filter(vendeur=boutique.user)
			for p in produit:
				p.active=False
				p.save()
				imgprod=ProduitImage.objects.filter(produit=p)
				for im in imgprod:
					im.active=False
					im.save()
			DesactivationDeBoutique(boutique.user)
		action="avertissement de l utilisateur  numero" + " " + str(boutique.user.id) +" "+ "pour motif"+" "+ motif
		identifiant=request.user
		ActionStaff.objects.create(identifiant=identifiant,action=action) 
		return Response({'success':'avertissement vendeur'})

class ReactivationVendeur(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		id=request.data.get('id')
		motif=request.data.get('motif')
		boutique=Boutique.objects.get(id=id)
		boutique.active=True
		boutique.avertissement=0
		boutique.save()
		produit=Produit.objects.filter(vendeur=boutique.user)
		for p in produit:
			if p.variation==True:
				p.active=True
				p.save()
				imgprod=ProduitImage.objects.filter(produit=p)
				for im in imgprod:
					if im.quantite>0:
						im.active=True
						im.save()

			else:
				if p.qte>0:
					p.active=True
					p.save()
					imgprod=ProduitImage.objects.filter(produit=p)
					for im in imgprod:
						im.active=True
						im.save()
		NotificationActivationBoutique(boutique.user)	
		action="reactivation  l utilisateur  numero" + " " + str(boutique.user.id) +" "+ "pour motif"+" "+ motif
		identifiant=request.user
		ActionStaff.objects.create(identifiant=identifiant,action=action) 
		return Response({'success':'reactivation vendeur'})



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
	

class GetBoutique(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		id=request.data.get('id')
		boutique=Boutique.objects.get(id=id)
		serializer=BoutiqueSerializer(boutique)
		return Response(serializer.data)


class ProblemeTechnique(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		probleme=request.data.get('probleme')
		users=User.objects.filter(is_staff=True,istechnique=True)
		NotificationProblemeTeechnique(probleme,users)
		action='Signal d un probleme technique' + " " + probleme
		identifiant=request.user
		ActionStaff.objects.create(action=action,identifiant=identifiant)
		return Response({'success':'probleme technique'})


class GetNotification(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		id=request.data.get('id')
		notif=Notification.objects.get(id=id)
		serializer=NotificationSerializer(notif)
		return Response(serializer.data)

		
		
	
		





	
