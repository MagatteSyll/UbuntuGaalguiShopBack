from django.urls import path,include
from .views import*
from rest_framework.routers import SimpleRouter



router=SimpleRouter()
router.register('modifcred',ModificationCredential)
router.register('handlenotify',HandleNotif)



urlpatterns=[
    path('',include(router.urls)),
    path('phonecodeconfirmation/',PhoneConfirmationRegistration.as_view()),
    path('registration/',RegistrationView.as_view()),
    path('connexion/',MyTokenObtainPairView.as_view()),
    path('token/refresh/', MyTokenRefreshPairView.as_view(), name='token_refresh'),
    path('isauthenticated/',Authent.as_view()),
    path('getuser/',GetUser.as_view()),
    path('isactive/',IsvendeurActive.as_view()),
    path('getchannel/',GetUserChannel.as_view()),
    path('getnotification/',GetNotifications.as_view()),
    path('getnewuser/',GetNewUser.as_view()),
     
    





]