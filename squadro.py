'''
Ce module permet d'encapsuler le jeu Squadro
class : Squadro(classe enfant de squadro interface)
    fonctions : vérification
                __str__
                déplacer_jeton
                jouer_un_coup
                demander_coup
                jeu_terminé
class : SquadroException
'''
from argparse import ArgumentParser
import json
from datetime import datetime
from copy import deepcopy
import os
from random import randrange
from squadro_interface import SquadroInterface




class Squadro(SquadroInterface):
    """Classe enfant de squadrointerface
    fonctions:
        vérification, __str__, déplacer_jeton,
        joueur_un_coup, demander_coup, jeu_terminé
    """
    def vérification(self, joueur_1, joueur_2):
        """Vérification d'initialisation d'une instance de la classe Squadro.

        Valide les données arguments de construction de l'instance et retourne
        l'état si valide.

        Args:
            joueur_1 (str/Dict): une chaîne de caractère représentant soit le nom du joueur
                soit un dictionnaire contant la clef `nom` représentant le nom du joueur
                et la clef `pions` représentant la liste des jetons du joueur.
                Le premier élément de la liste de jetons représente le premier jeton du joueur
                (de haut en bas pour le joueur 1, et de gauche à droite pour le joueur 2).
                L'entier assigné au jeton représente sa position
                (0 pour le départ, 6 pour la mi-chemin et 12 pour la fin).
            joueur_2 (str/Dict): une chaîne de caractère représentant soit le nom du joueur
                soit un dictionnaire contant la clef `nom` représentant le nom du joueur
                et la clef `pions` représentant la liste des jetons du joueur.
                Le premier élément de la liste de jetons représente le premier jeton du joueur
                (de haut en bas pour le joueur 1, et de gauche à droite pour le joueur 2).
                L'entier assigné au jeton représente sa position
                (0 pour le départ, 6 pour la mi-chemin et 12 pour la fin).
        Returns:
            List: L'état actuel du jeu sous la forme d'une liste de deux dictionnaires.
                  Le joueur 1 doit être à la première position de la liste.
                  Notez que les jetons doivent être sous forme de liste
                  [x1, x2, x3, x4, x5] uniquement.
        Raises:
            SquadroException: Le nom du joueur doit être une chaîne de caractère.
            SquadroException: L'objet `pions` doit être une liste.
            SquadroException: L'objet `pions` doit posséder 5 éléments uniquement.
            SquadroException: La position des jeton doit être un entier.
            SquadroException: La position des jeton doit être entre 0 et 12 inclusivement.
            SquadroException: Le joueur doit être une chaîne de caractère ou un dictionnaire.
        """
        liste_état = []
        liste_joueurs = [joueur_1, joueur_2]
        for joueur in liste_joueurs:
            if isinstance(joueur, str):
                liste_état.append({"nom":joueur, "pions":[0, 0, 0, 0, 0]})
            elif isinstance(joueur, dict):
                if isinstance(joueur["pions"], list) is False:
                    raise SquadroException("L'objet `pions` doit être une liste.")
                if isinstance(joueur["nom"], str) is False:
                    raise SquadroException("Le nom du joueur doit être une chaîne de caractère.")
                if len(joueur["pions"]) != 5:
                    raise SquadroException("L'objet `pions` doit posséder 5 éléments uniquement.")
                for position in joueur["pions"]:
                    if isinstance(position, int) is False:
                        raise SquadroException("La position des jeton doit être un entier.")
                    if position > 12 or position < 0:
                        raise SquadroException(
                            "La position des jeton doit être entre 0 et 12 inclusivement."
                            )
                liste_état.append(joueur)
            else:
                raise SquadroException(
                    "Le joueur doit être une chaîne de caractère ou un dictionnaire."
                    )
        return liste_état

    def __str__(self):
        """Produire un représentation en art ASCII de l'état actuel du jeu.

        Returns:
            str: La chaîne de caractères de la représentation.
        """
        nom1 = self.état_jeu()[0]['nom']
        nom2 = self.état_jeu()[1]['nom']
        pions1 = self.état_jeu()[0]['pions']
        pions2 = self.état_jeu()[1]['pions']

        col_rect = '█'
        col_cerc = '●'
        lin_carr = '□'
        lin_cerc = '○'
        espace = ' '
        board = list('''
       . | . : | : : | : : | : . | .
         |   . | .   |   . | .   |       
  ...    |     |     |     |     |      .
1 ───────┼─────┼─────┼─────┼─────┼───────
  ...    |     |     |     |     |      .
  .      |     |     |     |     |    ...
2 ───────┼─────┼─────┼─────┼─────┼───────
  .      |     |     |     |     |    ...
  ..     |     |     |     |     |     ..
3 ───────┼─────┼─────┼─────┼─────┼───────
  ..     |     |     |     |     |     ..
  .      |     |     |     |     |    ...
4 ───────┼─────┼─────┼─────┼─────┼───────
  .      |     |     |     |     |    ...
  ...    |     |     |     |     |      .
5 ───────┼─────┼─────┼─────┼─────┼───────
  ...    |     |     |     |     |      .
       . | .   |     |     |   . | .
       : | : . | . : | : . | . : | :''')

        for j, w in enumerate(pions1):
            if 6 <= w < 12:
                small_or_not = False
                w = 12 - w
            elif w == 12:
                small_or_not = False
            else:
                small_or_not = True

            if w in (0, 1):
                lin_carr1_index = 127 + (j*126) + 4*w
            elif w == 6:
                lin_carr1_index = 159 + (j*126)
            elif w == 12:
                lin_carr1_index = 128 + (j*126)
            else:
                new_w = w - 1
                lin_carr1_index = 127 + (j*126) + 4+6*new_w

            if small_or_not:
                lin_carr2_index = lin_carr1_index - 1
                lin_cerc_index = lin_carr1_index + 2
                lin_espace_index = lin_carr1_index + 1
            else:
                lin_carr2_index = lin_carr1_index + 1
                lin_cerc_index = lin_carr1_index - 2
                lin_espace_index = lin_carr1_index - 1
            board[lin_carr1_index] = lin_carr
            board[lin_carr2_index] = lin_carr
            board[lin_cerc_index] = lin_cerc
            board[lin_espace_index] = espace

        for i, v in enumerate(pions2):
            if v == 12:
                v = 0
                col_cerc_index = 47 + (v*84) + 6*i
                col_rect_index = col_cerc_index + 42
            else:
                if 6 <= v < 12:
                    small_or_not = False
                    v = 12 - v
                else:
                    small_or_not = True

                if v in (0, 1):
                    col_rect_index = 47 + (v*84) + 6*i
                elif v == 6:
                    col_rect_index = 47 + 672 + 6*i
                else:
                    new_v = v - 2
                    col_rect_index = 47 + (210+126*new_v) + 6*i

                if small_or_not:
                    col_cerc_index = col_rect_index + 42
                else:
                    col_cerc_index = col_rect_index - 42
            board[col_rect_index] = col_rect
            board[col_cerc_index] = col_cerc

        return f"Légende:\n  □ = {nom1}\n  ■ = {nom2}" + '\n' + "".join(board)

    def déplacer_jeton(self, joueur, jeton):
        """Déplacer un jeton.
        Pour le joueur spécifié, déplacer le jeton spécifié pour le nombre permis de cases.
        Args:
            joueur (str): Le nom du jouer tel que présent dans l'état.
            jeton (int): Le jeton à déplacer (de 1 à 5 inclusivement).
        Raises:
            SquadroException: Le nom du joueur est inexistant pour le jeu en cours.
            SquadroException: Le numéro du jeton devrait être entre 1 à 5 inclusivement.
            SquadroException: La jeu est déjà terminée.
            SquadroException: Ce jeton a déjà atteint la destination finale.
        """
        if joueur == self.état[0]["nom"]:
            index_joueur = 0
            index_joueur_ennemi = 1
            liste_déplacement_1 = [3, 1, 2, 1, 3]
            liste_déplacement_2 = [1, 3, 2, 3, 1]
        elif joueur == self.état[1]["nom"]:
            index_joueur = 1
            index_joueur_ennemi = 0
            liste_déplacement_1 = [1, 3, 2, 3, 1]
            liste_déplacement_2 = [3, 1, 2, 1, 3]
        else:
            raise SquadroException("Le nom du joueur est inexistant pour le jeu en cours.")
        if jeton < 1 or jeton > 5:
            raise SquadroException("Le numéro du jeton devrait être entre 1 à 5 inclusivement.")
        if self.état[0]["pions"].count(12) == 4 or self.état[1]["pions"].count(12) == 4:
            raise SquadroException("La jeu est déjà terminée.")
        position_jeton = self.état[index_joueur]["pions"][jeton - 1]
        fin_tour = 0
        if position_jeton == 12:
            raise SquadroException("Ce jeton a déjà atteint la destination finale.")
        if position_jeton < 6:
            for déplacement_max in range(0, 6):
                if position_jeton == 0:
                    position_jeton += 1
                elif position_jeton == 6:
                    fin_tour += 1
                    break
                elif (jeton == self.état[index_joueur_ennemi]["pions"][position_jeton - 1] or
                        12 - jeton == self.état[index_joueur_ennemi]["pions"][position_jeton - 1]):
                    if self.état[index_joueur_ennemi]["pions"][position_jeton - 1] < 6:
                        self.état[index_joueur_ennemi]["pions"][position_jeton - 1] = 0
                        position_jeton += 1
                        fin_tour += 1
                    else:
                        self.état[index_joueur_ennemi]["pions"][position_jeton - 1] = 6
                        position_jeton += 1
                        fin_tour += 1
                elif fin_tour == 0 and déplacement_max < liste_déplacement_1[jeton - 1]:
                    position_jeton += 1
            self.état[index_joueur]["pions"][jeton - 1] = position_jeton
        if position_jeton >= 6:
            for déplacement_max in range(0, 6):
                if position_jeton == 6 and fin_tour >= 1:
                    break
                if position_jeton == 6:
                    position_jeton += 1
                elif position_jeton == 12:
                    fin_tour += 1
                    break
                elif (jeton == self.état[index_joueur_ennemi]["pions"][11 - position_jeton] or
                        12 - jeton == self.état[index_joueur_ennemi]["pions"][11 - position_jeton]):
                    if self.état[index_joueur_ennemi]["pions"][11 - position_jeton] < 6:
                        self.état[index_joueur_ennemi]["pions"][11 - position_jeton] = 0
                        position_jeton += 1
                        fin_tour += 1
                    else:
                        self.état[index_joueur_ennemi]["pions"][11 - position_jeton] = 6
                        position_jeton += 1
                        fin_tour += 1
                elif fin_tour == 0 and déplacement_max < liste_déplacement_2[jeton - 1]:
                    position_jeton += 1
            self.état[index_joueur]["pions"][jeton - 1] = position_jeton

    def jouer_un_coup(self, joueur):
        """Jouer un coup automatique pour un joueur.

        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        du jeu.

        Args:
            joueur (str): Le nom du jouer tel que représenté dans l'état.

        Raises:
            SquadroException: Le nom du joueur est inexistant pour le jeu en cours.

        Returns:
            Tuple[str, int]: Un tuple composé du nom du joueur et du numéro du jeton joué.
        """

        pion = trouver_pion(self.état_jeu(), joueur)
        if pion is None:
            pion_déplacé = randrange(0, 5)
            pion_correct = True
            while pion_correct is True:
                if joueur == self.état_jeu()[0]["nom"]:
                    if self.état_jeu()[0]["pions"][pion_déplacé] == 12:
                        pion_déplacé = randrange(0, 5)
                    if self.état_jeu()[0]["pions"][pion_déplacé] != 12:
                        pion_correct = False
                        self.déplacer_jeton(joueur, pion_déplacé + 1)
                elif joueur == self.état_jeu()[1]["nom"]:
                    if self.état_jeu()[1]["pions"][pion_déplacé] == 12:
                        pion_déplacé = randrange(0, 5)
                    if self.état_jeu()[1]["pions"][pion_déplacé] != 12:
                        pion_correct = False
                        self.déplacer_jeton(joueur, pion_déplacé + 1)
                else:
                    raise SquadroException("Le nom du joueur est inexistant pour le jeu en cours.")
            return (joueur, pion_déplacé + 1)
        return pion




    def demander_coup(self, joueur):
        """Demander le coup à jouer via le terminal

        Args:
            joueur (str): Le nom du jouer à qui la question est posée.

        Raises:
            SquadroException: Le nom du joueur est inexistant pour le jeu en cours.
            SquadroException: Le numéro du jeton devrait être entre 1 à 5 inclusivement.
            SquadroException: Ce jeton a déjà atteint la destination finale.

        Returns:
            int: Un entier représentant le numéro du jeton à déplacer.
        """

        if joueur not in (self.état_jeu()[0]["nom"], self.état_jeu()[1]["nom"]):
            raise SquadroException("Le nom du joueur est inexistant pour le jeu en cours.")
        input_pion = int(input(f'{joueur} veuillez choisir le pion à déplacer:')) - 1

        if input_pion < 0 or input_pion > 4:
            raise SquadroException("Le numéro du jeton devrait être entre 1 à 5 inclusivement.")

        if joueur == self.état_jeu()[0]["nom"]:
            if self.état_jeu()[0]["pions"][input_pion] == 12:
                raise SquadroException("Ce jeton a déjà atteint la destination finale.")
        elif joueur == self.état_jeu()[1]["nom"]:
            if self.état_jeu()[1]["pions"][input_pion] == 12:
                raise SquadroException("Ce jeton a déjà atteint la destination finale.")
        return input_pion + 1

    def jeu_terminé(self):
        """Déterminer si le jeu est terminé.

        Returns:
            str/bool: Le nom du gagnant si le jeu est terminé; False autrement.
        """
        if self.état_jeu()[0]["pions"].count(12) == 4:
            return self.état_jeu()[0]["nom"]
        if self.état[1]["pions"].count(12) == 4:
            return self.état_jeu()[1]["nom"]
        return False

