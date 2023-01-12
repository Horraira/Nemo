from django.urls import path
from . import views

app_name = 'Login'

urlpatterns = [
    path('', views.basePage, name="base"),
    path('login/', views.userLogin, name="login"),
    path('reg/userReg/', views.user_reg, name="userReg"),
    path('reg/adminReg/', views.admin_user_reg, name="adminReg"),
    path('reg/logout/', views.logout_user, name="logout"),
]
