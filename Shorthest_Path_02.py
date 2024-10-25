import csv
from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx

def find_csv_files():
    """ค้นหาไฟล์ CSV ในโฟลเดอร์ปัจจุบัน"""
    current_dir = Path(__file__).resolve().parent
    csv_files = list(current_dir.glob('*.csv'))
    return [(f.name, str(f.absolute())) for f in sorted(csv_files)]

def find_all_paths(dict_csv, start, end):
    """หาเส้นทางที่เป็นไปได้ทั้งหมด"""
    paths = []
    stack = [(start, [start])]
    while stack:
        node, path = stack.pop()
        if node == end:
            paths.append(path)
        for p in dict_csv[node]:
            if p not in path:
                stack.append((p, path + [p]))
    return paths

def calculate_path_length(path, roads):
    """คำนวณระยะทางรวม"""
    total = 0
    for i in range(len(path) - 1):
        for road in roads:
            if (road[0] == path[i] and road[1] == path[i + 1]) or \
                (road[1] == path[i] and road[0] == path[i + 1]):
                total += int(road[2])
                break
    return total

def visualize_shortest_path(dict_csv, paths, roads, start, end):
    """แสดงแผนที่และเส้นทางที่สั้นที่สุด"""
    # สร้างกราฟ
    G = nx.Graph()
    for road in roads:
        G.add_edge(road[0], road[1], weight=int(road[2]))
    
    # หาเส้นทางที่สั้นที่สุด
    shortest_path = min(paths, key=lambda p: calculate_path_length(p, roads))
    shortest_length = calculate_path_length(shortest_path, roads)
    
    # สร้างภาพ
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)
    
    # วาดเส้นทางทั้งหมด
    nx.draw_networkx_edges(G, pos, alpha=0.2, edge_color='gray')
    
    # วาดโหนด
    node_colors = ['lightblue' if node not in [start, end] 
                    else 'green' if node == start else 'red' 
                    for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors)
    
    # แสดงชื่อเมือง
    nx.draw_networkx_labels(G, pos)
    
    # แสดงระยะทาง
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    
    # วาดเส้นทางที่สั้นที่สุด
    path_edges = list(zip(shortest_path[:-1], shortest_path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, 
                            edge_color='r', width=2)
    
    plt.title(f"ShortestPath: {' -> '.join(shortest_path)}\n"
                f"Distance: {shortest_length} unit")
    plt.axis('off')
    plt.show()

def main(start, end, file_path):
    try:
        # อ่านข้อมูลจากไฟล์ CSV
        with open(file_path, encoding="utf-8", newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # ข้ามส่วนหัวตาราง
            roads = list(reader)

        if not roads:
            print("ไม่พบข้อมูลในไฟล์ CSV")
            return

        # สร้าง dict เก็บข้อมูลเส้นทาง
        dict_csv = {}
        for row in roads:
            node1, node2 = row[0], row[1]
            if node1 not in dict_csv: dict_csv[node1] = []
            if node2 not in dict_csv: dict_csv[node2] = []
            dict_csv[node1].append(node2)
            dict_csv[node2].append(node1)

        # ตรวจสอบเมืองต้นทางและปลายทาง
        if start not in dict_csv or end not in dict_csv:
            print(f"ไม่พบเมือง {start} หรือ {end} ในแผนที่")
            return

        # หาเส้นทางและแสดงผล
        paths = find_all_paths(dict_csv, start, end)
        if not paths:
            print(f"ไม่พบเส้นทางจาก {start} ไปยัง {end}")
            return

        visualize_shortest_path(dict_csv, paths, roads, start, end)

    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {str(e)}")

if __name__ == '__main__':
    print("โปรแกรมค้นหาเส้นทางที่สั้นที่สุด")
    print("-" * 50)
    
    available_files = find_csv_files()
    if not available_files:
        print("ไม่พบไฟล์ CSV ในระบบ")
        exit()

    print("\nไฟล์ CSV ที่มีอยู่:")
    for i, (name, _) in enumerate(available_files, 1):
        print(f"{i}. {name}")

    while True:
        file_input = input('\nเลือกไฟล์ (ป้อนหมายเลข): ').strip()
        if file_input.isdigit():
            index = int(file_input) - 1
            if 0 <= index < len(available_files):
                selected_file = available_files[index][1]
                break
        print("กรุณาป้อนหมายเลขให้ถูกต้อง")

    start = input('ป้อนเมืองต้นทาง: ').strip().upper()
    end = input('ป้อนเมืองปลายทาง: ').strip().upper()
    
    main(start, end, selected_file)
