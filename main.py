import pygame

pygame.init()

widthscreen = 620
heightscreen = widthscreen+200
screen = pygame.display.set_mode((widthscreen, heightscreen))
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

gap = 60
marginleft = 10
margintop = 30
tablesize = widthscreen-20
myfont = pygame.font.Font(None,40)
size = 10
walls = []
startpoint = [0,0]
endpoint = [size-1,size-1]
starthover = False
endhover = False
w = tablesize // size

buttonlist = []
for i in range(marginleft,tablesize+marginleft,w):
        for j in range(margintop,tablesize+margintop,w):
            buttonlist.append([i,j,grey])
buttonlist[0][2] = blue
buttonlist[-1][2] = green
text = ''
already = 0
appeartext = 0

def reset():
    global text,appeartext
    appeartext = 0
    text = ''
    global buttonlist, walls, startpoint, endpoint, starthover, endhover, already, w
    buttonlist = []
    w = tablesize // size
    for i in range(marginleft,tablesize,w):
        for j in range(margintop,tablesize+margintop,w):
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
    global textbutton
    for [x,y,color] in buttonlist:
        pygame.draw.rect(screen, color, (x, y, w, w))
        pygame.draw.rect(screen, black, (x, y, w, w),1)
    
    buttonrestart = pygame.Rect((205, tablesize+gap , 60, 60))
    restart = pygame.image.load('Python/FindPathVisualizer/restart.png')
    restart = pygame.transform.scale(restart, (60, 60))
    restartrect = restart.get_rect(center = buttonrestart.center)   
    screen.blit(restart, restartrect)

    buttonstart = pygame.Rect((280, tablesize+gap , 60, 60))
    start = pygame.image.load('Python/FindPathVisualizer/start.png')
    start = pygame.transform.scale(start, (60, 60))
    startrect = start.get_rect(center = buttonstart.center)
    screen.blit(start, startrect)

    buttonreset = pygame.Rect((130, tablesize+gap , 60, 60))
    reset = pygame.image.load('Python/FindPathVisualizer/reset.png')
    reset = pygame.transform.scale(reset, (60, 60))
    resetrect = reset.get_rect(center = buttonreset.center)
    screen.blit(reset, resetrect)

    buttonup = pygame.Rect((355, tablesize+gap , 60, 60))
    up = pygame.image.load('Python/FindPathVisualizer/up.png')
    up = pygame.transform.scale(up, (60, 60))
    uprect = up.get_rect(center = buttonup.center)   
    screen.blit(up, uprect)

    buttondown = pygame.Rect((430, tablesize+gap , 60, 60))
    down = pygame.image.load('Python/FindPathVisualizer/down.png')
    down = pygame.transform.scale(down, (60, 60))
    downrect = down.get_rect(center = buttondown.center)   
    screen.blit(down, downrect)

    if appeartext == 1:
        textbutton = pygame.Rect(235,tablesize + 2.5*gap,150,40)
        render = myfont.render(text,True,black)
        textrect = render.get_rect(center = textbutton.center)
        screen.blit(render,textrect)

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
                    text = str(lis[endpoint[0]][endpoint[1]]) + ' moves'
                    return spread,optimalpath,text
                break
    optimalpath = []
    test = path[endpoint[0]*size+endpoint[1]]
    if test == []:
        text = 'No path'
        return spread,[],text
    else:
        prev = test[0]
        while prev != startpoint:
            optimalpath.append(prev)
            prev = path[prev[0]*size+prev[1]][0]
        text = str(lis[endpoint[0]][endpoint[1]]) + ' moves'
        return spread,optimalpath,text
running = True
while running:
    screen.fill(white)
    drawbuttons()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            location = pygame.mouse.get_pos()
            if (marginleft-1<location[0]<tablesize+marginleft) and (margintop-1<location[1]<tablesize+margintop and already == 0):
                x = ((location[0]-marginleft)//w)*w + marginleft
                y = ((location[1]-margintop)//w)*w + margintop
                index = (y-margintop)//w + (x)//(w) * size

                if buttonlist[index][2] == grey:
                    if starthover:
                        buttonlist[index][2] = blue
                        startpoint = [(y-margintop)//w, (x)//w]
                        starthover = False
                        hover = (100,100,100)
                    elif endhover:
                        buttonlist[index][2] = green
                        endpoint = [(y-margintop)//w, (x)//w]
                        endhover = False
                        hover = (100,100,100)
                    else:
                        buttonlist[index][2] = red
                        walls.append([(y-margintop)//w,(x)//w])
                elif buttonlist[index][2] == red:
                    if starthover:
                        buttonlist[index][2] = blue
                        startpoint = [(y-margintop)//w, (x)//w]
                        walls.remove([(y-margintop)//w, (x)//w])
                        starthover = False
                        hover = (100,100,100)
                    elif endhover:
                        buttonlist[index][2] = green
                        endpoint = [(y-margintop)//w, (x)//w]
                        walls.remove([(y-margintop)//w,(x)//w])
                        endhover = False
                        hover = (100,100,100)
                    else:
                        buttonlist[index][2] = grey
                        walls.remove([(y-margintop)//w,(x)//w])
                elif buttonlist[index][2] == blue:
                    if endhover:
                        buttonlist[index][2] = green
                        endpoint = [(y-margintop)//w, (x)//w]
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
                        startpoint = [(y-margintop)//w, (x)//w]
                        starthover = False
                        endhover = True
                        hover = (100, 255, 100)
                    else:
                        buttonlist[index][2] = grey
                        endpoint = [999,999]
                        endhover = True
                        hover = (100, 255, 100)
                pygame.draw.rect(screen, buttonlist[index][2], (x, y, w, w))
            elif 280<location[0]<340 and tablesize+gap<location[1]<tablesize+gap+60 and already == 0:
                global results
                spreadpattern,results,text = findpath(startpoint, endpoint, walls)
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
                appeartext = 1
                drawbuttons()
            elif 205<location[0]<265 and tablesize+gap<location[1]<tablesize+gap+60 and already == 1:
                for k in spreadpattern:
                    for [i,j] in k:
                        if [i,j] != endpoint:
                            buttonlist[j*size+i][2] = grey
                for [i,j] in results:
                    buttonlist[j*size+i][2] = grey
                already = 0
                appeartext = 0
                drawbuttons()
            elif 130<location[0]<190 and tablesize+gap<location[1]<tablesize+gap+60:
                reset()
            elif 355<location[0]<415 and tablesize+gap<location[1]<tablesize+gap+60 and already == 0:
                if size == 10:
                    size = 20
                    reset()
                elif size == 20:
                    size = 30
                    reset()
            elif 430<location[0]<490 and tablesize+gap<location[1]<tablesize+gap+60 and already == 0:
                if size == 30:
                    size = 20
                    reset()
                elif size == 20:
                    size = 10
                    reset()
        pygame.display.flip()
    location = pygame.mouse.get_pos()
    if (marginleft-1<location[0]<tablesize+marginleft) and (margintop-1<location[1]<tablesize+margintop) and already == 0:
        x = ((location[0]-marginleft)//w)*w + marginleft
        y = ((location[1]-margintop)//w)*w + margintop
        pygame.draw.rect(screen, hover, (x, y, w, w))
    pygame.display.flip()

pygame.quit()
