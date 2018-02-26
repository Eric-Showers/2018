"""Tracks connectedness of our board. Provides lightning fast lookups to see exactly
what squares are reachable from where."""

class DisjointSet:
    """The disjointed set that provides information
    on the connectedness of the board.

    Has following attributes:
    board           Board           - Board object
    map             {'[x,y]':Node}  - dict mapping coords to Node objects
    """

    def __init__(self, board):
        """
        Initialize the disjoint set.
        
        param1: Board - Board object
        """
        self.board = board
        self.map = {} # maps coords to Node objects
        
    def update(self):
        """
        Update connectivity based on Snake objects.
        """
        self.map = {}
        boardWidth = self.board.getWidth()
        boardHeight = self.board.getHeight()
        for x in range(boardWidth):
            for y in range(boardHeight):
                strCoord = '[' + str(x) + ', ' + str(y) + ']'                
                newNode = Node(strCoord)
                self.map[strCoord] = newNode

                weight = self.board.getWeight([x, y])
                if weight is not 0:
                    surrounding = []
                    if (x - 1) >= 0:
                        surrounding.append(str([x - 1, y]))
                    if (x + 1) < boardWidth:
                        surrounding.append(str([x + 1, y]))
                    if (y + 1) < boardHeight:
                        surrounding.append(str([x, y + 1]))
                    if (y - 1) >= 0:
                        surrounding.append(str([x, y - 1]))
                    
                    for coord in surrounding:
                        if coord in self.map:
                            self.union(self.map[coord], newNode)

    def find(self, child):
        """
        Determines the root of a given Node.

        param1: Node - child to find the root of
        return: Node - root of the child
        """
        parent = child.parent
        if parent is None:
            return child
        else:
            return self.find(parent)

    def union(self, node1, node2):
        """
        Provides a way for 2 disconnected components to connect.

        param1: Node - first component to connect
        param2: Node - second component to connect
        """
        root1 = self.find(node1)
        rank1 = root1.rank
        root2 = self.find(node2)
        rank2 = root2.rank
        
        if root1 == root2: # already connected
            return
        
        if rank1 < rank2:
            root1.parent = root2
            root2.directChildren.add(root1)
        elif rank1 > rank2:
            root2.parent = root1
            root1.directChildren.add(root2)
        else:
            root1.parent = root2
            root2.rank = rank2 + 1
            root2.directChildren.add(root1)

    def getConnected(self, coord):
        """
        Return list of squares connected to the provided one.

        param1: [x,y] - name of square to find connected components from
        return: [[x,y]] - list of connected squares
        """
        # TODO: this currently only return one level, it must be recursive
        root = self.find(self.map[str(coord)])
        return [eval(node.name) for node in root.directChildren] + [eval(root.name)]

    def areConnected(self, coord1, coord2):
        """
        Determine if 2 nodes are connected.

        param1: [x,y] - first node position
        param2: [x,y] - second node position
        return: bool - True if connected, False otherwise
        """
        return self.find(self.map[str(coord1)]) == self.find(self.map[str(coord2)])

    def getNode(self, coord):
        """
        Return the Node object that corresponds to a gives square.

        param1: [x,y] - name of the square to find
        return: Node - object corresponding to square
        """
        return self.map[str(coord)]

    def toString(self, root):
        """
        Provides a way to print out the tree in a human-readable format.

        param1: string - name of root to display from
        """
        print('\t'*(5 - root.rank) + root.name) # NOTE: Incredibly crude implementation
        for child in root.directChildren:
            self.toString(child)


class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.directChildren = set()
        self.rank = 0
