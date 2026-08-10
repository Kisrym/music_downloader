import requests
from json import load

class Refresh:
    def __init__(self):
        with open(r"config.json") as f:
            data = load(f)
            self.refresh_token = data["refresh_token"]
            self.auth = data["auth"]

    def refresh(self):
        print("chammou")
        r = requests.post(r"https://accounts.spotify.com/api/token",
                        data = {"grant_type" : "refresh_token", "refresh_token" : self.refresh_token},
                        headers = {"Authorization" : "Basic " + self.auth},
                        timeout=5
                    )

        print("acabou")
        
        if len(r.json()) > 2:
            return r.json()["access_token"]
        else:
            raise KeyError("Informações inválidas e/ou incompletas. Por favor, adicione as informações necessárias. Use -h para mais informações.")

if __name__ == "__main__":
    a = Refresh()
    print(a.refresh())