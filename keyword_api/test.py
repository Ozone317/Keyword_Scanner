import requests

url = "http://127.0.0.1:5000/getkeywords"

response = requests.post(url=url, json={"text": "There's something about the way the sun sets over the horizon that's truly mesmerizing. The golden hues of the sky as it transitions from day to night is a sight to behold. It's as if the sun is painting the sky with its final rays, creating a masterpiece that can never be replicated. Repetition is key when it comes to appreciating this natural wonder. You have to take the time to observe every detail, every shade of color, and every change that occurs. The more you look, the more you'll realize just how unique and breathtaking every sunset is."})

print(response.text)