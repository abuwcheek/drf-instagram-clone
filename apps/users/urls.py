from django.urls import path

from rest_framework_simplejwt.views import (
     TokenObtainPairView,
     TokenRefreshView,
     )


urlpatterns = [
     # Token olish uchun
     path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),

     # Tokenni yangilash uchun
     path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]


urlpatterns += [
     
]