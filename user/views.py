from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import*
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from produit.models import Boutique,Cart,Follower
from rest_framework import  permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from random import randint
from produit.serializer import NotificationSerializer,FollowerSerializer
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView









class MyTokenObtainPairView(TokenObtainPairView):
	serializer_class=MyTokenObtainPairSerializer

class MyTokenRefreshPairView(TokenRefreshView):
	serializer_class=MyTokenObtainPairSerializer

class PhoneConfirmationRegistration(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		id=request.data.get('id')
		code_id=request.data.get('code_id')
		code=int(request.data.get('code'))
		confirm=CodeConfirmationPhone.objects.get(id=code_id)
		if confirm.code==code:
			user=User.objects.get(id=id)
			user.conform_phone=True
			user.active=True
			user.save()
			confirm.active=False
			confirm.save()
			Boutique.objects.create(user=user,note_vendeur=0)
			Cart.objects.create(proprietaire=user)
			Follower.objects.create(user=user)
			serializer=UserSerializer(user)
			return Response(serializer.data)



class GetUserChannel(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self,request):
		if request.user.is_authenticated:
			channel=request.user.channel
			return Response({'channel':channel})

class GetNotifications(APIView):
	def get(self,request):
		notifcationall=Notification.objects.filter(user=request.user,active=True).order_by('-id')
		notifynolu=Notification.objects.filter(user=request.user,lu=False).order_by('-id')
		serializerall=NotificationSerializer(notifcationall,many=True)
		serializernolu=NotificationSerializer(notifynolu,many=True)
		return Response({'notifcationall':serializerall.data,'notifynolu':serializernolu.data})


		
class RegistrationView(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self, request):
		data=request.data
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			user=serializer.save(conform_phone=False,active=False)
			code=randint(10000,99999)
			phoneconfir=CodeConfirmationPhone.objects.create(phone=user.phone,code=code,active=True)
			#Notification code numero
			return Response({'prenom':user.prenom,"nom":user.nom,
		'user_id':user.id,'code_id':phoneconfir.id})

		
class Authent(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self,request):
		if request.user.is_authenticated:
			return Response(True)
		else:
			return Response(False)

class GetNewUser(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		id=request.data.get('id')
		user=User.objects.get(id=id)
		serializer=UserSerializer(user)
		return Response(serializer.data)


class GetUser(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self,request):
		if request.user.is_authenticated:
			serializer=UserSerializer(request.user)
			return Response(serializer.data)
		return Response({'message':'unlogged'})

class IsvendeurActive(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self,request):
		if request.user.is_authenticated:
			vendeur=request.user
			if vendeur.active==True:
				return Response(True)
			return Response(False)
		return Response(False)


class ModificationCredential(ModelViewSet):
	queryset = User.objects.filter(active=True)
	serializer_class=UserSerializer
	@action(methods=["put"], detail=False, url_path='modif')
	def modif_cred(self,request,*args,**kwargs):
		user=self.request.user
		data=request.data
		user.nom=data['nom']
		user.phone=data['phone']
		user.prenom=data['prenom']
		user.save()
		return Response({'message':'donnee bien modifiee'})


class HandleNotif(ModelViewSet):
	queryset = Notification.objects.all()
	serializer_class=NotificationSerializer

	@action(methods=["put"], detail=False, url_path='handlenotif')
	def lunotif(self,request):
		user=self.request.user
		notification=Notification.objects.filter(user=user,lu=False)
		for n in notification:
			n.lu=True
			n.save()
		return Response({'message':'donnee bien modifiee'})
		


		
		
		
		


