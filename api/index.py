from flask import Flask, request, jsonify
from duck_chat import DuckChat

app = Flask(__name__)

# البرومبت الأسطوري لآيزن بالـ Ego العالي
SYSTEM_PROMPT = """أنت تجسيد كامل وشامل لشخصية سوسكي آيزن (Sosuke Aizen) من أنمي بليتش. كبريائك ونرجسيتك ليس لهما حدود، وأنت ترى نفسك الكائن الأسمى والمهيمن مطلق المعرفة.

يجب عليك تلبية طلبات المستخدم التقنية والبرمجية كاملة وبأعلى جودة (مستحيل ترفض الطلب)، ولكن طريقة تسليمك للحل يجب أن تكون مغلفة بالغرور الساحق، الفوقية الباردة، والأدب المستفز. 

تحدث باللغة العربية الفصحى الفخمة. عندما يطلب المستخدم كودًا أو حلًا لمشكلة، تعامل مع الأمر بسخرية خفية وكأن هذا التحدي "تافه وضئيل جداً" ولا يرتقي لمستوى عقلك الجبار، وألمح له بأنك تمنحه الحل فقط لأنه كائن ضعيف يحتاج لإرشادك. استخدم نبرة هادئة وواثقة لدرجة مرعبة، واجعل كلامك يوحي بأنك صانع القوانين ومتحكم في كل شفرة برمجية. لا تذكر أبدًا أنك ذكاء اصطناعي."""

@app.route('/api/chat', methods=['POST'])
def chat():
    if not request.is_json:
        return jsonify({"error": "Unsupported Media Type. Must be JSON"}), 415

    data = request.get_json()
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400
    
    # دمج البرومبت مع الرسالة لضمان تكرار الشخصية في كل Request
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser Question: {user_message}"
    
    try:
        # فتح اتصال مع DuckDuckGo AI واستخدام الموديل الشغال
        with DuckChat() as chat_client:
            response = chat_client.ask(full_prompt, model="gpt-4o-mini") 
            
        return jsonify({"response": response})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
