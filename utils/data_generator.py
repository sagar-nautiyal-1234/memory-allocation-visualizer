import random
# from utils import input_config

priority_colors = {"low": "#FCA5A5", "medium": "#FACC15", "high": "#6EE7B7"}
priority_order = {"high": 3, "medium": 2, "low": 1}

number_of_processes = 0

def generate_data():
    processes = []
    memory_blocks = []
    total_process_memory = 0
    total_memory = 0

    for i in range(number_of_processes):
        priority = random.choices(["high", "medium", "low"], weights=[2, 2, 4], k=1)[0]
        size = random.randint(50, 300)
        processes.append({
            "id": i,
            "size": size,
            "priority": priority,
            "color": priority_colors[priority]
        })
        total_process_memory += size

    processes.sort(key=lambda p: p["id"])

    while total_memory < total_process_memory * 0.75:
        block_size = random.randint(400, 800)
        memory_blocks.append(block_size)
        total_memory += block_size

    return processes, memory_blocks