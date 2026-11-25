from django.urls import path

from . import views

app_name = 'assistant'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('chat/', views.chat_view, name='chat'),
    path('api/chat/', views.chat_api_view, name='chat_api'),
    path('api/chat/clear/', views.clear_chat_api_view, name='clear_chat_api'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('guides/', views.guide_list_view, name='guide_list'),
    path('guides/<slug:slug>/', views.guide_detail_view, name='guide_detail'),
]
