# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
##原作者：小木   参考CSDN：https://blog.csdn.net/weixin_46625757/article/details/122367961

def get_yiqing():
    result=""
    URL = requests.get('http://m.sy72.com/covid19/')
    URL2 = URL.content
    Soup = BeautifulSoup(URL2, 'html.parser', from_encoding="utf-8")  # 解析器

    """更新日期"""
    date = Soup.find('div', attrs={'class': 'gn'}).find('span').get_text()
    result+=str('【国内疫情】: [' + date + ']')

    Existing_diagnosis = Soup.find('div', attrs={'class': 't2'}).get_text()
    Existing_diagnosis_list = Soup.find('div', attrs={'class': 't1 c0'}).get_text()
    Existing_diagnosis_list2 = Soup.find('span', attrs={'class': 'c0'}).get_text()

    Cumulative_diagnosis = Soup.find_all('div', attrs={'class': 't2'})[1].get_text()
    Cumulative_diagnosis_list = Soup.find('div', attrs={'class': 't1 c1'}).get_text()
    Cumulative_diagnosis_list2 = Soup.find('span', attrs={'class': 'c1'}).get_text()

    Suspected_case = Soup.find_all('div', attrs={'class': 't2'})[2].get_text()
    Suspected_case_list = Soup.find('div', attrs={'class': 't1 c2'}).get_text()
    Suspected_case_list2 = Soup.find('span', attrs={'class': 'c2'}).get_text()

    Cured_cases = Soup.find_all('div', attrs={'class': 't2'})[3].get_text()
    Cured_cases_list = Soup.find('div', attrs={'class': 't1 c3'}).get_text()
    Cured_cases_list2 = Soup.find('span', attrs={'class': 'c3'}).get_text()

    Cases_deaths = Soup.find_all('div', attrs={'class': 't2'})[4].get_text()
    Cases_deaths_list = Soup.find('div', attrs={'class': 't1 c4'}).get_text()
    Cases_deaths_list2 = Soup.find('span', attrs={'class': 'c4'}).get_text()

    # result+=str(
    #     '\n[' + Existing_diagnosis + f'：{Existing_diagnosis_list}{Existing_diagnosis_list2}]\n[' + Cumulative_diagnosis + f'：{Cumulative_diagnosis_list}{Cumulative_diagnosis_list2}]\n[' + Suspected_case + f'：{Suspected_case_list}{Suspected_case_list2}]\n[' + Cured_cases + f'：{Suspected_case_list}{Cured_cases_list2}]\n[' + Cases_deaths + f'：{Cases_deaths_list}{Cases_deaths_list2}]')

    Overseas_input = Soup.find_all('div', attrs={'class': 't2'})[5].get_text()
    Overseas_input_list = Soup.find('div', attrs={'class': 't1 c5'}).get_text()
    Overseas_input_list2 = Soup.find('span', attrs={'class': 'c5'}).get_text()

    Asymptomatic = Soup.find_all('div', attrs={'class': 't2'})[6].get_text()
    Asymptomatic_list = Soup.find('div', attrs={'class': 't1 c6'}).get_text()
    Asymptomatic_list2 = Soup.find('span', attrs={'class': 'c6'}).get_text()

    Existing_symptoms = Soup.find_all('div', attrs={'class': 't2'})[7].get_text()
    Existing_symptoms_list = Soup.find('div', attrs={'class': 't1 c7'}).get_text()
    Existing_symptoms_list2 = Soup.find('span', attrs={'class': 'c7'}).get_text()

    High_risk_areas = Soup.find_all('div', attrs={'class': 't2'})[8].get_text()
    High_risk_areas_list = Soup.find('div', attrs={'class': 't1 c8'}).get_text()
    # High_risk_areas_list2 = Soup.find('span', attrs={'class': 'c8'}).get_text()


    Medium_risk_area = Soup.find_all('div', attrs={'class': 't2'})[9].get_text()
    Medium_risk_area_list = Soup.find('div', attrs={'class': 't1 c9'}).get_text()
    # Medium_risk_area_list2 = Soup.find('span', attrs={'class': 'c9'}).get_text()
    result+=str(
    '\n[' + Existing_diagnosis + f'：{Existing_diagnosis_list}{Existing_diagnosis_list2}]\n[' + Cumulative_diagnosis + f'：{Cumulative_diagnosis_list}{Cumulative_diagnosis_list2}]\n[' + Asymptomatic + f'：{Asymptomatic_list}{Asymptomatic_list2}]\n[' +Suspected_case + f'：{Suspected_case_list}{Suspected_case_list2}]\n[' + Cured_cases + f'：{Suspected_case_list}{Cured_cases_list2}]\n[' + Cases_deaths + f'：{Cases_deaths_list}{Cases_deaths_list2}]')


    result+=(
        '\n[' + Overseas_input + f'：{Overseas_input_list}{Overseas_input_list2}]\n['+ Existing_symptoms + f'：{Existing_symptoms_list}{Existing_symptoms_list2}]\n[' + High_risk_areas + f'：{High_risk_areas_list}]\n[' + Medium_risk_area + f'：{Medium_risk_area_list}]')

    URL = requests.get('http://m.sy72.com/world/')
    URL2 = URL.content
    Soup = BeautifulSoup(URL2, 'html.parser', from_encoding="utf-8")  # 解析器
    result+=str('\n【国外疫情】: [' + date + ']')

    Existing_diagnosis_1 = Soup.find('div', attrs={'class': 't2'}).get_text()
    Existing_diagnosis_1_list = Soup.find('div', attrs={'class': 't1 c1'}).get_text()
    Existing_diagnosis_1_list2 = Soup.find('div', attrs={'class': 'sjj'}).find('span').get_text()

    Total_definite_diagnosis = Soup.find_all('div', attrs={'class': 't2'})[1].get_text()
    Total_definite_diagnosis_list = Soup.find_all('div', attrs={'class': 't1 c1'})[1].get_text()
    Total_definite_diagnosis_list2 = Soup.find_all('div', attrs={'class': 'sjj'})[1].find('span').get_text()

    Total_cured = Soup.find_all('div', attrs={'class': 't2'})[2].get_text()
    Total_cured_list = Soup.find('div', attrs={'class': 't1 c3'}).get_text()
    Total_cured_list2 = Soup.find_all('div', attrs={'class': 'sjj'})[2].find('span').get_text()

    Total_deaths = Soup.find_all('div', attrs={'class': 't2'})[3].get_text()
    Total_deaths_list = Soup.find('div', attrs={'class': 't1 c4'}).get_text()
    Total_deaths_list2 = Soup.find_all('div', attrs={'class': 'sjj'})[3].find('span').get_text()

    result+=str(
        '\n[' + Existing_diagnosis_1 + f'：{Existing_diagnosis_1_list}{Existing_diagnosis_1_list2}]\n[' + Total_definite_diagnosis + f'：{Total_definite_diagnosis_list}{Total_definite_diagnosis_list2}]\n'f'[' + Total_cured + f'：{Total_cured_list}{Total_cured_list2}]\n[' + Total_deaths + f'：{Total_deaths_list}{Total_deaths_list2}]')
    return result