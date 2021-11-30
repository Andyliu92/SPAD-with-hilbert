from PIL import Image, ImageDraw
import sys
import copy
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


def hilbert(order, ptlist):
    index = order - 1
    shift = 2**(order)
    res_list = []

    # SW block
    temp_list = copy.deepcopy(ptlist[index])
    flip1(temp_list, [shift, shift])
    for i in range(0, len(temp_list), 1):
        res_list.append(temp_list[i])

    # NW block
    temp_list = []
    for i in range(0, len(ptlist[index])):
        temp_list.append(copy.deepcopy(
            [ptlist[index][i][0], ptlist[index][i][1]+shift]))
    for i in range(0, len(temp_list), 1):
        res_list.append(temp_list[i])

    # NE block
    temp_list = []
    for i in range(0, len(ptlist[index])):
        temp_list.append(copy.deepcopy([ptlist[index][i][0]+shift,
                         ptlist[index][i][1]+shift]))
    for i in range(0, len(temp_list), 1):
        res_list.append(temp_list[i])

    # SE block
    temp_list = []
    for i in range(0, len(ptlist[index])):
        temp_list.append(copy.deepcopy(
            [ptlist[index][i][0]+shift, ptlist[index][i][1]]))
    flip4(temp_list, [shift+1, shift])
    for i in range(0, len(temp_list), 1):
        res_list.append(temp_list[i])

    return res_list


print("The order of hilbert's curve?")
order = int(input())
scale = 3

time_start = time.time()

if order <= 0:
    print("order <= 0 !")
    sys.exit(0)

ptlist = [[[1, 1], [1, 2], [2, 2], [2, 1]]]


for i in range(2, order+1):
    current_list = hilbert(i-1, ptlist)
    ptlist.append(current_list)
    print("finished order:", i)

time_end = time.time()
print('Time cost = %fs' % (time_end - time_start))

result = ptlist[order-1]

blockConvert(result, scale=scale)

imglen = (2**order)*scale+int(scale/2)

img = Image.new("RGB", (imglen,
                imglen), (255, 255, 255))
draw = ImageDraw.Draw(img)


for i in range(1, len(result)):
    draw.line((result[i-1][0], imglen - result[i-1][1],
              result[i][0], imglen - result[i][1]), 'black')

img.show()
img.save(str(order) + ' order hilbert curve.jpg')


input()
