import json
import os

# Configurazione
input_file = "data.json"
output_dir = "conversations"
os.makedirs(output_dir, exist_ok=True)

def ricostruisci_conversazione(mapping, current_id):
    thread = []
    visited = set()

    while current_id and current_id not in visited:
        visited.add(current_id)
        node = mapping.get(current_id)

        if not isinstance(node, dict):
            break

        message = node.get("message")
        if (
            isinstance(message, dict) and
            isinstance(message.get("author"), dict) and
            message["author"].get("role") in ["user", "assistant"] and
            isinstance(message.get("content"), dict)
        ):
            parts = message["content"].get("parts")
            if not (isinstance(parts, list) and len(parts) > 0):
                parts = [""]

            autore = message["author"]["role"]
            contenuto = parts[0]
            thread.append((autore, contenuto))

        figli = node.get("children")
        if isinstance(figli, list) and len(figli) > 0:
            current_id = figli[0]  # prendo solo il primo figlio per linearità
        else:
            break

    return thread

# Carica il file data.json
try:
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    print(f"Errore nella lettura di {input_file}: {e}")
    exit(1)

conversazioni = data if isinstance(data, list) else [data]

for idx, conv in enumerate(conversazioni):
    if not isinstance(conv, dict):
        print(f"Conversazione {idx+1} non valida, salto...")
        continue

    mapping = conv.get("mapping")
    if not isinstance(mapping, dict):
        print(f"Nessun mapping valido nella conversazione {idx+1}")
        continue

    title = conv.get("title") or f"conversazione_{idx+1}"
    # Normalizza il nome file
    title_norm = "".join(c if c.isalnum() or c in " _-" else "_" for c in title).strip()
    filename = os.path.join(output_dir, f"{idx+1:03d}_{title_norm}.json")

    # Trova nodo radice
    root_id = None
    for k, v in mapping.items():
        if not isinstance(v, dict):
            continue
        if "parent" not in v or v.get("parent") is None:
            root_id = k
            break
    if not root_id:
        print(f"Nessun nodo radice trovato nella conversazione {idx+1}")
        continue

    thread = ricostruisci_conversazione(mapping, root_id)

    # Costruisci lista di coppie User - assistant
    conversazione_strutturata = []
    i = 0
    while i < len(thread):
        user_msg = thread[i][1] if thread[i][0] == "user" else ""
        assistant_msg = ""
        if i+1 < len(thread) and thread[i+1][0] == "assistant":
            assistant_msg = thread[i+1][1]
            i += 2
        else:
            i += 1
        if user_msg or assistant_msg:
            conversazione_strutturata.append({"User": user_msg, "assistant": assistant_msg})

    # Salva su file JSON
    try:
        with open(filename, "w", encoding="utf-8") as out:
            json.dump(conversazione_strutturata, out, ensure_ascii=False, indent=2)
        print(f"Salvata conversazione {idx+1} in {filename}")
    except Exception as e:
        print(f"Errore salvando {filename}: {e}")

print(f"\nTutte le conversazioni salvate nella cartella: {output_dir}")
