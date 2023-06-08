import random
import datetime
import os
import pickle
import sys

TABLE_SIMPLE_MAX = 12

def teste_reponse_entier(resultat, temps_max):
    start_time = datetime.datetime.now().timestamp()
    reponse = input("> ")
    if reponse == "":
        print(f"La réponse était {resultat}")
        return 0
    if int(reponse) == resultat:
        print("Bravo !")
        time = datetime.datetime.now().timestamp() - start_time
        return max(1, temps_max - time)
    else:
        print(f"La réponse était {resultat}")
        return 0

def teste_reponse_fraction(resultat_int, facteur, temps_max):
    start_time = datetime.datetime.now().timestamp()
    reponse = input("> ")
    if reponse == "":
        print(f"La réponse était {resultat_int / facteur}")
        return 0
    if int(float(reponse) * facteur) == resultat_int:
        print("Bravo !")
        time = datetime.datetime.now().timestamp() - start_time
        return max(1, temps_max - time)
    else:
        print(f"La réponse était {resultat_int / facteur}")
        return 0

def multiplication_simple():
    facteur_a = random.randint(2, TABLE_SIMPLE_MAX)
    facteur_b = random.randint(2, TABLE_SIMPLE_MAX)
    resultat = facteur_a * facteur_b
    print(f"{facteur_a} * {facteur_b} = ?")
    return teste_reponse_entier(resultat, 5)

def multiplication_difficile():
    facteur_a = random.randint(2, 13)
    facteur_b = random.randint(2, 13)
    resultat = facteur_a * facteur_b
    print(f"{facteur_a} * {facteur_b} = ?")
    return teste_reponse_entier(resultat, 5)

def division_simple():
    resultat = random.randint(2, TABLE_SIMPLE_MAX)
    denominateur = random.randint(2, TABLE_SIMPLE_MAX)
    numerateur = resultat * denominateur
    print(f"{numerateur} / {denominateur} = ?")
    return teste_reponse_entier(resultat, 10)

def division_difficile():
    resultat_int = random.randint(1, 100)
    resultat = resultat_int
    denominateur = random.randint(2, 20)
    numerateur = resultat * denominateur
    facteur = 1
    while numerateur % 10 == 0:
        numerateur //= 10
        resultat /= 10
        facteur *= 10
    start_time = datetime.datetime.now().timestamp()
    print(f"{numerateur} / {denominateur} = ?")
    return teste_reponse_fraction(resultat_int, facteur, 60)

TESTS = {
    'facile': [multiplication_simple, division_simple],
    'moyen': [multiplication_simple, multiplication_difficile, division_simple],
    'dur': [multiplication_simple, division_simple, division_difficile],
    'difficile': [multiplication_simple, multiplication_difficile, division_simple, division_difficile]
}

def charge_etat():
    if os.path.exists("calculmental_save.pkl"):
        with open("calculmental_save.pkl", "rb") as f:
            return pickle.load(f)
    else:
        return {'joueurs': {}, 'meilleur_scores': []}

def enregistre_etat(etat):
    with open("calculmental_save.pkl", "wb") as f:
        pickle.dump(etat, f)

def main():
    etat = charge_etat()
    print("Bienvenue dans Calcul Mental !")
    nom = input("Quel est votre nom ? ")
    if nom not in etat['joueurs']:
        print(f"Ravi de faire votre connaissance, {nom}")
        mot_de_passe = input("Choisissez un mot de passe :")
        etat['joueurs'][nom] = {'niveau': 'facile', 'meilleurs_scores': {}, 'mot_de_passe': mot_de_passe}
    elif 'mot_de_passe' not in etat['joueurs'][nom]:
        mot_de_passe = input("Choisissez un mot de passe :")
        etat['joueurs'][nom]['mot_de_passe'] = mot_de_passe
    else:
        mot_de_passe = input("Quel est votre mot de passe ? ")
        while mot_de_passe != etat['joueurs'][nom]['mot_de_passe']:
            print("Désolé, le mot de passe est incorrect")
            sys.exit(1)
    print(f"Content de vous revoir, {nom}")
    niveau = etat['joueurs'][nom]['niveau']
    if niveau == 'facile' and etat['joueurs'][nom]['meilleurs_scores'].get('facile', 0) > 100:
        print("Bravo, vous avez atteint le niveau difficile !")
        niveau = 'moyen'
        etat['joueurs'][nom]['niveau'] = niveau
    elif niveau not in ('facile', 'moyen'):
        niveau = 'moyen'
        etat['joueurs'][nom]['niveau'] = niveau
    print(f"Vous êtes au niveau {niveau}")
    print("Vous allez devoir répondre à 20 questions")

    score = 0
    tests = TESTS[niveau]
    for _ in range(20):
        test = random.choice(tests)
        score += test()
        print(f"Votre score est de {int(score)} points")
        print()
    print(f"Votre score final est de {int(score)} points")
    meilleur_score_precedent = None
    if niveau in etat['joueurs'][nom]['meilleurs_scores']:
        meilleur_score_precedent = etat['joueurs'][nom]['meilleurs_scores'][niveau]
    if meilleur_score_precedent is None:
        etat['joueurs'][nom]['meilleurs_scores'][niveau] = score
    elif score > meilleur_score_precedent:
        print("Bravo, vous avez battu votre meilleur score sur ce niveau !")
        etat['joueurs'][nom]['meilleurs_scores'][niveau] = score
    else:
        print(f"Bravo, mais vous avez fait mieux, votre meilleur score sur ce niveau est {int(meilleur_score_precedent)}")
    enregistre_etat(etat)

if __name__ == '__main__':
    main()