class SquadroException(Exception):
    """Permet de soulever des exceptions de type SquadroExpection
    hérite toutes ses méthodes de la classe Exception
    """

def traiter_la_ligne_de_commande():
    """Génère un évaluateur de ligne de commande
    l'analyseur offre (1) argument positionnel:
        IDUl: IDUl du ou des joueurs.
    Ainsi que les (2) arguments optionnel:
        help: show this help message and exit
        parties: lister les 20 dernières parties.
    Returns:
        Namespace: Retourne un objet de type Namespace possédant
            les clefs «IDUL» et «parties».
    """
    parser = ArgumentParser(description="Squadro")
    parser.add_argument(
        'IDUL',
        nargs='+',
        help='IDUL du ou des joueur(s)'
    )
    parser.add_argument(
        '-a', '--automatique',
        action = 'store_true',
        help='Activer le mode automatique.'
    )
    parser.add_argument(
        '-l', '--local',
        action='store_true',
        help='Jouer localement.'
    )
    parser.add_argument(
        '-p', '--parties',
        action='store_true',
        help="Lister les 20 dernières parties"
    )
    return parser.parse_args()

def enregistrer_partie_local(id_partie, prochain_joueur, état, gagnant = None):
    '''Enregistre la partie en cours sous format json.
    Crée un nouveau fichier pour chaque combinaison de joueur.
    Append à ce fichier chaque nouvelle partie crée ou
    apporte les modifs nécéssaires à la partie qui a été reprise
    '''
    joueur1 = état[0]['nom']
    joueur2 = état [1]['nom']
    id_existant = False

    if os.path.exists(f"{joueur1}-{joueur2}.json"):
        with open(f"{joueur1}-{joueur2}.json", 'r') as file:
            data = json.load(file)
        for partie in data['parties']:
            if partie['id'] == id_partie:
                partie['prochain_joueur'] = prochain_joueur
                partie['état'] = état
                partie['gagnant'] = gagnant
                id_existant = True
        if not id_existant:
            data['parties'].append({
                'id': id_partie,
                'date': datetime.today().isoformat(sep=' ', timespec='seconds'),
                'prochain_joueur': prochain_joueur,
                'joueurs': [joueur1, joueur2],
                'état': état,
                'gagnant': gagnant})
        with open(f"{joueur1}-{joueur2}.json", 'w') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    else:
        data = {}
        data['parties'] = []
        data['parties'].append({
            'id': id_partie,
            'date': datetime.today().isoformat(sep=' ', timespec='seconds'),
            'prochain_joueur': prochain_joueur,
            'joueurs': [joueur1, joueur2],
            'état': état,
            'gagnant': gagnant})
        with open(f"{joueur1}-{joueur2}.json", 'w') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

