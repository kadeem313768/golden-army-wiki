from flask import Flask, jsonify

app = Flask(__name__)

# 讀取Wiki資料
wiki_data = {}

with open('golden_army_wiki.txt', 'r', encoding='utf-8') as f:
    current_title = None
    current_content = []
    for line in f:
        line = line.strip()
        if line.startswith('### '):
            if current_title:
                wiki_data[current_title] = "\n".join(current_content)
            current_title = line[4:]
            current_content = []
        else:
            current_content.append(line)
    if current_title:
        wiki_data[current_title] = "\n".join(current_content)

@app.route('/wiki', methods=['GET'])
def get_all_wiki():
    return jsonify(wiki_data)

@app.route('/wiki/<string:title>', methods=['GET'])
def get_single_wiki(title):
    return jsonify({title: wiki_data.get(title, "Not Found")})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
