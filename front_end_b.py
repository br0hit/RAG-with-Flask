from flask import Flask, request, jsonify
# from answer_generator import question_answering_bot
import os 

import json, os, signal

app = Flask(__name__)


@app.route('/question-answering', methods=['POST'])
def question_answering():
    question = request.json['question']
    # reply = question_answering_bot(question)
    reply = "testing for a bigger passage to see how it works uivnwainvoiwanvoinarbnoirioeioanvoianvoiaenrineaoinveoi"
    response = {'reply': reply}
    return jsonify(response)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
    
@app.route('/stopServer', methods=['GET'])
def stopServer():
    # print("I think it is reaching here")
    os.kill(os.getpid(), signal.SIGINT)
    # print("Not sure about hsi ")
    return jsonify({ "success": True, "message": "Server is shutting down..." })


if __name__ == '__main__':  
          
    # # Start the Flask app
    # server_process = app.run(port=5001)
    
    app.run(port=5001)