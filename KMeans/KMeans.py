
import pygame  
from random import randint
import math
from sklearn.cluster import KMeans

pygame.init() 

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1]-p2[1])**2)

screen = pygame.display.set_mode((1200,700)) 
pygame.display.set_caption("KMeans visualization")
clock = pygame.time.Clock()

running = True

# initialize  corlor CONSTANT variable
            #  R,  G,  B
BACKGROUND = (214,214,214)
BLACK = (0,0,0)
WHITE = (255,255,255)
PANEL = (249,255,230)

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (147,153, 35)
PURPLE = (255, 0, 255)
SKY = (0, 255, 255)
ORANCE = (255, 125,25)
GRAPE = (100, 25,125)
GRASS = (55, 155, 65)

COLOR = [RED, GREEN, BLUE, YELLOW, PURPLE, SKY, ORANCE, GRAPE, GRASS, BLACK ]

# initialize Font
font = pygame.font.SysFont('sans', 40) # 40: size, sans: font chu
font_Small = pygame.font.SysFont('sans', 20)

# initialize text
text_plus = font.render('+', True, WHITE)
text_subtract = font.render('-', True, WHITE)
text_Run = font.render('Run', True, WHITE)
text_Random = font.render('Random', True, WHITE)
text_Algorithm = font.render('Algorithm', True, WHITE)
text_Reset = font.render('Reset', True, WHITE)



K = 0
error = 0
points =[]
clusters = []
labels = []

while running:

    clock.tick(60)
    screen.fill(BACKGROUND)
    
    # POSITION MOUSE

    mouse_x, mouse_y = pygame.mouse.get_pos()
    #print(mouse_x, ";", mouse_y)

## Draw interface


    # Draw panel
    pygame.draw.rect(screen, BLACK, (50,50, 700, 500))
    pygame.draw.rect(screen, PANEL, (55,55, 690, 490))

    # button +
    pygame.draw.circle(screen, BLACK, (850, 75), 25)
    screen.blit(text_plus, (840,50))

    # button -
    pygame.draw.circle(screen, BLACK, (950,75), 25)
    screen.blit(text_subtract, (945,50))

    # K =
    text_K = font.render('K = ' + str(K), True, BLACK)
    screen.blit(text_K, (1025,50))

    # button Run
    pygame.draw.rect(screen, BLACK, (825,150, 150, 50))
    screen.blit(text_Run, (875,150))

    # button Random
    pygame.draw.rect(screen, BLACK, (825,250, 150, 50))
    screen.blit(text_Random, (840,250))

    # Error =
    #text_error = font.render('Error = ' + str(error), True, BLACK)
    #screen.blit(text_error, (825, 350))

    # button Algorithm
    pygame.draw.rect(screen, BLACK, (825,450, 150, 50))
    screen.blit(text_Algorithm, (830,450))

    # button Reset
    pygame.draw.rect(screen, BLACK, (825,550, 150, 50))
    screen.blit(text_Reset, (860,550))

    # Draw mouse position
    if 55< mouse_x < 745 and 55< mouse_y < 545:
        text_mouse = font_Small.render("(" + str(mouse_x - 55) + "," + str(mouse_y -55) + ")", True, BLACK)
        screen.blit(text_mouse, (mouse_x+10, mouse_y))
    
## End draw interface

## Check Event

    for event in pygame.event.get():

        if event.type == pygame.QUIT:  
            print("END")
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # check in panel
            if 55<mouse_x<745 and 55<mouse_y<545:
                labels =[]
                point = [mouse_x-55, mouse_y-55]
                points.append(point)
                print("on panel")
            # check in press plus
            elif math.sqrt((mouse_x - 850)**2 + (mouse_y - 75)**2) <= 25:
                if K < len(COLOR):
                    K+=1
                print("press +")
            # check in press subtract
            elif math.sqrt((mouse_x - 950)**2 + (mouse_y - 75)**2) <= 25:
                if K>0:
                    K-=1
                print("press -")
            # check in press Run
            elif 825<mouse_x<975 and 150<mouse_y<200:
                labels = []

                if clusters == []:
                    continue

                for p in points:
                    distances_to_cluster = []
                    for c in clusters:
                        _distance = distance(p,c)
                        distances_to_cluster.append(_distance)
                            
                    min_distance = min(distances_to_cluster)
                    label = distances_to_cluster.index(min_distance)
                    labels.append(label)

                for i in range(K):
                    sum_x =0
                    sum_y =0
                    count =0

                    for j in range(len(points)):
                        if labels[j] == i:
                            sum_x += points[j][0]
                            sum_y += points[j][1]
                            count +=1
                    if count != 0:
                        new_cluster_x = sum_x/count
                        new_cluster_y = sum_y/count 
                        clusters[i] = [new_cluster_x, new_cluster_y]


                print("press Run")
            # check in Random
            elif 825<mouse_x<975 and 250<mouse_y<300:
                clusters = []
                labels =[]
                for i in range(K):
                    random_point = [randint(0,691), randint(0,491)]
                    clusters.append(random_point)

                print("press Random")
            # check in algorithm
            elif 825<mouse_x<975 and 450<mouse_y<500:

                kmeans = KMeans(n_clusters = K).fit(points)
                labels = kmeans.predict(points)
                clusters = kmeans.cluster_centers_

                print("press Algorithm")
            # check in reset
            elif 825<mouse_x<975 and 550<mouse_y<600:
                K = 0
                error = 0
                points =[]
                clusters = []
                labels =[]
                print("press Reset")

## Done check
        
    # Draw cluster
    for i in range(len(clusters)):
        pygame.draw.circle(screen, COLOR[i], (clusters[i][0] +55, clusters[i][1] +55), 7)
 

    # Draw point
    for i in range(len(points)):
        pygame.draw.circle(screen, BLACK, (int(points[i][0]) +55, int(points[i][1]) +55), 6)
        if labels == []:
            pygame.draw.circle(screen, WHITE, (points[i][0] +55, points[i][1] +55), 5)
        else:
            pygame.draw.circle(screen, COLOR[labels[i]], (points[i][0] +55, points[i][1] +55), 5)

     # Caculator and draw error
     
    error = 0
    if clusters != [] and labels != []:
        for i in range(len(points)):
            error += distance(points[i], clusters[labels[i]])

    
    text_error = font.render('Error = ' + str(int(error)), True, BLACK)
    screen.blit(text_error, (825, 350))







    pygame.display.flip()
    
pygame.quit()

