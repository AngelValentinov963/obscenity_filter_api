import os
import ahocorasick
import json

print("Looking for file in:", os.getcwd())

def build_automaton(filepath):
    A = ahocorasick.Automaton()
    with open(filepath, "r", encoding="utf-8") as file:
        keywords = [line.strip() for line in file if line.strip()]
        for idx, word in enumerate(keywords):
            A.add_word(word, (idx, word))
    A.make_automaton()
    return A

def find_words_aho(input_str, automaton):
    found = []
    for _, (_, word) in automaton.iter(input_str):
        found.append(word)
    return list(set(found))  # remove duplicates

# Resolve file path relative to script location
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "bg-obscene-cyrillic.txt")

# Build automaton once
automaton = build_automaton(file_path)

if __name__ == "__main__":
    user_input = input("Enter text to check: ")
    matches = find_words_aho(user_input, automaton)
    result = {
        "input": user_input,
        "matches_found": bool(matches),
        "matched_words": matches
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
