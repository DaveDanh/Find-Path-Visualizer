import pygame

pygame.init()

screen = pygame.display.set_mode((500, 550))
pygame.display.set_caption("Path Finder Visualizer")

white = (255, 255, 255)
black = (0, 0, 0)
hover =  (100, 100, 100)
grey = (150, 150, 150)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 100)
pink = (255,192,203)

size =40
walls = []
startpoint = [0,0]
endpoint = [size-1,size-1]
starthover = False
endhover = False
w = 400 // size

cache = []
buttonlist = []
for i in range(50,450,w):
        for j in range(30,430,w):
            buttonlist.append([i,j,grey])
buttonlist[0][2] = blue
buttonlist[-1][2] = green

already = 0

def reset():
    global buttonlist, walls, startpoint, endpoint, starthover, endhover, already
    buttonlist = []
    for i in range(50,450,w):
        for j in range(30,430,w):
            buttonlist.append([i,j,grey])
    buttonlist[0][2] = blue
    buttonlist[-1][2] = green
    walls = []
    startpoint = [0,0]
    endpoint = [size-1,size-1]
    starthover = False
    endhover = False
    already = 0
    drawbuttons()

def drawbuttons():
    for [x,y,color] in buttonlist:
        pygame.draw.rect(screen, color, (x, y, w, w))
    
    buttonrestart = pygame.Rect((75, 460 , 60, 60))
    restart = pygame.image.load('Python/FindPathVisualizer/restart.png')
    restart = pygame.transform.scale(restart, (60, 60))
    restartrect = restart.get_rect(center = buttonrestart.center)
    screen.blit(restart, restartrect)

    buttonstart = pygame.Rect((225, 460 , 60, 60))
    start = pygame.image.load('Python/FindPathVisualizer/start.jpg')
    start = pygame.transform.scale(start, (60, 60))
    startrect = start.get_rect(center = buttonstart.center)
    screen.blit(start, startrect)

    buttonreset = pygame.Rect((375, 460 , 60, 60))
    reset = pygame.image.load('Python/FindPathVisualizer/reset.png')
    reset = pygame.transform.scale(reset, (60, 60))
    resetrect = reset.get_rect(center = buttonreset.center)
    screen.blit(reset, resetrect)

def findpath(startpoint, endpoint, walls):
    spread = []
    firststatus = []
    firstlis = []
    status = []
    lis = []
    for i in range(size):
        firststatus.append(False)
        firstlis.append(999)
    for i in range(size):
        status.append(firststatus.copy())
        lis.append(firstlis.copy())
    path = [[] for _ in range(size) for _ in range(size)]
    waitlist = []
    waitlist.append(startpoint)
    lis[startpoint[0]][startpoint[1]] = 0
    y = startpoint[0]
    x = startpoint[1]
    recur = 0
    while waitlist != [] or recur < 100:
        if waitlist == []:
            recur += 1
        else:
            recur = 0
        spread.append([])
        new = []
        direction  = [[y+1,x],[y-1,x],[y,x+1],[y,x-1]]
        for [i,j] in direction:
            if 0 <= i < size and 0 <= j < size:
                if [i,j] not in walls:
                    if status[i][j] == False:
                        new.append([i,j])
                        waitlist.append([i,j])
        for [i,j] in new:
            if status[i][j] == False:
                spread[-1].append([i,j])
                if lis[i][j] > lis[y][x]+1:
                    lis[i][j] = lis[y][x]+1
                    path[i*size+j].append([y,x])
        status[y][x] = True
        for [i,j] in waitlist:
            if status[i][j] == True:
                waitlist.remove([i,j])
            else:
                y = waitlist[0][0]
                x = waitlist[0][1]
                waitlist.pop(0)
                if [y,x] == endpoint:
                    optimalpath = []
                    test = path[endpoint[0]*size+endpoint[1]]
                    prev = test[0]
                    while prev != startpoint:
                        optimalpath.append(prev)
                        prev = path[prev[0]*size+prev[1]][0]
                    print("It takes %s moves" %lis[endpoint[0]][endpoint[1]])
                    return spread,optimalpath
                break
    optimalpath = []
    test = path[endpoint[0]*size+endpoint[1]]
    if test == []:
        print("No Path Found")
        return spread,[]
    else:
        prev = test[0]
        while prev != startpoint:
            optimalpath.append(prev)
            prev = path[prev[0]*size+prev[1]][0]
        print("It takes %s moves" %lis[endpoint[0]][endpoint[1]])
        return spread,optimalpath
