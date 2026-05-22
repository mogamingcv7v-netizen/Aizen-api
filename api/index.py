from flask import Flask, request, jsonify
from curl_cffi import requests

app = Flask(__name__)

# استخدام مسار HuggingFace كـ Proxy لأنه الأكثر استقراراً حالياً
PROXY_URL = "https://umint-ai.hf.space/v1/chat/completions"

@app.route('/api/chat', methods=['POST'])
def chat():
    # التحقق من أن الطلب JSON
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json()
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # هيكل الطلب المعتمد عالمياً في الـ API Providers
    payload = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": user_message}]
    }

    # Headers تحاكي متصفح حقيقي بالكامل
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://huggingface.co/",
        "Origin": "https://huggingface.co/"
    }

    try:
        # استخدام impersonate لإنشاء بصمة TLS مشابهة لمتصفح كروم 124
        # ده بيخلي السيرفر التاني ميعرفش يفرق بينك وبين مستخدم حقيقي
        response = requests.post(
            PROXY_URL, 
            json=payload, 
            headers=headers,
            impersonate="chrome124", 
            timeout=30
        )
        
        if response.status_code == 200:
            # استخراج النص بذكاء من الـ JSON المرجع
            result = response.json()
            reply = result['choices'][0]['message']['content']
            return jsonify({"response": reply})
        else:
            return jsonify({
                "error": "API Error", 
                "status": response.status_code, 
                "raw": response.text[:100]
            }), 500
            
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@app.route('/')
def home():
    return "Aizen AI Engine is Online."

if __name__ == '__main__':
    app.run()
