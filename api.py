"""Module d'API du jeu Gobblet

Attributes:
    URL (str): Constante représentant le début de l'url du serveur de jeu.

Functions:
    * lister_parties - Récupérer la liste des parties reçus du serveur.
    * débuter_partie - Créer une nouvelle partie et retourne l'état de cette dernière.
    * récupérer_partie - Retrouver l'état d'une partie spécifique.
    * jouer_coup - Exécute un coup et retourne le nouvel état de jeu.
"""

import requests

URL = "https://pax.ulaval.ca/gobblet/api/"


def lister_parties(idul, secret):
    """Lister les parties

    Args:
        idul (str): idul du joueur
        secret (str): secret récupérer depuis le site de PAX

    Raises:
        PermissionError: Erreur levée lorsque le serveur retourne un code 401.
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

    Returns:
        list: Liste des parties reçues du serveur,
             après avoir décodé le json de sa réponse.
    """
    rep = requests.get(URL+'parties', auth=(idul, secret))

    if rep.status_code == 200:
        # la requête s'est déroulée normalement;
        # décoder le JSON et afficher la liste de parties
        rep = rep.json()
        return rep['parties']

    elif rep.status_code == 401:
        raise PermissionError()
    elif rep.status_code == 406:
        raise RuntimeError()
    else:
        raise ConnectionError()


def débuter_partie(idul, secret):
    """Débuter une partie

    Args:
        idul (str): idul du joueur
        secret (str): secret récupérer depuis le site de PAX

    Raises:
        PermissionError: Erreur levée lorsque le serveur retourne un code 401.
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

    Returns:
        tuple: Tuple constitué de l'identifiant de la partie,
            de l'état du plateau de jeu et de la liste des joueurs,
            après avoir décodé le JSON de sa réponse.
    """
    rep = requests.post(URL+'partie', auth=(idul, secret))

    if rep.status_code == 200:

        rep = rep.json()
        a = rep['id']
        b = rep['plateau']
        nom_du_joueur1 = rep['joueurs'][0]
        nom_du_joueur2 = rep['joueurs'][1]
        return(a, b, [nom_du_joueur1, nom_du_joueur2])

    elif rep.status_code == 401:
        raise PermissionError()
    elif rep.status_code == 406:
        raise RuntimeError()
    else:
        raise ConnectionError()


def récupérer_partie(id_partie, idul, secret):
    """Récupérer une partie

    Args:
        id_partie (str): identifiant de la partie à récupérer
        idul (str): idul du joueur
        secret (str): secret récupérer depuis le site de PAX

    Raises:
        PermissionError: Erreur levée lorsque le serveur retourne un code 401.
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

    Returns:
        tuple: Tuple constitué de l'identifiant de la partie,
            de l'état du plateau de jeu et de la liste des joueurs,
            après avoir décodé le JSON de sa réponse.
    """

    rep = requests.get(URL+'partie'+ str(id_partie), auth=(idul, secret))

    if rep.status_code == 200:
        # la requête s'est déroulée normalement;
        # décoder le JSON et afficher la liste de parties
        ep = rep.json()
        a = rep['id']
        b = rep['plateau']
        nom_du_joueur1 = rep['joueurs'][0]['nom']
        nom_du_joueur2 = rep['joueurs'][1]['nom']
        return(a, b, [nom_du_joueur1, nom_du_joueur2])

    elif rep.status_code == 401:
        raise PermissionError()
    elif rep.status_code == 406:
        raise RuntimeError()
    else:
        raise ConnectionError()


def jouer_coup(id_partie, origine, destination, idul, secret):
    """Jouer un coup

    Args:
        id_partie (str): identifiant de la partie
        origine (int ou list): l'origine est soit un entier représentant
                               le numéro de la pile du joueur ou une liste de 2 entier [x, y]
                               représentant le Gobblet sur le plateau.
        destination (list): la destination estune liste de 2 entier [x, y]
                            représentant le Gobblet sur le plateau
        idul (str): idul du joueur
        secret (str): secret récupérer depuis le site de PAX

    Raises:
        StopIteration: Erreur levée lorsqu'il y a un gagnant dans la réponse du serveur.
        PermissionError: Erreur levée lorsque le serveur retourne un code 401.
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

    Returns:
        tuple: Tuple constitué de l'identifiant de la partie,
            de l'état du plateau de jeu et de la liste des joueurs,
            après avoir décodé le JSON de sa réponse.
    """
    rep = requests.put(URL+'jouer', auth=(idul, secret), json={
        "id": id_partie,
        "destination": destination,
        "origine": origine, })

    if rep.status_code == 200:
        rep = rep.json()
        nom_du_gagnant = rep['gagnant']
        if nom_du_gagnant is not None:
            raise StopIteration()
        a = rep['id']
        b = rep['plateau']
        nom_du_joueur1 = rep['joueurs'][0]
        nom_du_joueur2 = rep['joueurs'][1]
        return(a, b, [nom_du_joueur1, nom_du_joueur2])

    elif rep.status_code == 401:
        raise PermissionError()
    elif rep.status_code == 406:
        raise RuntimeError()
    else:
        raise ConnectionError()
