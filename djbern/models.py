from django.db import models

class ForumPost(models.Model):
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    auteur = models.CharField(max_length=255)
    date_publication = models.DateTimeField(auto_now_add=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.titre


class ReponsePost(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name="reponses", null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="sous_reponses", null=True, blank=True)
    auteur = models.CharField(max_length=255)
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Réponse de {self.auteur} sur {self.post.titre if self.post else 'réponse à une réponse'}"

    


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import requests  

class Donnee(models.Model):
    nom = models.CharField(max_length=255)
    Age = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    code_postal = models.CharField(max_length=10, default="000000") 
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    Niveau_Education = models.CharField(
        max_length=50,
        choices=[
            ("Aucune","Aucune"), 
            ("Primaire","Primaire"), 
            ("Bac","Bac"), 
            ("Licence", "Licence"),
            ("Matrice", "Matrice"),
            ("PhD", "PhD")])
    
    ville = models.CharField(max_length=255)
    Province = models.CharField(
        max_length=50,
        choices=[
            ("Alberta","Alberta"),
            ("Colombie-Britannique","Colombie-Britannique"),
            ("Île-du-Prince-Édouard","Île-du-Prince-Édouard"),
            ("Manitoba","Manitoba"),
            ("Nouveau-Brunswick","Nouveau-Brunswick"),
            ("Nouvelle-Écosse","Nouvelle-Écosse"),
            ("Nunavut","Nunavut"),
            ("Ontario","Ontario"),
            ("Québec","Québec"),
            ("Saskatchewan","Saskatchewan"),
            ("Terre-Neuve-et-Labrador","Terre-Neuve-et-Labrador"),
            ("Territoires du Nord-Ouest","Territoires du Nord-Ouest"),
            ("Yukon","Yukon")])
    


    type_exploitation = models.CharField(
        max_length=50,
        choices=[
            ("Culture", "Culture"), 
            ("Élevage", "Élevage"), 
            ("Mixte", "Mixte"), 
            ("Autre", "Autre")] )
    
    type_Culture = models.CharField(max_length=255)
    
    Elvage= models.CharField(
        max_length=50,
        choices=[
            ("Aucune","Aucune"),
            ("Bovin","Bovin"),
            ("Caprin","Caprin"),    
            ("Ovin","Ovin"),
            ("Volaille","Volaille"),
            ("Equin","Equin"),  
            ("Autre","Autre"),   
            ])
    
    Autre_Elevage = models.CharField(max_length=255)
    Effective_Elevage= models.IntegerField(validators=[MinValueValidator(0)], default=0)
        # Capital physique
    surface_Exploitation = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    surface_cultivée = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    surface_irriguée = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    qualité_sol = models.CharField(
        max_length=50,
        choices=[
        ("Pauvre","Pauvre"),
        ("Moyen","Moyen"),
        ("Bon","Bon"),
        ("Très bon","Très bon")
])

    # Capital humain
    employés_permanents = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    employés_temporaires = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    employé_avec_competence_NTIC = models.CharField(
        max_length=50,
        choices=[
            ("1", "Oui"), 
            ("2", "Non")])



    # Capital financier
    Capital_Financier = models.DecimalField(max_digits=15, decimal_places=2,default=0)


    # Capital social
    Membre_association= models.CharField(
        max_length=50,
        choices=[
            ("1", "Oui"), 
            ("2", "Non")])

    # Capital technologique
    utilise_Drone = models.CharField(
        max_length=50,
        choices=[
            ("1", "Oui"), 
            ("2", "Non")])
    
    utilise_Capteur= models.CharField(
        max_length=50,
        choices=[
            ("1", "Oui"), 
            ("2", "Non")])
    
    utilise_tracteur_connecté= models.CharField(
        max_length=50,
        choices=[
            ("1", "Oui"), 
            ("2", "Non")])
    
    utilise_autre_NTIC= models.CharField(
        max_length=50,
        choices=[
            ("1", "Oui"), 
            ("2", "Non")])
    def __str__(self):
        return f"{self.nom} - {self.ville}"

    def geolocaliser_par_code_postal(self):
        # API de géolocalisation OpenCage
        api_key = "2ac144d0466a4565a3c280232a5b094a"
        url = f"https://api.opencagedata.com/geocode/v1/json?q={self.code_postal}&key={api_key}"
        
        response = requests.get(url).json()
        if response['results']:
            latitude = response['results'][0]['geometry']['lat']
            longitude = response['results'][0]['geometry']['lng']
            self.latitude = latitude
            self.longitude = longitude
        else:
            self.latitude = None
            self.longitude = None

    def save(self, *args, **kwargs):
        # Avant de sauvegarder, remplir automatiquement latitude et longitude
        self.geolocaliser_par_code_postal()
        super(Donnee, self).save(*args, **kwargs)















# class Donnee(models.Model):
#     nom = models.CharField(max_length=255)
#     code_postal = models.CharField(max_length=10)  # Ajout pour la localisation
#     latitude = models.FloatField(blank=True, null=True)
#     longitude = models.FloatField(blank=True, null=True)
    
#     localisation = models.CharField(max_length=255)
#     type_exploitation = models.CharField(
#         max_length=50,
#         choices=[
#             ("Culture", "Culture"), 
#             ("Élevage", "Élevage"), 
#             ("Mixte", "Mixte"), 
#             ("Autre", "Autre")
#         ]
#     )

#     # Capital humain
#     employes_permanents = models.IntegerField(validators=[MinValueValidator(0)], default=0)
#     employes_temporaires = models.IntegerField(validators=[MinValueValidator(0)], default=0)
#     heures_travail_semaine = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(168)], default=0)

#     # Capital physique
#     valeur_materiel_agricole = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
#     surface_cultivee = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

#     # Capital financier
#     fonds_disponibles = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
#     pret_bancaire = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])

#     # Capital naturel
#     surface_irriguee = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
#     qualite_sol = models.IntegerField(choices=[
#         (1, "Très pauvre"),
#         (2, "Pauvre"),
#         (3, "Moyen"),
#         (4, "Bon"),
#         (5, "Très bon")
#     ])

#     # Capital social
#     nb_associations = models.IntegerField(validators=[MinValueValidator(0)], default=0)

#     # Capital technologique
#     utilise_technologie = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.nom} - {self.localisation}"

    

   # pour la migration
   # python manage.py makemigrations
   # python manage.py migrate
   # python manage.py runserver
