import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict, deque

class GraphAlgorithms:
    def __init__(self):
        self.graph = defaultdict(list)
        self.visited = set()
        self.rec_stack = set()
        self.parent = {}
        self.bridges = []
        self.disc = {}
        self.low = {}
        self.timer = 0
        
    def add_edge(self, u, v):
        """Добавить ребро в граф"""
        self.graph[u].append(v)
        # Для неориентированного графа добавляем обратное ребро
        self.graph[v].append(u)
    
    def find_cycle_dfs(self, v, parent=-1, cycle=[]):
        """
        Поиск цикла в графе методом DFS
        Рекурсивный обход графа с отслеживанием родительского узла
        """
        self.visited.add(v)
        
        for u in self.graph[v]:
            if u not in self.visited:
                self.parent[u] = v
                if self.find_cycle_dfs(u, v, cycle):
                    return True
            elif u != parent:
                # Найден цикл
                return True
        
        return False
    
    def find_articulation_points(self):
        """
        Поиск узловых вершин (articulation points) - вершин,
        удаление которых разбивает граф на несвязные компоненты
        """
        self.disc = {}
        self.low = {}
        self.parent = {}
        self.timer = 0
        articulation_points = set()
        
        def dfs(u):
            children = 0
            self.disc[u] = self.low[u] = self.timer
            self.timer += 1
            
            for v in self.graph[u]:
                if v not in self.disc:
                    children += 1
                    self.parent[v] = u
                    dfs(v)
                    
                    self.low[u] = min(self.low[u], self.low[v])
                    
                    # Если u - корень и имеет более одного поддерева
                    if self.parent.get(u) is None and children > 1:
                        articulation_points.add(u)
                    
                    # Если u не корень и low[v] >= disc[u]
                    if self.parent.get(u) is not None and self.low[v] >= self.disc[u]:
                        articulation_points.add(u)
                        
                elif v != self.parent.get(u):
                    self.low[u] = min(self.low[u], self.disc[v])
        
        for node in self.graph:
            if node not in self.disc:
                self.parent[node] = None
                dfs(node)
        
        return articulation_points
    
    def find_bridges(self):
        """
        Поиск мостов (bridges) - рёбер, удаление которых разбивает граф
        """
        self.disc = {}
        self.low = {}
        self.parent = {}
        self.bridges = []
        self.timer = 0
        
        def dfs(u):
            self.disc[u] = self.low[u] = self.timer
            self.timer += 1
            
            for v in self.graph[u]:
                if v not in self.disc:
                    self.parent[v] = u
                    dfs(v)
                    
                    self.low[u] = min(self.low[u], self.low[v])
                    
                    # Если low[v] > disc[u], то (u, v) - мост
                    if self.low[v] > self.disc[u]:
                        self.bridges.append((u, v))
                        
                elif v != self.parent.get(u):
                    self.low[u] = min(self.low[u], self.disc[v])
        
        for node in self.graph:
            if node not in self.disc:
                self.parent[node] = None
                dfs(node)
        
        return self.bridges


def visualize_graph(graph_obj, title="Graph", bridges=None, articulation_points=None):
    """
    Визуализация графа с помощью matplotlib и networkx
    """
    G = nx.Graph()
    
    # Добавляем ребра
    for u in graph_obj.graph:
        for v in graph_obj.graph[u]:
            G.add_edge(u, v)
    
    # Создаем визуализацию
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42, k=2, iterations=50)
    
    # Рисуем все узлы по умолчанию
    node_colors = ['lightblue'] * len(G.nodes())
    
    # Выделяем узловые вершины красным
    if articulation_points:
        for i, node in enumerate(G.nodes()):
            if node in articulation_points:
                node_colors[i] = 'red'
    
    # Рисуем узлы
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                          node_size=800, alpha=0.9)
    
    # Рисуем рёбра
    edge_colors = ['black'] * len(G.edges())
    if bridges:
        for i, (u, v) in enumerate(G.edges()):
            for bridge_u, bridge_v in bridges:
                if (u == bridge_u and v == bridge_v) or (u == bridge_v and v == bridge_u):
                    edge_colors[i] = 'red'
                    break
    
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2)
    
    # Рисуем метки узлов
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    return plt


# Пример использования - Вариант 4
def main():
    print("=" * 60)
    print("ЛАБОРАТОРИЯ 3 - ВАРИАНТ 4")
    print("Поиск узких мест графа (узловые вершины и мосты)")
    print("=" * 60)
    
    # Создаем граф
    algo = GraphAlgorithms()
    
    # Добавляем рёбра для примера
    edges = [
        (1, 2),
        (1, 3),
        (2, 3),
        (2, 4),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 5)
    ]
    
    print("\nДобавленные рёбра:")
    for u, v in edges:
        algo.add_edge(u, v)
        print(f"  {u} -- {v}")
    
    # Находим узловые вершины (articulation points)
    articulation_points = algo.find_articulation_points()
    print(f"\nУзловые вершины (критические точки): {sorted(articulation_points)}")
    
    # Находим мосты (bridges)
    bridges = algo.find_bridges()
    print(f"Мосты (критические рёбра): {bridges}")
    
    # Визуализируем граф с выделением узловых вершин
    plt1 = visualize_graph(
        algo, 
        title="Граф с выделением узловых вершин (красным)",
        articulation_points=articulation_points
    )
    plt1.savefig('graph_articulation_points.png', dpi=300, bbox_inches='tight')
    print("\n✓ Граф с узловыми вершинами сохранен: graph_articulation_points.png")
    
    # Визуализируем граф с выделением мостов
    plt2 = visualize_graph(
        algo,
        title="Граф с выделением мостов (красным)",
        bridges=bridges
    )
    plt2.savefig('graph_bridges.png', dpi=300, bbox_inches='tight')
    print("✓ Граф с мостами сохранен: graph_bridges.png")
    
    # Выводим детальный анализ
    print("\n" + "=" * 60)
    print("АНАЛИЗ ГРАФА")
    print("=" * 60)
    print(f"Количество узлов: {len(algo.graph)}")
    print(f"Количество рёбер: {sum(len(v) for v in algo.graph.values()) // 2}")
    print(f"Количество узловых вершин: {len(articulation_points)}")
    print(f"Количество мостов: {len(bridges)}")
    
    plt.show()


if __name__ == "__main__":
    main()
