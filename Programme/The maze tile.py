import time
import pymunk
import pygame
from sys import exit
import math
import random



class Point(object):
    def __init__(self ,X ,Y):
        self.X = X*game.echelle + game.plus
        self.Y = Y*game.echelle + game.plus

    def rotation(self, theta):
        X1 = (self.X - game.screen_dim_X/2) * math.cos(theta) - (self.Y - game.screen_dim_Y/2) * math.sin(theta) + game.screen_dim_X/2
        Y1 = (self.X - game.screen_dim_X/2) * math.sin(theta) + (self.Y - game.screen_dim_Y/2) * math.cos(theta) + game.screen_dim_Y/2
        self.X = X1
        self.Y = Y1


class Segment(object):
    def __init__(self, depart, arrivee, seg_couleur):
        self.depart = depart
        self.arrivee = arrivee
        self.couleur = seg_couleur

    def rotation(self, theta):
        self.depart.rotation(theta)
        self.arrivee.rotation(theta)

    #affichage des segments en les dessinant
    def dessiner(self, screen):
        mx, my =  (self.depart.X + self.arrivee.X)/2 , (self.depart.Y + self.arrivee.Y)/2
        #Verifier la difficulté du jeu qui est la distance max pour l'affichage
        if math.sqrt((ball.body.position.x - mx)**2 + (ball.body.position.y-my)**2) < game.difficulty:
            pygame.draw.line(screen, self.couleur , (self.depart.X,self.depart.Y),(self.arrivee.X,self.arrivee.Y), 5)


