import pygame
import heapq
import random

pygame.init()

widthscreen = 620
heightscreen = widthscreen+200
screen = pygame.display.set_mode((widthscreen, heightscreen))
pygame.display.set_caption("Path Finder Visualizer")

white = (255, 255, 255)
black = (20, 20, 20)
hover = white
grey = (80,80,80)
red = (255,0,0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 100)
spreadcolor = (62, 95, 138)
pathcolor = (240, 240, 240)

gap = 60
marginleft = 10
margintop = 65
tablesize = widthscreen-20
myfont = pygame.font.Font(None,30)
size = 10
walls = []
startpoint = [0,0]
endpoint = [size-1,size-1]
starthover = False
endhover = False
w = tablesize // size
hold = 0
holdvisit = []
hold1 = 0
hold1visit = []
seleclist = ['Dijkstra','A*']
selected = 'Dijkstra'

tipsstatus = 0

buttonlist = []
for i in range(marginleft,tablesize+marginleft,w):
        for j in range(margintop,tablesize+margintop,w):
            buttonlist.append([i,j,black])
buttonlist[0][2] = blue
buttonlist[-1][2] = red
text = ''
already = 0
appeartext = 0

def reset():
    global text,appeartext
    appeartext = 0
    text = ''
    global buttonlist, walls, startpoint, endpoint, starthover, endhover, already, w, selected,hover
    buttonlist = []
    w = tablesize // size
    for i in range(marginleft,tablesize,w):
        for j in range(margintop,tablesize+margintop,w):
            buttonlist.append([i,j,black])
    buttonlist[0][2] = blue
    buttonlist[-1][2] = red
    walls = []
    startpoint = [0,0]
    endpoint = [size-1,size-1]
    starthover = False
    endhover = False
    hover = white
    already = 0
    selected = 'Dijkstra'
    drawbuttons()

def drawbuttons():
    global textbutton
    for [x,y,color] in buttonlist:
        pygame.draw.rect(screen, color, (x, y, w, w))
        pygame.draw.rect(screen, (60,60,60), (x, y, w, w),1)
    
    pygame.draw.rect(screen,(80,80,80),(510,10,100,40))
    generatebutton = pygame.Rect(510,10,100,40)
    generatetext = myfont.render("Generate",True,white)
    generatetextrect = generatetext.get_rect(center = generatebutton.center)
    screen.blit(generatetext,generatetextrect)
    

    buttonrestart = pygame.Rect((205, tablesize+1.5*gap , 60, 60))
    restart = pygame.image.load('Python/FindPathVisualizer/restart.png')
    restart = pygame.transform.scale(restart, (60, 60))
    restartrect = restart.get_rect(center = buttonrestart.center)   
    screen.blit(restart, restartrect)

    buttonstart = pygame.Rect((280, tablesize+1.5*gap , 60, 60))
    start = pygame.image.load('Python/FindPathVisualizer/start.png')
    start = pygame.transform.scale(start, (60, 60))
    startrect = start.get_rect(center = buttonstart.center)
    screen.blit(start, startrect)

    buttonreset = pygame.Rect((130, tablesize+1.5*gap , 60, 60))
    reset = pygame.image.load('Python/FindPathVisualizer/reset.png')
    reset = pygame.transform.scale(reset, (60, 60))
    resetrect = reset.get_rect(center = buttonreset.center)
    screen.blit(reset, resetrect)

    buttonup = pygame.Rect((355, tablesize+1.5*gap , 60, 60))
    up = pygame.image.load('Python/FindPathVisualizer/up.png')
    up = pygame.transform.scale(up, (60, 60))
    uprect = up.get_rect(center = buttonup.center)   
    screen.blit(up, uprect)

    buttondown = pygame.Rect((430, tablesize+1.5*gap , 60, 60))
    down = pygame.image.load('Python/FindPathVisualizer/down.png')
    down = pygame.transform.scale(down, (60, 60))
    downrect = down.get_rect(center = buttondown.center)   
    screen.blit(down, downrect)

    pygame.draw.rect(screen,(80,80,80),(10,10,100,40))
    selectedbutton = pygame.Rect(10,10,100,40)
    selectedtext = myfont.render(selected,True,white)
    selectedtextrect = selectedtext.get_rect(center = selectedbutton.center)
    screen.blit(selectedtext,selectedtextrect)
    
    if appeartext == 1:
        textbutton = pygame.Rect(235,tablesize + 2.8*gap,150,40)
        render = myfont.render(text,True,black)
        textrect = render.get_rect(center = textbutton.center)
        screen.blit(render,textrect)

