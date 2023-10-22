# Music Downloader

Um código capaz de instalar músicas e playlists do Spotify e Youtube.

Para melhores resultados, experimente usar o link da música do artista original.

## Usando o código

Há dois métodos para rodar o código: modificando o próprio arquivo/importando para outro arquivo Python ou utilizando `argparse`

Antes de rodar o código, certifique-se de que o este esteja configurado corretamente (Veja [Configuração](#configuração)).

#### Modificando/importando o arquivo

Você pode editar manualmente o arquivo do código fonte e rodá-lo. Por exemplo:

```python
if __name__ == "__main__":
   app = Spotify()
   app.track(url)
   app.download()
```

Ou, em outro arquivo, importar o código fonte:

```python
from music_downloader import Spotify

app = Spotify()
app.track(url)
app.download()
```

#### Argparse

Os argumentos presentes são:

- -**audio**: Link da música/playlist
- -**type**: A plataforma da música/playlist a ser instalada
- --**path**: O diretório de instalação (Padrão é o diretório atual)

Caso você deseja instalar uma playlist, há mais dois argumentos opcionais:

- --**offset** A primeira música a ser instalada na playlist
- --**amount**: A quantidade de músicas a serem instaladas (0 para todas)

Para instalar as músicas, é necessário utilizar o operador `install` antes dos argumentos. Veja nos exemplos:

##### Exemplos:

```bash
python music_downloader.py install -type youtube -audio url_da_musica
```

Ou, caso queira instalar uma playlist

```bash
python music_downloader.py install -type spotify -audio url_da_playlist --offset 5 --amount 10
```

## Configuração

As configurações podem ser feitas também com `argparse` ou, em última medida, manualmente no arquivo `config.json`

No arquivo `config.json` estão dispostas duas informações:

| Key           | Value                                            |
| ------------- | ------------------------------------------------ |
| refresh_token | Seu refresh_token do Spotify.                    |
| auth          | `client_id:secret_id` criptografado em base64. |

Ambas configurações são adquiridas criando um aplicativo no [Spotify for Developers](https://developer.spotify.com).

#### Configurando com argumentos

Para configurar, você deve mudar a operação de `install` para `config` e disponibilizar as informações necessárias. Por exemplo:

```bash
python music_downloader.py config -client_id client_id_spotify -secret_id secret_id_spotify -refresh_token refresh_token_spotify
```

É preciso configurar apenas uma vez, logo depois poderá começar a usar o código da maneira que quiseres.

## Instalação dos requisitos

Para instalar as bibliotecas necessárias pro código, utiliza-se o comando:

```python
pip install -r requirements.txt
```

Além das bibliotecas, também é precido o **FFmpeg**, que pode ser instalado manualmente no próprio site ou com o comando (Linux):

```bash
sudo apt install ffmpeg
```
