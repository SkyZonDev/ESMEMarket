"""
@Description Point d'entrée principal de l'application ESMEMarket
"""

from cli.console import ConsoleCLI
from cli.interface import InterfaceCLI

def main():
    """
    @Description Fonction principale qui lance l'interface utilisateur
    """
    # Crée et lance l'interface CLI
    # cls = ConsoleCLI()
    # cls.run()

    cli = InterfaceCLI()
    cli.run()
    
if __name__ == "__main__":
    main()