def findpathdij(startpoint, endpoint, walls):
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

def heuristic(curpoint,endpoint):
    return abs(endpoint[0]-curpoint[0]) + abs(endpoint[1]-curpoint[1])

def findpathastar(startpoint, endpoint, walls):
    global size 
    spread = []
    start_node = tuple(startpoint)
    end_node = tuple(endpoint)
    wall_set = {tuple(w) for w in walls}
    waitlist = []
    g_costs = {start_node: 0}
    parents = {start_node: None}
    
    h_cost_start = heuristic(start_node, end_node)
    f_cost_start = g_costs[start_node] + h_cost_start
    heapq.heappush(waitlist, (f_cost_start, start_node))

    path_found = False

    while waitlist:
        spread.append([])
        current_f, current_node = heapq.heappop(waitlist)

        if current_node == end_node:
            path_found = True
            break

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)] 
        for dy, dx in directions:
            neighbor = (current_node[0] + dy, current_node[1] + dx)
            if not (0 <= neighbor[0] < size and 0 <= neighbor[1] < size):
                continue
            if neighbor in wall_set:
                continue
            new_g_cost = g_costs[current_node] + 1
            if neighbor not in g_costs or new_g_cost < g_costs[neighbor]:
                parents[neighbor] = current_node
                g_costs[neighbor] = new_g_cost
                h_cost = heuristic(neighbor, end_node)
                f_cost = new_g_cost + h_cost
                heapq.heappush(waitlist, (f_cost, neighbor))
                if neighbor != start_node and neighbor != end_node:
                    spread[-1].append(list(neighbor))
    if not path_found:
        return spread, [], 'No Path'

    path = []
    node = end_node
    while node is not None:
        path.append(list(node))
        node = parents[node]
    result_text = str(len(path) - 1) + " moves"

    return spread, path[1:-1], result_text

def generate_maze(size, startpoint):
    walls = set()
    for y in range(size):
        for x in range(size):
            walls.add((y, x))
    start_y, start_x = startpoint
    start_node = (start_y, start_x)
    if start_node in walls:
        walls.remove(start_node)
    stack = [start_node]
    max_stack_size = 1
    deepest_cell = start_node

    while stack:
        current_y, current_x = stack[-1]
        neighbors = []
        for dy, dx in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            ny, nx = current_y + dy, current_x + dx
            if 0 <= ny < size and 0 <= nx < size and (ny, nx) in walls:
                neighbors.append((ny, nx))
        if neighbors:
            next_y, next_x = random.choice(neighbors)
            next_node = (next_y, next_x)
            wall_between_y = (current_y + next_y) // 2
            wall_between_x = (current_x + next_x) // 2
            if (wall_between_y, wall_between_x) in walls:
                walls.remove((wall_between_y, wall_between_x))
            if next_node in walls:
                walls.remove(next_node)
            stack.append(next_node)
            if len(stack) > max_stack_size:
                max_stack_size = len(stack)
                deepest_cell = next_node
        else:
            stack.pop()
    final_walls_list = [list(w) for w in walls]
    return final_walls_list, list(deepest_cell)