def lister_les_parties_local(liste_joueurs):
    '''Créé une liste de dictionnaire contenant
    l'id, la date, les joueurs et le gagnant (si existant)
    pour chaque partie judqu'à un maximum des 20 dernières parties
    les plus récentes.
    '''
    liste_parties = []
    counter = 0
    if len(liste_joueurs) == 1:
        with open(f"{liste_joueurs[0]}-robot_local.json", 'r') as file:
            data = json.load(file)
        for partie in reversed(data['parties']):
            del partie['prochain_joueur']
            del partie['état']
            liste_parties.append(partie)
            counter += 1
            if counter == 20:
                break
    else:
        with open(f"{liste_joueurs[0]}-{liste_joueurs[1]}.json", 'r') as file:
            data = json.load(file)
        for partie in reversed(data['parties']):
            del partie['prochain_joueur']
            del partie['état']
            liste_parties.append(partie)
            counter += 1
            if counter == 20:
                break
    return liste_parties

def formatter_les_parties(parties):
    """Formatter les parties
    Args:
        parties (list): liste des parties d'un joueur.
    Returns:
        str: Chaîne de caractière représentant votre liste de parties
    """
    repr_text = str()
    for i, v in enumerate(parties):
        repr_text += f"{i+1:<2.0f}: {v['date']}, {v['joueurs'][0]} vs {v['joueurs'][1]}"

        if v['gagnant'] is not None:
            repr_text += f", gagnant: {v['gagnant']}\n"
        else:
            repr_text += "\n"
    return repr_text

