## Lorsque toutes les cellules sont découvertes, on passe directement à la manche suivante, on n'a même pas le temps de voir les dernières cellules découvertes, s'il y a un item derrière ces dernières cellules, on ne peut pas le récuperer, comment faire ? Un bouton "prochaine manche" ?
-> * Sacha : Je pense qu'un bouton peut être pas mal oui, ou alors le perso qui dirait "Appuie sur \[touche\] pour passer à la manche suivante"

## Comment est-ce que le joueur quitte le marchand pour continuer le jeu ?
-> Petit panneau en bois avec une indication "passer son chemin" avec une flèche

## Faut-il un objet joueur pour l'inventaire par exemple et peut-être d'autres choses ?
-> Oui
Contenu de l'objet:
Attributs: - inventory: dict
           - discovered_items: list

Méthodes: - speak
          - animation (loupe, lunettes bioniques, bouclier, armure, clé à moletete)

Objet Item: - tqt

## Pouvons-nous utiliser deux objets en même temps (la loupe et le bouclier) ?
...

## Quelqu'un arrive à comprendre dans quel ordre les bombes sont découvertes sur le [démineur de google](https://g.co/kgs/VAGmvHQ) lorsque nous perdons ? Pouvez-vous expliquer rapidement, en français, comment refaire cet algorithme en python ?
...

## Lorsque le joueur meurt, la musique doit à un moment donné disparaître, pour laisser au final apparaître un simple écran noir, pendant peut-être 3 secondes, avant de revenir au menu principal avec la musique qui reprend. La question est la suivante: de quelle manière la musique disparaît-elle ? Avec un simple fondu ? Si la musique possède un thème court qui se repète, devrions-nous attendre que ce thème se termine avant de couper la musique "d'un coup" ?
-> La musique s'arrête d'un coup, un petit "clic" se fait entendre, la cinématique se joue, il y a de la musique en arrière plan, le joueur marche, fini par marcher sur une bombe, elle explose (avec un son), le joueur explose aussi, fondu au noir, plus de musique, plus rien, puis apparation du menu principal avec la musique qui revient avec un fondu.