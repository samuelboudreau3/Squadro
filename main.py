'''
Ce programme permet de créer les instances de jeu Squadro ainsi que de les jouer.
'''

import uuid
from squadro import (
    Squadro, charger_partie_local, enregistrer_partie_local, formatter_les_parties,
    lister_les_parties_local, traiter_la_ligne_de_commande
    )
from api import (créer_une_partie, jouer_un_coup, lister_les_parties, récupérer_une_partie)



def boucle_de_jeu_pvp_local(liste_iduls):
    '''
    Cette boucle permet de créer une nouvelle partie localement, en joueur contre joueur,
    de la jouer en mode manuel, ainsi que l'enregistrer à tous les tours
    '''
    partie = Squadro(liste_iduls[0], liste_iduls[1])
    id_partie= str(uuid.uuid4())
    enregistrer_partie_local(
        id_partie,
        partie.état_jeu()[0]["nom"],
        partie.état_jeu()
        )
    print(partie)
    while partie.jeu_terminé() is False:
        pion = partie.demander_coup(partie.état[0]["nom"])
        partie.déplacer_jeton(partie.état[0]["nom"], pion)
        enregistrer_partie_local(
            id_partie,
            partie.état_jeu()[1]["nom"],
            partie.état_jeu()
            )
        prochain_joueur = partie.état_jeu()[1]["nom"]
        print(partie)
        if partie.jeu_terminé() is False:
            pion = partie.demander_coup(partie.état[1]["nom"])
            partie.déplacer_jeton(partie.état[1]["nom"], pion)
            enregistrer_partie_local(
                id_partie,
                partie.état_jeu()[0]["nom"],
                partie.état_jeu()
                )
            prochain_joueur = partie.état_jeu()[0]["nom"]
            print(partie)
    enregistrer_partie_local(
        id_partie,
        prochain_joueur,
        partie.état_jeu(),
        gagnant=partie.jeu_terminé()
        )
    print(partie.jeu_terminé())

def boucle_de_jeu_pvr_local(liste_iduls):
    '''
    Cette boucle permet de créer une nouvelle partie localement, en joueur contre robot,
    de la jouer en mode manuel, ainsi que l'enregistrer à tous les tours
    '''
    partie = Squadro(liste_iduls[0], liste_iduls[1])
    id_partie = str(uuid.uuid4())
    enregistrer_partie_local(
        id_partie,
        partie.état_jeu()[0]["nom"],
        partie.état_jeu()
        )
    print(partie)
    while partie.jeu_terminé() is False:
        pion = partie.demander_coup(partie.état[0]["nom"])
        partie.déplacer_jeton(partie.état[0]["nom"], pion)
        enregistrer_partie_local(
            id_partie,
            partie.état_jeu()[1]["nom"],
            partie.état_jeu()
            )
        prochain_joueur = partie.état_jeu()[1]["nom"]
        if partie.jeu_terminé() is False:
            pion_déplacé = partie.jouer_un_coup(partie.état[1]["nom"])
            partie.déplacer_jeton(partie.état[1]["nom"], pion_déplacé[1])
            enregistrer_partie_local(
                id_partie,
                partie.état_jeu()[0]["nom"],
                partie.état_jeu()
                )
            prochain_joueur = partie.état_jeu()[0]["nom"]
            print(partie)
    enregistrer_partie_local(
        id_partie,
        prochain_joueur,
        partie.état_jeu(),
        gagnant=partie.jeu_terminé()
        )
    print(partie.jeu_terminé())

