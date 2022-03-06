from django.contrib import admin
from .models import*




class CategoryAdmin(admin.ModelAdmin):
	list_display=['category']
	search_fields=['category']
	class Meta:
		model=Category


class FollowerAdmin(admin.ModelAdmin):
	list_display=['id']
	search_fields=['id']
	class Meta:
		model=Follower

class RegionAdmin(admin.ModelAdmin):
	list_display=['region']
	search_fields=['region']
	class Meta:
		model=Region

class AdressAdmin(admin.ModelAdmin):
	list_display=['adress']
	search_fields=['adress']
	class Meta:
		model=Adress

class DeviseAdmin(admin.ModelAdmin):
	list_display=['devise']
	search_fields=['devise']
	class Meta:
		model=Devise


		

class BoutiqueAdmin(admin.ModelAdmin):
	list_display=['note_vendeur','id']
	search_fields=['note_vendeur']
	class Meta:
		model=Boutique

class ProduitAdmin(admin.ModelAdmin):
	list_display=['nom','prix','active','vendu']
	search_fields=['nom','prix']
	class Meta:
		model=Produit

class ProduitImageAdmin(admin.ModelAdmin):
	list_display=['id','active']
	class Meta:
		model=ProduitImage


class CartProductAdmin(admin.ModelAdmin):
	list_display=['quantity','subtotal']
	#search_fields=['product__nom']
	class Meta:
		model=CartProduct


class CartAdmin(admin.ModelAdmin):
	list_display=['total']
	#search_fields=['propri']
	class Meta:
		model=CartProduct


class CommandeAdmin(admin.ModelAdmin):
	list_display=['nom_client','phone','total']
	class Meta:
		model=Commande


admin.site.register(Category,CategoryAdmin)
admin.site.register(Follower,FollowerAdmin)
admin.site.register(Region,RegionAdmin)
admin.site.register(Adress,AdressAdmin)
admin.site.register(Produit,ProduitAdmin)
admin.site.register(CartProduct,CartProductAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Commande,CommandeAdmin)
admin.site.register(Boutique,BoutiqueAdmin)
admin.site.register(ProduitImage,ProduitImageAdmin)
admin.site.register(Devise,DeviseAdmin)



