def allocate_memory(mem, size):
    for idx in range(len(mem) - size + 1):
        # Check if the current block of the required size is free
        if all(byte == 0 for byte in mem[idx:idx + size]):
            # Allocate memory
            mem[idx:idx + size] = [1] * size
            return idx
    return -1

if __name__ == '__main__':
    memory = [0] * 100
    process_size = 10
    index = allocate_memory(memory, process_size)

    print('Starting index of allocated memory:', index)
    print('Memory after allocation: ', *memory[:15], sep='')