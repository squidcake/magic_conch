from pypinyin import lazy_pinyin, Style

def getfirst_words(str_data):
    """
       获取字符串的首字母
       :param str_data: 字符串
       :return: 返回首字母缩写(大写)
       """
    a = ''.join(lazy_pinyin(str_data, style=Style.FIRST_LETTER))
    return a.upper()

# print(getfirst("瘠薄"))