class Labyrinthe(object):
    def __init__(self):
        self.segments = []
        self.bodys = []
        self.shapes = []
        self.taille = game.taille

    def ajouteSegment(self, segment):
        self.segments.append(segment)

    def rotation(self, theta):
        for segment in self.segments:
            segment.rotation(theta)

    def afficher(self, screen):
        for segment in self.segments:
            segment.dessiner(screen)

    #générer tout les points de la grille du labyrinthe
    def generation(self):
        listeDePoints = []
        for i in range(1, self.taille+2):
            for j in range(1, self.taille+2):
                listeDePoints.append((i,j))
        return listeDePoints

    #recupérer les couples de coordonnée des segments verticaux
    def SegmentVertical(self, liste):
        returnedListe = []
        for i in range(0,len(liste)-1):
                if liste[i][0] == liste[i+1][0]:
                    returnedListe.append((liste[i],liste[i+1]))
        return returnedListe

    # recupérer les couples de coordonnée des segments horizontaux
    def SegmentHorizontal(self, liste):
        returnedListe = []
        for i in range(0,len(liste)-1):
                if i<= len(liste) - (self.taille+2) and liste[i][1] == liste[i+self.taille+1][1]:
                    returnedListe.append((liste[i],liste[i+self.taille+1]))
        return returnedListe

    #actualise le corps ( hitbox ) des segments qui est géré par Pymunk
    def actualiser_body_segment(self):
        for body in self.bodys:
            game.space._remove_body(body)

        for shape in self.shapes:
            game.space._remove_shape(shape)

        self.bodys = []
        self.shapes = []

    #générer une sortie aléatoire sur les murs extérieurs du labyrinthe
    def Sortie(self):
        p = random.randint(0, 3)
        spawn = random.randint(1, game.taille)
        #Parcourir la liste des segments et comparer ses coordonnées avec spawn et le supprimer
        for segment in labyrinthe.segments:
            x1 = (segment.depart.X - game.plus) / game.echelle
            x2 = (segment.arrivee.X - game.plus) / game.echelle
            y1 = (segment.depart.Y - game.plus) / game.echelle
            y2 = (segment.arrivee.Y - game.plus) / game.echelle

            if p == 0:
                if x1 == 1 and x2 == 1 and y1 == spawn and y2 == spawn + 1:
                    labyrinthe.segments.remove(segment)
                    break

            elif p == 1:
                if x1 == spawn and x2 == spawn + 1 and y1 == 1 and y2 == 1:
                    labyrinthe.segments.remove(segment)
                    break

            elif p == 2:
                if x1 == 11 and x2 == 11 and y1 == spawn and y2 == spawn + 1:
                    labyrinthe.segments.remove(segment)
                    break

            elif p == 3:
                if x1 == spawn and x2 == spawn + 1 and y1 == 11 and y2 == 11:
                    labyrinthe.segments.remove(segment)
                    break


    def hitbox(self):
        for segment in labyrinthe.segments:
            x1 = segment.depart.X
            x2 = segment.arrivee.X
            y1 = segment.depart.Y
            y2 = segment.arrivee.Y
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            self.bodys.append(body)
            shape = pymunk.Segment(body, (x1, y1),(x2, y2), 5)
            self.shapes.append(shape)
            game.space.add(body, shape)


    def Generation_Aleatoire(self, liste):
        visited = []
        points = []

        #recupérer la liste de tout les points qui compose la grille du labyrinthe
        for point in liste:
            if point[0] != 1 and point[1] != 1:
                points.append(point)

        #choisir la cellule de départ
        number = random.randint(0, len(points)-1)

        #ajouter la cellule de départ à la liste des cellules visitées
        visited.append(points[number])

        #répeter l'opération jusqu'à parcourir toutes les cellules
        while len(visited) < (self.taille)**2:
            avancer = True
            voisins = []

            if points[number][0] != 2:  # présence de cellule à gauche
                voisins.append(points[number - self.taille])

            if points[number][1] != 2:  # présence de cellule en haut
                voisins.append(points[number - 1])

            if points[number][0] != self.taille+1:  # présence de cellule à droite
                voisins.append(points[number + self.taille])

            if points[number][1] != self.taille+1:  # présence de cellule en bas
                voisins.append(points[number + 1])


            random.shuffle(voisins)
            for voisin in voisins:
                if (voisin not in visited):
                    visited.append(voisin)
                    avancer = False

                    #récupérer les coordonnées du segment qui les sépare et le supprimer
                    for segment in labyrinthe.segments:
                        x1 = (segment.depart.X - game.plus)/game.echelle
                        x2 = (segment.arrivee.X - game.plus)/game.echelle
                        y1 = (segment.depart.Y - game.plus)/game.echelle
                        y2 = (segment.arrivee.Y - game.plus)/game.echelle

                        if points[number][1] != self.taille+1:
                            if voisin == points[number+1]:
                                if x1 == points[number][0]-1 and y1 == points[number][1] and x2 == points[number][0] and y2 == points[number][1]:
                                    labyrinthe.segments.remove(segment)
                                    break

                        if points[number][1] != 2:
                            if voisin == points[number-1]:
                                if x1 == points[number][0]-1 and y1 == points[number][1]-1 and x2 == points[number][0] and y2 == points[number][1]-1:
                                    labyrinthe.segments.remove(segment)
                                    break

                        if points[number][0] != self.taille+1:
                            if voisin == points[number+self.taille]:
                                if x1 == points[number][0] and y1 == points[number][1]-1 and x2 == points[number][0] and y2 == points[number][1]:
                                    labyrinthe.segments.remove(segment)
                                    break


                        if points[number][0] != 2:
                            if voisin == points[number-self.taille]:
                                if x1 == points[number][0]-1 and y1 == points[number][1]-1 and x2 == points[number][0]-1 and y2 == points[number][1]:
                                    labyrinthe.segments.remove(segment)
                                    break

                    number = points.index(voisin)
                    break

            #revenir à la cellule précedente en cas d'absence de nouveau voisin à visiter dans la cellule actuelle
            if avancer == True:
                number = points.index(visited[visited.index(points[number])-1])

        control.update()


