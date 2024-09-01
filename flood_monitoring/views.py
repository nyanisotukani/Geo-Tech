from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

# Create your views here.
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
    
def map_dashboard(request):
    return render(request,'map_dashboard.html')

def reports(request):
    return render(request, 'reports.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def alerts(request):
    return render(request,'alerts.html')


from google.cloud import texttospeech



import requests
from django.http import JsonResponse

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body
            body = json.loads(request.body)
            message = body.get('message')
            
            # Your API key and endpoint
            YOUR_API_KEY = "AIzaSyAH81fCgUSgbY6WdDnojPNGPmyHzjzQ_hw"
            url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={YOUR_API_KEY}'
            headers = {'Content-Type': 'application/json'}
            data = {
                "contents": [
                    {
                        "parts": [
                            {"text": message}
                        ]
                    }
                ]
            }
            
            # Make the API request
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            response_json = response.json()
            bot_response = response_json['candidates'][0]['content']['parts'][0]['text']
            # client = texttospeech.TextToSpeechClient()

            # synthesis_input = texttospeech.SynthesisInput(text=bot_response)
            # voice = texttospeech.VoiceSelectionParams(
            #     language_code="en-US", name="en-US-Wavenet-D"
            # )
            # audio_config = texttospeech.AudioConfig(
            #     audio_encoding=texttospeech.AudioEncoding.MP3
            # )

            # response = client.synthesize_speech(
            #     input=synthesis_input, voice=voice, audio_config=audio_config
            # )

            # with open("output.mp3", "wb") as out:
            #     out.write(response.audio_content)
                        
            # Return the response as JSON
            return JsonResponse({'response': bot_response})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)