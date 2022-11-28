# Spotify Downloader

Um código capaz de extrair todas as músicas de uma playlist do Spotify e instalá-las automaticamente.
## Usando o código

Para usar o código, só é preciso instalá-lo (prestando atenção com as pastas *img* e *musicas*, necessárias para o funcionamento do código) e rodar com o comando:

```bash
python3 spotify_downloader.py
```

ou

```bash
python spotify_downloader.py
```

## Configuração

As configurações do código são feitas no `config.json`.

| Key           | Value                                    |
|---------------|------------------------------------------|
| refresh_token | Seu refresh_token do Spotify.            |
| auth          |  `client_id:secret_id` criptografado em base64. |

## Instalação dos requisitos

Para instalar as bibliotecas necessárias pro código, utiliza-se o comando:

```python
pip install -r requirements.txt
```

Além das bibliotecas, também é precido o **FFmpeg**, que pode ser instalado manualmente no próprio site ou com o comando (Linux):

```bash
sudo apt install ffmpeg
```
