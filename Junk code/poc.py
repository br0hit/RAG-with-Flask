from flask import Flask, request, render_template, jsonify

# Importing whisper to control audio
import whisper
model = whisper.load_model("base")

# # Importing the classifier agent to distinguish between commands and question/answering
# from conv2_withagent import CommandClassifier


# # Importing the question answering bot 
# from answer_generator import question_answering_bot


# # Importing prompt template, Sales order Class and functions for Creating sales order 
# from createsalesorder import SalesOrder, Creating_SalesOrder_Step1, Creating_SalesOrder_Step2, Creating_SalesOrder_Step3


app = Flask(__name__)

# Initialize the list to store question-reply pairs
conversation = []

@app.route('/')
def index():
    return render_template('saving.html',conversation=conversation)

@app.route('/upload-audio', methods=['POST','GET'])
def upload_audio():
    
    audio_file = request.files['audio']
    # Save the audio file to a desired location
    audio_file.save('audio.wav')

    text_from_audio = model.transcribe("audio.wav")   
    transcription = text_from_audio["text"]
    print(transcription)

    
    global transcription_data, reply, conversation
    transcription_data = transcription
    
    response = {}
    

    # reply = question_answering_bot(transcription_data)
    reply = "test"
    
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
        
        # reply = question_answering_bot(transcription_data)       
        reply = "test"
        
        # Assuming the question is stored in the variable 'question' and the reply is stored in the variable 'reply'
        conversation.append({'question': transcription_data, 'reply': reply})
        
        response['data'] = 'response1'
        response['redirect'] = '/Question_Answering'

    return jsonify(response)


@app.route('/Question_Answering')
def Question_Answering():
    if(transcription_data==None):
        return render_template('saving.html',transcription="Ask me anything")
    

    return render_template('saving.html',conversation=conversation)




if __name__ == '__main__':  
    app.run()