import networkx as nx
import matplotlib.pyplot as plt

# 手动指定节点位置
pos = {
    1: (1, 4), 2: (4, 2), 3: (3, 1), 4: (0, 3), 
    5: (1, 3), 6: (2, 3), 7: (3, 3), 8: (4, 3),
    9: (1, 2), 10: (2, 2), 11: (3, 2), 12: (2, 4),
    13: (2, 1)
}

def generate_network_custom_layout():
    # 创建一个有向图
    G = nx.DiGraph()

    # 添加节点和边
    nodes = range(1, 14)
    edges = [(1, 5), (1, 12), (4, 5), (4, 9), (5, 6), (5, 9), (6, 7), (6, 10),
             (7, 8), (7, 11), (8, 2), (9, 10), (9, 13), (10, 11), (11, 2),
             (11, 3), (12, 6), (12, 8), (13, 3)]
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # 设置边属性
    edge_labels = {(u, v): i for i, (u, v) in enumerate(edges, 1)}
    nx.set_edge_attributes(G, edge_labels, 'label')

    # 绘制图形（可选，视情况而定是否启用）
    # nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, arrowstyle='->', arrowsize=10, font_size=12, font_weight='bold')
    # edge_labels = nx.get_edge_attributes(G, 'label')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    # plt.show()

    return G

def get_upstream(G, edge_label):
    upstream_edges = set()
    for edge in G.in_edges():
        if G.edges[edge]['label'] == edge_label:
            start_node = edge[0]
            upstream_edges.update(G.edges[edge]['label'] for edge in G.in_edges(start_node))

    if not upstream_edges:
        upstream_edges = {-1}  # 用一个无效值替代空集合  
              
    return upstream_edges

def get_downstream(G, edge_label):
    downstream_edges = set()
    for edge in G.out_edges():
        if G.edges[edge]['label'] == edge_label:
            end_node = edge[1]
            downstream_edges.update(G.edges[edge]['label'] for edge in G.out_edges(end_node))
    
    if not downstream_edges:
        downstream_edges = {-1}  # 用一个无效值替代空集合
    
    return downstream_edges



# 生成有向图
G = generate_network_custom_layout()

# 测试上游边和下游边的函数
# 注意替换`some_edge_label`为实际的边标签值，例如1或2
upstream_edges = get_upstream(G, 0)
downstream_edges = get_downstream(G, 19)

print("Upstream edges:", upstream_edges)
print("Downstream edges:", downstream_edges)
