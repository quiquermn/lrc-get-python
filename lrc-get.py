import requests
from mutagen.wave import WAVE

url = 'https://lrclib.net/api/get'


params = dict(artist_name="LIT Killah",
              track_name='MAN$ION',
              album_name="SnipeZ",
              duration=200,)
res = requests.get(url, params=params)


print(res.text)
print("Hola")
