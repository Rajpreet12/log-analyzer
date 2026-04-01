from src.parser import parse_line

line = "2026-03-31 10:15:42 [ERROR] something failed"
entry = parse_line(line)

print("Parsed Log Entry:")
print(f"Time: {entry.timestamp}")
print(f"Level: {entry.level}")
print(f"Message: {entry.message}")
