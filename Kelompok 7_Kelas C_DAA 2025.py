import heapq

# Definisi Topologi Jaringan (Graph)
# Format: 'Node': {'Neighbor': (Cost, Capacity)}
graph = {
    'A': {'B': (1, 1000), 'C': (1, 500)},
    'B': {'F': (1, 10)},
    'C': {'D': (1, 500)},
    'D': {'E': (1, 500)},
    'E': {'F': (1, 500)},
    'F': {}
}

#  Algoritma Shortest Path (Standard Dijkstra)
def shortest_path(graph, start, end):
    # Priority Queue menyimpan (current_cost, current_node, path_taken)
    queue = [(0, start, [start])]
    visited = set()
    
    while queue:
        cost, node, path = heapq.heappop(queue)
        
        if node in visited:
            continue
        visited.add(node)
        
        if node == end:
            return path, cost
            
        for neighbor, (link_cost, link_cap) in graph[node].items():
            if neighbor not in visited:
                heapq.heappush(queue, (cost + link_cost, neighbor, path + [neighbor]))
    return None, float('inf')

# Fungsi bantu hitung throughput jalur
def calculate_throughput(graph, path):
    min_cap = float('inf')
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        capacity = graph[u][v][1]
        if capacity < min_cap:
            min_cap = capacity
    return min_cap

# Algoritma Bottleneck Path (Modified Dijkstra / Max-Min)
def bottleneck_path(graph, start, end):
    # Menggunakan Max-Heap (di Python pakai min-heap nilai negatif)
    # Menyimpan (-width, current_node, path_taken)
    # Width awal adalah infinity
    queue = [(-float('inf'), start, [start])]
    widths = {node: 0 for node in graph}
    widths[start] = float('inf')
    
    while queue:
        current_width_neg, u, path = heapq.heappop(queue)
        current_width = -current_width_neg
        
        if u == end:
            return path, current_width
            
        for v, (cost, capacity) in graph[u].items():
            # Logika Max-Min: Kapasitas dibatasi oleh link terkecil
            new_width = min(current_width, capacity)
            
            # Jika menemukan jalur yang lebih "lebar" ke v
            if new_width > widths[v]:
                widths[v] = new_width
                heapq.heappush(queue, (-new_width, v, path + [v]))
                
    return None, 0

print("SIMULASI PERBANDINGAN ALGORITMA ROUTING")
print("Topologi: Sesuai Tabel 1 (Source: A, Destination: F)")

# Jalankan Shortest Path
sp_path, sp_cost = shortest_path(graph, 'A', 'F')
sp_throughput = calculate_throughput(graph, sp_path)

print(f"\n[1] ALGORITMA SHORTEST PATH (DIJKSTRA)")
print(f"    - Jalur Terpilih : {' -> '.join(sp_path)}")
print(f"    - Total Cost     : {sp_cost} (Hops)")
print(f"    - Throughput     : {sp_throughput} Mbps")

# Jalankan Bottleneck Path
bp_path, bp_width = bottleneck_path(graph, 'A', 'F')

print(f"\n[2] ALGORITMA BOTTLENECK PATH (MAX-MIN)")
print(f"    - Jalur Terpilih : {' -> '.join(bp_path)}")
print(f"    - Total Cost     : {len(bp_path)-1} (Hops)")
print(f"    - Throughput     : {bp_width} Mbps")