class Ball(object):
    def __init__(self, positionX, positionY, couleur):
        self.positionX = positionX*game.echelle + game.plus
        self.positionY = positionY*game.echelle + game.plus
        self.couleur = couleur
        self.mass = 300
        self.body = pymunk.Body(1, self.mass, body_type=pymunk.Body.DYNAMIC)
        self.body.position = (self.positionX, self.positionY)
        self.shape = pymunk.Circle(self.body, 5)

    def afficher(self, screen):
        pygame.draw.circle(screen, self.couleur, (self.body.position.x, self.body.position.y), 7, 20)

    def rotation(self, theta):
        X = (self.body.position.x - game.screen_dim_X/2) * math.cos(theta) - (self.body.position.y - game.screen_dim_Y/2) * math.sin(theta) + game.screen_dim_X/2
        Y = (self.body.position.x - game.screen_dim_X/2) * math.sin(theta) + (self.body.position.y - game.screen_dim_Y/2) * math.cos(theta) + game.screen_dim_Y/2
        self.body.position = (X,Y)


class Control(object):
    def __init__(self, labyrinthe, ball):
        self.screen = pygame.display.set_mode((game.screen_dim_X, game.screen_dim_Y))
        self.labyrinthe = labyrinthe
        self.ball = ball

    def update(self):
        self.screen.blit(background, (0,0))
        self.labyrinthe.afficher(self.screen)
        self.ball.afficher(self.screen)
        game.space.step(1/40)                   #vitesse de calcul du moteur physique
        pygame.display.update()
        game.space.gravity = (0,2)              #sens et force de la gravité(x,y)


class Game:

    def __init__(self):
        self.is_playing = False
        self.gravity = (math.pi, 0.002)
        self.space = pymunk.Space()         #création de l'espace physique
        self.space.gravity = (0, 2)
        self.screen_dim_X = 700
        self.screen_dim_Y = 700
        self.taille = 10
        self.echelle = 48                   #ordre de grandeur pour les points
        self.plus = 64
        self.rotate = math.pi/400           #degrée de rotation
        self.difficulty = 700               # rayon de vision du joueur ( distance max d'un segment par rapport à la balle)
        self.couleur = ["#401811", "#56E317","#0A5A24", "#0A0C38", "#48085E", "#B40E66", "#BD0D0D"]



