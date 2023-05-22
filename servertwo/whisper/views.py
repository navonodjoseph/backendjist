from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
# from rest_framework.views import APIView
from django.views import View
from . models import Audio
from . serializer import *
from rest_framework.response import Response
from django.http import JsonResponse
# from .processAudio import process_wav_file
from pydub import AudioSegment
import io
import os
import requests
import datetime


class AudioUploadView(View):
    def get(self, request): 
        return JsonResponse({'Message': 'This is a GET request'})
    
    def post(self, request):
        audio_file = request.FILES.get('audio')
        if audio_file: 
            audio_data = audio_file.read()

            # convert to audio segment using pydub
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_data))
            
            # save to folder
            output_folder = 'output'
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            
            # generate unique filename
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            output_filename = f'audio_{timestamp}.wav'

            # save audio as wav.file
            output_file_path = os.path.join(output_folder, output_filename)
            audio_segment.export(output_file_path, format='wav')
            print('Saved file to: ', output_file_path)

            # transcribe audio
            transcriptions_folder = 'transcriptions'
            if not os.path.exists(transcriptions_folder):
                os.makedirs(transcriptions_folder)
            
            transcription_filename = f'transcription_{timestamp}.txt'
            transcription_filepath = os.path.join(transcriptions_folder, transcription_filename)

            # make api request to Whisper Ai for transcription 
            whisper_api_url = 'https://api.openai.com/v1/audio/transcriptions'
            headers ={
                'Authorization': "Bearer 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",
                'Content-Type': 'audio/wav'
                }
            files = {'audio': open(output_file_path, 'rb')}

            transcription = ''

            # make api request for Whisper
            response = requests.post(whisper_api_url, headers=headers, files=files)

            if response.status_code==200:
                transcription = response.text
            
            # save transcription to a file
            if transcription: 
                output_file_path = os.path.join(output_folder, output_filename)
                with open(transcription_filepath, 'w') as file:
                    file.write(transcription)
            
                print('Transcription saved to:', transcription_filepath)
            else: print('No transcription available')
            # create a record in the database
            audio_file_record = Audio(transcribe=transcription_filepath)
            audio_file_record.save()

            return JsonResponse({'message': 'Audio conversation and save completed'})
        else: 
            return JsonResponse({'message': 'No audio file found'}, status=400)
        