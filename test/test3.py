import requests
import json

url="https://api.lolicon.app/setu/v2"
myparams={

}
res=requests.post(url=url)
print(res.content,res.headers)