if __name__ == '__main__':
    pygame.init()
    game = Game()
    pygame.display.set_caption("The Maze Tale")


    arial_font = pygame.font.SysFont("arial", 50)

    #background
    background = pygame.image.load('images/fond.jpg')
    background = pygame.transform.scale(background, (game.screen_dim_X,game.screen_dim_Y))

    #bannière du jeu
    banner = pygame.image.load('images/banniere.png')
    banner = pygame.transform.scale(banner, (400,100))
    banner_rect = banner.get_rect()
    banner_rect.x = game.screen_dim_X / 5
    banner_rect.y = game.screen_dim_Y / 6

    #bouton play
    play = pygame.image.load('images/play.png')
    play_rect = play.get_rect()
    play_rect.x = game.screen_dim_X/2.55
    play_rect.y = game.screen_dim_Y/3
    play_texte = arial_font.render("LOADING..", True, "black")

    #bouton quitter
    quitter = pygame.image.load('images/quite.png')
    quitter_rect = quitter.get_rect()
    quitter_rect.x = game.screen_dim_X/2.55
    quitter_rect.y = game.screen_dim_Y/1.75

    #gagner
    win_texte = arial_font.render("YOU WIN", True, "green")

    #bouton easy
    easy = pygame.image.load('images/easy.png')
    easy_rect = easy.get_rect()
    easy_rect.x = game.screen_dim_X / 1.66
    easy_rect.y = game.screen_dim_Y / 2.2
    easy_texte = arial_font.render("Difficulty: Easy", True, "black")

    #bouton medium
    medium = pygame.image.load('images/medium.png')
    medium_rect = medium.get_rect()
    medium_rect.x = game.screen_dim_X / 2.55
    medium_rect.y = game.screen_dim_Y / 2.2
    medium_texte = arial_font.render("Difficulty: Medium", True, "black")

    #bouton hard
    hard = pygame.image.load('images/hard.png')
    hard_rect = hard.get_rect()
    hard_rect.x = game.screen_dim_X / 5.5
    hard_rect.y = game.screen_dim_Y / 2.2
    hard_texte = arial_font.render("Difficulty: Hard", True, "black")




    while True:

        #création et affichage du menu
        if game.is_playing == False:
            control = Control(None, None)
            control.screen.blit(background, (0,0))
            control.screen.blit(banner, banner_rect)
            control.screen.blit(play, play_rect)
            control.screen.blit(quitter, quitter_rect)
            control.screen.blit(easy, easy_rect)
            control.screen.blit(medium, medium_rect)
            control.screen.blit(hard, hard_rect)
            pygame.display.update()

        #lancement de la partie
        else:
            keys = pygame.key.get_pressed()

            #création de la balle et du labyrinthe
            if control.ball == None:
                labyrinthe = Labyrinthe()
                points = labyrinthe.generation()
                seg_couleur = game.couleur[random.randint(0,len(game.couleur)-1)]

                for segment in labyrinthe.SegmentVertical(points):
                    labyrinthe.ajouteSegment(Segment( Point(segment[0][0], segment[0][1]) , Point(segment[1][0], segment[1][1]), seg_couleur))

                for segment in labyrinthe.SegmentHorizontal(points):
                    labyrinthe.ajouteSegment(Segment( Point(segment[0][0], segment[0][1]), Point(segment[1][0], segment[1][1]), seg_couleur))

                ball = Ball((game.taille+1)/2, (game.taille+1)/2, game.couleur[random.randint(0,len(game.couleur)-1)])

                control = Control(labyrinthe, ball)
                labyrinthe.Generation_Aleatoire(points)
                labyrinthe.Sortie()
                labyrinthe.hitbox()
                game.space.add(ball.body, ball.shape)
                control.update()

            #verifier si la balle est sortie du labyrinthe
            else:
                if ball.body.position[1] > 2000:
                    control.screen.fill((0,0,0))
                    control.screen.blit(win_texte, (250, 300))
                    pygame.display.update()
                    game.is_playing = False
                    labyrinthe.actualiser_body_segment()
                    time.sleep(1.5)

            #Rotation à gauche et actualisation de l'affichage et la hitbox
            if keys[pygame.K_LEFT]:
                labyrinthe.actualiser_body_segment()
                labyrinthe.rotation(-game.rotate)
                ball.rotation(-game.rotate)
                labyrinthe.hitbox()
                game.space.gravity = (0, 30)

            #rotation à droite et actualisation de l'affichage et la hitbox
            if keys[pygame.K_RIGHT]:
                labyrinthe.actualiser_body_segment()
                labyrinthe.rotation(game.rotate)
                ball.rotation(game.rotate)
                labyrinthe.hitbox()
                game.space.gravity = (0, 30)

            control.update()

        for events in pygame.event.get():

            #détécter les cliques de la souris sur les boutons du menu
            if not game.is_playing and events.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(events.pos):
                    control.screen.blit(background, (0,0))
                    control.screen.blit(play_texte, (250, 300))
                    pygame.display.update()
                    time.sleep(0.7)
                    game.is_playing = True

                if easy_rect.collidepoint(events.pos):
                    control.screen.blit(easy_texte, (200,600))
                    pygame.display.update()
                    time.sleep(0.7)
                    game.difficulty = 700

                if medium_rect.collidepoint(events.pos):
                    control.screen.blit(medium_texte, (200, 600))
                    pygame.display.update()
                    time.sleep(0.7)
                    game.difficulty = 200

                if hard_rect.collidepoint(events.pos):
                    control.screen.blit(hard_texte, (200, 600))
                    pygame.display.update()
                    time.sleep(0.7)
                    game.difficulty = 130

                if quitter_rect.collidepoint(events.pos):
                    pygame.quit()
                    exit()

            elif events.type == pygame.QUIT:
                pygame.quit()
                exit()