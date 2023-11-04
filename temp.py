import requests
import json

url = "https://api.play.ht/api/v2/voices"

headers = {
    "accept": "application/json",
    "AUTHORIZATION": "22cf5809f001411e808c64bb6f8b5bec",
    "X-USER-ID": "8R48EcHJo3MMHiwT0F6Kp0ULVxq2"
}

response = requests.get(url, headers=headers)
reponse = response.json()

#response = json.load(response)
for id in reponse:
    
    name = id.get('id')
    print(name)

#print(response.text)