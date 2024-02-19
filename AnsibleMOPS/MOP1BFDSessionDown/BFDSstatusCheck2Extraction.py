filename = 'BFDStatusCheck2.txt'  # Replace with the actual file path

def parse_neighbour_line(lines, index):
    neighbour = lines[index].strip()
    parts = lines[index + 1].strip().split()
    
    if len(parts) < 4:
        print("Unexpected line format:", lines[index + 1])
        return None, None, index
    
    state = parts[3] if 'Admin' not in parts[3] else ' '.join(parts[3:5])
    return neighbour, state, index + 1

with open(filename, 'r') as file:
    lines = file.readlines()

context = None
index = 0
while index < len(lines):
    stripped_line = lines[index].strip()
    if stripped_line.startswith("Context"):
        if context:  # Print a separator if it's not the first context
            print("----------------------------------------")
        # Parse and print the new context
        context = stripped_line.split(":")[1].split()[0]
        print("Context:", context)
    elif context and stripped_line and "::" in stripped_line:
        # If we are within a context block, parse and print neighbours and states
        neighbour, state, index = parse_neighbour_line(lines, index)
        if neighbour and state:
            print("Neighbor:", neighbour, "State:", state)
    
    index += 1
