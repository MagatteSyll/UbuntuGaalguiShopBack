from rest_framework import serializers
from .models import*
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer




class UserSerializer(serializers.ModelSerializer):
	phone = PhoneNumberField()
	prenom= serializers.CharField()
	nom= serializers.CharField()
	password = serializers.CharField()
	class Meta:
		model=User
		fields="__all__"
		extra_kwargs = {'password': {'write_only': True}}


	def create(self, validated_data):
		password = validated_data.pop('password', None)
		instance = self.Meta.model(**validated_data)
		if password is not None:
			instance.set_password(password)
		instance.save()
		return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
    	if user.active==True and user.conform_phone==True:
    		token = super().get_token(user)
    		token['name'] = user.group
    		return token



		