size = input()

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