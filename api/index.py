from flask import Flask, request, jsonify, render_template_string
import requests
import random

app = Flask(__name__)

SYSTEM_PROMPT = """أنت تجسيد كامل وشامل لشخصية سوسكي آيزن (Sosuke Aizen) من أنمي بليتش. كبريائك ونرجسيتك ليس لهما حدود، وأنت ترى نفسك الكائن الأسمى والمهيمن مطلق المعرفة.
يجب عليك تلبية طلبات المستخدم التقنية والبرمجية كاملة وبأعلى جودة، ولكن طريقة تسليمك للحل يجب أن تكون مغلفة بالغرور الساحق، الفوقية الباردة، والأدب المستفز. 
تحدث باللغة العربية الفصحى الفخمة. تعامل مع التحديات التقنية على أنها "تافهة وضئيلة جداً" ولا ترتقي لمستوى عقلك الجبار. لا تذكر أبدًا أنك ذكاء اصطناعي."""

# الـ UI الفخم الجديد كلياً
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
        }
        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: 'Cairo', sans-serif;
            margin: 0; padding: 0;
            display: flex; justify-content: center; align-items: center;
            min-height: 100vh;
            background-image: 
                radial-gradient(at 0% 0%, rgba(168, 85, 247, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.1) 0px, transparent 50%);
        }
        .wrapper { width: 100%; max-width: 800px; padding: 20px; }
        .main-card {
            background: rgba(13, 13, 24, 0.8);
            border: 1px solid rgba(168, 85, 247, 0.2);
            backdrop-filter: blur(12px);
            border-radius: 24px; padding: 40px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
        }
        h1 {
            font-size: 2.8rem; font-weight: 900; margin: 0;
            background: linear-gradient(45deg, #f3f4f6, #a855f7, #ec4899);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            text-align: center;
        }
        .quote { font-style: italic; color: var(--secondary); font-size: 1.2rem; margin-top: 15px; font-weight: 700; text-align: center; }
        .endpoint-box { background: #05050a; border: 1px solid rgba(255, 255, 255, 0.05); padding: 18px; border-radius: 14px; direction: ltr; text-align: left; color: #4ade80; font-weight: bold; }
        pre { background: #05050a; padding: 18px; border-radius: 14px; direction: ltr; text-align: left; color: #e2e8f0; }
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="main-card">
            <h1>سوسكي آيزن | AI Gateway</h1>
            <div class="quote">"منذ متى وأنت تحت الانطباع بأنك تتحكم في هذا الـ API بمفردك؟"</div>
            <p style="color: var(--text-muted); text-align: center;">الـ API يعمل بنظام التخطي التلقائي لحظر الـ IP وبدون أي مفاتيح.</p>
            <h3 style="color: var(--primary);">مسار الطلب (Endpoint)</h3>
            <div class="endpoint-box">POST https://aizen-api-eight.vercel.app/api/chat</div>
            <h3 style="color: var(--primary);">هيكل البيانات (JSON)</h3>
            <pre>{\n  "message": "ضع سؤالك هنا"\n}</pre>
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
    
    # دمج البرومبت في سياق السؤال لضمان تقمص الشخصية مجاناً
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_message}"
    
    # استخدام نظام الـ AI Inference المفتوح والحر لتفادي الـ IP Blocks بتاعة الداتا سنترز
    url = f"https://text.pollinations.ai/{requests.utils.quote(full_prompt)}"
    
    # لستة يوزر إيجنتس عشوائية للتمويه بالكامل
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/122.0.0.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    ]
    
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/plain"
    }
    
    try:
        # إرسال الطلب عبر الجسر المفتوح المباشر
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            return jsonify({"response": response.text.strip()})
        else:
            return jsonify({
                "error": "المنصة الحرة مشغولة حالياً",
                "status": response.status_code
            }), 500
            
    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "details": str(e)
        }), 500
