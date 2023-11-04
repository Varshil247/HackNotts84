import requests
import pygame
from io import BytesIO


url = "https://api.play.ht/api/v2/tts/stream"

payload = {
    "text": "Hello from a realistic voice.",
    "voice": "s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json",
    "output_format": "mp3",
    "voice_engine": "PlayHT2.0-turbo"
}
headers = {
    #"accept": "text/event-stream",
    "accept": "audio/mpeg",
    "content-type": "application/json",
    "AUTHORIZATION": "22cf5809f001411e808c64bb6f8b5bec",
    "X-USER-ID": "8R48EcHJo3MMHiwT0F6Kp0ULVxq2"
}

requests.head("https://api.play.ht/api/v2/tts")

pygame.mixer.init()
response = requests.post(url, json=payload, headers=headers )

if response.status_code == 200:
    # Convert the response content to a bytes stream
    audio_data = BytesIO(response.content)

    # Load the audio data into Pygame mixer
    pygame.mixer.music.load(audio_data)

    # Play the audio
    pygame.mixer.music.play()

    # Wait for the audio to finish (you can add other logic here)
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

else:
    print('Failed to retrieve the audio file.')


"""# Get the 'Content-Type' header from the response
content_type = response.headers.get('Content-Type')

if content_type:
    print(f'Content-Type: {content_type}')
else:
    print('Content-Type header not found in the response.')

# You can also check for specific content types, for example, JSON
if content_type and 'application/json' in content_type:
    # The response is in JSON format, you can parse it
    data = response.json()
    print(data)
else:
    print('Response is not in JSON format.')"""


#print(response.text)
#print(response.json())


"""
accept: 'text/event-stream',
example output:
event: generating
data: {"id":"UjsnTtuZMAtv9vES1T","progress":0,"stage":"queued"}

event: generating
data: {"id":"UjsnTtuZMAtv9vES1T","progress":0.01,"stage":"active"}

event: generating
data: {"id":"UjsnTtuZMAtv9vES1T","progress":0.01,"stage":"preload","stage_progress":0}
...
event: generating
data: {"id":"UjsnTtuZMAtv9vES1T","progress":0.99,"stage":"postprocessing","stage_progress":1}

event: completed
data: {"id":"UjsnTtuZMAtv9vES1T","progress":1,"stage":"complete","url":"https://peregrine-results.s3.amazonaws.com/pigeon/UjsnTtuZMAtv9vES1T_0.mp3","duration":3.8933,"size":79725}

##############################################################################################################################################################################################################################

accept : 'application/json'
{
  "id": "f0gZrOKBKL7veJ6o1M",
  "created": "2023-03-04T01:12:03.981Z",
  "input": {
    "text": "Hello! Said the realistic voice.",
    "voice": "s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json",
    "quality": "draft",
    "output_format": "mp3",
    "speed": 1,
    "sample_rate": 24000,
    "seed": null,
    "temperature": null,
    "voice_engine": "PlayHT2.0",
    "emotion": "female_happy",
    "voice_guidance": 3,
    "style_guidance": 20
  },
  "output": {
    "duration": 1.664,
    "size": 35085,
    "url": "https://peregrine-results.s3.amazonaws.com/pigeon/f0gZrOKBKL7veJ6o1M_0.mp3"
  },
  "_links": [
    "{\n  href: 'https://play.ht/api/v2/tts/f0gZrOKBKL7veJ6o1M',\n  method: 'GET',\n  contentType: 'application/json',\n  rel: 'self',\n  description: \"Fetches this job's data. Poll it for the latest status.\",\n}\n"
  ]
}

"""