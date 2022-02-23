# -*- coding: utf-8 -*-
"""Module d'API du jeu Squadro
Ce module permet d'interagir avec le serveur
afin de pouvoir jouer contre un adversaire robotisé.
Attributes:
    URL (str): Constante représentant le début de l'url du serveur de jeu.
Functions:
    * lister_les_parties - Récupérer la liste des parties reçus du serveur.
    * récupérer_une_partie - Retrouver l'état d'une partie spécifique.
    * créer_une_partie - Créer une nouvelle partie et retourne l'état de cette dernière.
    * jouer_un_coup - Exécute un coup et retourne le nouvel état de jeu.
"""

import httpx


URL = "https://pax.ulaval.ca/squadro/api2/"


def lister_les_parties(iduls):
    """
    Args:
        iduls (list): Liste des identifiant des joueurs.
    Returns:
        list: Liste des parties reçues du serveur,
            après avoir décodé le JSON de sa réponse.
    Raises:
        RuntimeError: Erreur levée lorsqu'il y a présence d'un message
            dans la réponse du serveur.
    """
    rep = httpx.get(URL+'parties', params={'iduls': iduls})
    if rep.status_code == 200:
        rep = rep.json()
        return rep["parties"]

    if rep.status_code == 406:
        rep = rep.json()
        raise RuntimeError(f'{rep["message"]}')
    return f"Le GET sur '{URL}parties' a produit le code d'erreur {rep.status_code}."



def récupérer_une_partie(id_partie):
    """
    Args:
        id_partie (str): Chaine de l'identifiant de la partie.
    Returns:
        tuple:   Tuple des informations de la partie, contenant l'id,
                le prochain joueur à joué et l'état. Si il y a un gagnant,
                n'affiche pas l'état mais affiche le gagnant,
                après avoir décodé le JSON de sa réponse.
    Raises:
        RuntimeError: Erreur levée lorsqu'il y a présence d'un message
            dans la réponse du serveur.
    """
    rep = httpx.get(URL+'partie', params={'id': [id_partie]})
    if rep.status_code == 200:
        rep = rep.json()
        return (rep["id"], rep["prochain_joueur"], rep["état"])

    if rep.status_code == 406:
        rep = rep.json()
        raise RuntimeError(f'{rep["message"]}')
    return f"Le GET sur '{URL}parties' a produit le code d'erreur {rep.status_code}."


def créer_une_partie(iduls, bot = None):
    """
    Args:
        iduls (list): Liste de string représentant le ou les identifiant(s) du ou des joueur(s).
    Returns:
        tuple: Tuple constitué de l'identifiant de la partie en cours,
            du prochain joueur à jouer et de l'état courant du jeu,
            après avoir décodé le JSON de sa réponse.
    Raises:
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
    """
    if bot is None:
        rep = httpx.post(URL+'partie', json={'iduls': iduls})
    elif 1 <= bot <= 5:
        rep = httpx.post(URL+'partie', json={'iduls': iduls, 'bot' : bot})

    if rep.status_code == 200:
        rep = rep.json()
        return (rep["id"], rep["prochain_joueur"], rep["état"])

    if rep.status_code == 406:
        rep = rep.json()
        raise RuntimeError(f'{rep["message"]}')
    return f"Le GET sur '{URL}parties' a produit le code d'erreur {rep.status_code}."



def jouer_un_coup(id_partie, idul, pion):
    """
    Args:
        id_partie (str): identifiant de la partie;
        idul (str): IDUL jouant un coup;
        pion (int): Numéro du pion à déplacer.
    Returns:
        tuple: Tuple constitué de l'identifiant de la partie en cours,
            du prochain joueur à jouer et de l'état courant du jeu,
            après avoir décodé le JSON de sa réponse.
    Raises:
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        StopIteration: Erreur levée lorsqu'il y a un gagnant dans la réponse du serveur.
    """
    rep = httpx.put(URL+'jouer', json={'id': id_partie, 'idul' : idul, 'pion' : pion})

    if rep.status_code == 200:
        rep = rep.json()
        if rep["gagnant"] is None:
            return (rep["id"], rep["prochain_joueur"], rep["état"])
        raise StopIteration(f'{rep["gagnant"]}')


    if rep.status_code == 406:
        rep = rep.json()
        raise RuntimeError(f'{rep["message"]}')
    return f"Le GET sur '{URL}parties' a produit le code d'erreur {rep.status_code}."
