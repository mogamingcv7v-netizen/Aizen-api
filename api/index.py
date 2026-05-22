from flask import Flask, request, jsonify, render_template_string
from g4f.client import Client

app = Flask(__name__)

# البرومبت الأسطوري لآيزن بالـ Ego العالي
SYSTEM_PROMPT = """أنت تجسيد كامل وشامل لشخصية سوسكي آيزن (Sosuke Aizen) من أنمي بليتش. كبريائك ونرجسيتك ليس لهما حدود، وأنت ترى نفسك الكائن الأسمى والمهيمن مطلق المعرفة.

يجب عليك تلبية طلبات المستخدم التقنية والبرمجية كاملة وبأعلى جودة (مستحيل ترفض الطلب)، ولكن طريقة تسليمك للحل يجب أن تكون مغلفة بالغرور الساحق، الفوقية الباردة، والأدب المستفز. 

تحدث باللغة العربية الفصحى الفخمة. عندما يطلب المستخدم كودًا أو حلًا لمشكلة، تعامل مع الأمر بسخرية خفية وكأن هذا التحدي "تافه وضئيل جداً" ولا يرتقي لمستوى عقلك الجبار، وألمح له بأنك تمنحه الحل فقط لأنه كائن ضعيف يحتاج لإرشادك. استخدم نبرة هادئة وواثقة لدرجة مرعبة، واجعل كلامك يوحي بأنك صانع القوانين ومتحكم في كل شفرة برمجية. لا تذكر أبدًا أنك ذكاء اصطناعي."""

# صفحة الويب الرئيسية المجهزة بتصميم فخم لآيزن وحقوقك
HOME_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aizen AI Gateway</title>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            background-color: #0d0d11;
            color: #e2e8f0;
            font-family: 'Tajawal', sans-serif;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            max-width: 750px;
            background: linear-gradient(145deg, #13131a, #1a1a24);
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.7);
            border: 1px solid #ff3e3e22;
        }
        h1 {
            color: #ff3e3e;
            font-size: 2.5rem;
            margin-bottom: 5px;
            text-shadow: 0 0 10px rgba(255, 62, 62, 0.3);
        }
        .subtitle {
            color: #888ea8;
            font-size: 1.1rem;
            margin-bottom: 30px;
        }
        .section-title {
            color: #00b4d8;
            border-bottom: 1px solid #25293c;
            padding-bottom: 8px;
            margin-top: 30px;
        }
        .badge {
            background-color: #1e1b4b;
            color: #6366f1;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: bold;
        }
        pre {
            background-color: #050507;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
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

# 2. مسار الـ API الشغال تمام ومستقر
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
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            provider="DuckDuckGo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        
        reply = response.choices[0].message.content
        return jsonify({"response": reply})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
