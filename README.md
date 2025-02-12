# ESMEMarket

ESMEMarket est une application Python conçue pour l'analyse et la gestion des données de vente. Elle offre à la fois une interface en ligne de commande (CLI) et une interface graphique (GUI) pour une expérience utilisateur flexible.

## 🌟 Fonctionnalités

- Chargement et validation de fichiers CSV de données de vente
- Analyse détaillée des ventes avec calcul de statistiques
- Visualisation des tendances de vente
- Filtrage des données par date, produit, et autres critères
- Modification et ajout de nouvelles entrées de vente
- Export des analyses au format texte
- Interface graphique moderne avec graphiques interactifs

## 📁 Structure du Projet

```
ESMEMarket/
├── data/                  # Dossier contenant les fichiers CSV
├── core/                  # Modules principaux
│   ├── data_loader.py     # Gestion du chargement des données
│   └── data_processor.py  # Traitement des données
├── cli/                   # Interface utilisateur
│   ├── console.py         # Interface en ligne de commande
│   └── interface.py       # Interface graphique
└── main.py                # Point d'entrée
```

## 🔧 Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/votre-username/ESMEMarket.git
cd ESMEMarket
```

2. Installez les dépendances requises :
```bash
pip install -r requirements.txt
```

## 📊 Format des Données

L'application attend des fichiers CSV avec les colonnes suivantes :
- `Order ID` : Identifiant unique de la commande
- `Product` : Nom du produit
- `Quantity Ordered` : Quantité commandée
- `Price Each` : Prix unitaire
- `Order Date` : Date de la commande
- `Purchase Address` : Adresse d'achat

## 🚀 Utilisation

### Interface en Ligne de Commande (CLI)

Lancez l'application en mode console :
```bash
python main.py --cli
```

Fonctionnalités disponibles :
1. Charger un fichier de données
2. Afficher les ventes pour une date
3. Afficher les ventes pour un produit
4. Rechercher par seuils (quantité/prix)
5. Trouver le produit le plus vendu
6. Calculer le chiffre d'affaires
7. Modifier une entrée
8. Ajouter une nouvelle vente
9. Analyser les tendances de ventes
0. Sauvegarder les modifications

### Interface Graphique (GUI)

Lancez l'application en mode graphique :
```bash
python main.py --gui
```

L'interface graphique offre :
- Un tableau de bord interactif
- Des graphiques de visualisation
- Des filtres dynamiques
- Export des analyses
- Gestion intuitive des données

## 📝 Documentation du Code

### Core

#### DataLoader (core/data_loader.py)
Gère le chargement et la validation des données CSV :
- Vérification du format des fichiers
- Gestion des valeurs manquantes
- Conversion des types de données
- Validation des colonnes requises

#### DataProcessor (core/data_processor.py)
Traite et analyse les données de vente :
- Calcul des statistiques de vente
- Analyse des tendances
- Filtrage des données
- Modification des entrées

### CLI

#### ConsoleCLI (cli/console.py)
Interface en ligne de commande avec :
- Menu interactif
- Gestion des commandes utilisateur
- Affichage formaté des résultats

#### InterfaceCLI (cli/interface.py)
Interface graphique moderne avec :
- Design responsive
- Graphiques interactifs
- Filtres dynamiques
- Export des analyses

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## ✨ Remerciements

- Merci à tous les contributeurs qui ont participé à ce projet
- Bibliothèques utilisées : pandas, matplotlib, tkinter

## 📞 Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Contactez l'équipe de développement
