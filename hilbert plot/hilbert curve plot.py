import turtle
import time


def flip1(pointlist, ne):
    for i in range(0, len(pointlist), 1):
        new_x = ne[0] - ne[1] + pointlist[i][1]
        new_y = ne[1] - ne[0] + pointlist[i][0]
        pointlist[i][0] = new_x
        pointlist[i][1] = new_y
    return pointlist


def flip4(pointlist, nw):
    for i in range(0, len(pointlist), 1):
        new_x = nw[0] + nw[1] - pointlist[i][1]
        new_y = nw[0] + nw[1] - pointlist[i][0]
        pointlist[i][0] = new_x
        pointlist[i][1] = new_y
    return pointlist


def blockConvert(pointlist, scale=10):
    for i in range(0, len(pointlist), 1):
        pointlist[i] = [pointlist[i][0]*scale-1, pointlist[i][1]*scale-1]
    return pointlist


def hilbert(order, nw=0, se=0, init=True, scale=10):
    res_list = []
    if init == True:  # first-time run : automatically determine the size
        nw = [1, 2 ** order]
        se = [2 ** order, 1]

    if order <= 0:  # some error must occurred to make order <= 0.
        return

    if order == 1:  # end condition for recursive
        return [[nw[0], se[1]], [nw[0], nw[1]], [se[0], nw[1]], [se[0], se[1]]]

    # if not 1 order, solve recursively.

    # SW block
    nw_temp = [nw[0], int(se[1] + (nw[1]-se[1]-1)/2)]
    se_temp = [int(nw[0]+(se[0]-nw[0]-1)/2), se[1]]
    temp_list = hilbert(order-1, nw_temp, se_temp, False, scale=scale)
    flip1(temp_list, [se_temp[0], nw_temp[1]])
    for i in range(0, len(temp_list), 1):
        res_list.append(temp_list[i])

    # NW block
    nw_temp = nw
    se_temp = [nw[0] + int((se[0]-nw[0]-1)/2), se[1] + int((nw[1]-se[1]+1)/2)]
    temp_list = hilbert(order-1, nw_temp, se_temp, False, scale=scale)
    for i in range(0, len(temp_list), 1):
        res_list.append(temp_list[i])

    # NE block
    nw_temp = [nw[0] + int((se[0] - nw[0]+1)/2), nw[1]]
    se_temp = [se[0], se[1] + int((nw[1] - se[1]+2)/2)]
    temp_list = hilbert(order-1, nw_temp, se_temp, False, scale=scale)
    for i in range(0, len(temp_list), 1):
        res_list.append(temp_list[i])

    # SE block
    nw_temp = [nw[0]+int((se[0]-nw[0]+1)/2), se[1]+int((nw[1]-se[1]-1)/2)]
    se_temp = se
    temp_list = hilbert(order-1, nw_temp, se_temp, False, scale=scale)
    flip4(temp_list, nw_temp)
    for i in range(0, len(temp_list), 1):
        res_list.append(temp_list[i])

    return res_list


def drawPointList(pointlist):
    for pt in pointlist:
        turtle.goto(pt[0], pt[1])


print("The order of hilbert's curve?")
order = int(input())
scale = 10

time_start = time.time()


pointlist = hilbert(order, scale=scale)

time_end = time.time()
print('Time cost = %fs' % (time_end - time_start))

blockConvert(pointlist, scale=scale)


turtle.screensize(3000, 3000, 'white')
turtle.up()
turtle.goto(pointlist[0][0], pointlist[0][1])
turtle.down()
drawPointList(pointlist)

input()
