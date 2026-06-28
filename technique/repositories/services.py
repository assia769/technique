# ce fichier contient la logique pour detecter les fichiers critiques
# j'ai voulu isoler ca des vues pour que ce soit plus propre

# noms de fichiers qui sont sensibles par nature
FICHIERS_SENSIBLES = [
    '.env',
    '.env.local',
    'secret.key',
    'secrets.py',
    'id_rsa',
    'private.key',
]

# extensions qui correspondent a des fichiers de config
EXTENSIONS_CONFIG = [
    '.config',
    '.cfg',
    '.ini',
    '.yml',
    '.yaml',
    '.toml',
    '.env',
]

# 5 Mo en octets
TAILLE_MAX = 5 * 1024 * 1024


def fichier_est_critique(fichier):
    """
    Verifie si un fichier doit etre marque comme critique.
    Retourne True si au moins un critere est rempli.
    """

    # fichier trop grand
    if fichier.taille > TAILLE_MAX:
        return True

    # pas de description = on sait pas ce que c'est
    if not fichier.description or fichier.description.strip() == '':
        return True

    # fichier de type config
    if fichier.type_fichier == 'config':
        return True

    # nom du fichier dans la liste des fichiers sensibles
    nom_lower = fichier.nom.lower()
    if nom_lower in FICHIERS_SENSIBLES:
        return True

    # extension sensible
    for ext in EXTENSIONS_CONFIG:
        if nom_lower.endswith(ext):
            return True

    return False