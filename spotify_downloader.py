import requests, urllib, re, youtube_dl, eyed3, os
from unidecode import unidecode
from eyed3.id3.frames import ImageFrame

TOKEN = "BQCBlcG5cL8LGECvrcgSP-QUqXZu85IZh30rR-a2OexVYZlWEVvfXeJXssSsGJI7gG3LUplxm530sVE0ESYfhlYtjv24sQHszkyFEzRwO_Vab_IEmXqb98DfYtLDD5esV_B1G57KVi_E-pg0oItxFl7BHbG_s6sROtGgDObsUadilEt0KQrWTU4h0XxVBxo"
playlist = "https://open.spotify.com/playlist/23fJjWSRNwxKtPNbsU7CSW?si=86f4a01b0e6749a9"[34:].split("?")[0]

ydl_opts = {
    'format': '250',
    'addmetadata': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }],
    'postprocessor_args': [
        '-ar', '16000'
    ],
    'prefer_ffmpeg': True,
    'keepvideo': False
}

cont_offset = 0
cont = 0

while True:
    try:
        r = requests.get(f"https://api.spotify.com/v1/playlists/{playlist}/tracks?offset={cont_offset}", headers = {"Authorization": f"Bearer {TOKEN}"}).json()

        #! Pegando as imagens
        if not os.path.exists(f'img/{r["items"][cont]["track"]["name"]}.png'):
            imagem = requests.get(r["items"][cont]["track"]["album"]["images"][0]['url']).content #? dando request na imagem do álbum
            with open(f'img/{r["items"][cont]["track"]["name"]}.png', 'wb') as a: #? criando o arquivo com o nome da música
                a.write(imagem)

        #! Baixando a música
        html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={unidecode(r['items'][cont]['track']['name'].replace(' ', '+'))}+{unidecode(r['items'][cont]['track']['album']['artists'][0]['name'].replace(' ', '+'))}") #? procurando o nome da música e do artista
        print(r['items'][cont]['track']['name'].replace(' ', '+'))
        video_id = re.findall(r"watch\?v=(\S{11})", html.read().decode())[0] #? pegando o id do vídeo

        if not os.path.exists(f"musicas/{r['items'][cont]['track']['name']}.mp3"):
            while True:
                try:
                    ydl_opts["outtmpl"] = f"musicas/{r['items'][cont]['track']['name']}.%(ext)s" #? evitando corrupção do arquivo
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([f'https://www.youtube.com/watch?v={video_id}'])
                    break

                except youtube_dl.utils.DownloadError:
                    continue
        
            #! Colocando as tags
            c = f"{r['items'][cont]['track']['name']}.mp3"
            print(c)
            musica = eyed3.load("musicas/" + c)

            if musica.tag == None: musica.initTag()

            musica.tag.artist = r['items'][cont]['track']['album']['artists'][0]['name']
            musica.tag.album = r['items'][cont]['track']['album']['name']

            with open(f"img/{c[0:-4]}.png", "rb") as imagem: 
                musica.tag.images.set(ImageFrame.FRONT_COVER, imagem.read(), 'image/png')
                musica.tag.save()

        if cont == 99:
            cont_offset += 100
            cont = 0

        cont += 1
    except IndexError:
        for img in os.listdir("img"): os.remove(img) #? removendo as imagens
        break