def boucle_de_jeu_partie_récupérée_local_pvp(partie):
    '''
    Cette boucle permet de récupérer une partie sauvegardée localement,
    en joueur contre joueur, de la jouer en mode manuel, ainsi que l'enregistrer à tous les tours
    '''
    liste_infos = charger_partie_local(partie["id"], partie["joueurs"])
    état = liste_infos[2]
    prochain_joueur = liste_infos[1]
    partie_interne = Squadro(état[0]["nom"], état[1]["nom"])
    partie_interne.état = état
    print(partie_interne)
    if prochain_joueur == état[0]["nom"]:
        enregistrer_partie_local(
            partie["id"],
            partie_interne.état_jeu()[0]["nom"],
            partie_interne.état_jeu()
            )
        while partie_interne.jeu_terminé() is False:
            pion_local = partie_interne.demander_coup(état[0]["nom"])
            partie_interne.déplacer_jeton(état[0]["nom"], pion_local)
            enregistrer_partie_local(
                partie["id"],
                partie_interne.état_jeu()[1]["nom"],
                partie_interne.état_jeu()
                )
            prochain_joueur = partie_interne.état_jeu()[1]["nom"]
            print(partie_interne)
            if partie_interne.jeu_terminé() is False:
                pion_local = partie_interne.demander_coup(état[1]["nom"])
                partie_interne.déplacer_jeton(état[1]["nom"], pion_local)
                enregistrer_partie_local(
                    partie["id"],
                    partie_interne.état_jeu()[0]["nom"],
                    partie_interne.état_jeu()
                    )
                prochain_joueur = partie_interne.état_jeu()[0]["nom"]
                print(partie_interne)
        enregistrer_partie_local(
            partie["id"],
            prochain_joueur,
            partie_interne.état_jeu(),
            gagnant=partie_interne.jeu_terminé()
            )
        print(partie_interne.jeu_terminé())
    if prochain_joueur == état[1]["nom"]:
        enregistrer_partie_local(
            partie["id"],
            partie_interne.état_jeu()[1]["nom"],
            partie_interne.état_jeu()
            )
        while partie_interne.jeu_terminé() is False:
            pion_local = partie_interne.demander_coup(état[1]["nom"])
            partie_interne.déplacer_jeton(état[1]["nom"], pion_local)
            enregistrer_partie_local(
                partie["id"],
                partie_interne.état_jeu()[0]["nom"],
                partie_interne.état_jeu()
                )
            prochain_joueur = partie_interne.état_jeu()[0]["nom"]
            print(partie_interne)
            if partie_interne.jeu_terminé() is False:
                pion_local = partie_interne.demander_coup(état[0]["nom"])
                partie_interne.déplacer_jeton(état[0]["nom"], pion_local)
                enregistrer_partie_local(
                    partie["id"],
                    partie_interne.état_jeu()[1]["nom"],
                    partie_interne.état_jeu()
                    )
                prochain_joueur = partie_interne.état_jeu()[1]["nom"]
                print(partie_interne)
        enregistrer_partie_local(
            partie["id"],
            prochain_joueur,
            partie_interne.état_jeu(),
            gagnant=partie_interne.jeu_terminé()
            )
        print(partie_interne.jeu_terminé())

def boucle_de_jeu_partie_récupérée_local_pvr(partie):
    '''
    Cette boucle permet de récupérer une partie sauvegardée localement,
    en joueur contre robot, de la jouer en mode manuel, ainsi que l'enregistrer à tous les tours
    '''
    liste_infos = charger_partie_local(partie["id"], partie["joueurs"])
    état = liste_infos[2]
    prochain_joueur = liste_infos[1]
    partie_interne = Squadro(état[0]["nom"], état[1]["nom"])
    partie_interne.état = état
    for i in état:
        if état[état.index(i)]['nom'] != "robot_local":
            index_humain = état.index(i)
    print(partie_interne)
    if prochain_joueur == état[index_humain]["nom"]:
        enregistrer_partie_local(
            partie['id'],
            partie_interne.état_jeu()[index_humain]["nom"],
            partie_interne.état_jeu()
            )
        while partie_interne.jeu_terminé() is False:
            pion_local = partie_interne.demander_coup(état[index_humain]["nom"])
            partie_interne.déplacer_jeton(état[index_humain]["nom"], pion_local)
            enregistrer_partie_local(
                partie['id'],
                "robot_local",
                partie_interne.état_jeu()
                )
            prochain_joueur = "robot_local"
            print(partie_interne)
            if partie_interne.jeu_terminé() is False:
                pion_déplacé = partie_interne.jouer_un_coup("robot_local")
                partie_interne.déplacer_jeton("robot_local", pion_déplacé[1])
                enregistrer_partie_local(
                    partie['id'],
                    partie_interne.état_jeu()[index_humain]["nom"],
                    partie_interne.état_jeu()
                    )
                prochain_joueur = partie_interne.état_jeu()[index_humain]["nom"]
                print(partie_interne)
        enregistrer_partie_local(
            partie["id"],
            prochain_joueur,
            partie_interne.état_jeu(),
            gagnant=partie_interne.jeu_terminé()
            )
        print(partie_interne.jeu_terminé())
    if prochain_joueur == "robot_local":
        enregistrer_partie_local(
            partie['id'],
            "robot_local",
            partie_interne.état_jeu()
            )
        while partie_interne.jeu_terminé() is False:
            pion_déplacé = partie_interne.jouer_un_coup("robot_local")
            partie_interne.déplacer_jeton("robot_local", pion_déplacé[1])
            enregistrer_partie_local(
                partie['id'],
                partie_interne.état_jeu()[index_humain]["nom"],
                partie_interne.état_jeu()
                )
            prochain_joueur = partie_interne.état_jeu()[index_humain]["nom"]
            print(partie_interne)
            if partie_interne.jeu_terminé() is False:
                pion_local = partie_interne.demander_coup(état[index_humain]["nom"])
                partie_interne.déplacer_jeton(état[index_humain]["nom"], pion_local)
                enregistrer_partie_local(
                    partie['id'],
                    "robot_local",
                    partie_interne.état_jeu()
                    )
                prochain_joueur = "robot_local"
                print(partie_interne)
        enregistrer_partie_local(
            partie["id"],
            prochain_joueur,
            partie_interne.état_jeu(),
            gagnant=partie_interne.jeu_terminé()
            )
        print(partie_interne.jeu_terminé())

