# Music Downloader

Um código capaz de instalar músicas e playlists do Spotify e Youtube.

Para melhores resultados, experimente usar o link da música do artista original.

## Usando o código

Para usar o código, só é preciso instalá-lo (prestando atenção com as pastas *img* e *musicas*, necessárias para o funcionamento do código) e rodar com o comando:

```bash
python3 music_downloader.py
```

ou

```bash
python music_downloader.py
```

## Exemplos

```python
app = Spotify()
app.playlist(spotify_link)
app.download()
# Mesma coisa com a classe Youtube
```

## Configuração

As configurações do código são feitas no `config.json`.

| Key           | Value                                            |
| ------------- | ------------------------------------------------ |
| refresh_token | Seu refresh_token do Spotify.                    |
| auth          | `client_id:secret_id` criptografado em base64. |

Ambas configurações são adquiridas criando um aplicativo no [Spotify for Developers](https://developer.spotify.com).

## Instalação dos requisitos

Para instalar as bibliotecas necessárias pro código, utiliza-se o comando:

```python
pip install -r requirements.txt
```

Além das bibliotecas, também é precido o **FFmpeg**, que pode ser instalado manualmente no próprio site ou com o comando (Linux):

```bash
sudo apt install ffmpeg
```
