import os
import dotenv
from flask import Flask, request, jsonify, send_from_directory
from utils import tools
from utils import retriever


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
    if not os.path.exists('.env'):
        raise FileNotFoundError("Please create a .env file in the root directory with the OPENAI_API_KEY variable set.")

    count = len([entry for entry in os.scandir("data") if entry.is_file()])
    if count == 0:
        raise FileNotFoundError("Please add a pdf to the data folder.")
    
    retriever.rebuild_db()

    app.run(
        host='localhost',
        port=8888,
        debug=True
    )