def boucle_de_jeu_pvp_serveur(liste_iduls):
    '''
    Cette boucle permet de créer une nouvelle partie sur le serveur, en joueur contre joueur,
    de la jouer en mode manuel, ainsi que l'enregistrer à tous les tours
    '''
    partie = créer_une_partie(liste_iduls)
    partie_interne = Squadro(partie[2][0]["nom"], partie[2][1]["nom"])
    print(partie_interne)
    fin_jeu = False
    while fin_jeu is False:
        try:
            pion_local = partie_interne.demander_coup(partie_interne.état[0]["nom"])
            infos = jouer_un_coup(partie[0], partie_interne.état[0]["nom"], pion_local)
            partie_interne.état = infos[2]
            print(partie_interne)
            pion_local = partie_interne.demander_coup(partie_interne.état[1]["nom"])
            infos = jouer_un_coup(partie[0], partie_interne.état[1]["nom"], pion_local)
            partie_interne.état = infos[2]
            print(partie_interne)
        except StopIteration as gagnant:
            fin_jeu = True
            print(str(gagnant))


def boucle_de_jeu_pvr_serveur(idul):
    '''
    Cette boucle permet de créer une nouvelle partie sur le serveur, en joueur contre robot,
    de la jouer en mode manuel
    '''
    partie = créer_une_partie(idul, bot=2)
    partie_interne = Squadro(partie[2][0]["nom"], partie[2][1]["nom"])
    print(partie_interne)
    fin_jeu = False
    while fin_jeu is False:
        try:
            pion_local = partie_interne.demander_coup(partie[2][0]["nom"])
            partie_interne.déplacer_jeton(partie[2][0]["nom"], pion_local)
            infos = jouer_un_coup(partie[0], partie[2][0]["nom"], pion_local)
            partie_interne.état = infos[2]
            print(partie_interne)
        except StopIteration as gagnant:
            fin_jeu = True
            print(str(gagnant))

def boucle_de_jeu_rvr_serveur(idul):
    '''
    Cette boucle permet de créer une nouvelle partie sur le serveur, en joueur contre robot,
    de la jouer en mode automatique
    '''
    bot = 4
    partie = créer_une_partie(idul, bot=bot)
    partie_interne = Squadro(idul[0], f'robot-{bot}')
    print(partie_interne)
    fin_jeu = False
    while fin_jeu is False:
        try:
            pion_local = partie_interne.jouer_un_coup(idul[0])[1]
            print(partie_interne)
            infos = jouer_un_coup(partie[0], idul[0], pion_local)
            partie_interne.état = infos[2]
            print(partie_interne)
        except StopIteration as gagnant:
            fin_jeu = True
            print(str(gagnant))

