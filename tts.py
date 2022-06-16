import os
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk
import requests
from boto3 import Session
from dotenv import load_dotenv
from google.cloud import texttospeech

import corpus

# Load .env file
load_dotenv()

# Set up Larynx
LARYNX_URL = os.getenv("LARYNX_URL")

# Set up Microsoft
MICROSOFT_KEY = os.getenv("MICROSOFT_KEY")
MICROSOFT_REGION = os.getenv("MICROSOFT_REGION")

# Set up AWS
AWS_PROFILE = os.getenv("AWS_PROFILE")
session = Session(profile_name=AWS_PROFILE)
polly = session.client("polly")

# Get word corpus
CORPUS_FILE = os.getenv("CORPUS_FILE")
CORPUS_WEB = os.getenv("CORPUS_WEB")
data = corpus.get_corpus(CORPUS_WEB, CORPUS_FILE)


def ssml_to_audio(engine: str, word: str, ssml_element: str, lang: str) -> bool:
    """Convert SSML+IPA to an audio file via a couple of different TTS engines"""

    # Yes I know, ew, if/elif/else is ugly
    if engine == "polly":
        response = polly.synthesize_speech(
            TextType="ssml", VoiceId="Joanna", OutputFormat="mp3", Text=ssml_element
        )
        file_name = f"./polly/{word}.mp3"
        with open(file_name, "wb") as file:
            file.write(response["AudioStream"].read())
            print(f"Audio content written to file {file_name}")
            file.close()
        return True

    elif engine == "google":
        client = texttospeech.TextToSpeechClient()

        synthesis_input = texttospeech.SynthesisInput(ssml=ssml_element)

        voice = texttospeech.VoiceSelectionParams(
            language_code=lang, ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        file_name = f"./google/{word}.mp3"
        with open(file_name, "wb") as file:
            file.write(response.audio_content)
            print(f"Audio content written to file {file_name}")
            file.close()
        return True

    elif engine == "larynx":
        url = f"{LARYNX_URL}&text={ssml_element}&ssml=true"

        response = requests.get(url)

        if response.status_code == 200:
            file_name = f"./larynx/{word}.mp3"
            with open(file_name, "wb") as file:
                file.write(response.content)
                print(f"Audio content written to file {file_name}")
                file.close()
        else:
            print(f"Error: {word} had API response {response.status_code}")
        return True

    elif engine == "microsoft":
        speech_config = speechsdk.SpeechConfig(
            subscription=MICROSOFT_KEY, region=MICROSOFT_REGION
        )

        speech_config.speech_synthesis_language = lang

        speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
        )

        file_name = f"./microsoft/{word}.mp3"
        Path(file_name).touch()
        file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=file_config
        )

        result = speech_synthesizer.speak_ssml_async(ssml_element).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"Audio content written to file {file_name}")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")
            return False
        return True

    else:
        print(f"Error: {engine} is not a valid engine")
        return False


if __name__ == "__main__":
    print("Cannot be invoked directly :)")
