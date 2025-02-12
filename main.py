import argparse
from cli.console import CLI
from cli.interface import GUI

def main():
    parser = argparse.ArgumentParser(description="Choisir le mode de l'application")
    parser.add_argument("--cli", action="store_true", help="Lancer l'interface en mode console")
    parser.add_argument("--gui", action="store_true", help="Lancer l'interface graphique")

    args = parser.parse_args()

    if args.cli:
        cli = CLI()
        cli.run()
    elif args.gui:
        gui = GUI()
        gui.run()
    else:
        print(
            "\n⚠️  Veuillez spécifier un mode d'exécution !\n"
            "Utilisation :\n"
            "  python main.py --cli   # Pour lancer l'application en mode console\n"
            "  python main.py --gui   # Pour lancer l'application en mode graphique\n"
        )


if __name__ == "__main__":
    main()