running = True
while running:
    screen.fill(white)
    drawbuttons()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            location = pygame.mouse.get_pos()
            if (49<location[0]<451) and (29<location[1]<431 and already == 0):
                x = ((location[0]-50)//w)*w + 50
                y = ((location[1]-30)//w)*w + 30
                index = (y-30)//w + (x-50)//(w) * size

                if buttonlist[index][2] == grey:
                    if starthover:
                        buttonlist[index][2] = blue
                        startpoint = [(y-30)//w, (x-50)//w]
                        starthover = False
                        hover = (100,100,100)
                    elif endhover:
                        buttonlist[index][2] = green
                        endpoint = [(y-30)//w, (x-50)//w]
                        endhover = False
                        hover = (100,100,100)
                    else:
                        buttonlist[index][2] = red
                        walls.append([(y-30)//w,(x-50)//w])
                elif buttonlist[index][2] == red:
                    if starthover:
                        buttonlist[index][2] = blue
                        startpoint = [(y-30)//w, (x-50)//w]
                        walls.remove([(y-30)//w, (x-50)//w])
                        starthover = False
                        hover = (100,100,100)
                    elif endhover:
                        buttonlist[index][2] = green
                        endpoint = [(y-30)//w, (x-50)//w]
                        walls.remove([(y-30)//w,(x-50)//w])
                        endhover = False
                        hover = (100,100,100)
                    else:
                        buttonlist[index][2] = grey
                        walls.remove([(y-30)//w,(x-50)//w])
                elif buttonlist[index][2] == blue:
                    if endhover:
                        buttonlist[index][2] = green
                        endpoint = [(y-30)//w, (x-50)//w]
                        endhover = False
                        starthover = True
                        hover = (100, 100, 255)
                    else:
                        buttonlist[index][2] = grey
                        startpoint = [999,999]
                        starthover = True
                        hover = (100, 100, 255)
                elif buttonlist[index][2] == green:
                    if starthover:
                        buttonlist[index][2] = blue
                        startpoint = [(y-30)//w, (x-50)//w]
                        starthover = False
                        endhover = True
                        hover = (100, 255, 100)
                    else:
                        buttonlist[index][2] = grey
                        endpoint = [999,999]
                        endhover = True
                        hover = (100, 255, 100)
                pygame.draw.rect(screen, buttonlist[index][2], (x, y, w, w))
            elif 225<location[0]<285 and 460<location[1]<520 and already == 0:
                cache = buttonlist.copy()
                global results
                spreadpattern,results = findpath(startpoint, endpoint, walls)
                already = 1
                for k in spreadpattern:
                    if k != []:
                        for [i,j] in k:
                            if [i,j] != endpoint:
                                buttonlist[j*size+i][2] = yellow
                        drawbuttons()
                        pygame.display.flip()
                        pygame.time.wait(1)
                for [i,j] in results:
                    buttonlist[j*size+i][2] = pink
            elif 75<location[0]<135 and 460<location[1]<520 and already == 1:
                for k in spreadpattern:
                    for [i,j] in k:
                        if [i,j] != endpoint:
                            buttonlist[j*size+i][2] = grey
                for [i,j] in results:
                    buttonlist[j*size+i][2] = grey
                already = 0
                drawbuttons()
            elif 375<location[0]<435 and 460<location[1]<520:
                reset()
        pygame.display.flip()
    location = pygame.mouse.get_pos()
    if (49<location[0]<450) and (29<location[1]<430) and already == 0:
        x = ((location[0]-50)//w)*w + 50
        y = ((location[1]-30)//w)*w + 30
        pygame.draw.rect(screen, hover, (x, y, w, w))
    pygame.display.flip()

pygame.quit()