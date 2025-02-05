# ESMEMarket - Système de Gestion des Ventes

## Description
ESMEMarket est une application Python conçue pour gérer et analyser les données commerciales d'une PME. Le système permet de charger, analyser et visualiser les données de ventes à partir de fichiers CSV.

## Structure du Projet
```
app_1/
├── data/                  # Dossier contenant les fichiers CSV
├── core/                  # Modules principaux
│   ├── data_loader.py    # Gestion du chargement des données
│   └── data_processor.py # Traitement des données
├── cli/                   # Interface utilisateur
│   └── interface.py      # Interface en ligne de commande
└── main.py               # Point d'entrée
```

## Fonctionnalités
1. **Gestion des Données**
   - Chargement de fichiers CSV
   - Validation et nettoyage des données
   - Gestion des lignes vides et valeurs manquantes

2. **Analyse des Ventes**
   - Affichage des ventes par date
   - Affichage des ventes par produit
   - Recherche avec filtres (quantité/prix)
   - Identification du produit le plus vendu
   - Calcul du chiffre d'affaires

3. **Analyse des Tendances**
   - Tendances mensuelles
   - Tendances horaires
   - Meilleures ventes par mois et par produit

4. **Modification des Données**
   - Modification d'entrées existantes
   - Ajout de nouvelles ventes
   - Sauvegarde des modifications

5. **Export des Analyses**
   - Génération de rapports détaillés
   - Export au format texte avec métadonnées
   - Ouverture automatique dans le bloc-notes

## Format des Données
Le système attend des fichiers CSV avec les colonnes suivantes :
- Order ID : Identifiant unique de la commande
- Product : Nom du produit
- Quantity Ordered : Quantité commandée
- Price Each : Prix unitaire
- Order Date : Date de la commande
- Purchase Address : Adresse d'achat

## Utilisation
1. Placez vos fichiers CSV dans le dossier `data/`
2. Exécutez l'application :
   ```bash
   python main.py
   ```
3. Utilisez le menu interactif pour accéder aux différentes fonctionnalités

## Prérequis
- Python 3.8+
- pandas
- numpy

## Notes Importantes
- Les fichiers CSV peuvent contenir des lignes vides qui seront automatiquement gérées
- L'analyse des tendances génère un fichier texte avec horodatage
- Les modifications sont sauvegardées dans un nouveau fichier pour préserver les données originales