def charger_partie_local(id_partie, liste_joueurs):
    '''Retourne un tuple contennant l'id de la partie,
    le nom du prochain joueur et l'état de la partie
    que l'on cherche à aller chercher.
    '''
    if len(liste_joueurs) == 1:
        with open(f"{liste_joueurs[0]}-robot_local.json", 'r') as file:
            data = json.load(file)
        for partie in data['parties']:
            if partie['id'] == id_partie:
                prochain_joueur = partie['prochain_joueur']
                état = partie['état']
        return (id_partie, prochain_joueur, état)
    with open(f"{liste_joueurs[0]}-{liste_joueurs[1]}.json", 'r') as file:
        data = json.load(file)
    for partie in data['parties']:
        if partie['id'] == id_partie:
            prochain_joueur = partie['prochain_joueur']
            état = partie['état']
    return (id_partie, prochain_joueur, état)

def déplacer_jetons(état, joueur, jeton):
    '''
    Cette fonction permet de simuler le déplacement de jeton sans
    impacter l'instance état de la classe
    '''
    pion_retourné = 0
    liste_états = []
    état_copy = deepcopy(état)
    if joueur == état_copy[0]["nom"]:
        index_joueur = 0
        index_joueur_ennemi = 1
        liste_déplacement_1 = [3, 1, 2, 1, 3]
        liste_déplacement_2 = [1, 3, 2, 3, 1]
    elif joueur == état_copy[1]["nom"]:
        index_joueur = 1
        index_joueur_ennemi = 0
        liste_déplacement_1 = [1, 3, 2, 3, 1]
        liste_déplacement_2 = [3, 1, 2, 1, 3]
    else:
        raise SquadroException("Le nom du joueur est inexistant pour le jeu en cours.")
    if jeton < 1 or jeton > 5:
        raise SquadroException("Le numéro du jeton devrait être entre 1 à 5 inclusivement.")
    if état_copy[0]["pions"].count(12) == 4 or état_copy[1]["pions"].count(12) == 4:
        raise SquadroException("La jeu est déjà terminée.")
    position_jeton = état_copy[index_joueur]["pions"][jeton - 1]
    fin_tour = 0
    if position_jeton == 12:
        raise SquadroException("Ce jeton a déjà atteint la destination finale.")
    if position_jeton < 6:
        for déplacement_max in range(0, 6):
            if position_jeton == 0:
                position_jeton += 1
            elif position_jeton == 6:
                fin_tour += 1
                break
            elif (jeton == état_copy[index_joueur_ennemi]["pions"][position_jeton - 1] or
                    12 - jeton == état_copy[index_joueur_ennemi]["pions"][position_jeton - 1]):
                if état_copy[index_joueur_ennemi]["pions"][position_jeton - 1] < 6:
                    état_copy[index_joueur_ennemi]["pions"][position_jeton - 1] = 0
                    pion_retourné += 1
                    position_jeton += 1
                    fin_tour += 1
                else:
                    pion_retourné += 1
                    état_copy[index_joueur_ennemi]["pions"][position_jeton - 1] = 6
                    position_jeton += 1
                    fin_tour += 1
            elif fin_tour == 0 and déplacement_max < liste_déplacement_1[jeton - 1]:
                position_jeton += 1
        état_copy[index_joueur]["pions"][jeton - 1] = position_jeton
    if position_jeton >= 6:
        for déplacement_max in range(0, 6):
            if position_jeton == 6 and fin_tour >= 1:
                break
            if position_jeton == 6:
                position_jeton += 1
            elif position_jeton == 12:
                fin_tour += 1
                break
            elif (jeton == état_copy[index_joueur_ennemi]["pions"][11 - position_jeton] or
                    12 - jeton == état_copy[index_joueur_ennemi]["pions"][11 - position_jeton]):
                if état_copy[index_joueur_ennemi]["pions"][11 - position_jeton] < 6:
                    état_copy[index_joueur_ennemi]["pions"][11 - position_jeton] = 0
                    pion_retourné += 1
                    position_jeton += 1
                    fin_tour += 1
                else:
                    état_copy[index_joueur_ennemi]["pions"][11 - position_jeton] = 6
                    pion_retourné += 1
                    position_jeton += 1
                    fin_tour += 1
            elif fin_tour == 0 and déplacement_max < liste_déplacement_2[jeton - 1]:
                position_jeton += 1
    liste_états.append(état_copy[0])
    liste_états.append(état_copy[1])
    return [liste_états, pion_retourné]

