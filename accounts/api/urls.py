from django.urls import path

from accounts.api.views import RegisterUserView

urlpatterns = [
    path('register-user/', RegisterUserView.as_view())
]
