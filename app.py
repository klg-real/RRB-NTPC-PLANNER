import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else genai.Client()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/ai-notes', methods=['POST'])
def get_ai_notes():
    try:
        data = request.get_json() or {}
        topic = data.get('topic', 'RRB NTPC General Awareness Strategy')
        req_type = data.get('type', 'cheat-sheet')

        if req_type == 'cheat-sheet':
            prompt = f"Provide a concise, high-yield formula & shortcut revision sheet for RRB NTPC on topic: '{topic}'. Include core formulas, short tricks, and 1 solved example."
        else:
            prompt = f"Create 3 high-yield MCQs for RRB NTPC on topic: '{topic}' with 4 options and detailed answer explanation."

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=1000
            )
        )

        return jsonify({'success': True, 'notes': response.text})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
