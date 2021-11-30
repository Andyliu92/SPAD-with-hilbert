from PIL import Image, ImageDraw

hilbertOrder = 5
hilbertScale = 10
hilbertList = [[[1, 1], [1, 2], [2, 2], [2, 1]]]

if __name__ == '__main__':
    # Hilbert
    for i in range(1, hilbertOrder):
        tmpPower = 2 ** i
        hilbertList.append([])
        listSize = len(hilbertList[i - 1])

        # SW Block
        for j in range(0, listSize):
            hilbertList[i].append(
                [hilbertList[i - 1][j][1], hilbertList[i - 1][j][0]])

        # NW Block
        for j in range(0, listSize):
            hilbertList[i].append(
                [hilbertList[i - 1][j][0], hilbertList[i - 1][j][1] + tmpPower])

        # NE Block
        for j in range(0, listSize):
            hilbertList[i].append(
                [hilbertList[i - 1][j][0] + tmpPower, hilbertList[i - 1][j][1] + tmpPower])

        # SE Block
        for j in range(0, listSize):
            hilbertList[i].append(
                [tmpPower * 2 + 1 - hilbertList[i - 1][j][1], tmpPower + 1 - (hilbertList[i - 1][j][0])])

    hibertResult = hilbertList[hilbertOrder - 1]

    # Scaling
    for i in range(0, len(hibertResult)):
        hibertResult[i][0] = hibertResult[i][0] * hilbertScale - 1
        hibertResult[i][1] = hibertResult[i][1] * hilbertScale - 1

    # Image
    imgSize = (2 ** hilbertOrder) * hilbertScale + int(hilbertScale / 2)
    img = Image.new("RGB", (imgSize, imgSize), (255, 255, 255))
    imgDraw = ImageDraw.Draw(img)

    for i in range(1, len(hibertResult)):
        imgDraw.line(
            (hibertResult[i - 1][0], imgSize - hibertResult[i - 1][1],
                hibertResult[i][0], imgSize - hibertResult[i][1]),
            'black')

    img.show()
