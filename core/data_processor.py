## core/data_processor.py
from pathlib import Path
from typing import Dict, Any
import pandas as pd

class DataProcessor:
    """
    @Description Classe responsable du traitement et de l'analyse des données de vente
    """

    def __init__(self, data: pd.DataFrame):
        """
        @Description Initialise le processeur de données

        @Params {data} : pd.DataFrame => DataFrame contenant les données de vente
        """
        self.data = data

    def get_sales_summary(self) -> pd.DataFrame:
        """
        @Description Calcule un résumé des ventes pour chaque produit

        @Return: pd.DataFrame => DataFrame contenant les statistiques de ventes par produit
        """
        sales_summary = self.data.groupby("Product").agg({
            "Quantity Ordered": ["sum", "count"],  # sum pour quantité totale, count pour nombre de commandes
            "Price Each": ["mean"]  # prix moyen unitaire
        }).round(2)

        ## Aplatir les colonnes multi-index
        sales_summary.columns = ["total_quantity", "number_of_orders", "average_price"]

        ## Calculer le revenu total
        sales_summary["total_revenue"] = (sales_summary["total_quantity"] * sales_summary["average_price"]).round(2)

        ## Trier par quantité totale vendue
        sales_summary = sales_summary.sort_values("total_quantity", ascending=False)

        return sales_summary

    def get_best_selling_product(self) -> Dict[str, Any]:
        """
        @Description Trouve le produit le plus vendu avec des statistiques détaillées

        @Return: Dict[str, Any] => Dictionnaire contenant les informations du produit le plus vendu
        """
        sales_summary = self.get_sales_summary()
        best_product = sales_summary.index[0]  ## Premier produit car déjà trié par quantité

        return {
            "product": best_product,
            "total_quantity": int(sales_summary.loc[best_product, "total_quantity"]),
            "number_of_orders": int(sales_summary.loc[best_product, "number_of_orders"]),
            "average_price": float(sales_summary.loc[best_product, "average_price"]),
            "total_revenue": float(sales_summary.loc[best_product, "total_revenue"]),
        }

    def get_sales_trends(self) -> Dict[str, pd.DataFrame]:
        """
        @Description Analyse les tendances de ventes selon différentes périodes

        @Return: Dict[str, pd.DataFrame] => Dictionnaire contenant les différentes analyses de tendances
        """
        ## Créer une copie des données
        df = self.data.copy()

        ## Extraire différentes composantes de date
        df['Year'] = df['Order Date'].dt.year
        df['Month'] = df['Order Date'].dt.month
        df['Day'] = df['Order Date'].dt.day
        df['Hour'] = df['Order Date'].dt.hour

        ## Tendances par mois
        monthly_trends = df.groupby(['Year', 'Month']).agg({
            'Order ID': 'count',  # Nombre de commandes
            'Quantity Ordered': 'sum',  # Quantité totale
            'Price Each': lambda x: (x * df.loc[x.index, 'Quantity Ordered']).sum()  # Revenu total
        }).round(2).reset_index()
        monthly_trends.columns = ['Year', 'Month', 'number_of_orders', 'total_quantity', 'total_revenue']

        ## Tendances par heure
        hourly_trends = df.groupby('Hour').agg({
            'Order ID': 'count',
            'Quantity Ordered': 'sum',
            'Price Each': lambda x: (x * df.loc[x.index, 'Quantity Ordered']).sum()
        }).round(2).reset_index()
        hourly_trends.columns = ['Hour', 'number_of_orders', 'total_quantity', 'total_revenue']

        ## Tendances par produit et par mois
        product_monthly_trends = df.groupby(['Year', 'Month', 'Product']).agg({
            'Quantity Ordered': 'sum',
            'Price Each': lambda x: (x * df.loc[x.index, 'Quantity Ordered']).sum()
        }).round(2)
        product_monthly_trends.columns = ['total_quantity', 'total_revenue']

        return {
            'monthly': monthly_trends,
            'hourly': hourly_trends,
            'product_monthly': product_monthly_trends
        }

    def get_sales_by_threshold(self, min_quantity: int = None, max_quantity: int = None, min_price: float = None, max_price: float = None) -> pd.DataFrame:
        """
        @Description Filtre les ventes selon des seuils de quantité et de prix

        @Params {min_quantity} : int => Quantité minimum (optionnel)
        @Params {max_quantity} : int => Quantité maximum (optionnel)
        @Params {min_price} : float => Prix minimum (optionnel)
        @Params {max_price} : float => Prix maximum (optionnel)
        @Return: pd.DataFrame => DataFrame filtré selon les critères
        """
        filtered_data = self.data.copy()

        if min_quantity is not None:
            filtered_data = filtered_data[filtered_data['Quantity Ordered'] >= min_quantity]
        if max_quantity is not None:
            filtered_data = filtered_data[filtered_data['Quantity Ordered'] <= max_quantity]
        if min_price is not None:
            filtered_data = filtered_data[filtered_data['Price Each'] >= min_price]
        if max_price is not None:
            filtered_data = filtered_data[filtered_data['Price Each'] <= max_price]

        return filtered_data

    def calculate_total_revenue(self, start_date: str = None, end_date: str = None) -> float:
        """
        @Description Calcule le chiffre d'affaires total pour une période donnée

        @Params {start_date} : str => Date de début au format YYYY-MM-DD (optionnel)
        @Params {end_date} : str => Date de fin au format YYYY-MM-DD (optionnel)
        @Return: float => Chiffre d'affaires total
        """
        filtered_data = self.data.copy()

        if start_date:
            filtered_data = filtered_data[filtered_data['Order Date'] >= pd.to_datetime(start_date)]
        if end_date:
            filtered_data = filtered_data[filtered_data['Order Date'] <= pd.to_datetime(end_date)]

        # Calculer le revenu total (quantité * prix pour chaque vente)
        revenue = (filtered_data['Quantity Ordered'] * filtered_data['Price Each']).sum()

        return round(revenue, 2)

    def modify_sales_entry(self, order_id: str, new_quantity = None, new_price = None, selected_index = None) -> bool:
        """
        @Description Modifie une entrée de vente existante

        @Params {order_id} : str => Identifiant de la commande
        @Params {new_quantity} : Any => Nouvelle quantité (optionnel)
        @Params {new_price} : Any => Nouveau prix (optionnel)
        @Params {selected_index} : Any => Index spécifique de l'entrée à modifier (optionnel)
        @Return: bool => True si la modification a réussi, False sinon
        """
        try:
            if selected_index is not None:
                # Vérifier que l'index existe et correspond au bon Order ID
                if selected_index not in self.data.index or self.data.loc[selected_index, 'Order ID'] != order_id:
                    return False

                if new_quantity:
                    self.data.loc[selected_index, 'Quantity Ordered'] = int(new_quantity)
                if new_price:
                    self.data.loc[selected_index, 'Price Each'] = float(new_price)
            else:
                # Comportement original pour la rétrocompatibilité
                mask = self.data['Order ID'] == order_id
                if not mask.any():
                    return False

                if new_quantity:
                    self.data.loc[mask, 'Quantity Ordered'] = int(new_quantity)
                if new_price:
                    self.data.loc[mask, 'Price Each'] = float(new_price)

            return True
        except Exception:
            return False

    def add_sales_entry(self, new_entry: pd.DataFrame) -> bool:
        """
        @Description Ajoute une nouvelle entrée de vente

        @Params {new_entry} : pd.DataFrame => Nouvelle entrée à ajouter
        @Return: bool => True si l'ajout a réussi, False sinon
        """
        try:
            self.data = pd.concat([self.data, new_entry], ignore_index=True)
            return True
        except Exception:
            return False

    def save_data(self, original_filename: str) -> str:
        """
        @Description Sauvegarde les données dans un fichier CSV avec le suffixe _updated | Si un fichier _updated existe déjà, il sera mis à jour.

        @Params {original_filename} : str => Nom du fichier original
        @Return: str => Nom du fichier de sauvegarde créé/mis à jour
        """
        try:
            # Extraire le nom de base du fichier sans extension
            base_name = Path(original_filename).stem
            if "_updated" not in base_name:
                base_name = f"{base_name}_updated"

            # Construire le chemin complet du fichier
            output_path = Path("data") / f"{base_name}.csv"

            # Sauvegarder les données
            self.data.to_csv(output_path, index=False)
            return str(output_path)

        except Exception as e:
            raise Exception(f"Erreur lors de la sauvegarde: {str(e)}")
