# %%
import networkx as nx
import matplotlib.pyplot as plt

def generate_network():
    # 创建一个有向图
    G = nx.DiGraph()

    # 添加节点
    nodes = range(1, 14)
    G.add_nodes_from(nodes)

    # 添加有向边
    edges = [(1, 5), (1, 12), (4, 5), (4, 9), (5, 6), (5, 9), (6, 7), (6, 10),
             (7, 8), (7, 11), (8, 2), (9, 10), (9, 13), (10, 11), (11, 2),
             (11, 3), (12, 6), (12, 8), (13, 3)]
    G.add_edges_from(edges)

    # 设置节点属性
    node_labels = {node: str(node) for node in G.nodes}
    nx.set_node_attributes(G, node_labels, 'label')

    # 设置边属性
    edge_labels = {(edge[0], edge[1]): i for i, edge in enumerate(edges, 1)}
    nx.set_edge_attributes(G, edge_labels, 'label')

    # 绘制图形
    pos = nx.spring_layout(G)  # 指定节点位置布局
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            node_size=500, arrowstyle='->', arrowsize=10,
            font_size=12, font_weight='bold')

    # 添加边标签
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # 显示图形
    plt.show()

    return G

def get_upstream(G, edge_label):
    upstream_edges = set()
    for edge in G.in_edges():
        if G.edges[edge]['label'] == edge_label:
            start_node = edge[0]
            upstream_edges.update(G.edges[edge]['label'] for edge in G.in_edges(start_node))

    if not upstream_edges:
        upstream_edges = [-1]  # 用一个无效值替代空集合  
              
    return upstream_edges

def get_downstream(G, edge_label):
    downstream_edges = set()
    for edge in G.out_edges():
        if G.edges[edge]['label'] == edge_label:
            end_node = edge[1]
            downstream_edges.update(G.edges[edge]['label'] for edge in G.out_edges(end_node))
    
    if not downstream_edges:
        downstream_edges = [-1]  # 用一个无效值替代空集合
    
    return downstream_edges

# 生成网络
grid_graph = generate_network()

#测试 get_upstream() 方法
# edge_label = 2
# upstream_edges = get_upstream(grid_graph, edge_label)
# print(f"Upstream edges of edge {edge_label}: {upstream_edges}")

#测试 get_downstream() 方法
# edge_label = 16
# downstream_edges = get_downstream(grid_graph, edge_label)
# print(f"Downstream edges of edge {edge_label}: {downstream_edges}")

# %%
# import gurobipy as gp
# from gurobipy import GRB
# # 创建模型
# model = gp.Model()

# M=6  #观测时间段共有M个，每个时间段持续5min
# N=19 #共有N条link
# K=1 #共有K起事故
# M_range = range(1,M+1)
# N_range = range(1,N+1)
# K_range = range(1,K+1)

# # 创建二维变量矩阵P，并初始化为0
# P = {}
# for i in N_range:
#     for j in M_range:
#         P[i, j] = model.addVar(vtype=GRB.BINARY, name=f"P[{i},{j}]")
#         P[i, j].setAttr(GRB.Attr.Start, 0)

# origin_link_index = 5  # 事故发生link
# origin_time_index = 1  # 事故发生时间

# m = gp.Model("mip1")


# %%
import gurobipy as gp
from gurobipy import GRB
import random

# 设置随机种子
random.seed(123)

# 创建模型
model = gp.Model("mip1")

# 定义参数N和M的值
N = 19  # 边的编号
M = 5   # 时间的编号
K = 1
M_range = range(1,M+1)
N_range = range(1,N+1)
K_range = range(1,K+1)
time_span = 2 #事故持续时间
# 创建二维变量矩阵P，并初始化为0
P = {}
for i in N_range:
    for j in M_range:
        P[i, j] = model.addVar(vtype=GRB.BINARY, name=f"P[{i},{j}]")
        P[i, j].setAttr(GRB.Attr.Start, 0)

origin_link_index = 7  # 事故发生link
origin_time_index = 1  # 事故发生时间

P[origin_link_index, origin_time_index].setAttr(GRB.Attr.Start, 1)

for i in get_upstream(grid_graph, origin_link_index):
    for j in range((origin_time_index + 1),(origin_time_index + 2 + time_span)):
        P[i, j].setAttr(GRB.Attr.Start, 1)

for i in range(origin_link_index,origin_link_index+1):
    for j in range(origin_time_index,origin_time_index + time_span + 1):
        P[i, j].setAttr(GRB.Attr.Start, 1)


for i in get_upstream(grid_graph, 5):
    for j in range((origin_time_index + 2),(origin_time_index + 3 + time_span)):
        P[i, j].setAttr(GRB.Attr.Start, 1)

for i in get_upstream(grid_graph, 17):
    for j in range((origin_time_index + 2),(origin_time_index + 3 + time_span)):
        P[i, j].setAttr(GRB.Attr.Start, 1)

for i in range(origin_link_index,origin_link_index+1):
    for j in range(origin_time_index,origin_time_index + time_span + 1):
        P[i, j].setAttr(GRB.Attr.Start, 1)        


# 将所有变量添加到模型中
model.update()

# 随机选择noise个需要转换的值的索引
noise = 5
indices = []
while len(indices) < noise:
    index = random.choice(list(P.keys()))
    if index not in indices:
        indices.append(index)

# 对选定的索引进行值的转换
for index in indices:
    P[index].setAttr(GRB.Attr.Start, 1 - P[index].getAttr(GRB.Attr.Start))



