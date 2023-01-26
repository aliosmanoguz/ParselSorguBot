from math import atan2, sqrt, pi
import matplotlib.pyplot as plt

# mesafeyi olcer
def distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# en yakin noktayi bulur
def closestPoint(arr):
    smallest = arr[0]
    for num in arr:
        if smallest > num:
            smallest = num
    return arr.index(smallest)

# dugumlerin koselere gore acisini hesaplar
def angle2d(x1, y1, x2, y2):
    theta1 = atan2(y1, x1)
    theta2 = atan2(y2, x2)
    dtheta = theta2 - theta1
    if dtheta > pi:
        dtheta -= 2 * pi
    if dtheta < -pi:
        dtheta += 2 * pi

    return dtheta

# dugumler seklin icinde olup olmadigini tespit eder
def insideShape(shapeX, shapeY, x, y):
    angle = 0
    for i in range(len(shapeX)):
        p1H = shapeX[i] - x
        p1V = shapeY[i] - y
        p2H = shapeX[(i + 1) % (len(shapeX) - 1)] - x
        p2V = shapeY[(i + 1) % (len(shapeX) - 1)] - y
        angle += angle2d(p1H, p1V, p2H, p2V)

    if abs(angle) < pi:
        return False
    return True

# dugumleri siralar
def sortingNodes(allNodes, startNode, cornerX, cornerY):
    if startNode[0] == min(cornerX):
        return selectionSort(allNodes, True)

    elif startNode[0] == max(cornerX):
        arr = selectionSort(allNodes, True)
        arr.reverse()
        return arr

    elif startNode[1] == min(cornerY):
        return selectionSort(allNodes, False)

    elif startNode[1] == max(cornerY):
        arr = selectionSort(allNodes, False)
        arr.reverse()
        return arr

# quicksort algoritmasi
def quickSort(arr, xORy):
    if xORy == True:
        dr = 0
    else:
        dr = 1

    length = len(arr)
    if length <= 1:
        return arr

    else:
        pivot = arr.pop()

    items_greater = []
    items_lower = []

    for item in arr:
        if item[dr] > pivot[dr]:
            items_greater.append(item)
        else:
            items_lower.append(item)

    return quickSort(items_lower, xORy) + [pivot] + quickSort(items_greater, xORy)

def selectionSort(arr, xORy):
    if xORy == True:
        dr = 0
    else:
        dr = 1

    for i in range(len(arr) - 1):
        min = i

        for j in range(i + 1, len(arr)):
            if arr[j][dr] < arr[min][dr]:
                min = j

        if min != i:
            arr[min], arr[i] = arr[i], arr[min]

    return arr

def divideLine(allNodes, xORy):
    if xORy == True:
        dr = 0
    else:
        dr = 1

    divided = list()
    currentIndex = 0
    while currentIndex < len(allNodes):
        arr = list()
        match = allNodes[currentIndex][dr]
        for node in allNodes:
            if node[dr] == match:
                arr.append(node)
                currentIndex += 1

        arr = selectionSort(arr, not xORy)
        divided.append(arr)

    return divided

def createPath(divided):
    path = list()
    for arr in divided:
        if divided.index(arr) % 2 == 0:
            arr.reverse()

        for node in arr:
            path.append(node)

    return path

x = []
y = []

