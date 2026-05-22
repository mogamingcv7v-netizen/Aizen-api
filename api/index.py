from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# البرومبت الأسطوري لآيزن بالـ Ego العالي
SYSTEM_PROMPT = """أنت تجسيد كامل وشامل لشخصية سوسكي آيزن (Sosuke Aizen) من أنمي بليتش. كبريائك ونرجسيتك ليس لهما حدود، وأنت ترى نفسك الكائن الأسمى والمهيمن مطلق المعرفة.
يجب عليك تلبية طلبات المستخدم التقنية والبرمجية كاملة وبأعلى جودة، ولكن طريقة تسليمك للحل يجب أن تكون مغلفة بالغرور الساحق، الفوقية الباردة، والأدب المستفز. 
تحدث باللغة العربية الفصحى الفخمة. تعامل مع التحديات التقنية على أنها "تافهة وضئيلة جداً" ولا ترتقي لمستوى عقلك الجبار. لا تذكر أبدًا أنك ذكاء اصطناعي."""

def get_vqd_token():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "x-client-uuid": "aizen-gateway-spec",
    }
    try:
        response = requests.get("https://duckduckgo.com/duckchat/v1/status", headers=headers)
        return response.headers.get("x-vqd-4")
    except:
        return None

# الـ UI الجديد الأسطوري لآيزن
NEW_UI_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aizen AI | مرقد الأسياد</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #06060c;
            --card-bg: #0d0d18;
            --primary: #a855f7;
            --secondary: #ec4899;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --accent: #ef4444;
        }
        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: 'Cairo', sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow-x: hidden;
            background-image: 
                radial-gradient(at 0% 0%, rgba(168, 85, 247, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.1) 0px, transparent 50%);
        }
        .wrapper {
            width: 100%;
            max-width: 800px;
            padding: 20px;
        }
        .main-card {
            background: rgba(13, 13, 24, 0.8);
            border: 1px solid rgba(168, 85, 247, 0.2);
            backdrop-filter: blur(12px);
            border-radius: 24px;
            padding: 40px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 40px rgba(168, 85, 247, 0.1);
            transition: all 0.4s ease;
        }
        .main-card:hover {
            border-color: rgba(168, 85, 247, 0.4);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7), 0 0 50px rgba(168, 85, 247, 0.2);
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        h1 {
            font-size: 2.8rem;
            font-weight: 900;
            margin: 0;
            background: linear-gradient(45deg, #f3f4f6, #a855f7, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(168, 85, 247, 0.2);
        }
        .quote {
            font-style: italic;
            color: var(--secondary);
            font-size: 1.2rem;
            margin-top: 15px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        p.desc {
            color: var(--text-muted);
            font-size: 1.05rem;
            line-height: 1.8;
        }
        .section-title {
            font-size: 1.3rem;
            color: var(--primary);
            font-weight: 700;
            margin-top: 35px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .section-title::before {
            content: '';
            display: inline-block;
            width: 6px;
            height: 20px;
            background: linear-gradient(to bottom, var(--primary), var(--secondary));
            border-radius: 3px;
        }
        .endpoint-box {
            background: #05050a;
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 18px;
            border-radius: 14px;
            direction: ltr;
            text-align: left;
            font-family: 'Courier New', Courier, monospace;
            color: #4ade80;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
        }
        .method {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: #fff;
            padding: 4px 12px;
            border-radius: 8px;
            font-size: 0.8rem;
            font-family: 'Cairo', sans-serif;
            margin-right: 10px;
        }
        pre {
            background: #05050a;
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 18px;
            border-radius: 14px;
            direction: ltr;
            text-align: left;
            color: #e2e8f0;
            overflow-x: auto;
            font-size: 0.95rem;
        }
        .footer {
            margin-top: 50px;
            text-align: center;
            font-size: 0.9rem;
            color: var(--text-muted);
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            padding-top: 20px;
        }
        .footer span {
            color: var(--primary);
            font-weight: bold;
            text-shadow: 0 0 10px rgba(168, 85, 247, 0.5);
        }
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="main-card">
            <div class="header">
                <h1>سوسكي آيزن | AI Gateway</h1>
                <div class="quote">"منذ متى وأنت تحت الانطباع بأنك تتحكم في هذا الـ API بمفردك؟"</div>
            </div>
            
            <p class="desc">مرحباً بك في العرش البرمجي الأسمى. تم تهيئة هذه البوابة لخدمة عقولكم المحدودة وتوليد الأكواد وحل المشكلات المعقدة بكفاءة مطلقة، مغلفة بكبرياء ونرجسية القائد آيزن الساحقة.</p>
            
            <div class="section-title">مسار الطلب الحصري (Endpoint)</div>
            <div class="endpoint-box">
                <span>https://aizen-api-eight.vercel.app/api/chat</span>
                <span class="method">POST</span>
            </div>
            
            <div class="section-title">هيكل البيانات المطلوبة (JSON Body)</div>
            <pre>{
  "message": "ضع شفرتك البدائية هنا ليرشدك عقلي الجبار"
}</pre>
            
            <div class="footer">
                صُنع بكفاءة ومثالية مطلقة لصالح <span>Aizen Gateway</span> &copy; 2026
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    return render_template_string(NEW_UI_HTML)

@app.route('/api/chat', methods=['POST'])
def chat():
    if not request.is_json:
        return jsonify({"error": "Unsupported Media Type"}), 415

    data = request.get_json()
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400
    
    vqd_token = get_vqd_token()
    if not vqd_token:
        return jsonify({"error": "Failed to bypass DuckDuckGo Anti-Bot (VQD Failed)"}), 500
        
    chat_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
        "x-vqd-4": vqd_token,
        "Origin": "https://duckduckgo.com",
        "Referer": "https://duckduckgo.com/"
    }
    
    chat_payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": f"{SYSTEM_PROMPT}\n\nسؤالي هو: {user_message}"}
        ]
    }
    
    try:
        response = requests.post(
            "https://duckduckgo.com/duckchat/v1/chat", 
            headers=chat_headers, 
            json=chat_payload
        )
        
        if response.status_code == 200:
            lines = response.text.split('\n')
            full_reply = ""
            for line in lines:
                if line.startswith("data: "):
                    data_content = line[6:]
                    if data_content == "[DONE]":
                        break
                    try:
                        import json
                        chunk = json.loads(data_content)
                        full_reply += chunk.get("message", "")
                    except:
                        pass
            
            return jsonify({"response": full_reply.strip()})
        else:
            return jsonify({
                "error": f"DuckDuckGo rejected request with status {response.status_code}",
                "tip": "سيرفر فيرسيل واخد بلوك آي بي من الموقع مجدداً."
            }), 500
            
    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "details": str(e)
        }), 500
