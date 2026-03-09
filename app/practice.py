from pathlib import Path

file = Path("poem.txt")
file.write_text("Twinkle Twinkle Little Stars!!!")

content = file.read_text()
print(content)
