from django.db import models
from user.models import User


class ActionStaff(models.Model):
	identifiant=models.ForeignKey(User,on_delete=models.CASCADE)
	action=models.TextField()

	def __str__(self):
		return self.identifiant.prenom

