"""
Générateur de fanlinks : lit un fichier CSV et crée une page web par titre.

Ce fichier est un SQUELETTE : il y a 3 endroits marqués TODO à compléter.
Lance-le avec :  python generer_fanlinks.py
"""
import csv
from pathlib import Path
from string import Template

FICHIER_CSV = "tracks.csv"          # le fichier avec les titres et les liens
FICHIER_MODELE = "template.html"    # le modèle de page (avec $title, $artist, $buttons)
DOSSIER_SORTIE = Path("docs")       # les pages générées iront ici

# Les plateformes : nom affiché -> nom de la colonne dans le CSV
PLATEFORMES = {
    "Spotify": "spotify_url",
    "Deezer": "deezer_url",
    "Apple Music": "apple_music_url",
    "Boutique": "shop_url",
}


def lire_titres(chemin_csv):
    """Retourne la liste des titres du CSV, une ligne = un dictionnaire."""
    # def lire_titres(chemin_csv):
    """..."""
    with open(chemin_csv, encoding="utf-8", newline="") as fichier:
        lecteur = csv.DictReader(fichier)
        return list(lecteur)
    


def construire_boutons(ligne):
    """Retourne le texte HTML des boutons pour un titre.

    - Pour chaque plateforme qui a un lien (colonne non vide) : un bouton.
    - Si AUCUN lien n'est rempli : un message « Bientôt disponible ».
    """
    boutons = []
    for nom, colonne in PLATEFORMES.items():
        lien = ligne[colonne].strip()
        if lien:
            boutons.append(f'<a class="btn" href="{lien}">Écouter sur {nom}</a>')

    if not boutons:
        return '<div class="soon">Bientôt disponible</div>'
    return "\n    ".join(boutons)


def ecrire_page(ligne, modele):
    """Crée le fichier HTML d'un titre dans le dossier de sortie."""
    boutons = construire_boutons(ligne)
    texte = modele.substitute(title=ligne["title"], artist=ligne["artist"], buttons=boutons)
    chemin = DOSSIER_SORTIE / (ligne["slug"] + ".html")
    chemin.write_text(texte, encoding="utf-8")

def ecrire_index(titres):
    """Crée la page d'accueil (index.html) avec la liste de tous les titres."""
    lignes = []
    for ligne in titres:
        lignes.append(f'<li><a href="{ligne["slug"]}.html">{ligne["artist"]} : {ligne["title"]}</a></li>')
    liste = "\n    ".join(lignes)
    page = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Démo fanlinks</title></head>
<body style="font-family: Arial, sans-serif; max-width: 520px; margin: 24px auto; padding: 0 16px;">
  <h1>Démonstration : générateur de fanlinks</h1>
  <p>Chaque page est générée automatiquement à partir d'un fichier CSV.</p>
  <ul>
    {liste}
  </ul>
</body></html>"""
    (DOSSIER_SORTIE / "index.html").write_text(page, encoding="utf-8")

def main():
    DOSSIER_SORTIE.mkdir(exist_ok=True)
    modele = Template(Path(FICHIER_MODELE).read_text(encoding="utf-8"))
    titres = lire_titres(FICHIER_CSV)
    for ligne in titres:
        ecrire_index(titres)
        ecrire_page(ligne, modele)
        print("Page créée :", ligne["slug"] + ".html")
    print(len(titres), "pages générées dans le dossier", DOSSIER_SORTIE)


if __name__ == "__main__":
    main()
