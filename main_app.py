from flask import Flask, request, render_template, jsonify
import requests
import subprocess

# # Importing whisper to control audio
# import whisper
# model = whisper.load_model("base")

import os 
import shutil
import time

from Final_processing import PreProcessing

# # Importing the classifier agent to distinguish between commands and question/answering
# from conv2_withagent import CommandClassifier

# # Importing prompt template, Sales order Class and functions for Creating sales order 
# from createsalesorder import SalesOrder, Creating_SalesOrder_Step1, Creating_SalesOrder_Step2, Creating_SalesOrder_Step3


app = Flask(__name__)

# Initialize the list to store question-reply pairs
conversation = []
subprocess.Popen(['python', 'question_answering_app.py'])


@app.route('/')
def index():
    return render_template('saving.html',conversation=conversation)

@app.route('/upload-audio', methods=['POST','GET'])
def upload_audio():
    
    audio_file = request.files['audio']
    # Save the audio file to a desired location
    audio_file.save('audio.wav')

    # text_from_audio = model.transcribe("audio.wav")   
    # transcription = text_from_audio["text"]
    transcription = "Whisper Not loaded, This is just a Sample output "
    print(transcription)

    
    global transcription_data, reply, conversation
    transcription_data = transcription
    
    response = {}
    
    url = 'http://localhost:5001/question-answering'
    payload = {'question': transcription_data}
    getback = requests.post(url, json=payload)
    reply = getback.json().get('reply')
    

    # reply = question_answering_bot(transcription_data)
    # reply = "test"
    
    # Assuming the question is stored in the variable 'question' and the reply is stored in the variable 'reply'
    conversation.append({'question': transcription_data, 'reply': reply})
    
    response['data'] = 'response1'
    response['redirect'] = '/Question_Answering'
        

    
    return jsonify(response)

@app.route('/submit-input', methods=['POST'])
def submit_input():
    
    response = {}
    user_input = request.form.get('user_input')
    
    global transcription_data, reply, conversation
    
    if user_input:
        
        # Process the user's text input (e.g., send it to the question answering model, perform actions, etc.)
        transcription_data = user_input
        
        url = 'http://localhost:5001/question-answering'
        payload = {'question': transcription_data}
        getback = requests.post(url, json=payload)
        reply = getback.json().get('reply')
        
        
        
        # reply = question_answering_bot(transcription_data)       
        # reply = "test"
        
        # Assuming the question is stored in the variable 'question' and the reply is stored in the variable 'reply'
        conversation.append({'question': transcription_data, 'reply': reply})
        
        response['data'] = 'response1'
        response['redirect'] = '/Question_Answering'

    return jsonify(response)

@app.route('/upload-documents', methods=['POST'])
def upload_documents():
    response = {}

    # Check if the POST request contains any files
    if 'documents' in request.files:
        documents = request.files.getlist('documents')

        # Create a folder named "user_data" if it doesn't exist
        if not os.path.exists('user_data'):
            os.makedirs('user_data')

        for document in documents:
            # Save the uploaded document to the "user_data" folder
            document.save(os.path.join('user_data', document.filename))

        response['data'] = 'success'
        response['message'] = 'Documents uploaded successfully!'
        response['redirect'] = '/Question_Answering'
    else:
        response['data'] = 'error'
        response['message'] = 'No documents found in the request.'
        
    try:
        response = requests.get('http://localhost:5001/stopServer')
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        print("Server stopped successfully.")
    except requests.exceptions.RequestException as e:
        print("Error stopping the server:", str(e))
    time.sleep(5)
    PreProcessing("user_data")
    subprocess.Popen(['python', 'question_answering_app.py'])
    time.sleep(30)
    return jsonify(response)


@app.route('/Question_Answering')
def Question_Answering():
    if(transcription_data==None):
        conversation.append({'question': "Documents are successfully Uploaded", 'reply': "Feel Free to ask anything related to the documents"})
        
        return render_template('saving.html',conversation=conversation)
    

    return render_template('saving.html',conversation=conversation)


if __name__ == '__main__':  
    
    global transcription_data
    transcription_data = None
    
    # app.run()
    app.run()   