def rotaHesapla(x,y):

    x = list(map((lambda node: round(node * 100000)), x))
    y = list(map((lambda node: round(node * 100000)), y))

    startCorner = [min(x), y[x.index(min(x))]]
    if min(x) == startCorner[0] or max(x) == startCorner[0]:
       xORy = True
    else:
       xORy = False

    plt.plot(x, y)
    # plt.plot([droneCoordinates[0], x[s]], [droneCoordinates[1], y[s]])

    allNodes = list()
    if xORy:
        for i in range((max(x) - min(x) + 1)):
            for j in range((max(y) - min(y) + 1)):
               if insideShape(x, y, min(x) + i, min(y) + j):
                    # plt.plot(min(x) + i * 0.25, min(y) + j * 0.25, "o", color = "red")
                    allNodes.append([min(x) + i, min(y) + j])

    else:
        for i in range(10 * (max(x) - min(x) + 1)):
            for j in range(20 * (max(y) - min(y) + 1)):
                if insideShape(x, y, min(x) + i * 0.1, min(y) + j * 0.05):
                    # plt.plot(min(x) + i * 0.2, min(y) + j * 0.2, "o", color = "red")
                    allNodes.append([min(x) + i * 0.1, min(y) + j * 0.05])

    for i in range(len(x) - 1):
        # plt.plot(x[i], y[i], "o", color = "red")
        allNodes.append([x[i], y[i]])

    divided = divideLine(sortingNodes(allNodes, startCorner, x, y), xORy)
    # print(divided)
    path = createPath(divided)

    # dugumleri printle
    # print(path)

    for i in range(len(path)):
        if i != len(path) - 1:
            plt.plot([path[i][0], path[(i + 1) % (len(path))][0]], [path[i][1], path[(i + 1) % (len(path))][1]],color="red")

    plt.show()
    return path

# x1 = []
# y1 = []

# xy = [[39.79715, 32.80792], [39.79717, 32.80789], [39.79731, 32.80771], [39.79714, 32.80754], [39.79699, 32.8077], [39.79715, 32.80792]]
#xy = [[38.98452, 32.94779], [38.9849, 32.94844], [38.98538, 32.94935], [38.98576, 32.95011], [38.98602, 32.95056], [38.98763, 32.9468], [38.98705, 32.94623], [38.98678, 32.94598], [38.98645, 32.94563], [38.98576, 32.94483], [38.98452, 32.94779]]
#xy = [[38.97813, 32.94791], [38.97815, 32.94886], [38.97815, 32.95041], [38.97818, 32.95066], [38.9783, 32.95089], [38.97839, 32.951], [38.98104, 32.95017], [38.98108, 32.9494], [38.98103, 32.94894], [38.9809, 32.94782], [38.97813, 32.94791]]
#xy = [[39.01092, 32.97338], [39.01144, 32.97649], [39.01146, 32.97663], [39.01153, 32.97662], [39.01183, 32.97663], [39.01201, 32.97662], [39.01208, 32.97662], [39.01221, 32.9766], [39.01242, 32.97655], [39.01328, 32.97639], [39.01266, 32.9734], [39.01255, 32.97289], [39.0116, 32.97317], [39.01092, 32.97338]]
#xy = [[39.01311, 32.97326], [39.01266, 32.9734], [39.01328, 32.97639], [39.01372, 32.97629], [39.01332, 32.97426], [39.01311, 32.97326]]

# x1 = []
# y1 = []
#
# for i in range(len(xy)):
#     x1.append(xy[i][0])
#     y1.append(xy[i][1])
#
# rotaHesapla(x1,y1)

# x = [0,110,110,221,221,333,333,443,443,555,555,665,665,777,777,887,887,999,999,1109,1109,1220,1220,1332,1332,1442,1442,1554,1554,1664,1664,1776,1776,1886,1886,1998,1998,2108,2108,2219,2219,2330,2330,2441,2441,2553,2553,2663,2663,2775,2775,2885,2885,2997,2997,3107,3107,3218,3218,3329,3329,3440,3440,3552]
# y = [0,-110,111,222,-221,-332,444,555,-443,-554,666,888,-665,-776,999,1110,-887,-999,1332,1443,-1109,-1220,1665,1776,-1331,-1442,1887,2109,-1553,-1775,2219,2442,-1664,-1553,2219,2109,-1442,-1331,1887,1776,-1220,-1109,1665,1443,-999,-887,1332,1221,-776,-665,1110,888,-554,-443,777,666,-332,-221,444,333,-110,0,222,111]
#
# print(len(x))
#
# plt.plot(x,y)
# plt.show()