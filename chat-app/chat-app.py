from flask import Flask, request, jsonify
import requests
import os
import time

app = Flask(__name__)

LLM_ENDPOINT = os.getenv("LLM_ENDPOINT", "http://llm:8000")
MAX_RETRIES = 10
RETRY_DELAY = 3  # seconds


def wait_for_model():
    if not LLM_ENDPOINT:
        print("WARNING: No LLM endpoint found. Skipping health check.")
        return None

    print(f"Waiting for LLM at {LLM_ENDPOINT}...")

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(f"{LLM_ENDPOINT}/v1/models", timeout=5)

            if response.status_code == 200:
                print("LLM is ready!")
                return LLM_ENDPOINT

        except requests.exceptions.RequestException:
            pass

        print(f"Attempt {attempt}/{MAX_RETRIES} failed. Retrying in {RETRY_DELAY}s...")
        time.sleep(RETRY_DELAY)

    print("LLM did not become ready. Falling back.")
    return None


model_endpoint = wait_for_model()


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()

    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400

    user_message = data['message']

    if model_endpoint:
        try:
            response = requests.post(
                f"{model_endpoint}/v1/chat/completions",
                json={
                    "model": "smollm2",
                    "messages": [
                        {"role": "user", "content": user_message}
                    ]
                },
                timeout=20
            )

            response.raise_for_status()
            result = response.json()

            reply = result["choices"][0]["message"]["content"]

            return jsonify({"response": reply})

        except Exception as e:
            return jsonify({
                "error": "LLM request failed",
                "details": str(e)
            }), 500

    # fallback mode
    return jsonify({
        "response": f"(fallback) AI says: {user_message[::-1]}"
    })


@app.route('/')
def index():
    return '''
    <html>
    <body>
        <h1>Chat App</h1>
        <form id="chatForm">
            <input type="text" id="message" />
            <button type="submit">Send</button>
        </form>
        <div id="response"></div>

        <script>
            document.getElementById('chatForm').onsubmit = async function(e) {
                e.preventDefault();
                const message = document.getElementById('message').value;

                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ message })
                });

                const data = await res.json();
                document.getElementById('response').innerText = data.response;
            }
        </script>
    </body>
    </html>
    '''


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
