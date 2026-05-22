from flask import Flask, request, jsonify
from curl_cffi import requests # دي المكتبة اللي بتخدع حماية المواقع

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Bad Request"}), 400

    # استخدمنا هنا واحد من المصادر القوية اللي في الصور (origin.eqing.tech)
    url = "https://origin.eqing.tech/v1/chat/completions"
    
    payload = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": data['message']}]
    }

    try:
        # impersonate="chrome120" بتخلي السيرفر يفتكرك متصفح كروم حقيقي مش سكربت
        response = requests.post(url, json=payload, impersonate="chrome120", timeout=20)
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"API Rejected with code {response.status_code}", "raw": response.text}), 500
            
    except Exception as e:
        return jsonify({"error": "Connection Failed", "details": str(e)}), 500

if __name__ == '__main__':
    app.run()
