
from django.contrib import admin
from django.urls import path
from .views import like_post, dislike_post
from. import views # ici cela import les views creer dans le file views, just .import puisqu'ils sont dans le meme folder
from .views import afficher_donnees_json
from .views import analyse_donnees
# pour afficher les chemins sur le site
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view),
    path('contact/',views.contact_view),
    path('actualite/',views.actualite_view),
    # path('cartocap/',views.cartocap_view),
    path('map/',views.map_view),
    path('forum/', views.forum_view, name='forum'),
    path('donnees/', views.donnees_view, name='donnees'), # fumulaire de collecte des données
    path('afficher-donnees/', views.afficher_donnees, name='afficher_donnees'),
    path('export-json/', afficher_donnees_json, name='export_json'),
    path('analyse/',views.analyse_donnees),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('dislike/<int:post_id>/', dislike_post, name='dislike_post'),
    path('repondre/<int:post_id>/', views.reponse_view, name='reponse'),
]


# http://127.0.0.1:8000/export-json/ je veux mettre ce lien pour telecharger les données sous format json