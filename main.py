"""
@Description Point d'entrée principal de l'application ESMEMarket
"""

from cli.interface import ConsoleCLI

def main():
    """
    @Description Fonction principale qui lance l'interface utilisateur
    """
    # Crée et lance l'interface CLI
    cli = ConsoleCLI()
    cli.run()

if __name__ == "__main__":
    main()
