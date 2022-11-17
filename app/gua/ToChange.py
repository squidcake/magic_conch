import json
import random
import time
import os
from pathlib import Path
#别挂配置数据
gua_data_path = str(Path(__file__).resolve().parent)+"\data.json"

#别卦数据
gua_data_map = {
        
}
fake_delay = 1

#读取别卦数据
def init_gua_data(json_path):
	with open(gua_data_path,'r',encoding='utf8')as fp:
		global gua_data_map
		gua_data_map = json.load(fp)
#爻图标映射
yao_icon_map = {
	0:"- -",
	1:"---"
}

#经卦名
base_gua_name_map = {
	0:"坤",1:"震",2:"坎",3:"兑",4:"艮",5:"离",6:"巽",7:"乾"
}

#数字转化为二进制数组
def base_gua_to_yao(gua, yao_length=3):
	result = []
	while gua >= 1:
		level = 0 if gua % 2 == 0 else 1
		gua //= 2
		result.append(level)
	while len(result) < yao_length:
		result.append(0)
	return result

#二进制数组转化为数字
def base_yao_to_gua(array):
	array = array[:]
	while len(array) > 0 and array[-1] == 0:
		array.pop()
	result = 0
	for i in range(len(array)):
		if array[i] == 0:
			continue
		result += pow(2, i)
                
	return result

#打印一个挂
def print_gua(gua):
	yao_list = base_gua_to_yao(gua, 6)
	up_yao_list = yao_list[0:3]
	up = base_yao_to_gua(up_yao_list)
	res=""
	res+="\n"+yao_icon_map[up_yao_list[2]]
	res+="\n"+yao_icon_map[up_yao_list[1]] + " " + base_gua_name_map[up]
	res+="\n"+yao_icon_map[up_yao_list[0]]
        
	res+=("\n")

	down_yao_list = yao_list[3:6]
	down = base_yao_to_gua(down_yao_list)
	res+="\n"+yao_icon_map[down_yao_list[2]]
	res+="\n"+yao_icon_map[down_yao_list[1]] + " " + base_gua_name_map[down]
	res+="\n"+yao_icon_map[down_yao_list[0]]
	return res

#使用梅花易数
def calculate_with_plum_flower():
	global gua_data_path
	init_gua_data(gua_data_path)
	#起上卦
	result=""
	result+=str("使用梅花易数♣")
	print_a_wait_animation("卜上卦：", fake_delay)
	up_base_gua = int(round(time.time() * 1000)) % 8
	up_yao_array = base_gua_to_yao(up_base_gua)
	result+=str("\n上卦为:"+ base_gua_name_map[up_base_gua])
	#起下卦
	print_a_wait_animation("正在获取下卦：", fake_delay)
	down_base_gua = random.randint(0, 999999999999) % 8
	down_yao_array = base_gua_to_yao(down_base_gua)
	result+=str("\n下卦为:"+ base_gua_name_map[down_base_gua])
	#组成卦象
	print_a_wait_animation("\n组成本卦：", fake_delay)
	result+=str("【本卦】")
	yao_list = up_yao_array + down_yao_array
	gua = base_yao_to_gua(yao_list)
	result += print_gua(gua)
	#读取本卦象信息
	gua_code = str(base_gua_name_map[up_base_gua]) + str(base_gua_name_map[down_base_gua])
	gua_data = gua_data_map[gua_code]
	result+=str("\n本卦为:"+gua_data['name'])
	result+=str("\n【辞】:"+ gua_data['words']+"\n（译）:"+gua_data['white_words'])
	result+="\n【象】:"+ gua_data['picture']+"\n（译）:"+gua_data['white_picture']
	print_a_wait_animation("正在组成互卦：", fake_delay)
	result+=("\n\n【互卦】")
	#读取互卦象信息
	up_hu_yao_list = [yao_list[4],yao_list[5],yao_list[0]]
	up_hu_gua = base_yao_to_gua(up_hu_yao_list)
	down_hu_yao_list =[yao_list[5],yao_list[0],yao_list[1]]
	down_hu_gua = base_yao_to_gua(down_hu_yao_list)
	hu_yao_list = up_hu_yao_list + down_hu_yao_list
	hu_gua = base_yao_to_gua(hu_yao_list)
	hu_gua_code = str(base_gua_name_map[up_hu_gua]) + str(base_gua_name_map[down_hu_gua])
	hu_gua_data = gua_data_map[hu_gua_code]
	result+=print_gua(hu_gua)
	result+=str("\n互卦为:"+ hu_gua_data['name'])
	result+=str("\n【辞】:"+hu_gua_data['words']+"\n（译）:"+ hu_gua_data['white_words'])
	result+="\n【象】:"+ hu_gua_data['picture']+"\n（译）:" + hu_gua_data['white_picture']
	print_a_wait_animation("正在组成变卦：", fake_delay)
	result+=("\n\n【变卦】")
	change_index = int(round(time.time() * 1000)) % 6
	change_yao_list = yao_list[:]
	change_yao_list[change_index] = 0 if change_yao_list[change_index] == 1 else 1
	up_change_yao_list = change_yao_list[0:3]
	up_change_gua = base_yao_to_gua(up_change_yao_list)
	down_change_yao_list =change_yao_list[3:5]
	down_change_gua = base_yao_to_gua(down_change_yao_list)
	
	change_gua = base_yao_to_gua(change_yao_list)
	print_gua(change_gua)
	change_gua_code = str(base_gua_name_map[up_change_gua]) + str(base_gua_name_map[down_change_gua])
	change_gua_data = gua_data_map[change_gua_code]
	result+=str("\n变卦为:"+change_gua_data['name'])
	result+=str("\n【辞】:"+ change_gua_data['words']+"\n（译）:"+change_gua_data['white_words'])
	result+="\n【象】:"+change_gua_data['picture']+"\n(译):"+change_gua_data['white_picture']
	return result
def print_a_wait_animation(tips,times):
	animation = "|/-\\"
	idx = 0
	for i in range(times):
		print(tips + animation[idx % len(animation)],animation[idx % len(animation)],animation[idx % len(animation)],animation[idx % len(animation)],animation[idx % len(animation)], end="\r"),
		idx += 1
		time.sleep(0.1)

# init_gua_data(gua_data_path)
# calculate_with_plum_flower()
