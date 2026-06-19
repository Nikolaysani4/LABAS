import math

try:
    import matplotlib.pyplot as plt
except ImportError:  # pragma: no cover
    plt = None


def floyd_warshall_with_predecessor(weight_matrix):
    """Алгоритм Флойда-Уоршелла с матрицей предшественников H."""
    n = len(weight_matrix)
    dist = [row[:] for row in weight_matrix]
    h = [[None] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j and not math.isinf(dist[i][j]):
                h[i][j] = i

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if math.isinf(dist[i][k]) or math.isinf(dist[k][j]):
                    continue
                new_distance = dist[i][k] + dist[k][j]
                if new_distance < dist[i][j]:
                    dist[i][j] = new_distance
                    h[i][j] = h[k][j]

    return dist, h


def reconstruct_path_vertices(h, i, j):
    """
    Algorithm 7.4 (Floyd Algorithm) для восстановления последовательности вершин.
    Возвращает путь в обратном и прямом порядке.
    """
    q = j
    reverse_path = [q]

    while q != i:
        q = h[i][q]
        if q is None:
            return None, None
        reverse_path.append(q)

    forward_path = list(reversed(reverse_path))
    return reverse_path, forward_path


def print_matrix(matrix, title, as_predecessor=False):
    print(f"\n{title}")
    for row in matrix:
        formatted_row = []
        for value in row:
            if as_predecessor:
                formatted_row.append("-" if value is None else str(value + 1))
            else:
                formatted_row.append("∞" if math.isinf(value) else f"{int(value):2d}")
        print(" ".join(f"{cell:>3}" for cell in formatted_row))


def visualize_graph(vertices, edges, path):
    """Визуализация графа и кратчайшего пути средствами matplotlib (без networkx)."""
    if plt is None:
        raise RuntimeError("matplotlib не установлен. Установите пакет matplotlib для визуализации.")
    plt.figure(figsize=(9, 7))

    path_edges = set()
    for idx in range(len(path) - 1):
        a, b = path[idx], path[idx + 1]
        path_edges.add((a, b))
        path_edges.add((b, a))

    for u, v, w in edges:
        x1, y1 = vertices[u]
        x2, y2 = vertices[v]
        is_path_edge = (u, v) in path_edges
        plt.plot(
            [x1, x2],
            [y1, y2],
            color="red" if is_path_edge else "gray",
            linewidth=3 if is_path_edge else 1.8,
            zorder=1,
        )
        plt.text((x1 + x2) / 2, (y1 + y2) / 2, str(w), fontsize=10, color="black")

    for idx, (x, y) in vertices.items():
        is_path_vertex = idx in path
        plt.scatter(
            x,
            y,
            s=520,
            color="orange" if is_path_vertex else "lightblue",
            edgecolors="black",
            zorder=2,
        )
        plt.text(x, y, str(idx + 1), ha="center", va="center", fontsize=12, fontweight="bold", zorder=3)

    path_str = " → ".join(str(v + 1) for v in path)
    plt.title(f"Кратчайший путь: {path_str}", fontsize=13, fontweight="bold")
    plt.axis("equal")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def main():
    inf = math.inf

    # Пример графа: матрица расстояний
    d0 = [
        [0, 3, inf, 7, inf, inf],
        [3, 0, 2, inf, 6, inf],
        [inf, 2, 0, 1, inf, 4],
        [7, inf, 1, 0, 2, inf],
        [inf, 6, inf, 2, 0, 1],
        [inf, inf, 4, inf, 1, 0],
    ]

    dist, h = floyd_warshall_with_predecessor(d0)

    print("Алгоритм Флойда (Algorithm 7.4): восстановление пути по матрице H")
    print_matrix(d0, "Исходная матрица расстояний D0:")
    print_matrix(dist, "Матрица кратчайших расстояний D:")
    print_matrix(h, "Матрица предшественников H (вершины-предшественники):", as_predecessor=True)

    # Ищем путь из вершины 1 в вершину 6 (индексация с 0)
    i, j = 0, 5
    reverse_path, forward_path = reconstruct_path_vertices(h, i, j)

    if forward_path is None:
        print(f"\nПуть между вершинами {i + 1} и {j + 1} не существует.")
        return

    print(f"\nПуть (в обратном порядке, как в алгоритме): {[v + 1 for v in reverse_path]}")
    print(f"Путь (от i к j): {[v + 1 for v in forward_path]}")
    print(f"Длина кратчайшего пути: {int(dist[i][j])}")

    vertices = {
        0: (0, 2),
        1: (2, 4),
        2: (4, 3),
        3: (4, 1),
        4: (6, 2),
        5: (8, 3),
    }

    edges = [
        (0, 1, 3),
        (0, 3, 7),
        (1, 2, 2),
        (1, 4, 6),
        (2, 3, 1),
        (2, 5, 4),
        (3, 4, 2),
        (4, 5, 1),
    ]

    visualize_graph(vertices, edges, forward_path)


if __name__ == "__main__":
    main()
