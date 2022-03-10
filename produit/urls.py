from django.urls import path,include
from .views import*
from rest_framework.routers import SimpleRouter



router=SimpleRouter()
router.register('cartmanage',CartProductDeleteSingle)
router.register('produitmanage',Manageproduit)
router.register('produitimgmanage',ManageProduitImage)
router.register('rating',NoteVendeur)
router.register('commandemanage', RemoveCommande)
router.register('follower', RemoveFollower)
router.register('actioncommande',AnnulationCommande)




urlpatterns=[
    path('',include(router.urls)),
    path('region/',RegionList.as_view()),
    path('category/',CategoryList.as_view()),
   # path('vendeur/',IsVendeur.as_view()),
    path('addcart/',AddCartView.as_view()),
    path('cartview/',CartView.as_view()),
    path('ajout/',AjoutProduit.as_view()),
    path('ajoutunique/',AjoutSansVariation.as_view()),
    path('getcart/',GetPanier.as_view()),
    path('adress/',AdressList.as_view()),
    path('commande/',PostCommande.as_view()),
    path('mesproduits/',MesProduits.as_view()),
    path('produitvendu/',MesProduitsVendu.as_view()),
    path('produitvenduvuclient/',ProduitVenduVendeur.as_view()),
    path('devise/',Getdevise.as_view()),
    path('imageproduit/',ImageDunProduit.as_view()),
    path('newproduitimage/',AjoutProduitImage.as_view()),
    path('getproduitimg/',AllImageProduit.as_view()),
    path('maboutique/',BoutiqueView.as_view()),
    path('profilboutiquevuclient/',BoutiqueVuClient.as_view()),
    path('editboutiquepic/',EditBoutiquePic.as_view()),
    path('editboutiquedes/',EditBoutiqueDes.as_view()),
    path('produitpercategory/',DisplayPerCategory.as_view()),
    path('singleproduit/',GetProduit.as_view()),
    path('historiquevente/',ProdutVendu.as_view()),
    path('historiquedachat/',ProduitAchete.as_view()),
    path('commandeencours/',CommandeEnCours.as_view()),
    path('produitactif/',ProduitActifVendeur.as_view()),
    path('profilevendeur/',ProfileVendeur.as_view()),
    path('activationcommande/',ActivationCommande.as_view()),
    path('actifvendeur/',ActifVendeur.as_view()),
    path('getvendeur/',GetVendeur.as_view()),
    path('search/',ProduitSearch.as_view()),
   # path('getcartproduct/',GetCartProduct.as_view()),
   # path('vuvendeur/',VueVendeur.as_view()),
    #path('shopvendeur/',ShopVendeur.as_view()),
    path('nosvendeur/',NosVendeurs.as_view()),
    path('produitoccasion/',Occasions.as_view()),
    path('reactivationproduit/',ReactivationProduit.as_view()),
    path('cartcommande/',GetCartCommande.as_view()),
    path('calculivraison/',CalculLivraison.as_view()),
    path('getcommande/',GetCommande.as_view()),
    path('getnotification/',NotificationDetail.as_view()),
    path('addfollower/',AddFollower.as_view()),
    path('isabon/',VeriFollower.as_view()),
    path('commandepay/',CommandePay.as_view()),
    path('confirmationpaycommande/',ConfirmationPayCommande.as_view()),


    

    


    ]



   
