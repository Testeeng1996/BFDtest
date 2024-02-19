
def parse_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    context = None
    prefix = None
    result = []

    for line in lines:
        line = line.strip()

        # Detect context line and capture context value
        if "Context   :" in line:
            context = line.split(":")[1].split()[0]

        # Detect prefix and capture prefix value
        if "/128" in line:
            prefix = line.split()[0]

        # Detect addr and associate with current context and prefix
        if "addr" in line:
            addr = line.split()[2]
            entry = {
                "context": context,
                "prefix": prefix,
                "addr": addr
            }
            result.append(entry)

    return result

# Example usage
filename = "Check2BFDInputStatus.txt"
parsed_data = parse_file(filename)
for entry in parsed_data:
    print(entry)

import json
print(json.dumps(parsed_data))
