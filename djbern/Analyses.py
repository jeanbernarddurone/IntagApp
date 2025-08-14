# Analyses.py

import pandas as pd

def get_exploitations():
    # Exemple de données d'exploitations agricoles avec 10 exploitations
    data = {
        'Nom': ['Exploit1', 'Exploit2', 'Exploit3', 'Exploit4', 'Exploit5', 'Exploit6', 'Exploit7', 'Exploit8', 'Exploit9', 'Exploit10'],
        'Surface': [150, 200, 50, 120, 180, 90, 160, 300, 220, 110],
        'ChiffreAffaire': [100000, 200000, 50000, 120000, 150000, 90000, 180000, 250000, 300000, 110000],
        'NiveauEtudes': ['Bac', 'Maitrise', 'Doctorat', 'Bac', 'Maitrise', 'Doctorat', 'Bac', 'Maitrise', 'Doctorat', 'Bac'],
        'Latitude': [45.4215, 45.5096, 45.3984, 45.4165, 45.4235, 45.5200, 45.4945, 45.4500, 45.4785, 45.4900],
        'Longitude': [-75.6972, -73.6143, -74.0074, -75.6791, -75.6873, -73.6300, -74.0034, -75.7054, -74.0856, -75.6942],
    }

    df = pd.DataFrame(data)
    return df

