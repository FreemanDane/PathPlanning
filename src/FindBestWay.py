from CrossList import *
from DataAnalysis import *
i = 0
j = 0
# 调用函数：find_best_way(node_data, start, end)
# node data为创建的十字链表，start开始节点类型为node，end为结束节点类型为node
# 函数返回两个变量，第一个为一个从start到end的路径上所有节点的列表，第二个为整个路径的权值
# 若无通通路，返回：None，-1

#内部实现函数，不用管
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

#内部实现函数，不用管
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

def dijkstra2(node_data, start, end, waiting, result):
    global j
    j = j + 1
    if j > 900:
        j = 0
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
                if edge.can_ride is 0:
                    new_node_value = result[start][0] + edge.length
                else:
                    new_node_value = result[start][0] + edge.length * 0.001
            elif edge.jvex.id == start.id and edge.ivex not in result.keys():
                new_node = edge.ivex
                if edge.can_ride is 0:
                    new_node_value = result[start][0] + edge.length
                else:
                    new_node_value = result[start][0] + edge.length * 0.001
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
    return dijkstra2(node_data, add_node, end, waiting, result)

def find_best_walking_way(node_data, start, end):
    the_best_path = {}
    the_best_path[start] = [0, start]
    temp_waiting = {}
    temp_start = start
    temp_end = end
    while True:
        temp_start, temp_end, temp_waiting, the_best_path = dijkstra2(node_data, temp_start, temp_end, temp_waiting
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
        # for final_node in way_list:
        # print(final_node.id)
        # print(the_best_path[end][0])
        return way_list, the_best_path[end][0]
    else:
        print("No way from start to destination")
        return None, -1

#找到与输入点最近的路径上的点，内部实现不用管
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

#名字匹配：输入map和输入框中的名字，输出为与之匹配的所有name，返回一个name的list（str的list）
def Regular_match_name(map, way_name):
    input_name_length = len(way_name)
    name_list = []
    for ways in map.ways:
        if 'name' in ways.attr.keys():
            try_name = ways.attr.get('name')
            try_name_length = len(try_name)
            get_name = 1
            for i in range(input_name_length):
                is_match = 0
                j = 0
                while j < try_name_length:
                    if try_name[j] == way_name[i]:
                        is_match = 1
                        j = j + 1
                        break
                    j = j + 1
                if is_match == 1:
                    continue
                else:
                    get_name = 0
                    break
            if get_name is 1 and try_name not in name_list:
                name_list.append(try_name)
    for keynd in map.keynode:
        if 'name' in keynd.attr.keys():
            try_name = keynd.attr.get('name')
            try_name_length = len(try_name)
            get_name = 1
            for i in range(input_name_length):
                is_match = 0
                j = 0
                while j < try_name_length:
                    if try_name[j] == way_name[i]:
                        is_match = 1
                        j = j + 1
                        break
                    j = j + 1
                if is_match == 1:
                    continue
                else:
                    get_name = 0
                    break
            if get_name is 1 and try_name not in name_list:
                name_list.append(try_name)
    return name_list

#输入名字，输出点，若没有，输出None
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

#外部接口：通过名字查询
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

#外部接口：通过点查询
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

#需求查询：my_lat,my_lon 是我的当前位置所在的经纬度，need为数字：1代表我要吃饭，2代表我要运动，3代表我要学习，4代表我要约会
def search_by_need(map, my_lat, my_lon, need):
    if need == 1:
        canteen_name = ["荷园教工餐厅", "熙春园餐厅", "近春园", "芝兰园餐厅", "玉树园", "紫荆园","桃李园", "听涛园", "丁香园", "清芬园",
                "观畴园", "澜院教工餐厅"]
        best_way = []
        best_way_distance = 10000000
        place_name = ""
        for canteen in canteen_name:
            canteen_node = find_the_name_of_points(map, canteen)
            temp_best_way, temp_distance = search_by_node(map, my_lat, my_lon, canteen_node.lat, canteen_node.lon)
            if temp_distance < best_way_distance:
                best_way = temp_best_way
                best_way_distance = temp_distance
                place_name = canteen
        if best_way_distance == 10000000 and place_name == "":
            return None, -1, ""
        else:
            return best_way, best_way_distance, place_name
    elif need == 2:
        sporting_name = ["紫荆操场", "篮球场", "网球场", "排球场", "东大操场", "西大操场", "西区体育馆", "棒球场", "气膜体育馆",
                        "游泳馆", "射击馆", "保龄球练习馆", "综合体育馆", "篮球馆","东区体育馆"]
        best_way = []
        best_way_distance = 10000000
        place_name = ""
        for sporting in sporting_name:
            sporting_node = find_the_name_of_points(map, sporting)
            temp_best_way, temp_distance = search_by_node(map, my_lat, my_lon, sporting_node.lat, sporting_node.lon)
            if temp_distance < best_way_distance:
                best_way = temp_best_way
                best_way_distance = temp_distance
                place_name = sporting
        if best_way_distance == 10000000 and place_name == "":
            return None, -1, ""
        else:
            return best_way, best_way_distance, place_name
    elif need == 3:
        learning_name = ["第一教学楼", "第四教学楼", "第三教学楼三段","第五教学楼", "第六教学楼A区", "第六教学楼B区",
                         "第六教学楼C区","第三教学楼一、二段", "第二教学楼", "图书馆", "人文社科图书馆", "新水利馆" ]
        best_way = []
        best_way_distance = 10000000
        place_name = ""
        for learning in learning_name:
            learning_node = find_the_name_of_points(map, learning)
            temp_best_way, temp_distance = search_by_node(map, my_lat, my_lon, learning_node.lat, learning_node.lon)
            if temp_distance < best_way_distance:
                best_way = temp_best_way
                best_way_distance = temp_distance
                place_name = learning
        if best_way_distance == 10000000 and place_name == "":
            return None, -1, ""
        else:
            return best_way, best_way_distance, place_name
    elif need == 4:
        dating_name = ["情人坡", "紫荆操场", "紫荆雕塑园", "荷塘月色","大草坪"]
        best_way = []
        best_way_distance = 10000000
        place_name = ""
        for dating in dating_name:
            dating_node = find_the_name_of_points(map, dating)
            temp_best_way, temp_distance = search_by_node(map, my_lat, my_lon, dating_node.lat, dating_node.lon)
            if temp_distance < best_way_distance:
                best_way = temp_best_way
                best_way_distance = temp_distance
                place_name = dating
        if best_way_distance == 10000000 and place_name == "":
            return None, -1, ""
        else:
            return best_way, best_way_distance, place_name
    else:
        print("Illegal Visit of search_by_need: need is illegal")
        return None, -2, ""

def search_by_node_best_riding_way(map, start_lat, start_lon, end_lat, end_lon):
    start_node = node(-1, start_lat, start_lon)
    end_node = node(-1, end_lat, end_lon)
    clo_start_node, start_distance = find_the_closest_point(map, start_node)
    clo_end_node, end_distance = find_the_closest_point(map, end_node)
    best_way_list, best_way_distance = find_best_walking_way(map.cross_list, clo_start_node, clo_end_node)
    if best_way_distance is -1:
        print("No Way!")
        return None, -1
    best_way_list.append(end_node)
    best_way_list.insert(0, start_node)
    best_way_distance += start_distance
    best_way_distance += end_distance
    return best_way_list, best_way_distance