def boucle_de_jeu_partie_récupérée_serveur_pvp(partie):
    '''
    Cette boucle permet de récupérer une partie sauvegardée sur le serveur,
    en joueur contre joueur, de la jouer en mode manuel
    '''
    liste_infos = récupérer_une_partie(partie["id"])
    état = liste_infos[2]
    prochain_joueur = liste_infos[1]
    partie_interne = Squadro(état[0]["nom"], état[1]["nom"])
    partie_interne.état = état
    print(partie_interne)
    fin_jeu = False
    if liste_infos[2][0]["pions"].count(12) == 4:
        print(liste_infos[2][0]["nom"])
    elif liste_infos[2][1]["pions"].count(12) == 4:
        print(liste_infos[2][1]["nom"])
    else:
        if prochain_joueur == état[0]["nom"]:
            while fin_jeu is False:
                try:
                    pion_local = partie_interne.demander_coup(état[0]["nom"])
                    partie_interne.déplacer_jeton(état[0]["nom"], pion_local)
                    infos = jouer_un_coup(liste_infos[0], état[0]["nom"], pion_local)
                    partie_interne.état = infos[2]
                    print(partie_interne)
                    pion_local = partie_interne.demander_coup(état[1]["nom"])
                    partie_interne.déplacer_jeton(état[1]["nom"], pion_local)
                    infos = jouer_un_coup(liste_infos[0], état[1]["nom"], pion_local)
                    partie_interne.état = infos[2]
                    print(partie_interne)
                except StopIteration as gagnant:
                    fin_jeu = True
                    print(str(gagnant))
        if prochain_joueur == état[1]["nom"]:
            while fin_jeu is False:
                try:
                    pion_local = partie_interne.demander_coup(état[1]["nom"])
                    partie_interne.déplacer_jeton(état[1]["nom"], pion_local)
                    infos = jouer_un_coup(liste_infos[0], état[1]["nom"], pion_local)
                    partie_interne.état = infos[2]
                    print(partie_interne)
                    pion_local = partie_interne.demander_coup(état[0]["nom"])
                    partie_interne.déplacer_jeton(état[0]["nom"], pion_local)
                    infos = jouer_un_coup(liste_infos[0], état[0]["nom"], pion_local)
                    partie_interne.état = infos[2]
                    print(partie_interne)
                except StopIteration as gagnant:
                    fin_jeu = True
                    print(str(gagnant))

def boucle_de_jeu_partie_récupérée_serveur_pvr(partie):
    '''
    Cette boucle permet de récupérer une partie sauvegardée sur le serveur,
    en joueur contre robot, de la jouer en mode manuel
    '''
    liste_infos = récupérer_une_partie(partie["id"])
    état = liste_infos[2]
    partie_interne = Squadro(état[0]["nom"], état[1]["nom"])
    partie_interne.état = état
    print(partie_interne)
    if liste_infos[2][0]["pions"].count(12) == 4:
        print(liste_infos[2][0]["nom"])
        
    elif liste_infos[2][1]["pions"].count(12) == 4:
        print(liste_infos[2][1]["nom"])
    else:
        fin_jeu = False
        while fin_jeu is False:
            try:
                pion_local = partie_interne.demander_coup(état[0]["nom"])
                partie_interne.déplacer_jeton(état[0]["nom"], pion_local)
                infos = jouer_un_coup(partie["id"], état[0]["nom"], pion_local)
                partie_interne.état = infos[2]
                print(partie_interne)
            except StopIteration as gagnant:
                fin_jeu = True
                print(str(gagnant))





if __name__ == "__main__":
    args = traiter_la_ligne_de_commande()
    iduls = args.IDUL
    if not args.parties or not args.local or not args.automatique:
        if len(iduls) == 1 and not (args.parties or args.local or args.automatique):
            boucle_de_jeu_pvr_serveur(iduls)
        elif len(iduls) == 2 and not (args.parties or args.local or args.automatique):
            boucle_de_jeu_pvp_serveur(iduls)

    if args.parties and not args.local:
        liste_parties = lister_les_parties(iduls)
        parties_formattées = formatter_les_parties(liste_parties)
        print(parties_formattées)
        input_partie = int(input("Veuillez choisir la partie à continuer :"))
        partie_sélectionnée = liste_parties[input_partie - 1]
        if len(iduls) == 2:
            boucle_de_jeu_partie_récupérée_serveur_pvp(partie_sélectionnée)
        if len(iduls) == 1:
            boucle_de_jeu_partie_récupérée_serveur_pvr(partie_sélectionnée)
    elif args.local and not args.parties:
        if len(iduls) == 1:
            iduls.append('robot_local')
            boucle_de_jeu_pvr_local(iduls)
        elif len(iduls) == 2:
            boucle_de_jeu_pvp_local(iduls)
    elif args.automatique:
        boucle_de_jeu_rvr_serveur(iduls)
    elif args.local and args.parties:
        liste_parties_local = lister_les_parties_local(iduls)
        parties_formattées = formatter_les_parties(liste_parties_local)
        print(parties_formattées)
        input_partie = int(input("Veuillez choisir la partie à continuer :"))
        partie_sélectionnée = liste_parties_local[input_partie - 1]
        if len(iduls) == 2:
            boucle_de_jeu_partie_récupérée_local_pvp(partie_sélectionnée)
        if len(iduls) == 1:
            boucle_de_jeu_partie_récupérée_local_pvr(partie_sélectionnée)
