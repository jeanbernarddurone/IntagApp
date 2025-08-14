# forms.py de ton application existante
from django import forms
from .models import ForumPost

from django import forms
from .models import ForumPost, ReponsePost

from django import forms
from .models import ForumPost, ReponsePost

class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ["titre", "contenu", "auteur"]
        widgets = {
            'contenu': forms.Textarea(attrs={'cols': 80, 'rows': 4, 'placeholder': 'Écrivez votre message ici...'}),
            'titre': forms.TextInput(attrs={'placeholder': 'Titre du message'}),
            'auteur': forms.TextInput(attrs={'placeholder': 'Votre nom'})
        }

class ReponsePostForm(forms.ModelForm):
    class Meta:
        model = ReponsePost
        fields = ["auteur", "contenu"]
        widgets = {
            'contenu': forms.Textarea(attrs={'cols': 80, 'rows': 4, 'placeholder': 'Écrivez votre réponse ici...'}),
            'auteur': forms.TextInput(attrs={'placeholder': 'Votre nom'})
        }


from .models import Donnee
class DonneeForm(forms.ModelForm):
    class Meta:
        model = Donnee
        fields = '__all__'
        exclude = ['latitude', 'longitude']
