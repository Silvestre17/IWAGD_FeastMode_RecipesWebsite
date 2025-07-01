from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve
from django.contrib.auth import views as auth_views

from . import views

app_name = 'recipe'
urlpatterns = [
    # Ficheiros do 'static' e 'media' quando 'DEBUG= False'
    # Fonte: https://stackoverflow.com/questions/73953475/request-media-files-in-django-when-the-debug-is-false
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    # Site - Home | Contactos
    path("", views.home, name="home"),

    # Contactos
    path('contactos/', views.contactos, name='contactos'),

    # User - Login | Logout | Registo | Perfil
    path("login/", views.login_page, name="login_page"),
    path('login-/', views.login_view, name="login"),
    path("registar/", views.registar_page, name="registar_page"),
    path("adicionar_registo/", views.adicionar_registo, name='adicionar_registo'),
    path('logout/', views.logout_view, name='logout'),

    path('perfil/<str:username>/', views.perfil, name='perfil'),
    path('perfil/<str:username>/editar', views.editar_perfil, name='editar_perfil'),
    path('perfil/<str:username>/editar_perfil_view', views.editar_perfil_view, name='editar_perfil_view'),

    # Receitas - Detalhes | Adicionar | Remover | Filtrar | Ingredientes | Comentário | Avaliação
    path('receitas/', views.receitas, name="receitas"),
    path('receitas/<str:categoria>/', views.mudar_categoria, name="mudar_categoria"),
    path('receitas/grau_dificuldade/<str:grau_dificuldade>/', views.mudar_grau_dificuldade, name='mudar_grau_dificuldade'),
    path('receitas/<str:categoria>/filtros/', views.receitas_filtros, name='receitas_filtros'),
    path('adicionar_receita/', views.adicionar_receita, name='adicionar_receita'),
    path('criar_receita/', views.criar_receita, name='criar_receita'),

    path('<str:receita_titulo>/editar_receita/', views.editar_receita, name='editar_receita'),
    path('editar_receita_view/<int:receita_id>', views.editar_receita_view, name='editar_receita_view'),
    path('remover_receita/<int:receita_id>/', views.remover_receita, name='remover_receita'),

    path('<str:receita_titulo>/', views.detalhe, name='detalhe'),
    path('<str:receita_titulo>/review/', views.review, name='review'),
]

# Ficheiros do 'static' e 'media' quando 'DEBUG=True'
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