def analyse_jeu(état, joueur):
    '''
    Cette fonction permet d'analyser le jeu en simulant le déplacement de chaque pion du joueur.
    '''
    liste_retours_moi = []
    liste_retours_autres = []
    liste_retours_sép = []
    état_pion = ["salut", "test"]
    if joueur == état[0]["nom"]:
        joueur_ennemi = état[1]["nom"]
    elif joueur == état[1]["nom"]:
        joueur_ennemi = état[0]["nom"]
    for x in range(1, 6):
        for y in range(1, 6):
            try:
                état123 = état
                état_pion = déplacer_jetons(état123, joueur, x)
                état5 = état_pion[0]
                new_état_pion = déplacer_jetons(état5, joueur_ennemi, y)
                liste_retours_autres.append(new_état_pion[1])
            except SquadroException:
                état_pion[1] = None
                liste_retours_autres.append(0)
        liste_retours_moi.append(état_pion[1])
    for i in range(0, 25, 5):
        liste_retours_sép.append(liste_retours_autres[:25][i:i + 5])
    return liste_retours_moi, liste_retours_sép, liste_retours_autres[:25], état

def trouver_pion(état, joueur):
    '''
    Cette fonction permet de trouver le meilleur pion
    à joueur suite à la simulation de analyse_jeu().
    '''
    tuple_infos = analyse_jeu(état, joueur)
    liste_meilleurs_candidats = []
    best_play = None
    if joueur == état[0]["nom"]:
        indice = 0
    elif joueur == état[1]["nom"]:
        indice = 1
    if tuple_infos[0].count(0) == 5:
        pass
    else:
        for i, valeurs in enumerate(tuple_infos[0]):
            if valeurs is None:
                pass
            elif valeurs > 0:
                liste_meilleurs_candidats.append((i, valeurs))

    if tuple_infos[2].count(0) == 25:
        pass
    else:
        for i, candidat in enumerate(liste_meilleurs_candidats):
            if tuple_infos[1][candidat[0]].count(1) != 0:
                liste_meilleurs_candidats.pop(i)
    if len(liste_meilleurs_candidats) == 1:
        best_play = (joueur, liste_meilleurs_candidats[0][0] + 1)
    elif len(liste_meilleurs_candidats) > 0:
        meilleur_coup = liste_meilleurs_candidats[0]
        for i, candidat in enumerate(liste_meilleurs_candidats):
            if candidat[1] < meilleur_coup[1]:
                meilleur_coup = candidat
        best_play = (joueur, meilleur_coup[0] + 1)
    elif len(liste_meilleurs_candidats) == 0:
        coup_moyen = (0, 0)
        for index, position_pion in enumerate(état[indice]["pions"]):
            if position_pion >= coup_moyen[1]:
                if état[indice]["pions"][index] != 12:
                    coup_moyen = (index, position_pion)
        if coup_moyen != (0, 0):
            best_play = (joueur, coup_moyen[0] + 1)
    return best_play
