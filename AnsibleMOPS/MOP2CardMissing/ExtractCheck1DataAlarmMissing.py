import re

with open("NewCheck1AlarmMissing.txt", "r") as f:
    data = f.read()

# Search for the "Card Missing" alarm and extract the card number
matches = re.findall(r"source\s+/cardipr:card\[cardipr:card-slot='(\d+)'\]\n.*?additional-text\s+\"Card Missing\"", data, re.DOTALL)

if matches:
    card_numbers = ', '.join(matches)
    print(f"Card Slot Numbers: {card_numbers}")
else:
    print("Card number not found")
    
