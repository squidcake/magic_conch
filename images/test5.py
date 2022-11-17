import base64

def get_img_base_loacl(uri):
    try:
        png = open(uri, 'rb')
    except Exception as e:
        print(e)
        print(uri)
        return
    res = png.read()
    s = base64.b64encode(res)
    png.close()
    return s