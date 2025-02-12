## core/data_loader.py
from typing import List
import pandas as pd
from pathlib import Path

class DataLoader:
    """
    @Description Classe responsable du chargement et de la validation des données CSV

    """
    def __init__(self):
        self.data = None

    def load_csv(self, file_path: str) -> pd.DataFrame:
        """
        @Description Charge un fichier CSV et valide son format

        @Params {file_path} : str => Chemin vers le fichier CSV
        @Return: pd.DataFrame => DataFrame contenant les données du CSV
        """
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")

        try:
            ## Lire le CSV en ignorant les lignes vides et en gérant les valeurs manquantes
            df = pd.read_csv(
                file_path,
                skip_blank_lines=True,  ## Ignore les lignes complètement vides
                na_values=['', 'nan', 'NaN', 'NULL'],  ## Valeurs considérées comme NaN
                keep_default_na=True
            )

            required_columns = ["Order ID", "Product", "Quantity Ordered","Price Each", "Order Date", "Purchase Address"]

            if not all(col in df.columns for col in required_columns):
                raise ValueError("Le CSV ne contient pas toutes les colonnes requises")

            ## Supprimer les lignes où toutes les colonnes sont NaN
            df = df.dropna(how='all')

            ## Supprimer les lignes avec des valeurs manquantes dans les colonnes essentielles
            essential_columns = ["Order ID", "Product", "Quantity Ordered", "Price Each"]
            df = df.dropna(subset=essential_columns)

            ## Conversion des types avec gestion des erreurs
            df["Quantity Ordered"] = pd.to_numeric(df["Quantity Ordered"], errors='coerce')
            df["Price Each"] = pd.to_numeric(df["Price Each"], errors='coerce')

            ## Convertir les dates en gérant les formats invalides
            df["Order Date"] = pd.to_datetime(df["Order Date"], format='mixed', errors='coerce')

            ## Supprimer les lignes avec des conversions échouées
            df = df.dropna(subset=["Quantity Ordered", "Price Each", "Order Date"])

            ## Convertir les quantités en entiers
            df["Quantity Ordered"] = df["Quantity Ordered"].astype(int)

            print(f"Données chargées : {len(df)} lignes valides sur {len(df) + df.isna().any(axis=1).sum()} lignes totales")

            self.data = df
            return df

        except Exception as e:
            raise Exception(f"Erreur lors du chargement du CSV: {str(e)}")

    def get_unique_products(self) -> List[str]:
        """
        @Description Récupère la liste des produits uniques

        @Return: List[str] => Liste des noms de produits uniques
        """
        if self.data is None:
            raise Exception("Aucune donnée n'a été chargée")
        return self.data["Product"].unique().tolist()

    def filter_by_date(self, date: str) -> pd.DataFrame:
        """
        @Description Filtre les données pour une date spécifique

        @Params {date} : str => Date au format YYYY-MM-DD
        @Return: pd.DataFrame => DataFrame filtré pour la date donnée
        """
        if self.data is None:
            raise Exception("Aucune donnée n'a été chargée")
        return self.data[self.data["Order Date"].dt.date == pd.to_datetime(date).date()]