running = True
while running:
    screen.fill(white)
    if tipsstatus == 0:
        tipsbutton = pygame.Rect(225,10,100,40)
        tipstext = myfont.render("<-- Click to change the algorithm",True,grey)
        tipstextrect = tipstext.get_rect(center = tipsbutton.center)
        screen.blit(tipstext,tipstextrect)
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
                
                if buttonlist[index][2] == black:
                    hold = 1
                    holdvisit = walls.copy()
                    holdvisit.append(index)
                    if starthover:
                        buttonlist[index][2] = blue
                        startpoint = [(y-margintop)//w, (x)//w]
                        starthover = False
                        hover = white
                    elif endhover:
                        buttonlist[index][2] = red
                        endpoint = [(y-margintop)//w, (x)//w]
                        endhover = False
                        hover = white
                    else:
                        buttonlist[index][2] = grey
                        walls.append([(y-margintop)//w,(x)//w])
                elif buttonlist[index][2] == grey:
                    hold1 = 1
                    hold1visit.append(index)
                    if starthover:
                        buttonlist[index][2] = blue
                        startpoint = [(y-margintop)//w, (x)//w]
                        walls.remove([(y-margintop)//w, (x)//w])
                        starthover = False
                        hover = white
                    elif endhover:
                        buttonlist[index][2] = red
                        endpoint = [(y-margintop)//w, (x)//w]
                        walls.remove([(y-margintop)//w,(x)//w])
                        endhover = False
                        hover = white
                    else:
                        buttonlist[index][2] = black
                        walls.remove([(y-margintop)//w,(x)//w])
                elif buttonlist[index][2] == blue:
                    if endhover:
                        buttonlist[index][2] = red
                        endpoint = [(y-margintop)//w, (x)//w]
                        endhover = False
                        starthover = True
                        hover = blue
                    else:
                        buttonlist[index][2] = black
                        startpoint = [999,999]
                        starthover = True
                        hover = blue
                elif buttonlist[index][2] == red:
                    if starthover:
                        buttonlist[index][2] = blue
                        startpoint = [(y-margintop)//w, (x)//w]
                        starthover = False
                        endhover = True
                        hover = red
                    else:
                        buttonlist[index][2] = black
                        endpoint = [999,999]
                        endhover = True
                        hover = red
                pygame.draw.rect(screen, buttonlist[index][2], (x, y, w, w))
            elif 280<location[0]<340 and tablesize+1.5*gap<location[1]<tablesize+1.5*gap+60 and already == 0:
                global results
                if selected == "Dijkstra":
                    spreadpattern,results,text = findpathdij(startpoint, endpoint, walls)
                else:
                    spreadpattern,results,text = findpathastar(startpoint, endpoint, walls)
                for k in spreadpattern:
                    if k != []:
                        for [i,j] in k:
                            if [i,j] != endpoint:
                                buttonlist[j*size+i][2] = spreadcolor
                        drawbuttons()
                        pygame.display.flip()
                        pygame.time.wait(1)
                for [i,j] in results[::-1]:
                    buttonlist[j*size+i][2] = pathcolor
                    drawbuttons()
                    pygame.display.flip()
                    pygame.time.wait(10)
                appeartext = 1
                already = 1
                drawbuttons()
            elif 205<location[0]<265 and tablesize+1.5*gap<location[1]<tablesize+1.5*gap+60 and already == 1:
                for k in spreadpattern:
                    for [i,j] in k:
                        if [i,j] != endpoint:
                            buttonlist[j*size+i][2] = black
                for [i,j] in results:
                    buttonlist[j*size+i][2] = black
                already = 0
                appeartext = 0
                drawbuttons()
            elif 130<location[0]<190 and tablesize+1.5*gap<location[1]<tablesize+1.5*gap+60:
                reset()
            elif 355<location[0]<415 and tablesize+1.5*gap<location[1]<tablesize+1.5*gap+60 and already == 0:
                if size == 10:
                    size = 20
                    reset()
                elif size == 20:
                    size = 30
                    reset()
            elif 430<location[0]<490 and tablesize+1.5*gap<location[1]<tablesize+1.5*gap+60 and already == 0:
                if size == 30:
                    size = 20
                    reset()
                elif size == 20:
                    size = 10
                    reset()
            elif 10<location[0]<110 and 10<location[1]<50 and already == 0:
                tipsstatus = 1
                if selected == "Dijkstra":
                    selected = 'A*'
                else:
                    selected = "Dijkstra"
            elif 510 < location[0] < 610 and 10 < location[1] < 50 and already == 0:
                generated_walls, newend = generate_maze(size, startpoint)
                walls = generated_walls
                endpoint = newend
                for y in range(size):
                    for x in range(size):
                        index = x * size + y
                        if [y, x] == startpoint:
                            buttonlist[index][2] = blue
                        elif [y, x] == endpoint:
                            buttonlist[index][2] = red
                        elif [y, x] in walls:
                            buttonlist[index][2] = grey
                        else:
                            buttonlist[index][2] = black
                    drawbuttons()
                    pygame.display.flip()
                    pygame.time.wait(1)
        elif event.type == pygame.MOUSEBUTTONUP:
            hold = 0
            holdvisit = []
            hold1 = 0
            hold1visit = []
        pygame.display.flip()
    location = pygame.mouse.get_pos()
    if (marginleft-1<location[0]<tablesize+marginleft) and (margintop-1<location[1]<tablesize+margintop) and already == 0:
        x = ((location[0]-marginleft)//w)*w + marginleft
        y = ((location[1]-margintop)//w)*w + margintop
        index = (y-margintop)//w + (x)//(w) * size
        if hold == 1 and index not in holdvisit and not starthover and not endhover:
            if index not in [startpoint[0]+startpoint[1]*size,endpoint[0]+endpoint[1]*size]:
                if buttonlist[index][2] == black:
                    buttonlist[index][2] = grey
                    walls.append([(y-margintop)//w,(x)//w])
                holdvisit.append(index)
                drawbuttons()
        elif hold1 == 1 and index not in hold1visit and not starthover and not endhover:
            if index not in [startpoint[0]+startpoint[1]*size,endpoint[0]+endpoint[1]*size]:
                if buttonlist[index][2] == grey:
                    buttonlist[index][2] = black
                    walls.remove([(y-margintop)//w,(x)//w])
                hold1visit.append(index)
                drawbuttons()
        else:
            pygame.draw.rect(screen, hover, (x, y, w, w),5)
    elif 130<location[0]<190 and tablesize+1.5*gap<location[1]<tablesize+1.5*gap+60:
        pygame.draw.rect(screen,black,(130, tablesize+1.5*gap , 60, 60),3)
    elif 355<location[0]<415 and tablesize+1.5*gap<location[1]<tablesize+1.5*gap+60:
        pygame.draw.rect(screen,black,(355, tablesize+1.5*gap , 60, 60),3)
    elif 430<location[0]<490 and tablesize+1.5*gap<location[1]<tablesize+1.5*gap+60:
        pygame.draw.rect(screen,black,(430, tablesize+1.5*gap , 60, 60),3)
    elif 205<location[0]<265 and tablesize+1.5*gap<location[1]<tablesize+1.5*gap+60:
        pygame.draw.rect(screen,black,(205, tablesize+1.5*gap , 60, 60),3)
    elif 280<location[0]<340 and tablesize+1.5*gap<location[1]<tablesize+1.5*gap+60:
        pygame.draw.rect(screen,black,(280, tablesize+1.5*gap , 60, 60),3)
    elif 510 < location[0] < 610 and 10 < location[1] < 50:
        pygame.draw.rect(screen,(150,150,150),(510,10,100,40))
        generatebutton = pygame.Rect(510,10,100,40)
        generatetext = myfont.render("Generate",True,white)
        generatetextrect = generatetext.get_rect(center = generatebutton.center)
        screen.blit(generatetext,generatetextrect)
    elif 10<location[0]<110 and 10<location[1]<50:
        pygame.draw.rect(screen,(150,150,150),(10,10,100,40))
        selectedbutton = pygame.Rect(10,10,100,40)
        selectedtext = myfont.render(selected,True,white)
        selectedtextrect = selectedtext.get_rect(center = selectedbutton.center)
        screen.blit(selectedtext,selectedtextrect)
    pygame.display.flip()
pygame.quit()
