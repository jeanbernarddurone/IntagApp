
from django.http import HttpResponse
from django.shortcuts import render

def home_view(request):
   return render(request,'home.html')


def contact_view(request):
   return render(request,'contact.html')

def actualite_view(request):
   return render(request,'actualite.html')

def pdscap_view(request):
   return render(request,'pdscap.html')


###########################################
import folium
from django.shortcuts import render

from django.shortcuts import render
from .models import Donnee
import folium

def map_view(request):
    # Récupérer toutes les exploitations
    exploitations = Donnee.objects.all()

    # Récupérer les filtres depuis la requête GET
    niveau_etudes_filter = request.GET.get("niveau_etudes")
    capital_min = request.GET.get("capital_min", "")
    capital_max = request.GET.get("capital_max", "")

    # Appliquer le filtre par niveau d'études
    if niveau_etudes_filter:
        exploitations = exploitations.filter(Niveau_Education=niveau_etudes_filter)

    # Appliquer le filtre par capital financier
    if capital_min and capital_max:
        try:
            capital_min = float(capital_min)
            capital_max = float(capital_max)
            exploitations = exploitations.filter(
                Capital_Financier__gte=capital_min,
                Capital_Financier__lte=capital_max
            )
        except ValueError:
            pass  # Si la conversion échoue, ne rien faire

    # Créer la carte centrée sur le Québec
    m = folium.Map(location=[52.9399, -66.2900], zoom_start=6)

    # Ajouter les exploitations à la carte
    for exploitation in exploitations:
        if exploitation.latitude and exploitation.longitude:
            popup_content = f"""
                <b>{exploitation.nom}</b><br>
                Ville: {exploitation.ville}, {exploitation.Province}<br>
                Type: {exploitation.type_exploitation}<br>
                Surface cultivée: {exploitation.surface_cultivée} ha<br>
                Qualité du sol: {exploitation.qualité_sol}<br>
                Capital financier: {exploitation.Capital_Financier} $<br>
                Employés permanents: {exploitation.employés_permanents}<br>
                Employés temporaires: {exploitation.employés_temporaires}<br>
                Utilisation de Drone: {'Oui' if exploitation.utilise_Drone == '1' else 'Non'}<br>
                Utilisation de Capteur: {'Oui' if exploitation.utilise_Capteur == '1' else 'Non'}
            """
            folium.Marker(
                location=[exploitation.latitude, exploitation.longitude],
                popup=popup_content,
                icon=folium.Icon(color="green")
            ).add_to(m)

    # Convertir la carte en HTML
    map_html = m._repr_html_()

    return render(request, 'map.html', {
        'map_html': map_html,
        'niveau_etudes_filter': niveau_etudes_filter,
        'capital_min': capital_min,
        'capital_max': capital_max
    })




from django.shortcuts import render, get_object_or_404, redirect
from .models import ForumPost, ReponsePost
from .forms import ForumPostForm, ReponsePostForm

def forum_view(request):
    posts = ForumPost.objects.prefetch_related("reponses").all().order_by('-date_publication')
    form = ForumPostForm()

    # Gestion des likes et dislikes
    if request.method == "POST":
        # Si l'on clique sur "like" ou "dislike"
        if "like" in request.POST or "dislike" in request.POST:
            post_id = request.POST.get("post_id")
            post = get_object_or_404(ForumPost, id=post_id)
 
            if "like" in request.POST:
                post.likes += 1
            elif "dislike" in request.POST:
                post.dislikes += 1
            post.save()
            return redirect("forum")
        
        # Si la requête est pour une réponse
        elif "post_id" in request.POST:
            post = get_object_or_404(ForumPost, id=request.POST["post_id"])
            reponse_form = ReponsePostForm(request.POST)
            if reponse_form.is_valid():
                reponse = reponse_form.save(commit=False)
                reponse.post = post  # Associer la réponse au post
                reponse.save()
                return redirect("forum")  # Rafraîchir la page après soumission
        else:
            form = ForumPostForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("forum")  # Rediriger après avoir ajouté un post

    reponse_form = ReponsePostForm()
    return render(request, "forum.html", {"posts": posts, "form": form, "reponse_form": reponse_form})



def reponse_view(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    reponse_form = ReponsePostForm()

    if request.method == "POST":
        reponse_form = ReponsePostForm(request.POST)
        if reponse_form.is_valid():
            reponse = reponse_form.save(commit=False)
            reponse.post = post  # Associer la réponse au post
            reponse.save()
            return redirect("forum")  # Rediriger après soumission de la réponse

    return render(request, "reponse.html", {"post": post, "reponse_form": reponse_form})






# pour la collecte de données
from .models import Donnee
from .forms import DonneeForm

def donnees_view(request):
    if request.method == 'POST':
        form = DonneeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('donnees')  
    else:
        form = DonneeForm()

    donnees = Donnee.objects.all()
    return render(request, 'donnees.html', {'form': form})




from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import ForumPost

def like_post(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    post.likes += 1
    post.save()
    return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})

def dislike_post(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    post.dislikes += 1
    post.save()
    return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})






# afficher les données
from django.shortcuts import render
from .models import Donnee

def afficher_donnees(request):
    # Récupérer toutes les données
    donnees = Donnee.objects.all()

    # Passer les données au template
    return render(request, 'afficher_donnees.html', {'donnees': donnees})



import pandas as pd
from django.http import JsonResponse
from .models import Donnee

def afficher_donnees_json(request):
    # Récupérer les données
    donnees = Donnee.objects.all()
    
    # Transformer en liste de dictionnaires
    data_list = list(donnees.values())
    
    # Transformer en DataFrame (si nécessaire)
    df = pd.DataFrame(data_list)
    
    # Retourner en JSON
    return JsonResponse(data_list, safe=False)





import pandas as pd
import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render
from .models import Donnee

def analyse_donnees(request):
    # Récupérer toutes les données
    donnees = Donnee.objects.all()
    
    # Nombre d'exploitations
    nombre_exploitations = donnees.count()

    # Convertir les données en DataFrame pour analyses
    data_list = list(donnees.values())
    df = pd.DataFrame(data_list)

    # Calculer les statistiques descriptives
    stats = df.describe()

    # # Création du graphique (Histogramme)
    # plt.figure(figsize=(8, 5))
    # df["Capital_Financier"].hist(bins=20, color='skyblue', edgecolor='black')
    # plt.xlabel("Capital Financier")
    # plt.ylabel("Nombre d'exploitations")
    # plt.title("Répartition du Capital Financier")

    # # Sauvegarder l'image en mémoire
    # buffer = io.BytesIO()
    # plt.savefig(buffer, format='png')
    # buffer.seek(0)
    # image_png = buffer.getvalue()
    # buffer.close()

    # # Convertir en base64
    # graphique = base64.b64encode(image_png).decode('utf-8')
    # image_uri = f"data:image/png;base64,{graphique}"

    return render(request, 'analyse.html', {
        'stats': stats.to_html(),
        #'image_uri': image_uri,
        'nombre_exploitations': nombre_exploitations
    })