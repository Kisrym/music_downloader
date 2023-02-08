import requests, urllib, re, eyed3, os
from unidecode import unidecode
from eyed3.id3.frames import ImageFrame
from yt_dlp import YoutubeDL
from refresh_token import Refresh

class MusicDownloader:
    """MusicDownloader é um módulo em Python capaz de instalar músicas playlists do Spotify e Youtube."""
    def __init__(self):
        self.name = []
        self.config = []
        self.TOKEN = Refresh().refresh()
        self.yt = False
        self.out_path = "."
    
    def download(self):
        """
        Instala a música/playlist definida.
        """

        ydl_opts = {
            'ignoreerrors': True,
            'prefer_ffmpeg': True,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'keepvideo': False
        }

        for item in range(len(self.name)):
            if not self.yt:
                html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={self.name[item]}")
                video_id = re.findall(r"watch\?v=(\S{11})", html.read().decode())[0] #? pegando o id do vídeo

            else:
                video_id = self.name[item]

            if not os.path.exists(f"{self.out_path}/musicas/{self.config[item]['title']}.mp3"):
                ydl_opts["outtmpl"] = f"{self.out_path}/musicas/{self.config[item]['title']}.%(ext)s" #? evitando corrupção do arquivo
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([f'https://www.youtube.com/watch?v={video_id}'])

        self.__add_parameters()

    def __add_parameters(self):
        if "img" not in os.listdir(self.out_path): os.mkdir(f"{self.out_path}/img")
        
        #! Pegando as thumbnails
        for cont in range(len(self.config)):
            try:
                if not os.path.exists(f'{self.out_path}/img/{self.config[cont]["title"]}.png'):
                    imagem = requests.get(self.config[cont]["thumbnail"]).content #? dando request na imagem do álbum
                    with open(f'{self.out_path}/img/{self.config[cont]["title"]}.png', 'wb') as a: #? criando o arquivo com o nome da música
                        a.write(imagem)
            except:
                continue
        
        #! Colocando as tags
        for c in range(len(self.name)):
            try:
                musica = eyed3.load(f"{self.out_path}/musicas/{self.config[c]['title']}.mp3")

                if musica.tag == None: musica.initTag()

                musica.tag.title = self.config[c]["title"]
                musica.tag.release_date = self.config[c]["release_date"]
                musica.tag.artist = self.config[c]["artist"]
                musica.tag.album = self.config[c]["album"]
                musica.tag.track_num = self.config[c]["track_num"]
                musica.tag.disc_num = self.config[c]["disc_num"]

                with open(f"{self.out_path}/img/{self.config[c]['title']}.png", "rb") as imagem:
                    musica.tag.images.set(ImageFrame.FRONT_COVER, imagem.read(), 'image/png')
                    musica.tag.save()
            except:
                continue
        
        for img in os.listdir(f"{self.out_path}/img"): os.remove(f"{self.out_path}/img/" + img) #? removendo as imagens

class Spotify(MusicDownloader):
    def __init__(self, out_path: str = "."):
        super().__init__()
        self.out_path = out_path

    def playlist(self, playlist: str, offset = 0):
        """Objeto para o link da playlist do Spotify.

        Args:
            playlist (str): Link da playlist.
            offset (int, opcional): Música inicial do download da playlist. Default: 0

        Raises:
            ValueError: Se a playlist não existir ou não for do formato correto.
        """
        if "playlist" not in playlist:
            raise ValueError("Playlist inválida")
        
        playlist = playlist[34:].split("?")[0]
        cont = 0

        while True:
            try:
                r = requests.get(f"https://api.spotify.com/v1/playlists/{playlist}/tracks?offset={offset}", headers = {"Authorization": f"Bearer {self.TOKEN}"}).json()
                r["items"][cont]["track"]["name"] = r["items"][cont]["track"]["name"].replace("/", r"%2F") if "/" in r["items"][cont]["track"]["name"] else r["items"][cont]["track"]["name"]
                self.name.append(f"{unidecode(r['items'][cont]['track']['name'].replace(' ', '+'))}+{unidecode(r['items'][cont]['track']['album']['artists'][0]['name'].replace(' ', '+'))}")
                self.config.append({
                    "thumbnail" : r["items"][cont]["track"]["album"]["images"][0]['url'],
                    "title" : r['items'][cont]['track']['name'],
                    "release_date" : r['items'][cont]['track']['album']['release_date'],
                    "artist" : r['items'][cont]['track']['album']['artists'][0]['name'],
                    "album" : r['items'][cont]['track']['album']['name'],
                    "track_num" : r['items'][cont]['track']['track_number'],
                    "disc_num" : r['items'][cont]['track']['disc_number']
                })

                if cont == 99:
                    offset += 100
                    cont = 0
                
                cont += 1
            except IndexError:
                break
    
    def track(self, music: str, /):
        """Objeto para o link da música do Spotify.

        Args:
            music (str): Link da música.
        """
        music = music[31:].split("?")[0]

        r = requests.get(f"https://api.spotify.com/v1/tracks/{music}", headers = {"Authorization": f"Bearer {self.TOKEN}"}).json()
        self.name.append(f"{unidecode(r['name'].replace(' ', '+'))}+{unidecode(r['album']['artists'][0]['name'].replace(' ', '+'))}")
        self.config.append({
            "thumbnail" : r["album"]["images"][0]["url"],
            "title" : r['name'],
            "release_date" : r['album']['release_date'],
            "artist" : r['album']['artists'][0]['name'],
            "album" : r['album']['name'],
            "track_num" : r['track_number'],
            "disc_num" : r['disc_number']
        })

class Youtube(MusicDownloader):
    def __init__(self, out_path: str = "."):
        super().__init__()
        self.yt = True
        self.out_path = out_path
    
    def track(self, music: str, /):
        """Objeto para o link da música do Youtube.

        Args:
            music (str): Link da música.
        """
        music = music.split("=")[1]
        with YoutubeDL({}) as ydl:
            title = unidecode(ydl.extract_info(f"http://www.youtube.com/watch?v={music}", download = False).get("title", None).replace(" ", "%20").replace("-", "")) # getting the video name
        
        r = requests.get(f"https://api.spotify.com/v1/search?q={title}&type=track&limit=1", headers = {"Authorization": f"Bearer {self.TOKEN}"}).json()
        r = r["tracks"]["items"][0]

        self.config.append({
            "thumbnail" : r["album"]["images"][0]["url"],
            "title" : r['name'],
            "release_date" : r['album']['release_date'],
            "artist" : r['album']['artists'][0]['name'],
            "album" : r['album']['name'],
            "track_num" : r['track_number'],
            "disc_num" : r['disc_number']
        })

        self.name.append(music)