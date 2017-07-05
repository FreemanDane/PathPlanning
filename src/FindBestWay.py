from src.CrossList import *
from src.DataAnalysis import *
i = 0
# 调用函数：find_best_way(node_data, start, end)
# node data为创建的十字链表，start开始节点类型为node，end为结束节点类型为node
# 函数返回两个变量，第一个为一个从start到end的路径上所有节点的列表，第二个为整个路径的权值
# 若无通通路，返回：None，-1


def dijkstra(node_data, start, end, waiting, result):
    global i
    i = i + 1
    if i > 900:
        i = 0
        return start, end, waiting, result
    if start is not None:
        if start.id == end.id:
            result = {}
            result[start] = [0, start]  # 权值＋前驱节点
            return start, end, None, result
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
                waiting[key_node] = [value_node, start]  # 权值＋前驱节点
            else:
                if waiting[key_node][0] > value_node:
                    waiting[key_node][0] = value_node
                    waiting[key_node][1] = start
                    # 以上：将这些点集加入到待定集合中
    add_node = None
    add_value = -1
    if waiting is None:
        return start, end, None, result
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
        return start, end, None, result
    if add_node == end:
        result[add_node] = [add_value, waiting[add_node][1]]
        return start, end, None, result
    result[add_node] = [add_value, waiting[add_node][1]]
    waiting.pop(add_node)
    return dijkstra(node_data, add_node, end, waiting, result)


def find_best_way(node_data, start, end):
    the_best_path = {}
    the_best_path[start] = [0, start]
    temp_waiting = {}
    temp_start = start
    temp_end = end
    while True:
        temp_start, temp_end, temp_waiting, the_best_path = dijkstra(node_data, temp_start, temp_end, temp_waiting
                                                                     , the_best_path)
        if temp_waiting is None:
            break
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
        #for final_node in way_list:
            #print(final_node.id)
        #print(the_best_path[end][0])
        return way_list, the_best_path[end][0]
    else:
        print("No way from start to destination")
        return None, -1


'''def dijkstra2 (node_data, start, end, waiting, result):
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
                if edge.can_ride is 1:
                    new_node_value = result[start][0]
                else:
                    new_node_value = result[start][0] + edge.length
            elif edge.jvex.id == start.id and edge.ivex not in result.keys():
                new_node = edge.ivex
                if edge.can_ride is 1:
                    new_node_value = result[start][0]
                else:
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


def find_best_walking_way(node_data, start, end):
    the_best_path = dijkstra2(node_data, start, end, None, None)
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
        return None, -1'''


def find_the_closest_point(map, node):
    closest_node = None
    distance = 100000000
    for way in map.ways:
        for ref_node in way.point:
            nid = ref_node.attrs.get('ref')
            clo_node = map.cross_list.nodes.get(nid)
            if clo_node.is_highway is 1:
                temp_distance = node.distance(clo_node)
            if temp_distance < distance:
                closest_node = clo_node
                distance = temp_distance
    return closest_node, distance


def find_the_name_of_points(map, way_name):#找到离去的地方最近的点
    the_way = way(-1)
    for ways in map.ways:
        if 'name' in ways.attr.keys():
            if way_name in ways.attr.get('name'):
                the_way = ways
                break
    if the_way.id is -1:
        for keynd in map.keynode:
            if 'name' in keynd.attr.keys() and way_name in keynd.attr.get('name'):
                return keynd
        print("No place called this!")
        return node(-2, -1, -1)
    lat = 0
    lon = 0
    for way_node in the_way.point:
        nid = way_node.attrs.get('ref')
        clo_node = map.cross_list.nodes.get(nid)
        lat += clo_node.lat
        lon += clo_node.lon
    nd_num = len(the_way.point)
    ave_lat = lat / nd_num
    ave_lon = lon / nd_num
    ave_nid = -1
    ave_node = node(ave_nid,ave_lat, ave_lon)
    return ave_node

def search_by_name(map, start_name, end_name):
    true_start_node = find_the_name_of_points(map, start_name)
    start_node, start_distance = find_the_closest_point(map, true_start_node)
    true_end_node = find_the_name_of_points(map, end_name)
    end_node, end_distance = find_the_closest_point(map, true_end_node)
    if start_distance is -1:
        print('No name called ' , start_name)
        return None, -1
    elif end_distance is -1:
        print('No name called ', end_name)
        return None, -1
    else:
        best_way_list, best_way_distance = find_best_way(map.cross_list, start_node, end_node)
        if best_way_distance is -1:
            print("No Way!")
            return None, -1
        best_way_list.append(end_node)
        best_way_list.append(true_end_node)
        best_way_list.insert(0, start_node)
        best_way_list.insert(0,true_start_node)
        best_way_distance += start_distance
        best_way_distance += end_distance
        return best_way_list, best_way_distance


def search_by_node(map, start_lat, start_lon, end_lat, end_lon):
    start_node = node(-1, start_lat, start_lon)
    end_node = node(-1, end_lat, end_lon)
    clo_start_node, start_distance = find_the_closest_point(map, start_node)
    clo_end_node, end_distance = find_the_closest_point(map, end_node)
    best_way_list, best_way_distance = find_best_way(map.cross_list, clo_start_node, clo_end_node)
    if best_way_distance is -1:
        print("No Way!")
        return None, -1
    best_way_list.append(end_node)
    best_way_list.insert(0, start_node)
    best_way_distance += start_distance
    best_way_distance += end_distance
    return best_way_list, best_way_distance