# %%
# 创建决策变量
gamma  = model.addVars(K_range,M_range,N_range,vtype=GRB.BINARY, name="gamma") #link n在时间区间m上确实受到了事故k影响则为1
delta  = model.addVars(K_range,M_range,N_range,vtype=GRB.BINARY, name="delta") #事故k起源于在时间区间m上的link n则为1
lambda1 = model.addVar(vtype=gp.GRB.BINARY, name="lambda1")
lambda2 = model.addVar(vtype=gp.GRB.BINARY, name="lambda2")
lambda3 = model.addVar(vtype=gp.GRB.BINARY, name="lambda3")
lambda4 = model.addVar(vtype=gp.GRB.BINARY, name="lambda4")
lambda5 = model.addVar(vtype=gp.GRB.BINARY, name="lambda5")
lambda6 = model.addVar(vtype=gp.GRB.BINARY, name="lambda6")



# %%
# # 求解模型
# m.optimize()

# # 获取P的取值
# P_values = m.getAttr('X', P)

# # 打印P的取值
# for i in N_range:
#     for j in M_range:
#         print(f"P[{i},{j}] = {P_values[i,j]}")

    

# # 获取delta的取值
# delta_values = m.getAttr('X', delta)

# # 打印delta的取值
# for k in K_range:
#     for m in M_range:
#         for n in N_range:
#             print(f"delta[{k},{m},{n}] = {delta_values[k,m,n]}")    

# %%
#目标函数
model.setObjective(gp.quicksum(P[n,m]*(1-delta[k,m,n])+(1-P[n,m])*delta[k,m,n] for k in K_range for m in M_range for n in N_range), GRB.MINIMIZE)




# %%
for k in K_range:
    for m in M_range:
        for n in N_range:
            if k in K_range and m-1 in M_range and n in N_range:
                model.addConstr(gp.quicksum(delta[k,m,l] for l in get_downstream(grid_graph, n)) + delta[k,m-1,n] >= delta[k,m,n] - gamma[k,m,n], name="c1")

# %%
#约束1-2 保证冲击波的定向传播
#约束1：如果cell<m,n>受到了事故影响，且不是起源cell，那么该影响势必源自下游link或前一时刻或二者兼具
model.addConstrs((gp.quicksum(delta[k,m,l]for l in get_downstream(grid_graph, n))+delta[k,m-1,n]>=delta[k,m,n]-gamma[k,m,n] for k in K_range for m in M_range for n in N_range), "c1")

# %%
#约束3-6 保证冲击波的不间断传播
#约束3：
model.addConstrs((delta[k,m-1,n]<=lambda1 for k in K_range for m in M_range for n in N_range),"c3")
#约束4：
model.addConstrs((gp.quicksum(delta[k,m,l]for l in range(get_downstream(grid_graph, n)))<=lambda2*len(get_downstream(grid_graph, n)) for k in K_range for m in M_range for n in N_range), "c4")
#约束5:
model.addConstrs((delta[k,m,n]>=1-lambda3 for k in K_range for m in M_range for n in N_range),"c5")
#约束6:
model.addConstrs((lambda1+lambda2+lambda3<=2),"c6")

# %%
#约束7-10 当某一link受到事故影响，且该link的上游link也受到了事故影响，那么该link的其余上游link中，车道累计车辆数大于被影响的上游link的，也都应该被事故影响了
#约束7:
# m.addConstrs((gp.quicksum(delta[k,m,l]for l in range(get_upstream(grid_graph, n)))<=lambda4*len(get_upstream(grid_graph, n)) for k in K_range for m in M_range for n in N_range), "c7")
#约束8:


# %%
#约束11：针对每一起事故，有且仅有一个cell是事故的起源点
model.addConstrs((gp.quicksum(gamma(k,m,n)for m in M_range for n in N_range)==1 for k in K_range), "c11")

# %%
#约束12：如果cell<m,n>是起源点(终止点)，那么其必会受到事故的影响
model.addConstrs((gamma[k,m,n]<=delta[k,m,n]for k in K_range for m in M_range for n in N_range), "c12")

# %%
#约束13-14 当cell<m,n>是起源点时，前一时刻与上游路段集合的cell都不会受到事故影响
#约束13：
model.addConstrs((gp.quicksum(delta[k,m,l]for l in range(get_upstream(grid_graph, n)))<=(1-gamma[k,m,n])*len(get_upstream(grid_graph, n))for k in K_range for m in M_range for n in N_range), "c13")
#约束14：
model.addConstrs((1-gamma[k,m,n]>=delta[k,m-1,n]for k in K_range for m in M_range for n in N_range), "c14")
#约束15:反之亦然
model.addConstrs((gp.quicksum(delta[k,m,l]for l in range(get_upstream(grid_graph, n)))+delta[k,m-1,n]>=delta[k,m,n]-gamma[k,m,n]for k in K_range for m in M_range for n in N_range), "c15")

# %%
#约束16：针对每一个cell，其产生的拥堵影响只会归属于一起事故
model.addConstrs((gp.quicksum(delta(k,m,n)for k in K_range)==1 for m in M_range for n in N_range), "c16")

# %%
# 求解模型
model.optimize()

# 获取P的取值
P_values = model.getAttr('X', P)

# 打印P的取值
for i in N_range:
    for j in M_range:
        print(f"P[{i},{j}] = {P_values[i,j]}")

# 获取gamma的取值
gamma_values = model.getAttr('X', gamma)

# 打印gamma的取值
for k in K_range:
    for m in M_range:
        for n in N_range:
            print(f"gamma[{k},{m},{n}] = {gamma_values[k,m,n]}")      

# 获取delta的取值
delta_values = model.getAttr('X', delta)

# 打印delta的取值
for k in K_range:
    for m in M_range:
        for n in N_range:
            print(f"delta[{k},{m},{n}] = {delta_values[k,m,n]}")             


