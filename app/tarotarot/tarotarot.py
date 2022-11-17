import random
import json
from PIL import Image
import base64
from io import BytesIO
from pathlib import Path
SMALL_ROOM=[]

ROOT_PATH = str(Path(__file__).resolve().parent)
PATH=ROOT_PATH+"/explanation.json"
PIC_PATH=ROOT_PATH+"/pic/"
PIC2_PATH=ROOT_PATH+"/pic2/"
def app_tarotarot(new_flag=False):
    global PATH
    num=str(random.randint(0,21))
    with open(PATH,"r",encoding='utf-8') as file:
        data=json.load(file)

    side=(lambda ram : "font" if ram==1 else "back")(random.randint(0,1))
    img_base=app_get_img_base_loacl(num,rotate=("back"==side),new_flag=new_flag)
    result={"img":img_base,"side":side,"content":data[num][side]}
    result.update(data[num])
    print(side)
    return result



def app_get_img_base_loacl(num,rotate=False,new_flag=False):
    if new_flag:
        img=Image.open(PIC2_PATH+num+".png")
    else:
        img=Image.open(PIC_PATH+num+".png")

    if rotate:
        img=img.transpose(Image.ROTATE_180)
    else:
        pass
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    byte_data = img_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str


def app_pil_base64(image):
    img_buffer = BytesIO()
    image.save(img_buffer, format='PNG')
    byte_data = img_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str

app_tarotarot()