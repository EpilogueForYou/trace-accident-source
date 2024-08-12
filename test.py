import pygraphviz as pgv
import matplotlib.pyplot as plt
import io

def generate_grid_graph(a):
    # 创建有向图
    graph = pgv.AGraph(directed=True)
    
    # 添加节点
    node_counter = 1  # 节点计数器
    for i in range(a):
        for j in range(a):
            node_name = str(node_counter)
            graph.add_node(node_name)
            node_counter += 1
    
    # 添加边
    edge_counter = 1  # 边计数器
    for i in range(a):
        for j in range(a):
            node_name = str(i * a + j + 1)
            
            # 添加向右的边
            if j < a - 1:
                right_node_name = str(i * a + j + 2)
                graph.add_edge(node_name, right_node_name, label=str(edge_counter))
                graph.add_edge(right_node_name, node_name, label=str(edge_counter + 1))
                edge_counter += 2
            
            # 添加向下的边
            if i < a - 1:
                down_node_name = str((i + 1) * a + j + 1)
                graph.add_edge(node_name, down_node_name, label=str(edge_counter))
                graph.add_edge(down_node_name, node_name, label=str(edge_counter + 1))
                edge_counter += 2
    
    return graph

def visualize_graph(graph):
    # 可视化图形
    graph.layout(prog='dot')
    img_stream = graph.draw(format='png', prog='dot')
    
    # 显示图像
    img = plt.imread(io.BytesIO(img_stream))
    plt.imshow(img)
    plt.axis('off')
    plt.show()

# 生成网格图
a = 3  # 每行每列的节点数
grid_graph = generate_grid_graph(a)

# 可视化图形
visualize_graph(grid_graph)