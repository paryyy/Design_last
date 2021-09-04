from django.urls import path
from . import views

urlpatterns = [
    path('Home/', views.Home_page_view, name='Home'),
    path('Home/sieveTray/', views.sieveTray_view, name='sieveTray'),
    path('Home/packedtray/', views.packedTray_view, name='packedtray'),
    path('sieveTray', views.sieveTray_view, name='sieveTray')
]
