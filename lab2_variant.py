from itertools import combinations
from math import hypot


def generate_permutations(arr):
    """Генерация перестановок по алгоритму следующей перестановки."""
    arr = sorted(arr)
    yield arr[:]

    while True:
        i = len(arr) - 2
        while i >= 0 and arr[i] >= arr[i + 1]:
            i -= 1
        if i < 0:
            return

        j = len(arr) - 1
        while arr[j] <= arr[i]:
            j -= 1

        arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1:] = reversed(arr[i + 1:])
        yield arr[:]


def dist2(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def is_square(points):
    dists = sorted(
        dist2(points[i], points[j])
        for i, j in combinations(range(4), 2)
    )
    return dists[0] > 0 and dists[0] == dists[1] == dists[2] == dists[3] and dists[4] == dists[5] == 2 * dists[0]


def perimeter_square(points):
    side = hypot(points[0][0] - points[1][0], points[0][1] - points[1][1])
    return 4 * side


def solve(points):
    best = None
    best_perimeter = -1

    for quad in combinations(points, 4):
        if is_square(quad):
            per = perimeter_square(quad)
            if per > best_perimeter:
                best_perimeter = per
                best = quad

    return best, best_perimeter


def main():
    print("Лабораторная работа 2")
    print("Задача: выбрать 4 точки, являющиеся вершинами квадрата наибольшего периметра")

    n = int(input("Введите количество точек: "))
    points = []
    print("Введите координаты точек в формате x y:")
    for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))

    print("\nГенерация перестановок индексов (демонстрация алгоритма):")
    for p in generate_permutations(list(range(1, min(n, 4) + 1))):
        print(*p)

    square, per = solve(points)
    if square is None:
        print("\nКвадрат среди данных точек не найден.")
    else:
        print("\nНайденный квадрат с максимальным периметром:")
        for pt in square:
            print(pt)
        print(f"Периметр: {per:.6f}")


if __name__ == "__main__":
    main()
