from django.urls import path
from . import views
app_name = 'board'
urlpatterns = [
    path('', views.art_index, name='art_index'),
    path('<int:artpk>/', views.art_detail, name='art_detail'),
    path('create/', views.create_art, name='create_art'),
    path('<int:artpk>/update/', views.update_art, name='update_art'),
    path('<int:artpk>/delete/', views.delete_art, name='delete_art'),
    path('vote/<int:artpk>/', views.vote_art, name='vote_art'),
    path('<int:artpk>/comment/', views.create_com, name='create_com'),
    path('<int:artpk>/comment/<int:reppk>/delete/', views.delete_com, name='delete_com'),
    path('<int:artpk>/comment/<int:reppk>/vote/', views.vote_com, name='vote_com'),

]
