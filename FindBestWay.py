import CrossList

#调用函数：find_best_way(node_data, start, end)
#node data为创建的十字链表，start开始节点类型为node，end为结束节点类型为node
#函数返回两个变量，第一个为一个从start到end的路径上所有节点的列表，第二个为整个路径的权值
#若无通通路，返回：None，0
def dijkstra(node_data, start, end, waiting, result):
    if start is not None:
        if start.id == end.id:
            result = {}
            result[start] = [0, start]  # 权值＋前驱节点
            return result
        if result is None:
            result = {}
            result[start] = [0, start]
        if waiting is None:
            waiting = {}
        temp_road_list = node_data.get_edge(start)
        new_node_list = []
        for edge in temp_road_list:
            if edge.ivex.id == start.id and edge.jvex not in result.keys():
                new_node = edge.jvex
                new_node_value = result[start][0] + edge.length
            elif edge.jvex.id == start.id and edge.ivex not in result.keys():
                new_node = edge.ivex
                new_node_value = result[start][0] + edge.length
            else:
                continue
            new_node_list.append([new_node, new_node_value])
            # 以上：新加入确定集合的点相连接的点集
        for new_waiting_node in new_node_list:
            key_node = new_waiting_node[0]
            value_node = new_waiting_node[1]
            if key_node not in waiting.keys():
                waiting[key_node] = [value_node, start]#权值＋前驱节点
            else:
                if waiting[key_node][0] > value_node:
                    waiting[key_node][0] = value_node
                    waiting[key_node][1] = start
            # 以上：将这些点集加入到待定集合中
    add_node = None
    add_value = -1
    if waiting is None:
        return result
    for node_to_add in waiting.keys():
        if add_value == -1:
            add_node = node_to_add
            add_value = waiting[node_to_add][0]
        else:
            true_value = waiting[node_to_add][0]
            if add_value > true_value:
                add_node = node_to_add
                add_value = waiting[node_to_add][0]
    # 以上：寻找集合中权值最小的点
    if add_node is None or add_value == -1:
        return result
    if add_node == end:
        result[add_node] = [add_value, waiting[add_node][1]]
        return result
    result[add_node] = [add_value, waiting[add_node][1]]
    waiting.pop(add_node)
    return dijkstra(node_data, add_node, end, waiting, result)


def find_best_way(node_data, start, end):
    the_best_path = dijkstra(node_data, start, end, None, None)
    if_end_in_data = 0
    for data in the_best_path:
        if data is end:
            if_end_in_data = 1
    if if_end_in_data is 1:
        p = end
        way_list = []
        while p != start:
            way_list.append(p)
            p = the_best_path[p][1]
        way_list.append(start)
        way_list.reverse()
        for final_node in way_list:
            print(final_node.id)
        print(the_best_path[end][0])
        return way_list, the_best_path[end][0]
    else:
        print("No way from start to destination")
        return None, 0

