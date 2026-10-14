import math
import unittest

from lab7_floyd import floyd_warshall_with_predecessor, reconstruct_path_vertices


class FloydAlgorithmTests(unittest.TestCase):
    def test_reconstruct_shortest_path(self):
        inf = math.inf
        d0 = [
            [0, 3, inf, 7, inf, inf],
            [3, 0, 2, inf, 6, inf],
            [inf, 2, 0, 1, inf, 4],
            [7, inf, 1, 0, 2, inf],
            [inf, 6, inf, 2, 0, 1],
            [inf, inf, 4, inf, 1, 0],
        ]

        dist, h = floyd_warshall_with_predecessor(d0)
        reverse_path, forward_path = reconstruct_path_vertices(h, 0, 5)

        self.assertEqual(6, dist[0][5])
        self.assertEqual([5, 4, 3, 2, 1, 0], reverse_path)
        self.assertEqual([0, 1, 2, 3, 4, 5], forward_path)


if __name__ == "__main__":
    unittest.main()
