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
    path('depotcommande/',DepotCommande.as_view()),
    path('retraitcommande/',RetraitCommande.as_view()),
    path('annulationcommande/',AnnulationCommande.as_view()),
    path('modificationcommande/',ModificationEtatCommande.as_view()),
    path('avertissement/',AvertirVendeur.as_view()),
    path('getboutique/',GetBoutique.as_view()),
    path('reactivationboutique/',ReactivationVendeur.as_view()),
    path('signaledeprobleme/',ProblemeTechnique.as_view()),
    path('getprobleme/',GetNotification.as_view()),





] 