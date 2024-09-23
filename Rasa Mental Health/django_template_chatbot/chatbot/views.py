from django.http import JsonResponse
from django.shortcuts import render
import requests

URL_DEFAULT= "http://localhost:5005/webhooks/rest/webhook"

"""data = {
    "sender": "user1",
    "message": "Hello"
}
"""
turnchat= {
    'sender': "User", 
    'message': None
}

conversation_history = [
    
]

def call_rasa(message): 
    turnchat["message"]= message
    try: 
        response = requests.post(URL_DEFAULT, json= turnchat)
        if response.status_code== 200: 
            return response.json()[0]['text']
        else: 
            raise f'Error: {response.status_code}'
    except requests.RequestException as e: 
        raise f'Request Error: {e}'


def home(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        res = ask_rasa(message)
        return JsonResponse({'message':message, 'response':res })
    return render(request,"chatbot/chatbot.html")


def ask_rasa(user_message):   
     
    conversation_history.append({"role": "user", "content": user_message})
    response = call_rasa(user_message)
    conversation_history.append({"role": "assistant", "content": response})
    
    print(conversation_history)
    return response
