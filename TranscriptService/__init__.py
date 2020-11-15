import logging

import azure.functions as func
import azure.cognitiveservices.speech as speechsdk

import subprocess
import tempfile

def main(req: func.HttpRequest, audioBlob: func.InputStream, outputBlob: func.Out[func.InputStream]) -> func.HttpResponse:

    speech_config = speechsdk.SpeechConfig(subscription="<paste-your-subscription-key>", region="<paste-your-region>")

    audioFile = tempfile.NamedTemporaryFile(suffix='.ogg')
    audioData = audioBlob.read(-1)
    audioFile.write(audioData)

    audio_input = speechsdk.AudioConfig(filename=audioFile.name)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    result = speech_recognizer.recognize_once_async().get()

    transcriptFile = tempfile.NamedTemporaryFile(suffix='.srt')
    transcriptFile.write(result.text)

    outputBlob.set(transcriptFile)

    return func.HttpResponse(f"Project has been successfully transcribed and stored to output blob",status_code=200)