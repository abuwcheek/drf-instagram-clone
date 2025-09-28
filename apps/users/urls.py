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
                    UserProfileUpdateView, RequestDeleteProfileView, DeleteProfileUserView, ChangePasswordView, 
                    PasswordResetByUsernameView, PasswordResetConfirmView)



urlpatterns += [
     path('login-user', LogInUserView.as_view()),
     path('logout-user', LogoutUserView.as_view()),
     path('register-user', RegisterUserProfileView.as_view()),
     path('profile-user', UserProfileDataView.as_view()),
     path('update-profile-user', UserProfileUpdateView.as_view()),
     path('request-delete-profile', RequestDeleteProfileView.as_view()),
     path('delete-profile-user', DeleteProfileUserView.as_view()),
     path('change-password', ChangePasswordView.as_view()),
     path("password-reset/by-username/", PasswordResetByUsernameView.as_view()),
     path("password-reset/confirm/<str:uidb64>/<str:token>/", PasswordResetConfirmView.as_view()),
]