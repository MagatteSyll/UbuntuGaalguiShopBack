from django.urls import path,include
from .views import*
from rest_framework.routers import SimpleRouter

router=SimpleRouter()
router.register('actionproduit',DeleteProduit)


urlpatterns=[
    path('',include(router.urls)),
    path('commande/',RechercheCommandes.as_view()),
    path('staf/',IsStaf.as_view()),
    path('annuler/',AnnulationCommande.as_view()),
    path('desactivationvendeur/',DesactiverVendeur.as_view()),
    path('rechercheproduit/',RechercheProduit.as_view()),
    path('depotcommande/',DepotCommande.as_view()),
    path('retraitcommande/',RetraitCommande.as_view()),
    path('annulationcommande/',CommandeAnnulation.as_view())
    





] 