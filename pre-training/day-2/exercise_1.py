import re
from typing import Dict

def word_frequency(text: str) -> Dict[str, int]:
    if not isinstance(text, str):
        raise TypeError(f"text must be a string, got {type(text).__name__}")

    words = re.findall(r"[a-z0-9]+(?:'[a-z0-9]+)?", text.lower())

    freq: Dict[str, int] = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq

paragraph = (
    "Python is fun, and Python is easy to learn. "
    "When you practice every day, you start to code faster. "
    "Learning Python improves your problem-solving skills."
)

freq = word_frequency(paragraph)

top_5 = sorted(freq.items(), key=lambda item: item[1], reverse=True)[:5]
print("Top 5 words:")
for word, count in top_5:
    print(f"{word}: {count}")