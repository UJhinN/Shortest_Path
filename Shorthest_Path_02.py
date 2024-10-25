import csv
import os
from pathlib import Path

def find_csv_files():
    """ค้นหาไฟล์ CSV ในโครงสร้างโฟลเดอร์ทั้งหมด"""
    csv_files = []
    
    # หา path ของโฟลเดอร์ปัจจุบัน
    current_file = Path(__file__).resolve()
    current_dir = current_file.parent
    
    # ค้นหาไฟล์ CSV ในโฟลเดอร์เดียวกับไฟล์ .py
    csv_files.extend(current_dir.glob('*.csv'))
    
    # จัดเรียงไฟล์ตามชื่อ
    csv_files.sort()
    
    # แปลง Path objects เป็น tuples ของ (ชื่อไฟล์, path เต็ม)
    return [(f.name, str(f.absolute())) for f in csv_files]

def main(start, end, file_path):
    try:
        # อ่านแผนที่จากไฟล์ csv 
        with open(file_path, encoding="utf-8", newline='') as csvfile:
            reader = csv.reader(csvfile)
            roads = []
            next(reader)  # ข้ามส่วนหัวตาราง (header)
            for row in reader:
                roads.append(row) 

        if not roads:
            print("ไม่พบข้อมูลในไฟล์ CSV")
            return
        
        # สร้าง dict เก็บชื่อเมืองและระยะทาง
        dict_csv = {}
        for row in roads:
            node1 = row[0]
            node2 = row[1]
            if node1 not in dict_csv:
                dict_csv[node1] = []
            if node2 not in dict_csv:
                dict_csv[node2] = []
            if row == roads[0]:
                dict_csv[node1].append(node2)
                dict_csv[node2].append(node1)
            else:
                dict_csv[node1].append(node2)
        
        # ตรวจสอบว่าเมืองต้นทางและปลายทางมีอยู่ในแผนที่หรือไม่
        if start not in dict_csv:
            print(f"ไม่พบเมือง {start} ในแผนที่")
            return
        if end not in dict_csv:
            print(f"ไม่พบเมือง {end} ในแผนที่")
            return

        # หาเส้นทางที่เป็นไปได้ทั้งหมด
        paths = find_all_paths(dict_csv, start, end)
        
        if not paths:
            print(f"ไม่พบเส้นทางจากเมือง {start} ไปยังเมือง {end}")
            return

        # คำนวณระยะทาง
        all_sum_distance = sum_distance(paths, roads)

    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {str(e)}")

def find_all_paths(dict_csv, start, end):
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

def sum_distance(paths, roads):
    answer = []
    data = []
    data1 = []
    long = []
    sum_dist = []
    min_dist = []

    print("\nเส้นทางที่เป็นไปได้ทั้งหมด:")
    print("-" * 50)

    for path in paths:
        for i in roads:
            for y in range(0, len(path)):
                if (i[0] in (path[y-2])) and (i[1] in path[y-1]):
                    long.append(int(i[2]))
            sum_dist.append(long)
            long = []

        print(f'เส้นทาง: {" -> ".join(path)} ระยะทาง = {sum_sublists(sum_dist)} หน่วย')
        
        data.append(path)
        data.append(sum_sublists(sum_dist))
        data1.append(data)
        data = []

        for i in range(0, len(data1)):
            answer1 = {'path': data1[i][0], 'Distance': data1[i][1]}
            answer.append(answer1)
        min_dist.append(sum_sublists(sum_dist))
        sum_dist = []

    x = 0
    while True:
        if answer[x]['Distance'] == min(min_dist):
            print('\nผลลัพธ์:')
            print('-' * 50)
            print('เส้นทางที่สั้นที่สุด: {} ระยะทาง = {} หน่วย'.format(
                " -> ".join(answer[x]['path']), answer[x]['Distance']))
            print('-' * 50)
            break
        x += 1

def sum_sublists(value):
    total_sum = 0
    for sublist in value:
        if sublist:
            total_sum += sum(sublist)
    return total_sum

if __name__ == '__main__':
    print('-' * 50)
    print("โปรแกรมค้นหาเส้นทางที่สั้นที่สุด")
    print('-' * 50)
    
    # ค้นหาไฟล์ CSV ที่มีอยู่
    available_files = find_csv_files()
    
    if available_files:
        print("\nไฟล์ CSV ที่มีอยู่:")
        for i, (file_name, _) in enumerate(available_files, 1):
            print(f"{i}. {file_name}")
        print()
        
        # รับ input จากผู้ใช้
        while True:
            try:
                file_input = input('ป้อนหมายเลขหรือชื่อไฟล์ CSV: ').strip()
                
                # ถ้าผู้ใช้ป้อนหมายเลข
                if file_input.isdigit():
                    index = int(file_input) - 1
                    if 0 <= index < len(available_files):
                        selected_file = available_files[index][1]  # ใช้ full path
                        break
                    else:
                        print("หมายเลขไม่ถูกต้อง กรุณาลองใหม่")
                # ถ้าผู้ใช้ป้อนชื่อไฟล์
                else:
                    matching_files = [f[1] for f in available_files if f[0].lower() == file_input.lower()]
                    if matching_files:
                        selected_file = matching_files[0]  # ใช้ไฟล์แรกที่เจอ
                        break
                    else:
                        print("ไม่พบไฟล์ที่ระบุ กรุณาลองใหม่")
            except ValueError:
                print("กรุณาป้อนหมายเลขหรือชื่อไฟล์ที่ถูกต้อง")
    else:
        print("ไม่พบไฟล์ CSV ในระบบ")
        exit()

    start = input('ป้อนเมืองต้นทาง: ').strip().upper()
    end = input('ป้อนเมืองปลายทาง: ').strip().upper()
    
    main(start, end, selected_file)