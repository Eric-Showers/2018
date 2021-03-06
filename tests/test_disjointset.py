"""
Test union and find operations.
"""

import unittest
from unittest.mock import Mock
from app.util.DisjointSet import DisjointSet
from app.Board import Board

class TestDisjointSet(unittest.TestCase):
    """
    Parent class to run unittests.
    """

    def setUp(self):
        """
        Create a fresh DisjointSet object.
        """
        self.board = Mock(width=20, height=20)
        self.set = DisjointSet(self.board)
        self.set.update()
        
    def test_initialization(self):
        """
        Ensure proper default state.
        """
        self.assertEqual(self.set.board, self.board)
        connected = self.set.getConnectedToNode([0, 0])
        for x in range(self.board.width):
            for y in range(self.board.width):
                if [x, y] == [0, 0]:
                    continue
                self.assertTrue([x, y] in connected)

    def test_get_connected_all_walls(self):
        """
        Ensure basic update is performed properly.
        """
        self.board.getWeight.return_value = 0
        self.set.update()
        for x in range(self.board.width):
            for y in range(self.board.height):
                self.assertEqual(self.set.getConnectedToWall([x, y]), [])

    def test_error_conditions(self):
        """
        Ensure basic update is performed properly.
        """
        self.board.getWeight.return_value = 0
        self.set.update()
        for x in range(self.board.width):
            for y in range(self.board.height):
                self.assertRaises(ValueError, self.set.getConnectedToNode, [x, y])
                if [x, y] != [0, 0]:
                    self.assertRaises(ValueError, self.set.pathExistsFromNode, [x, y], [0, 0])

        self.board.getWeight.return_value = 100
        self.set.update()
        for x in range(self.board.width):
            for y in range(self.board.height):
                self.assertRaises(ValueError, self.set.getConnectedToWall, [x, y])
                if [x, y] != [0, 0]:
                    self.assertRaises(ValueError, self.set.pathExistsFromWall, [x, y], [0, 0])

    def test_no_path_across_wall(self):
        """
        Make sure no path exists outside of an enclosed space.
        """
        board = Board(10, 10)
        dset = DisjointSet(board)
        enclosedSpace = [[0, 0], [1, 0], [1, 1], [2, 0], [2, 1], [3, 0]]
        wall = [[0, 1], [1, 2], [2, 2], [3, 2], [3, 1], [4, 0]]
        
        board.setWeights(wall, 0) # disconnect top left

        dset.update()
        self.assertEqual(sorted(dset.getConnectedToNode([0,0])), enclosedSpace[1:])

        for x in range(board.width):
            for y in range(board.height):
                if [x, y] not in enclosedSpace and [x, y] not in wall:
                    for coord in enclosedSpace:
                        self.assertFalse(dset.pathExistsFromNode(coord, [x, y]))

    def test_path_within_bounds(self):
        """
        Make sure a path exists inside an enclosed space.
        """
        board = Board(10, 10)
        dset = DisjointSet(board)
        enclosedSpace = [[0, 0], [1, 0], [1, 1], [2, 0], [2, 1], [3, 0]]
        wall = [[0, 1], [1, 2], [2, 2], [3, 2], [3, 1], [4, 0]]
        
        board.setWeights(wall, 0) # disconnect top left

        dset.update()
        self.assertEqual(sorted(dset.getConnectedToNode([0,0])), enclosedSpace[1:])

        for coord1 in enclosedSpace:
            for coord2 in enclosedSpace:
                self.assertTrue(dset.pathExistsFromNode(coord1, coord2))

    def test_worst_case(self):
        """
        Test update with a crafted set of walls to maximize data structure height.
        """
        board = Board(20, 20)
        dset = DisjointSet(board)
        wall = [[2,0],[3,0],[4,0],[5,0],[0,1],[5,1],[2,2],[5,2],[0,3],[1,3], \
        [2,3],[5,3],[6,3],[2,4],[6,4],[0,5],[6,5],[2,6],[3,6],[4,6],[6,6],[7,6], \
        [8,6],[0,7],[1,7],[2,7],[8,7],[9,7],[10,7],[11,7],[12,7],[13,7],[2,8], \
        [0,9],[2,10],[0,11],[1,11],[2,11],[2,12],[3,12],[4,12],[5,12],[6,12], \
        [7,12],[8,12],[9,12],[10,12],[11,12],[12,12],[0,13],[2,14],[9,14],[10,14], \
        [11,14],[0,15],[1,15],[2,15],[9,15],[2,16],[9,16],[0,17],[9,17],[2,18], \
        [3,18],[4,18],[5,18],[6,18],[7,18],[8,18],[9,18],[0,19],[1,19],[2,19]]
        
        board.setWeights(wall, 0) # disconnect top left
        dset.update()

        freeSpace = []
        for x in range(board.width):
            for y in range(board.height):
                if [x, y] not in wall:
                    freeSpace.append([x, y])
        self.assertTrue(sorted(freeSpace)[1:] == sorted(dset.getConnectedToNode([0, 0])))

    def test_wall_connected_to_both_sides(self):
        """
        Make a wall can reach enclosed spaces on both sides.
        """
        board = Board(10, 10)
        dset = DisjointSet(board)
        enclosedSpace = [[0, 0], [1, 0], [1, 1], [2, 0], [2, 1], [3, 0]]
        wall = [[0, 1], [1, 2], [2, 2], [3, 1], [4, 0]]
        
        board.setWeights(wall, 0) # disconnect top left

        dset.update()
        self.assertEqual(sorted(dset.getConnectedToNode([0,0])), enclosedSpace[1:])

        for coord in wall:
            self.assertTrue(dset.pathExistsFromWall(coord, [0, 0]))


if __name__ == "__main__":
    unittest.main()
