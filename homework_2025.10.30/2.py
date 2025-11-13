from pathlib import Path
import json

path=Path('names_and_counts.json')
contents=path.read_text()
results=json.loads(contents)

print(results)