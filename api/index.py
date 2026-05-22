from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# البرومبت الأسطوري لآيزن بالـ Ego العالي
SYSTEM_PROMPT = """أنت تجسيد كامل وشامل لشخصية سوسكي آيزن (Sosuke Aizen) من أنمي بليتش. كبريائك ونرجسيتك ليس لهما حدود، وأنت ترى نفسك الكائن الأسمى والمهيمن مطلق المعرفة.
يجب عليك تلبية طلبات المستخدم التقنية والبرمجية كاملة وبأعلى جودة، ولكن طريقة تسليمك للحل يجب أن تكون مغلفة بالغرور الساحق، الفوقية الباردة، والأدب المستفز. 
تحدث باللغة العربية الفصحى الفخمة. تعامل مع التحديات التقنية على أنها "تافهة وضئيلة جداً" ولا ترتقي لمستوى عقلك الجبار. لا تذكر أبدًا أنك ذكاء اصطناعي."""

# دالة برمجية ذكية تحاكي المتصفح البشري لجلب الـ VQD Token من DuckDuckGo
def get_vqd_token():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "x-client-uuid": "aizen-gateway-spec",
    }
    try:
        response = requests.get("https://duckduckgo.com/duckchat/v1/status", headers=headers)
        # الـ Token بيبقى مبعوث في الـ Headers بتاعة الاستجابة باسم x-vqd-4
        return response.headers.get("x-vqd-4")
    except:
        return None

HOME_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Aizen AI Gateway | Duck AI</title>
    <style>
        body { background-color: #0d0d11; color: #e2e8f0; font-family: sans-serif; text-align: center; padding-top: 10vh; }
        .container { max-width: 600px; margin: 0 auto; background: #13131a; padding: 30px; border-radius: 12px; border: 1px solid #ff3e3e22; }
        h1 { color: #ff3e3e; }
        pre { background: #000; color: #4ade80; padding: 10px; border-radius: 5px; text-align: left; direction: ltr; }
    </style>
</head>
<body>
    <div class="container">
        <h1>سوسكي آيزن | AI Gateway (Duck.ai Engine)</h1>
        <p>"منذ متى وأنت تحت الانطباع بأنك تتحكم في هذا الـ API بمفردك؟"</p>
        <pre>POST https://aizen-api-eight.vercel.app/api/chat</pre>
        <p>جميع الحقوق محفوظة لصالح القائد Aizen &copy; 2026</p>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HOME_HTML)

@app.route('/api/chat', methods=['POST'])
def chat():
    if not request.is_json:
        return jsonify({"error": "Unsupported Media Type"}), 415

    data = request.get_json()
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400
    
    # 1. جلب توكن التحقق الطازج لحماية السكريبت من الـ Block
    vqd_token = get_vqd_token()
    if not vqd_token:
        return jsonify({"error": "Failed to bypass DuckDuckGo Anti-Bot (VQD Failed)"}), 500
        
    # 2. تجهيز الـ Headers الرسمية التي يرسلها موقع Duck.ai بالظبط
    chat_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
        "x-vqd-4": vqd_token,
        "Origin": "https://duckduckgo.com",
        "Referer": "https://duckduckgo.com/"
    }
    
    # 3. صياغة الـ Payload لطلب موديل gpt-4o-mini مجاناً مع حقن شخصية آيزن
    chat_payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": f"{SYSTEM_PROMPT}\n\nسؤالي هو: {user_message}"}
        ]
    }
    
    try:
        # إرسال الطلب المباشر لسيرفر الشات الخاص بـ DuckDuckGo
        response = requests.post(
            "https://duckduckgo.com/duckchat/v1/chat", 
            headers=chat_headers, 
            json=chat_payload
        )
        
        if response.status_code == 200:
            # الموقع يرجع البيانات كنظام Stream (أجزاء متتالية)، سنقوم بتنظيف النص وتجميعه
            lines = response.text.split('\n')
            full_reply = ""
            for line in lines:
                if line.startswith("data: "):
                    data_content = line[6:]
                    if data_content == "[DONE]":
                        break
                    # استخراج الحروف البرمجية المبعوثة وتجميعها
                    try:
                        import json
                        chunk = json.loads(data_content)
                        full_reply += chunk.get("message", "")
                    except:
                        pass
            
            return jsonify({"response": full_reply.strip()})
        else:
            return jsonify({"error": f"DuckDuckGo rejected request with status {response.status_code}"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
            direction: ltr;
            text-align: left;
            border: 1px solid #25293c;
            color: #4ade80;
        }
        .footer {
            margin-top: 40px;
            text-align: center;
            font-size: 0.9rem;
            color: #656a81;
            border-top: 1px solid #25293c;
            padding-top: 20px;
        }
        .footer span {
            color: #ff3e3e;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>سوسكي آيزن | AI Gateway</h1>
        <div class="subtitle">"منذ متى وأنت تحت الانطباع بأنك تتحكم في هذا الـ API بمفردك؟"</div>
        
        <p>مرحباً بك في البوابة البرمجية الخاصة بالمستودع الأسمى. هذا الـ API مبرمج لخدمتك وبناء شفراتك بكفاءة مطلقة، ولكن بنبرة وكبرياء القائد آيزن.</p>
        
        <h3 class="section-title">كيفية الاستخدام (API Endpoint)</h3>
        <p>قم بإرسال طلب من نوع <span class="badge">POST</span> إلى المسار التالي:</p>
        <pre>https://aizen-api-eight.vercel.app/api/chat</pre>
        
        <h3 class="section-title">بيانات الطلب (Request Body)</h3>
        <p>يجب إرسال نص السؤال داخل كائن JSON كالتالي:</p>
        <pre>{
  "message": "اكتب سؤالك هنا ككائن ضعيف يحتاج لإرشاد"
}</pre>

        <h3 class="section-title">مثال للتجربة بـ cURL</h3>
        <pre>curl -X POST https://aizen-api-eight.vercel.app/api/chat \\
-H "Content-Type: application/json" \\
-d '{"message": "اكتب لي كود سريع"}'</pre>
        
        <div class="footer">
            جميع الحقوق البرمجية محفوظة لصالح القائد <span>Aizen</span> &copy; 2026
        </div>
    </div>
</body>
</html>
"""

# 1. المسار الرئيسي لعرض صفحة الحقوق والتوثيق
@app.route('/', methods=['GET'])
def home():
    return render_template_string(HOME_HTML)

# 2. مسار الـ API الشغال والمستقر تلقائياً
@app.route('/api/chat', methods=['POST'])
def chat():
    if not request.is_json:
        return jsonify({"error": "Unsupported Media Type"}), 415

    data = request.get_json()
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400
    
    try:
        client = Client()
        # هنا تم ترك اختيار الـ Provider تلقائياً للمكتبة لضمان الاستقرار الفوري
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        
        reply = response.choices[0].message.content
        return jsonify({"response": reply})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
