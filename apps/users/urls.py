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



from .views import (LogInUserView, LogoutUserView,  RegisterUserProfileView, UserProfileDataView,
                    UserProfileUpdateView, )


urlpatterns += [
     path('login-user', LogInUserView.as_view()),
     path('logout-user', LogoutUserView.as_view()),
     path('register-user', RegisterUserProfileView.as_view()),
     path('profile-user', UserProfileDataView.as_view()),
     path('update-profile-user', UserProfileUpdateView.as_view()),
]