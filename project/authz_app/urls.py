from django.urls import path
from . import views
from .views import RoleList, PermissionList
from django.contrib.auth import views as auth_views


app_name = 'authz'

urlpatterns = [
    path('', views.index_view, name='index'),  # Главная страница
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('deactivate-account/', views.deactivate_account, name='deactivate_account'),
    path('roles/', RoleList.as_view(), name='role-list'),
    path('permissions/', PermissionList.as_view(), name='permission-list'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]



