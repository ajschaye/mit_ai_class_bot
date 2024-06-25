
import dotenv
from flask import Flask, request, jsonify, send_from_directory
from utils import tools


dotenv.load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory('./templates', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'response': 'No input provided'})
    
    chain = tools.get_chain()
    response = chain.invoke(user_input)
    
    print("\n=======================================\nUserInput: \n{}\n\n-------------------------------------\nResponse: \n{}\n=======================================\n".format(user_input, response))

    return jsonify({'response' : response})

if __name__ == '__main__':
    app.run(
        host='localhost',
        port=8888,
        debug=True
    )
