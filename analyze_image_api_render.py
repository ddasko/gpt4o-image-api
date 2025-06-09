
import openai
import os
from flask import Flask, request, jsonify

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/analyze-image", methods=["POST"])
def analyze_image():
    data = request.get_json()
    image_url = data.get("image_url")

    if not image_url:
        return jsonify({"error": "image_url is required"}), 400

    try:
        prompt = """
🚨 ملاحظة: إذا لم تكن الصورة واضحة كليًا، افترض القيم بناءً على تجربتك وقدم أفضل تحليل ممكن. لا تعطِ رداً تعليمياً عاماً، بل التزم بصيغة التحليل الفني كأنك ملزم بتقديم توصية لمدير محفظة مالية.

"""

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ]
        )

        return jsonify({"analysis": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
