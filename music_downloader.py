import requests, urllib, re, eyed3, os
from unidecode import unidecode
from eyed3.id3.frames import ImageFrame
from yt_dlp import YoutubeDL
from refresh_token import Refresh
from shutil import rmtree

class MusicDownloader:
    """MusicDownloader é um módulo em Python capaz de instalar músicas playlists do Spotify e Youtube."""
    def __init__(self):
        self.name = []
        self.config = []
        self.TOKEN = Refresh().refresh()
        self.yt = False
        self.out_path = os.getcwd()
        self.headers = {"Authorization": f"Bearer {self.TOKEN}"}
    
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
        
        rmtree(f"{self.out_path}/img") # removing the img temporary folder
    
    def _get_track_info(self, r: dict) -> None:
        self.config.append({
            "thumbnail" : r["album"]["images"][0]["url"],
            "title" : r['name'],
            "release_date" : r['album']['release_date'],
            "artist" : r["artists"][0]['name'],
            "album" : r['album']['name'],
            "track_num" : r['track_number'],
            "disc_num" : r['disc_number']
        })

class Spotify(MusicDownloader):
    def __init__(self, out_path: str = os.getcwd()):
        super().__init__()
        self.out_path = out_path

    def playlist(self, playlist: str, offset = 1, amount: int = 0):
        """Objeto para o link da playlist do Spotify.

        Args:
            playlist (str): Link da playlist.
            offset (int, opcional): Música inicial do download da playlist. Default: 1
            amount (int, opcional): Quantidade de músicas que vão ser instaladas. Default: Todas

        Raises:
            ValueError: Se a playlist não existir ou não for do formato correto.
        """
        if "playlist" not in playlist:
            raise ValueError("Playlist inválida")
        
        if amount < 0:
            raise IndexError("Quantidade incorreta")
        
        playlist = re.findall(r"(\w+\?\w+)", playlist)[0][0:-3]
        offset -= 1
        cont = 0

        if amount > self.get_playlist_size(playlist): raise IndexError("Quantidade informada maior que o tamanho da playlist")

        while True:
            try:
                r = requests.get(f"https://api.spotify.com/v1/playlists/{playlist}/tracks?offset={offset}", headers = self.headers).json() if amount == 0 else requests.get(f"https://api.spotify.com/v1/playlists/{playlist}/tracks?offset={offset}&limit={amount}", headers = self.headers).json()

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

                if cont == 100:
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
        music = re.findall(r"(\w+\?\w+)", music)[0][0:-3]

        r = requests.get(f"https://api.spotify.com/v1/tracks/{music}", headers = self.headers).json()

        self.name.append(f"{unidecode(r['name'].replace(' ', '+'))}+{unidecode(r['artists'][0]['name'].replace(' ', '+'))}")
        self._get_track_info(r)

    def get_playlist_size(self, playlist: str):
        """Retorna a quantidade de músicas dentro da playlist. Retorna 0 se não for uma playlist do Spotify válida.

        Args:
            playlist (str): Link da playlist

        Returns:
            int: Quantidade de músicas
        """
        
        if "spotify.com/playlist" not in playlist:
            return 0
        
        playlist = re.findall(r"(\w+\?\w+)", playlist)[0][0:-3]
        return requests.get(f"https://api.spotify.com/v1/playlists/{playlist}/tracks?offset=0", headers = self.headers).json()["total"]

class Youtube(MusicDownloader):
    def __init__(self, out_path: str = os.getcwd()):
        super().__init__()
        self.yt = True
        self.out_path = out_path
    
    def track(self, music: str, /):
        """Objeto para o link da música do Youtube.

        Args:
            music (str): Link da música.
        """
        music = music.split("=")[1] if "watch" in music else music.split("be/")[1]

        with YoutubeDL({}) as ydl:
            title = unidecode(ydl.extract_info(f"http://www.youtube.com/watch?v={music}", download = False).get("title", None).replace(" ", "+").replace("-", ""))
            author = unidecode(ydl.extract_info(f"http://www.youtube.com/watch?v={music}", download = False).get("channel", None).replace(" ", "+").replace("-", ""))
        
        r = requests.get(f"https://api.spotify.com/v1/search?q={title}+{author}&type=track&limit=1", headers = self.headers).json()
        r = r["tracks"]["items"][0]

        self._get_track_info(r)

        self.name.append(music)

    def playlist(self, playlist: str, offset = 1, amount: int = 0):
        """Objeto para o link da playlist do Youtube

        Args:
            playlist (str): Link da playlist
            offset (int, opcional): Música inicial da playlist. Default 1
            amount (int, opcional): Quantidade de músicas que vão ser instaladas. Default: Todas

        Raises:
            ValueError: Se a playlist não existir ou não for do formato correto.
            ValueError: Se o limite for igual ou menor a 0
        """

        if "playlist" not in playlist:
            raise ValueError("Playlist inválida")
        
        if amount < 0:
            raise IndexError("Quantidade incorreta")
               
        offset -= 1

        html = urllib.request.urlopen(playlist)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        new_video_ids = []

        for id in video_ids:
            if id not in new_video_ids:
                new_video_ids.append(id) # getting the video ids from the playlist
        
        if amount > len(new_video_ids):
            raise IndexError("Limite fora do range")
        
        new_video_ids = new_video_ids[offset:] if amount == 0 else new_video_ids[offset:amount]

        for id in new_video_ids:
            with YoutubeDL({}) as ydl:
                title = unidecode(ydl.extract_info(f"http://www.youtube.com/watch?v={id}", download = False).get("title", None).replace(" ", "%20").replace("-", ""))
                author = unidecode(ydl.extract_info(f"http://www.youtube.com/watch?v={id}", download = False).get("channel", None).replace(" ", "%20").replace("-", ""))
         
            r = requests.get(f"https://api.spotify.com/v1/search?q={title}+{author}&type=track&limit=1", headers = {"Authorization": f"Bearer {self.TOKEN}"}).json()
            r = r["tracks"]["items"][0]
        
            self._get_track_info(r)
        
            self.name.append(id)
    
    def get_playlist_size(self, playlist: str):
        """Retorna a quantidade de músicas dentro da playlist. Retorna 0 se não for uma playlist do Youtube válida.

        Args:
            playlist (str): Link da playlist

        Returns:
            int: Quantidade de músicas
        """
        html = urllib.request.urlopen(playlist)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        new_video_ids = []

        for id in video_ids:
            if id not in new_video_ids:
                new_video_ids.append(id)
        
        return len(new_video_ids)
