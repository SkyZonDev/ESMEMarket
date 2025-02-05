from typing import Any
from core.data_loader import DataLoader
from core.data_processor import DataProcessor
import os
from datetime import datetime
import pandas as pd

"""
@Description Interface en ligne de commande pour ESMEMarket
"""
class ConsoleCLI:
    def __init__(self):
        """
        @Description Initialise l'interface CLI
        """
        self.data_loader = DataLoader()
        self.data_processor = None
        self.current_file = None

    def display_menu(self) -> None:
        """
        @Description Affiche le menu principal
        """
        print("\n=== ESMEMarket - Dashboard1 ===")
        print("[1] Charger un fichier de données")
        print("[2] Afficher les ventes pour une date")
        print("[3] Afficher les ventes pour un produit")
        print("[4] Rechercher par seuils (quantité/prix)")
        print("[5] Trouver le produit le plus vendu")
        print("[6] Calculer le chiffre d'affaires")
        print("[7] Modifier une entrée")
        print("[8] Ajouter une nouvelle vente")
        print("[9] Analyser les tendances de ventes")
        print("[0] Sauvegarder les modifications")
        print("[E] Quitter")
    
    def export_analysis_to_file(self, analysis_type: str, data: Any) -> str:
        """
        @Description Exporte les résultats d'analyse dans un fichier texte

        @Params {analysis_type} : str => Type d'analyse effectuée
        @Params {data} : Any => Données à exporter
        @Return: str => Chemin du fichier créé
        """
        timestamp = datetime.now()
        filename = f"analysis_results_{analysis_type}_{timestamp.strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            # En-tête avec métadonnées
            f.write("=== Rapport d'analyse ESMEMarket ===\n")
            f.write(f"Date d'analyse: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Type d'analyse: {analysis_type}\n")
            if self.current_file:
                f.write(f"Fichier source: {self.current_file}\n")
            f.write("\n" + "="*50 + "\n\n")
            
            # Contenu de l'analyse
            if isinstance(data, pd.DataFrame):
                f.write(data.to_string())
            elif isinstance(data, dict):
                for key, value in data.items():
                    f.write(f"\n=== {key} ===\n")
                    if isinstance(value, pd.DataFrame):
                        f.write(value.to_string())
                    else:
                        f.write(str(value))
            else:
                f.write(str(data))
                
        return filename

    def analyze_sales_trends(self) -> None:
        """
        @Description Analyse et affiche les tendances de ventes
        """
        if not self._check_data_loaded():
            return
            
        print("\n=== Analyse des tendances de ventes ===")
        trends = self.data_processor.get_sales_trends()
        
        # Préparation du texte de l'analyse
        analysis_text = "ANALYSE DES TENDANCES DE VENTES\n\n"
        
        # Tendances mensuelles
        analysis_text += "=== Tendances mensuelles ===\n"
        analysis_text += trends['monthly'].to_string()
        analysis_text += "\n\n"
        
        # Tendances horaires
        analysis_text += "=== Tendances par heure ===\n"
        peak_hour = trends['hourly']['number_of_orders'].idxmax()
        analysis_text += f"Heure de pointe: {peak_hour}h avec {int(trends['hourly'].loc[peak_hour, 'number_of_orders'])} commandes\n"
        analysis_text += trends['hourly'].to_string()
        analysis_text += "\n\n"
        
        # Tendances par produit
        analysis_text += "=== Top produits par mois ===\n"
        monthly_best = trends['product_monthly'].groupby(['Year', 'Month'])['total_quantity'].idxmax()
        for (year, month), (_, _, product) in monthly_best.items():
            quantity = trends['product_monthly'].loc[(year, month, product), 'total_quantity']
            revenue = trends['product_monthly'].loc[(year, month, product), 'total_revenue']
            analysis_text += f"{year}-{month:02d}: {product} ({int(quantity)} unités, {revenue:.2f}€)\n"
        
        # Exporter l'analyse dans un fichier
        output_file = self.export_analysis_to_file("sales_trends", analysis_text)
        
        print(f"\nAnalyse exportée dans le fichier : {output_file}")
        
        # Ouvrir le fichier avec le bloc-notes
        try:
            if os.name == 'nt':  # Windows
                os.system(f'notepad.exe {output_file}')
            elif os.name == 'posix':  # macOS et Linux
                os.system(f'open {output_file}' if sys.platform == 'darwin' else f'xdg-open {output_file}')
        except Exception as e:
            print(f"\nErreur lors de l'ouverture du fichier: {str(e)}")
            print("Vous pouvez ouvrir le fichier manuellement.")

    def load_data(self) -> None:
        """
        @Description Charge un fichier CSV depuis le dossier data
        """
        print("\n=== Fichiers disponibles dans le dossier data ===")
        data_files = [f for f in os.listdir("data") if f.endswith('.csv')]
        
        for i, file in enumerate(data_files, 1):
            print(f"{i}. {file}")
            
        choice = input("\nChoisissez un fichier (numéro) : ")
        try:
            file_index = int(choice) - 1
            if 0 <= file_index < len(data_files):
                file_path = os.path.join("data", data_files[file_index])
                self.data_loader.load_csv(file_path)
                self.data_processor = DataProcessor(self.data_loader.data)
                self.current_file = file_path
                print(f"\nFichier {data_files[file_index]} chargé avec succès!")
            else:
                print("\nNuméro de fichier invalide!")
        except ValueError:
            print("\nEntrée invalide! Veuillez entrer un numéro.")

    def display_sales_by_date(self) -> None:
        """
        @Description Affiche les ventes pour une date donnée
        """
        if not self._check_data_loaded():
            return
            
        date_str = input("\nEntrez la date (YYYY-MM-DD) : ")
        try:
            filtered_data = self.data_loader.filter_by_date(date_str)
            if filtered_data.empty:
                print("\nAucune vente trouvée pour cette date.")
            else:
                print("\n=== Ventes pour la date", date_str, "===")
                print(filtered_data.to_string())
        except Exception as e:
            print(f"\nErreur: {str(e)}")

    def display_sales_by_product(self) -> None:
        """
        @Description Affiche les ventes pour un produit spécifique
        """
        if not self._check_data_loaded():
            return
            
        products = self.data_loader.get_unique_products()
        print("\n=== Produits disponibles ===")
        for i, product in enumerate(products, 1):
            print(f"{i}. {product}")
            
        choice = input("\nChoisissez un produit (numéro) : ")
        try:
            product_index = int(choice) - 1
            if 0 <= product_index < len(products):
                product = products[product_index]
                filtered_data = self.data_loader.data[self.data_loader.data["Product"] == product]
                print(f"\n=== Ventes pour {product} ===")
                print(filtered_data.to_string())
            else:
                print("\nNuméro de produit invalide!")
        except ValueError:
            print("\nEntrée invalide! Veuillez entrer un numéro.")

    def search_by_threshold(self) -> None:
        """
        @Description Recherche les ventes selon des seuils
        """
        if not self._check_data_loaded():
            return
            
        try:
            min_qty = input("\nQuantité minimum (Enter pour ignorer) : ")
            max_qty = input("Quantité maximum (Enter pour ignorer) : ")
            min_price = input("Prix minimum (Enter pour ignorer) : ")
            max_price = input("Prix maximum (Enter pour ignorer) : ")
            
            filtered_data = self.data_processor.get_sales_by_threshold(
                min_quantity=int(min_qty) if min_qty else None,
                max_quantity=int(max_qty) if max_qty else None,
                min_price=float(min_price) if min_price else None,
                max_price=float(max_price) if max_price else None
            )
            
            if filtered_data.empty:
                print("\nAucune vente ne correspond aux critères.")
            else:
                print("\n=== Résultats de la recherche ===")
                print(filtered_data.to_string())
        except ValueError:
            print("\nErreur: Veuillez entrer des nombres valides.")

    def find_best_selling_product(self) -> None:
        """
        @Description Affiche le produit le plus vendu et les statistiques de ventes
        """
        if not self._check_data_loaded():
            return
            
        print("\n=== Résumé des ventes par produit ===")
        sales_summary = self.data_processor.get_sales_summary()
        print("\nTop 5 des produits les plus vendus :")
        for product in sales_summary.head().index:
            stats = sales_summary.loc[product]
            print(f"\n{product}:")
            print(f"  - Quantité totale vendue: {int(stats['total_quantity'])}")
            print(f"  - Nombre de commandes: {int(stats['number_of_orders'])}")
            print(f"  - Prix moyen: {stats['average_price']:.2f} €")
            print(f"  - Chiffre d'affaires total: {stats['total_revenue']:.2f} €")
        
        print("\n=== Détails du produit le plus vendu ===")
        best_product = self.data_processor.get_best_selling_product()
        print(f"Produit: {best_product['product']}")
        print(f"Quantité totale vendue: {best_product['total_quantity']}")
        print(f"Nombre de commandes: {best_product['number_of_orders']}")
        print(f"Prix moyen: {best_product['average_price']:.2f} €")
        print(f"Chiffre d'affaires total: {best_product['total_revenue']:.2f} €")

    def calculate_revenue(self) -> None:
        """
        @Description Calcule et affiche le chiffre d'affaires
        """
        if not self._check_data_loaded():
            return
            
        start_date = input("\nDate de début (YYYY-MM-DD) ou Enter pour tout : ")
        end_date = input("Date de fin (YYYY-MM-DD) ou Enter pour tout : ")
        
        revenue = self.data_processor.calculate_total_revenue(
            start_date=start_date if start_date else None,
            end_date=end_date if end_date else None
        )
        
        print(f"\nChiffre d'affaires: {revenue:.2f} €")

    def modify_entry(self) -> None:
        """
        @Description Modifie une entrée existante
        """
        if not self._check_data_loaded():
            return
            
        order_id = input("\nEntrez l'Order ID à modifier : ")
        entry = self.data_loader.data[self.data_loader.data["Order ID"] == order_id]
        
        if entry.empty:
            print("\nOrder ID non trouvé!")
            return
            
        print("\nEntrée actuelle :")
        print(entry.to_string())
        
        try:
            new_quantity = input("\nNouvelle quantité (Enter pour ne pas modifier) : ")
            new_price = input("Nouveau prix (Enter pour ne pas modifier) : ")
            
            if new_quantity:
                self.data_loader.data.loc[self.data_loader.data["Order ID"] == order_id, "Quantity Ordered"] = int(new_quantity)
            if new_price:
                self.data_loader.data.loc[self.data_loader.data["Order ID"] == order_id, "Price Each"] = float(new_price)
                
            print("\nEntrée modifiée avec succès!")
        except ValueError:
            print("\nErreur: Valeurs invalides!")

    def add_new_sale(self) -> None:
        """
        @Description Ajoute une nouvelle vente
        """
        if not self._check_data_loaded():
            return
            
        try:
            print("\n=== Ajout d'une nouvelle vente ===")
            order_id = f"Order_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Affichage des produits existants
            products = self.data_loader.get_unique_products()
            print("\nProduits disponibles:")
            for i, product in enumerate(products, 1):
                print(f"{i}. {product}")
            
            product_choice = int(input("\nChoisissez un produit (numéro) : ")) - 1
            if not (0 <= product_choice < len(products)):
                print("\nNuméro de produit invalide!")
                return
                
            product = products[product_choice]
            quantity = int(input("Quantité : "))
            price = float(input("Prix unitaire : "))
            address = input("Adresse d'achat : ")
            
            new_sale = pd.DataFrame({
                "Order ID": [order_id],
                "Product": [product],
                "Quantity Ordered": [quantity],
                "Price Each": [price],
                "Order Date": [datetime.now()],
                "Purchase Address": [address]
            })
            
            self.data_loader.data = pd.concat([self.data_loader.data, new_sale], ignore_index=True)
            print("\nNouvelle vente ajoutée avec succès!")
            
        except ValueError:
            print("\nErreur: Valeurs invalides!")

    def save_modifications(self) -> None:
        """
        @Description Sauvegarde les modifications dans un nouveau fichier
        """
        if not self._check_data_loaded():
            return
            
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"data/sales_updated_{timestamp}.csv"
            self.data_loader.data.to_csv(new_filename, index=False)
            print(f"\nModifications sauvegardées dans : {new_filename}")
        except Exception as e:
            print(f"\nErreur lors de la sauvegarde: {str(e)}")

    def _check_data_loaded(self) -> bool:
        """
        @Description Vérifie si les données sont chargées

        @Return: bool => True si les données sont chargées, False sinon
        """
        if self.data_loader.data is None:
            print("\nErreur: Aucun fichier n'a été chargé! Veuillez d'abord charger un fichier.")
            return False
        return True

    def run(self) -> None:
        """
        @Description Lance l'interface CLI
        """
        while True:
            self.display_menu()
            choice = input("\nChoisissez une option (0-9) : ")
            
            if choice == "E":
                print("\nAu revoir!")
                break
            elif choice == "1":
                self.load_data()
            elif choice == "2":
                self.display_sales_by_date()
            elif choice == "3":
                self.display_sales_by_product()
            elif choice == "4":
                self.search_by_threshold()
            elif choice == "5":
                self.find_best_selling_product()
            elif choice == "6":
                self.calculate_revenue()
            elif choice == "7":
                self.modify_entry()
            elif choice == "8":
                self.add_new_sale()
            elif choice == "9":
                self.analyze_sales_trends()
            elif choice == "0":
                self.save_modifications()
            else:
                print("\nOption invalide! Veuillez choisir une option entre 0 et 9.")
