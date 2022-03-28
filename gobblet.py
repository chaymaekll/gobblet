"""Module Gobblet

Attributes:
    GOBBLET_REPRÉSENTATION (dict): Constante représentant les gobblet des joueurs.

Functions:
    * interpréteur_de_commande - Génère un interpréteur de commande.
    * formater_un_gobblet - Formater la représentation graphique d'un Gobblet.
    * formater_un_joueur - Formater la représentation graphique d'un joueur et de ses piles.
    * formater_plateau - Formater la représentation graphique d'un plateau.
    * formater_jeu - Formater la représentation graphique d'un jeu.
    * formater_les_parties - Formater la liste des dernières parties.
    * récupérer_le_coup - Demander le prochain coup à jouer au joueur.
"""
from argparse import ArgumentParser

# Voici la représentation des Gobblets, n'hésitez pas à l'utiliser.
# 1 pour le joueur 1, 2 pour le joueur 2.
GOBBLET_REPRÉSENTATION = {
    1: ["▫", "  ◇", "◯", "□"],
    2: ["▪", "◆", "●", "■"],
}


def interpréteur_de_commande():
    """Interpreteur de commande

    Returns:
        Namespace: Un objet Namespace tel que retourné par parser.parse_args().
                   Cette objet aura l'attribut IDUL représentant l'idul du joueur
                   et l'attribut lister qui est un booléen True/False.
    """
    parser = ArgumentParser(description="Gobblet")
    parser.add_argument('IDUL', help='IDUL du joueur', type=str)
    parser.add_argument("-l", "--lister", action='store_true',
                        help="lister les parties existantes")

    # Complétez le code ici
    # vous pourriez aussi avoir à ajouter des arguments dans ArgumentParser(...)

    return parser.parse_args()


def formater_un_gobblet(gobblet):
    """Formater un Gobblet

    Args:
        gobblet (list): liste vide ou de 2 entier [x, y] représentant le Gobblet

    Returns:
        str: Représentation du Gobblet pour le bon joueur
    """
    if gobblet == []:
        return " "
    tailles_du_joueur = GOBBLET_REPRÉSENTATION[gobblet[0]]
    taille_du_joueur = tailles_du_joueur[gobblet[1]]
    return taille_du_joueur


def formater_un_joueur(joueur):
    """Formater un joueur

    Args:
        joueur (dict): dictionnaire contenant le nom du joueurs et ses piles de Gobblet

    Returns:
        str: Représentation du joueur et de ses piles de Gobblet
    """
    nom_du_joueur = joueur['nom']
    chaine = ''
    chaine += nom_du_joueur + ':'
    for i in joueur['piles']:
        taille_du_joueur = formater_un_gobblet(i)
        chaine += taille_du_joueur
    return chaine


def formater_plateau(plateau):
    """Formater un plateau

    Args:
        plateau (list): plateau de jeu 4 x 4

    Returns:
        str: Représentation du plateau avec ses Gobblet
    """
    matrice = [['   ' for i in range(9)] for j in range(8)]
    liste123 = ['0', '1', '2', '3']
    chaineH = [' ─', "─", '─┼─', "─", '─┼─', "─", '─┼─', "──", '\n']
    for i in range(3):
        matrice[2 * i + 1] = chaineH
    for i in range(4):
        matrice[7][2 * i + 1] = liste123[i]
        matrice[6 - 2 * i][0] = liste123[i]
        matrice[2 * i][2] = '  |'
        matrice[2 * i][4] = '  |'
        matrice[2 * i][6] = '  |'
    for i in range(8):
        matrice[i][8] = '\n'
    matrice[7][0] = '  '
    for i in range(4):
        for j in range(4):
            matrice[2 * i][2 * j + 1] = formater_un_gobblet(plateau[i][j])
    chaine = ''
    for ligne in matrice:
        chaine += ''.join(ligne)
    return chaine


def formater_jeu(plateau, joueurs):
    """Formater un jeu

    Args:
        plateau (list): plateau de jeu 4 x 4
        joueurs (list): list de dictionnaire contenant le nom du joueurs et ses piles de Gobblet

    Returns:
        str: Représentation du jeu
    """
    print(joueurs)
    joueur1 = joueurs[0]
    joueur2 = joueurs[1]
    nom1 = joueur1['nom']
    nom2 = joueur2['nom']
    pile1 = joueur1['piles']
    pile2 = joueur2['piles']
    taille1 = len(nom1)
    taille2 = len(nom2)
    taillepile1 = len(pile1)
    taillepile2 = len(pile2)
    maximum_nom = max((taille1, taille2))
    maximum_pile = max((taillepile1, taillepile2))
    chaine = ''
    chaine += (maximum_nom + 3) * ' '
    chaine1 = ''

    for i in range(maximum_pile):
        chaine1 += str(i) + '   '
    chaine += chaine1
    chaine_joueur1 = formater_un_joueur(joueur1)
    chaine_joueur2 = formater_un_joueur(joueur2)
    diff = abs(len(chaine_joueur1) - len(chaine_joueur2))
    if len(chaine_joueur1) > len(chaine_joueur2):
        chaine_joueur2 = ' ' * diff + chaine_joueur2
    else:
        chaine_joueur1 = ' ' * diff + chaine_joueur1
    chaine_finale = chaine + '\n' + chaine_joueur1 + '\n' + chaine_joueur2
    creer_plateau = formater_plateau(plateau)
    return chaine_finale + '\n' * 2 + creer_plateau


def formater_les_parties(parties):
    """Formater une liste de parties

    L'ordre doit être exactement la même que ce qui est passé en paramètre.

    Args:
        parties (list): Liste des parties

    Returns:
        str: Représentation des parties
    """

    chaine = ''
    for i, partie in enumerate(parties):
        date = partie['date']
        joueurs = partie['joueurs'][0] + ' vs ' + partie['joueurs'][1]
        gagnant = partie[gagnant]
        chaine += str(i) + ' : ' + date + ', ' + joueurs
        if gagnant is not None:
            chaine += ', gagnant : ' + gagnant + ' \n'
        else:
            chaine += '\n'
    return chaine


def récupérer_le_coup():
    """Récupérer le coup

    Returns:
        tuple: Un tuple composé d'un origine et de la destination.
               L'origine est soit un entier représentant le numéro de la pile du joueur
               ou une liste de 2 entier [x, y] représentant le Gobblet sur le plateau
               La destination estune liste de 2 entier [x, y] représentant le Gobblet
               sur le plateau

    Examples:
        Quel Gobblet voulez-vous déplacer:
        Donnez le numéro de la pile (p) ou la position sur le plateau (x,y): 0
        Où voulez-vous placer votre Gobblet (x,y): 0,1

        Quel Gobblet voulez-vous déplacer:
        Donnez le numéro de la pile (p) ou la position sur le plateau (x,y): 2,3
        Où voulez-vous placer votre Gobblet (x,y): 0,1
    """
    origine = input(
        "Donnez le numéro de la pile (p) ou la position sur le plateau (x,y):")
    destination = input(" Où voulez-vous placer votre Gobblet (x,y):")
    if len(origine) == 1:
        return(int(origine), eval(destination))
    else:
        return(eval(origine), eval(destination))
