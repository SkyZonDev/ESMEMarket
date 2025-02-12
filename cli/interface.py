import tkinter as tk
import os
import webbrowser
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk, messagebox, filedialog
from core.data_loader import DataLoader
from core.data_processor import DataProcessor

class ModernFrame(ttk.Frame):
    """
    @Description: Frame personnalisé avec style moderne
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        style = ttk.Style()
        style.configure('Modern.TFrame', background='#f0f0f0')
        self['style'] = 'Modern.TFrame'

class InterfaceCLI:
    """
    @Description: Interface graphique moderne pour l'application ESMEMarket
    """
    def __init__(self):
        icon_path = "assets/icon.ico"
        self.window = tk.Tk()
        self.window.title("ESMEMarket - Tableau de Bord")
        self.window.iconbitmap(icon_path)
        self.window.geometry("1920x1080")
        self.window.configure(bg='#f0f0f0')

        # Initialisation des classes de données
        self.data_loader = DataLoader()
        self.data_processor = None
        self.current_df = None

        # Variables pour les filtres
        self.date_var = tk.StringVar()
        self.product_var = tk.StringVar()

        # Configuration du style
        self._configure_styles()

        # Création de l'interface
        self._create_menu()
        self._create_main_layout()

    def _configure_styles(self):
        """
        @Description: Configure les styles personnalisés pour l'interface
        """
        style = ttk.Style()
        style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
        style.configure('Stats.TLabel', font=('Helvetica', 10))
        style.configure('Title.TLabel', font=('Helvetica', 14, 'bold'))

    def _create_menu(self):
        """
        @Description: Crée le menu principal
        """
        menubar = tk.Menu(self.window)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Charger CSV", command=self._load_csv)
        file_menu.add_command(label="Exporter Analyse", command=self._export_analysis)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.window.quit)
        menubar.add_cascade(label="Fichier", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Documentation", command=self._show_documentation)
        help_menu.add_command(label="À propos", command=self._show_about)
        help_menu.add_separator()
        help_menu.add_command(label="Crédit", command=self._show_credit)
        menubar.add_cascade(label="Aide", menu=help_menu)

        self.window.config(menu=menubar)

    def _create_main_layout(self):
        """
        @Description: Crée la mise en page principale avec un design moderne
        """
        self.main_container = ModernFrame(self.window, padding="10")
        self.main_container.grid(row=0, column=0, sticky="nsew")

        self._create_header()

        self._create_filters()

        self._create_data_section()
        self._create_analysis_section()

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

    def _create_header(self):
        """
        @Description: Crée l'en-tête de l'application
        """
        header = ModernFrame(self.main_container, padding="5")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        title = ttk.Label(header, text="ESMEMarket - Tableau de bord", style='Title.TLabel')
        title.grid(row=0, column=0, padx=5, pady=5)

        self.file_info = ttk.Label(header, text="Aucun fichier chargé", style='Stats.TLabel')
        self.file_info.grid(row=1, column=0, padx=5)

        btn_frame = ttk.Frame(header)
        btn_frame.grid(row=0, column=1, rowspan=2, sticky="e")

        ttk.Button(btn_frame, text="Charger CSV", command=self._load_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Exporter Analyse", command=self._export_analysis).pack(side=tk.LEFT, padx=5)

    def _create_filters(self):
        """
        @Description: Crée la section des filtres
        """
        filter_frame = ModernFrame(self.main_container, padding="5")
        filter_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # Titre des filtres
        ttk.Label(filter_frame, text="Filtres", style='Header.TLabel').grid(row=0, column=0, sticky="w", pady=(0, 5))

        # Filtre par date
        ttk.Label(filter_frame, text="Date:").grid(row=1, column=0, padx=5)
        self.date_entry = ttk.Entry(filter_frame, textvariable=self.date_var)
        self.date_entry.grid(row=1, column=1, padx=5)
        ttk.Label(filter_frame, text="(YYYY-MM-DD)").grid(row=1, column=2, padx=5)

        # Filtre par produit
        ttk.Label(filter_frame, text="Produit:").grid(row=1, column=3, padx=5)
        self.product_combo = ttk.Combobox(filter_frame, textvariable=self.product_var)
        self.product_combo.grid(row=1, column=4, padx=5)

        # Bouton d'application des filtres
        ttk.Button(filter_frame, text="Appliquer Filtres", command=self._apply_filters).grid(row=1, column=5, padx=5)
        ttk.Button(filter_frame, text="Réinitialiser", command=self._reset_filters).grid(row=1, column=6, padx=5)

    def _create_data_section(self):
        """
        @Description: Crée la section de visualisation des données
        """
        data_frame = ModernFrame(self.main_container, padding="5")
        data_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 5))

        # Titre de la section
        ttk.Label(data_frame, text="Données", style='Header.TLabel').grid(row=0, column=0, sticky="w", pady=(0, 5))

        # Tableau de données
        self.tree = ttk.Treeview(data_frame, selectmode='browse', height=20)
        self.tree.grid(row=1, column=0, sticky="nsew")

        # Scrollbars
        vsb = ttk.Scrollbar(data_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=1, column=1, sticky="ns")
        hsb = ttk.Scrollbar(data_frame, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=2, column=0, sticky="ew")

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    def _create_analysis_section(self):
        """
        @Description: Crée la section d'analyse avec graphiques
        """
        analysis_frame = ModernFrame(self.main_container, padding="5")
        analysis_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 0))

        # Configure grid weights for analysis_frame
        analysis_frame.grid_rowconfigure(1, weight=1)
        analysis_frame.grid_columnconfigure(0, weight=1)

        # Titre de la section
        ttk.Label(analysis_frame, text="Analyse", style='Header.TLabel').grid(row=0, column=0, sticky="w", pady=(0, 5))

        # Notebook pour les différentes vues d'analyse
        self.notebook = ttk.Notebook(analysis_frame)
        self.notebook.grid(row=1, column=0, sticky="nsew")

        # Onglets d'analyse
        self.summary_tab = ModernFrame(self.notebook, padding="5")
        self.trends_tab = ModernFrame(self.notebook, padding="5")
        self.products_tab = ModernFrame(self.notebook, padding="5")

        self.notebook.add(self.summary_tab, text="Résumé")
        self.notebook.add(self.trends_tab, text="Tendances")
        self.notebook.add(self.products_tab, text="Produits")

        # Initialisation des figures et canvas
        self.summary_fig = Figure(figsize=(6, 4), dpi=100)
        self.trends_fig = Figure(figsize=(6, 4), dpi=100)
        self.products_fig = Figure(figsize=(6, 4), dpi=100)

        self.summary_canvas = FigureCanvasTkAgg(self.summary_fig, master=self.summary_tab)
        self.trends_canvas = FigureCanvasTkAgg(self.trends_fig, master=self.trends_tab)
        self.products_canvas = FigureCanvasTkAgg(self.products_fig, master=self.products_tab)

        self.summary_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.trends_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.products_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _load_csv(self):
        """
        @Description: Charge un fichier CSV et met à jour l'interface
        """
        try:
            filename = filedialog.askopenfilename(
                title="Sélectionner un fichier CSV",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )

            if filename:
                # Chargement des données
                df = self.data_loader.load_csv(filename)
                self.data_processor = DataProcessor(df)

                # Mise à jour de l'interface
                self._update_file_info(filename)
                self._update_data_table(df)
                self._update_analysis()

                messagebox.showinfo("Succès", f"Fichier chargé avec succès\n{len(df)} lignes valides")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement: {str(e)}")

    def _update_file_info(self, filename):
        """
        @Description: Met à jour les informations sur le fichier chargé
        """
        file_info = f"Fichier: {os.path.basename(filename)}"
        self.file_info.config(text=file_info)

    def _update_data_table(self, df):
        """
        @Description: Met à jour le tableau de données
        """
        # Réinitialiser le tableau
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Configurer les colonnes
        self.tree['columns'] = list(df.columns)
        self.tree['show'] = 'headings'

        for column in df.columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=100)

        # Ajouter les données
        for _, row in df.head(1000).iterrows():  # Limiter à 1000 lignes pour la performance
            self.tree.insert("", "end", values=list(row))

    def _update_analysis(self):
        """
        @Description: Met à jour les analyses et graphiques
        """
        if self.data_processor:
            # Récupérer les données d'analyse
            sales_summary = self.data_processor.get_sales_summary()
            best_seller = self.data_processor.get_best_selling_product()
            trends = self.data_processor.get_sales_trends()

            # Mettre à jour les graphiques
            self._update_summary_graph(sales_summary)
            self._update_trends_graph(trends)
            self._update_products_analysis(sales_summary)

    def _update_analysis(self):
        """
        @Description: Met à jour les analyses et graphiques
        """
        if self.data_processor:
            # Récupérer les données d'analyse
            sales_summary = self.data_processor.get_sales_summary()
            trends = self.data_processor.get_sales_trends()

            # Mettre à jour les graphiques
            self._update_summary_graph(sales_summary)
            self._update_trends_graph()
            self._update_products_graph(sales_summary)

    def _update_summary_graph(self, sales_summary):
        """
        @Description: Met à jour le graphique de résumé
        """
        self.summary_fig.clear()
        ax = self.summary_fig.add_subplot(111)

        # Créer un graphique à barres des meilleures ventes
        sales_summary.head(10)['total_quantity'].plot(kind='bar', ax=ax)
        ax.set_title('Top 10 des Produits les Plus Vendus')
        ax.set_xlabel('Produit')
        ax.set_ylabel('Quantité Vendue')
        plt.xticks(rotation=45)

        self.summary_fig.tight_layout()
        self.summary_canvas.draw()

    def _update_filters(self):
        """
        @Description: Met à jour les options des filtres
        """
        if self.current_df is not None:
            # Mise à jour des produits disponibles
            products = self.current_df['Product'].unique().tolist()
            self.product_combo['values'] = [''] + products

            # Réinitialisation des valeurs
            self.date_var.set('')
            self.product_var.set('')

    def _apply_filters(self):
        """
        @Description: Applique les filtres sélectionnés
        """
        if self.current_df is None:
            return

        filtered_df = self.current_df.copy()

        # Filtre par date
        date_filter = self.date_var.get()
        if date_filter:
            try:
                date = pd.to_datetime(date_filter).date()
                filtered_df = filtered_df[filtered_df['Order Date'].dt.date == date]
            except ValueError:
                messagebox.showerror("Erreur", "Format de date invalide")
                return

        # Filtre par produit
        product_filter = self.product_var.get()
        if product_filter:
            filtered_df = filtered_df[filtered_df['Product'] == product_filter]

        # Mise à jour de l'affichage
        self._update_data_table(filtered_df)
        self.data_processor = DataProcessor(filtered_df)
        self._update_analysis()

    def _reset_filters(self):
        """
        @Description: Réinitialise tous les filtres
        """
        self.date_var.set('')
        self.product_var.set('')
        if self.current_df is not None:
            self._update_data_table(self.current_df)
            self.data_processor = DataProcessor(self.current_df)
            self._update_analysis()

    def _update_trends_graph(self, event=None):
        """
        @Description: Met à jour le graphique des tendances
        """
        self.trends_fig.clear()
        ax = self.trends_fig.add_subplot(111)
        trends = self.data_processor.get_sales_trends()
        monthly_trends = trends['monthly']

        monthly_trends = monthly_trends.sort_values(by=['Year', 'Month'])
        monthly_trends['Date'] = pd.to_datetime(
            monthly_trends[['Year', 'Month']].assign(DAY=1)
        )

        ax.plot(monthly_trends['Date'], monthly_trends['total_revenue'], marker='o', linestyle='-')
        ax.set_title('Tendances Mensuelles des Ventes')
        ax.set_xlabel('Mois')
        ax.set_ylabel('Revenu Total')

        self.trends_fig.tight_layout()
        self.trends_canvas.draw()

    def _update_products_graph(self, sales_summary):
        """
        @Description: Met à jour le graphique des produits
        """
        self.products_fig.clear()
        ax = self.products_fig.add_subplot(111)

        # Créer un camembert des parts de marché basé sur le revenu total
        sales_summary['market_share'] = sales_summary['total_revenue'] / sales_summary['total_revenue'].sum() * 100
        top_5_products = sales_summary.head(5)

        wedges, texts, autotexts = ax.pie(top_5_products['market_share'], labels=top_5_products.index, autopct='%1.1f%%', startangle=90)

        ax.set_title('Part de Marché des 5 Meilleurs Produits')

        self.products_fig.tight_layout()
        self.products_canvas.draw()

    def _export_analysis(self):
        """
        @Description: Exporte l'analyse actuelle dans un fichier texte
        """
        if not self.data_processor:
            messagebox.showwarning("Attention", "Aucune donnée n'est chargée")
            return

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"analysis_{timestamp}.txt"

            filename = filedialog.asksaveasfilename(
                initialfile=default_filename,
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )

            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    # Résumé des ventes
                    sales_summary = self.data_processor.get_sales_summary()
                    f.write("=== Résumé des Ventes ===\n\n")
                    f.write(sales_summary.to_string())
                    f.write("\n\n")

                    # Meilleur produit
                    best_seller = self.data_processor.get_best_selling_product()
                    f.write("=== Meilleur Produit ===\n\n")
                    for key, value in best_seller.items():
                        f.write(f"{key}: {value}\n")
                    f.write("\n")

                    # Tendances
                    trends = self.data_processor.get_sales_trends()
                    f.write("=== Tendances Mensuelles ===\n\n")
                    f.write(trends['monthly'].to_string())

                messagebox.showinfo("Succès", "Analyse exportée avec succès")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export: {str(e)}")

    def _show_documentation(self):
        url = "https://github.com/SkyZonDev/ESMEMarket/blob/main/README.md"  # Remplacez par l'URL souhaitée
        webbrowser.open(url)

    def _show_about(self):
        pass

    def _show_credit(self):
        pass

    def run(self):
        """
        @Description: Lance l'application
        """
        self.window.mainloop()
