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

        # Aplatir les colonnes multi-index
        sales_summary.columns = ["total_quantity", "number_of_orders", "average_price"]
        
        # Calculer le revenu total
        sales_summary["total_revenue"] = (sales_summary["total_quantity"] * 
                                        sales_summary["average_price"]).round(2)
        
        # Trier par quantité totale vendue
        sales_summary = sales_summary.sort_values("total_quantity", ascending=False)
        
        return sales_summary

    def get_best_selling_product(self) -> Dict[str, Any]:
        """
        @Description Trouve le produit le plus vendu avec des statistiques détaillées

        @Return: Dict[str, Any] => Dictionnaire contenant les informations du produit le plus vendu
        """
        sales_summary = self.get_sales_summary()
        best_product = sales_summary.index[0]  # Premier produit car déjà trié par quantité
        
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
        # Créer une copie des données
        df = self.data.copy()
        
        # Extraire différentes composantes de date
        df['Year'] = df['Order Date'].dt.year
        df['Month'] = df['Order Date'].dt.month
        df['Day'] = df['Order Date'].dt.day
        df['Hour'] = df['Order Date'].dt.hour
        
        # Tendances par mois
        monthly_trends = df.groupby(['Year', 'Month']).agg({
            'Order ID': 'count',  # Nombre de commandes
            'Quantity Ordered': 'sum',  # Quantité totale
            'Price Each': lambda x: (x * df.loc[x.index, 'Quantity Ordered']).sum()  # Revenu total
        }).round(2).reset_index()
        monthly_trends.columns = ['Year', 'Month', 'number_of_orders', 'total_quantity', 'total_revenue']
        
        # Tendances par heure
        hourly_trends = df.groupby('Hour').agg({
            'Order ID': 'count',
            'Quantity Ordered': 'sum',
            'Price Each': lambda x: (x * df.loc[x.index, 'Quantity Ordered']).sum()
        }).round(2).reset_index()
        hourly_trends.columns = ['Hour', 'number_of_orders', 'total_quantity', 'total_revenue']
        
        # Tendances par produit et par mois
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
