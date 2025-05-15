import xkcd as x
import random
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import threading

write_lock = threading.Lock()  # Global lock for file writing

def write_quote(quote: str, count: int):
    with write_lock:
        with open("data.txt", "a+", encoding="utf-8") as f:
            f.write(f"{count} - {quote}\n")

def process_comic(i):
    try:
        # Replace with your actual XKCD fetching logic if needed
        text = x.get_alt_text_from_xkcd_url(f"https://xkcd.com/{i}/")
        write_quote(text, i)
        return True
    except Exception as e:
        print(f"Error processing comic {i}: {str(e)}")
        return False

def fetch_all():
    current_xkcd_count = 3089
    y = list(range(1, current_xkcd_count + 1))
    y.remove(404)

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(process_comic, i): i for i in y}
        for t, future in enumerate(as_completed(futures), 1):
            if t % 100 == 0:
                print(f"Processed {t}/{current_xkcd_count} comics")

def strip_punctuation(_in: str):
    translator = str.maketrans('', '', string.punctuation)
    return _in.translate(translator)

def data_to_list():
    out = []
    with open("data.txt", "r+", encoding="utf-8") as f:
        lines = f.readlines()
        for l in lines:
            start = l.find(" - ") + 3
            out.append(l[start:].strip())
    return set(out)

def data_to_tuples():
    out = []
    with open("data.txt", "r+", encoding="utf-8") as f:
        lines = f.readlines()
        for l in lines:
            start = l.find(" - ")
            i = int(l[:start].strip())
            start = l.find(" - ") + 3
            text = l[start:].strip()
            out.append((i, text))
    return set(out)

def assemble_dictionary(lines: set):
    words = {}
    for line in lines:
        for word in line[1].split():
            key = word.lower()
            if key not in words:
                words[key] = [line[0]]
            else:
                words[key].append(line[0])
    return words

def get_text_of(i: int):
    lines = data_to_tuples()
    for line in lines:
        if line[0] == i:
            return line[1]
    print("Could not find comic:", i)

def encrypt(text: str):
    text = strip_punctuation(text)
    lines = data_to_tuples()
    words = assemble_dictionary(lines)
    cypher = []
    for word in text.split(" "):
        try:
            candidates = words[word.lower()]
        except KeyError:
            print("Word not found:", word.lower())
            cypher.append((0, 0))
            continue
        c = random.choice(candidates)
        t = get_text_of(c)
        word_number = t.lower().split(" ").index(word.lower()) + 1
        cypher.append((c, word_number))
    out = ""
    for o in cypher:
        out += f"{o[0]}:{o[1]}-"
    return out[:-1]

def decrypt(text: str):
    words = text.split("-")
    out = ""
    for word in words:
        word_number = int(word.split(":")[1]) - 1
        x_number = int(word.split(":")[0])
        text_split = get_text_of(x_number).strip().lower().split(" ")
        decrypted_word = text_split[word_number]
        out += decrypted_word
        out += " "
    return out.capitalize()

def regenerate_text():
    with open("data.txt", "w", encoding="utf-8") as f:
        f.write("")
    fetch_all()

def main():
    fetch_all()
    print("Welcome to the XES-3088 Encryption Terminal")
    input()
    while True:
        os.system("clear")
        mode = input("Encrypt or Decrypt? (e/d) ").lower().strip()
        _in = input("Enter text here: ")
        if mode == "e":
            out = encrypt(_in)
        elif mode == "d":
            out = decrypt(_in)
        print("\nOutput:", out)
        input("\n\n[ENTER] to continue\n")

if __name__ == "__main__":
    main()
