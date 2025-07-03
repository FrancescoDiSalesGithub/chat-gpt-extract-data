import json
import sys

with open(sys.argv[1], 'r',encoding='utf-8') as file:
    data = json.load(file)
    list_user = []
    list_assistant = []

    for index in range(len(data)):
        keys = data[index]["mapping"].keys()
        for keyitem in keys:
            try:
                key_items = data[index]["mapping"][keyitem]
              
                if key_items["message"]["author"]["role"] == "assistant":
                    author = {"author": "assistant", "content": key_items["message"]["content"]["parts"],"id": key_items["message"]["id"],"children": key_items["children"]}
                    list_assistant.append(author)
                elif key_items["message"]["author"]["role"] == "user":
                    author = {"author": "user", "content": key_items["message"]["content"]["parts"],"id": key_items["message"]["id"],"children": key_items["children"]}
                    list_user.append(author)
               
            except Exception as e:
                continue

    with open("user.txt", "w", encoding='utf-8') as user_file:
        for item in list_user:
            user_file.write(str(item) +"\n")

    with open("assistant.txt", "w", encoding='utf-8') as assistant_file:
        for item in list_assistant:
            assistant_file.write(str(item) + "\n")
