import requests
from bs4 import BeautifulSoup
import time
def app_search(question):
    time.sleep(0.6)
    head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
    'Host': 'www.baidu.com',
    'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / avif, image / webp, * / *;q = 0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection':"keep-alive",
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    "Cookie": "BIDUPSID=729E480F1B8CEB5347D8572AE6495CFA; PSTM=1645237046; BAIDUID=729E480F1B8CEB53DEEB6344B7C88A22:FG=1; BD_UPN=123253; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; __yjs_duid=1_695315baa9a328fc73db6db6ba9ee8781645357087938; MSA_WH=1324_311; H_PS_PSSID=35106_31660_35765_34584_35872_35818_35948_35954_35315_26350_22159; H_PS_645EC=ab89Uk1B6EQVOEBnfF64C5jyWp40Rge9HGeQ8Q2fEodX81kjh6WtOKBhR2A; BAIDUID_BFESS=729E480F1B8CEB53DEEB6344B7C88A22:FG=1; BA_HECTOR=2g8g040k818g0l21a31h1g5g60r; baikeVisitId=9a933a90-dc5c-4192-93d2-10526d401267; WWW_ST=1645745708722"
    # 'Cookie': 'BAIDUID=D7E8011E093FFEA2FA837D62BFD8A45E:FG=1; BIDUPSID=96A143434858A19D3452D1209706D522; PSTM=1653541648; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDUSS=k1mZmtmdWFKcUNLTWhMd3NNMH42UXhiS3J3eHExTmVjOEM4S2Y3dGpsS1B6YlppRVFBQUFBJCQAAAAAAAAAAAEAAAD9bzQo0KG60HpoaQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI9Aj2KPQI9iV; BA_HECTOR=8h052g24aga0042k811h99vjr15; ZFY=gaqtv2b8l3Ynm5W:B38GkMNG:BgXQlxcP:BL:AZlm92Jw5k:C; av1_switch_v3=0; RT="z=1&dm=baidu.com&si=o8bjs2gv3d&ss=l3t25sva&sl=3&tt=1sw&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=2lw"; ariaDefaultTheme=undefined; H_PS_PSSID=36427_36455_31254_36452_36424_36165_36487_36055_36497_36236_26350_36469; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=1; BDRCVFR[gltLrB7qNCt]=mk3SLVN4HKm'
    }
    url="https://www.baidu.com/s?wd="+question
    response = requests.get(url=url, headers=head)
    print("input:",question)
    raw=BeautifulSoup(response.content,"html.parser")
    content=None


    if content is None:
        result = raw.select('div.c-border')
        if result:
            content=result[0].text.strip()
            index=content.find('“')
            if index!=-1 and index!=0:
                content=content[0:index]+"\n"+content[index:]

    if content is None:
        result=raw.select('div.wenda-abstract-old_2wsAy')
        if result:
            content=result[0].text.strip()

    return content


print(app_search("嘉然是谁"))