from flask import Flask, request, jsonify
from flask_cors import CORS
from sql_engine import build_sql_agent, query

app = Flask(__name__)
CORS(app)

# Initialize the SQL Agent
agent = build_sql_agent()

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        user_query = data.get("text")
        
        if not user_query:
            return jsonify({"response": "Hey! I didn't hear anything."}), 400

        # result is a dict: {"summary": "...", "data": [...]}
        result = query(agent, user_query)
        
        return jsonify({
            "status": "success",
            "response": result.get("summary", "Done!"),
            "data": result.get("data", [])  
        })
    except Exception as e:
        print(f"Backend Error: {e}")
        return jsonify({"response": f"Hey! Backend error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)