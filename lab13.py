import math
import numpy as np
import matplotlib.pyplot as plt

class Node:
    def __init__(self, point):
        self.point = point
        self.f = 999999999
        self.g = 999999999
        self.h = 999999999
        self.parent = None

def adjacent(m, pos):
    """
    Computes a list of adjacent cells for the given map and position
    :param m: Map of the environment (numpy matrix)
    :param pos: Query Position Tuple (row, column), 0-based
    :return: list of adjacent positions
    """
    result = []
    if pos[0] > 0 and m[pos[0] - 1, pos[1]] == 0:
        result.append((pos[0] - 1, pos[1]))
    if pos[0] < m.shape[0] - 1 and m[pos[0] + 1, pos[1]] == 0:
        result.append((pos[0] + 1, pos[1]))
    if pos[1] > 0 and m[pos[0], pos[1] - 1] == 0:
        result.append((pos[0], pos[1] - 1))
    if pos[1] < m.shape[1] - 1 and m[pos[0], pos[1] + 1] == 0:
        result.append((pos[0], pos[1] + 1))
    return result

def EuclideanDistance(start, goal):
    return math.sqrt((math.pow(start[0] - goal[0], 2)) + (math.pow(start[1] - goal[1], 2)))

def addNodeToClosedList(m, node, closedList, openList, goalPoint):
    closedList.append(node)
    
    #Now remove node from openList
    openList.remove(node)
    
    #Now add successors to Open List
    successors = adjacent(m, (node.point))
    for point in successors:
        #make it a node
        newNode = Node(point)
        newNode.parent = node
        newNode.g = node.g + 1
        newNode.h = EuclideanDistance(node.point, goalPoint)
        newNode.f = newNode.g + newNode.h
        
        #If the successor is already in the closedList, then don't add it to the openlist
        inClosed = False
        for n in closedList:
            if n.point == point:
                inClosed = True
                break
        if inClosed:
            pass
        
        #now is the point in the open list?
        indexInOpenList = -1
        for n in range(0, len(openList)):
            if openList[n].point == point:
                indexInOpenList = n
                break
        if indexInOpenList >= 0:
            print(openList[indexInOpenList].point)
            print(point)
            #Compare f values
            if openList[indexInOpenList].f >= newNode.f:
                #don't add the new node to the open then.
                pass
            else:
                #remove old node and add new one
                #we do this by simply redoing the values
                openList[indexInOpenList].f = newNode.f
                openList[indexInOpenList].g = newNode.g
                openList[indexInOpenList].h = newNode.h
                openList[indexInOpenList].parent = newNode.parent
        else:
            print("Not in open")
            #Node isn't in the openList. So lets add it!
            openList.append(newNode)

def a_star(m, start_pos, goal_pos):
    openList = []
    closedList = []
    path = []
    reachedGoal = False
    if start_pos == goal_pos:
        return path
    else:
        #start by adding start node to closedList and populating openList
        startNode = Node(start_pos)
        startNode.g = 0
        startNode.h = EuclideanDistance(start_pos, goal_pos)
        startNode.f = startNode.h
        node = startNode
        openList.append(node)
        print("Starting search!")
        while openList:
            print("Starting while loop")
            minFval = 9999999
            for openNode in openList:
                if openNode.f < minFval:
                    minFval = openNode.f
                    node = openNode
            if node:
                addNodeToClosedList(m, node, closedList, openList, goal_pos)
                #If this is the goal, stop
                if node.point == goal_pos:
                    print("Reached Goal!")
                    reachedGoal = True
                    break
            else:
                print("Open list empty")
                break
        #Done with loops
        if reachedGoal:
            print(node.point)
            path.append(node.point)
            while(node.parent):
                node = node.parent
                path.append(node.point)
                print(node.point)
            path.reverse()
            return path
        else:
            return path


        

def returnPathFromNode(node):
    path = [node.point]
    node = node.parent
    while node:
        path.append(node.point)
        node = node.parent
    path.reverse()
    return path
        
def a_star_try_two(m, start_pos, goal_pos):
    closedList = []
    startNode = Node(start_pos)
    openList = [startNode]
    
    while openList:
        #Choose the node with the lowest f-value
        currNode = openList[0]
        for node in openList:
            if node.f < currNode.f:
                currNode = node
        #if it is the goal, then we are done
        if currNode.point == goal_pos:
            #reached goal!
            print("Reached Goal! Returning path...")
            return returnPathFromNode(currNode)
        openList.remove(currNode)
        closedList.append(currNode)
        neighbors = adjacent(m, currNode.point)
        for point in neighbors:
            #Check if the point is in the closedList
            inClosed = False
            for node in closedList:
                if node.point == point:
                    inClosed = True
                    break
            if inClosed:
                pass
            #Now calculate the f, g, and h values
            g = currNode.g + 1
            h = EuclideanDistance(point, goal_pos)
            f = g + h
            #Check if this point is in the openList
            openListIndex = -1
            for index in range(0, len(openList)):
                if openList[index].point == point:
                    openListIndex = index
                    break
            if openListIndex < 0:
                #Not in openList, so we must create the node and add it!
                newNode = Node(point)
                newNode.parent = currNode
                newNode.f = f
                newNode.g = g
                newNode.h = h
                #And add to openList
                openList.append(newNode)
            else:
                if openList[openListIndex].f > f:
                    #Change the node!
                    openList[openListIndex].f = f
                    openList[openListIndex].g = g
                    openList[openListIndex].h = h
                    openList[openListIndex].parent = currNode
    print("No Goal reached")
    return []
        
if __name__ == "__main__":
    # load the map
    m = np.loadtxt("map2.txt", delimiter=",")
    path = a_star_try_two(m, (1, 1), (7, 15))
    print(path)
    #path = [(0,1),(0,2)]
    # Add the path to the map (for visualization)
    for p in path:
        m[p] = 128
    # change the values (for better visualization)
    m[m == 0] = 255
    m[m == 1] = 0
    # Plot the map (& result)
    plt.matshow(m, cmap=plt.cm.gray)
    plt.show()
