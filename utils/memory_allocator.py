from utils.data_generator import priority_order

def allocate_memory(processes, memory_blocks, strategy):
    blocks = memory_blocks[:]
    allocation = [-1] * len(processes)
    failures = []
    allocation_visual = [[] for _ in range(len(blocks))]
    logs = []
    last_index = 0

    for i, process in enumerate(sorted(processes, key=lambda p: priority_order[p["priority"]], reverse=True)):
        selected_idx = -1
        logs.append(f"Allocating P{process['id']} (Size: {process['size']}) Priority: {process['priority']}")

        if strategy == "next_fit":
            n = len(blocks)
            # scan from last_index → end, then 0 → last_index-1
            for offset in range(n):
                j = (last_index + offset) % n
                if blocks[j] >= process["size"]:
                    selected_idx = j
                    last_index = j              
                    break
        else:
            for j, block in enumerate(blocks):
                if block >= process["size"]:
                    if strategy == "first_fit":
                        selected_idx = j
                        break
                    elif strategy == "best_fit":
                        if selected_idx == -1 or block < blocks[selected_idx]:
                            selected_idx = j
                    elif strategy == "worst_fit":
                        if selected_idx == -1 or block > blocks[selected_idx]:
                            selected_idx = j

        if selected_idx != -1:
            allocation[i] = selected_idx
            blocks[selected_idx] -= process["size"]
            allocation_visual[selected_idx].append((process["id"], process["size"], process["color"]))
            logs.append(f" → Allocated to Block {selected_idx} (Remaining: {blocks[selected_idx]})")
        else:
            failures.append(process)
            logs.append(" → Failed to Allocate")

    return allocation, failures, allocation_visual, blocks, logs
