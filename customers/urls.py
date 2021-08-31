from django.urls import path

from .views import(
    registerPageRest,
)

app_name = "account"

urlpatterns = [
    path('register/', registerPageRest, name='register_rest'),
    # path('login/', obtain_auth_token, name='login'),
]