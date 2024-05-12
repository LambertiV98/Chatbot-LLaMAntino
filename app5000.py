from flask import Flask, Response, send_from_directory, request
from ollama import Client

app = Flask("Chatbot LLaMantino",
            static_url_path='', 
            static_folder='static'
            )

url = "http://localhost:11434/api/generate"
ollama_url = 'http://localhost:11434'

headers = {
    'Content-Type': 'application/json',
}

client = Client(host=ollama_url)

conversation_history = []

@app.route("/")
def send_index ():
    return send_from_directory('static', "index.html")

@app.route("/query", methods = ['POST'])
def test_py():
    prompt = request.get_data(as_text=True)
    print(type(prompt))
    result = client.generate(
        model="ifioravanti/llamantino-2:latest",
        prompt=prompt,
        stream=True,
    )
    def generator ():
        for chunk in result:
            message = chunk['response']
            yield message
    return Response(generator(), mimetype='application/json')

#start il server (con debug options)
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
    