from django.urls import path

from accounts.api.views import RegisterUserView, BlackListTokenView

urlpatterns = [
    path('register-user/', RegisterUserView.as_view()),
    path('logout/', BlackListTokenView.as_view(), name='token_blacklist'),
]
