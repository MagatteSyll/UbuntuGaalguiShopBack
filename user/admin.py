from django.contrib import admin
from .models import*




class UserAdmin(admin.ModelAdmin):
	list_display=['prenom', 'nom', 'phone', 'active',]
	search_fields=['prenom','nom', 'phone']
	class Meta:
		model=User

class PhoneConfirmationAdmin(admin.ModelAdmin):
	list_display=['phone', 'code']
	search_fields=['phone','code']
	class Meta:
		model=CodeConfirmationPhone

class NotificationAdmin(admin.ModelAdmin):
	list_display=['message', 'lu']
	search_fields=['message']
	class Meta:
		model=Notification


admin.site.register(User,UserAdmin)
admin.site.register(Notification,NotificationAdmin)
admin.site.register(CodeConfirmationPhone,PhoneConfirmationAdmin)