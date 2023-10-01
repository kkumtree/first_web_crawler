# main.py
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd 
from datetime import datetime
import os
import re
"""
[dependency: python3]
pip install bs4
pip install selenium
pip install pandas
"""
NULL = ''
URL = os.environ['URL']
URL_PAGE = os.environ['URL_PAGE']
URL_FILE = os.environ['URL_FILE']

def getCompany(List):
  temp_string = []
  for i in List:
    temp_string = str(i).strip()
    if len(temp_string) == 0: continue
    elif 'span' in temp_string: continue
    else: return temp_string

def getAttribute(List):
  result = []
  j = 0
  for i in List:
    if j == 0:
      j += 1
      continue
    else:
      j += 1
      result.append(i.text.strip())
  return result

# Chrome의 경우 | chromedriver의 위치를 지정
# driver = webdriver.Chrome('.\\chromedriver_win32\\chromedriver.exe')
driver = webdriver.Chrome()
# # PhantomJS의 경우 | PhantomJS의 위치를 지정해준다.
# driver = webdriver.PhantomJS('./phantomjs-2.1.1-windows')

# 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
driver.implicitly_wait(3)

# 파일명
now = datetime.now()
month = '0' + str(now.month) if 1 <= now.month <= 9 else now.month
day = '0' + str(now.day) if 1 <= now.day <= 9 else now.day
hour = '0' + str(now.hour) if 1 <= now.hour <= 9 else now.hour
minute = '0' + str(now.minute) if 1 <= now.minute <= 9 else now.minute
file_datetime = '-'.join([str(now.year), str(month), str(day), str(hour), str(minute)])
file_datetime = file_datetime + '.csv'
file_flag = 1

driver.get(URL)
# last_page_number = int(re.sub(r'[^0-9]', '', driver.find_element_by_class_name('current_next').get_attribute('href')))
last_page_element = driver.find_element(By.CLASS_NAME, 'current_next')
last_page_href = last_page_element.get_attribute('href')
last_page_number = int(re.sub(r'[^0-9]', '', last_page_href))

print(last_page_number, "&&", type(last_page_number))

for i in range(0, last_page_number):
  pageIndex = i + 1
  driver.get(URL + URL_PAGE + str(pageIndex))
  html = driver.page_source
  soup = BeautifulSoup(html, 'html.parser')
  item_list = soup.find_all('div', 'product_list row mt30 pb20 br_line_bottom')
  item_count = len(item_list)
  print('==== 현재 $$ ' + str(pageIndex) + " $$ 페이지 item 갯수 : " + str(item_count) + " ====")
  for j in range(0, item_count):
    item_index = j + 1
    # 0. 초기화
    col_section = col_company = col_item = col_desc = col_table = col_sample = col_format = col_reg_date = col_desc_before_resolve = ""
    col_attribute = []

    # 1. 대분류(파일/API/가공서비스) 처리 [+속성]
    # document.querySelector("#listType > div:nth-child(1) > div.contents > div.mb5 > span.icon_file")
    item_query = '#listType > div:nth-child(' + str(item_index) + ') > div.contents > div.mb5 > span'
    query_section = soup.select(item_query)
    col_section = query_section[0].text.strip()

    # 2. 분류별 제목, 제공업체명, 등록일 추출
    # document.querySelector("#listType > div:nth-child(1) > div.contents > a > p")
    item_query = '#listType > div:nth-child(' + str(item_index) + ') > div.contents > a > p'
    if col_section == "가공":
      # 제목은 일괄처리
      col_item = "가공서비스 제공업체"
      # 제공업체명
      col_company = soup.select(item_query)[0].text.strip()
      # 등록일
      # document.querySelector("#listType > div:nth-child(4) > div.summary > ul > li:nth-child(3) > span")
      item_query = '#listType > div:nth-child(' + str(item_index) + ') > div.summary > ul > li:nth-child(3) > span'
      col_reg_date = soup.select(item_query)[0].text.strip()
    else:
      # 제목
      col_item = soup.select(item_query)[0].text.strip()
      # 제공업체명
      # document.querySelector("#listType > div:nth-child(1) > div.contents > div.mb5")
      item_query = '#listType > div:nth-child(' + str(item_index) + ') > div.contents > div.mb5'
      col_company = getCompany(soup.select(item_query)[0].contents)
      # 등록일
      # document.querySelector("#listType > div:nth-child(3) > div.summary > ul > li:nth-child(4) > span")
      item_query = '#listType > div:nth-child(' + str(item_index) + ') > div.summary > ul > li:nth-child(4) > span'
      col_reg_date = soup.select(item_query)[0].text.strip()
    
    # 3. 속성추출 (from. 1번의 query_section)
    item_query = '#listType > div:nth-child(' + str(item_index) + ') > div.contents > div.mb5 > span'
    query_section = soup.select(item_query)
    col_attribute = getAttribute(query_section)
    # 3-1. 속성 리스트 String으로 임시변환
    col_attribute = ', '.join(col_attribute)

    # 4. 단가표 [+샘플파일] (링크로 제공함)
    if col_section == "가공":
      # 단가표
      item_query = '#listType > div:nth-child(' + str(item_index) + ') > div.summary > ul > li:nth-child(2) > a'
      if (soup.select(item_query)):
        query_table = soup.select(item_query)[0]['onclick'].split('\'')
        col_table = URL_FILE
        for i in query_table:
          if '=' in i:
            col_table += i.replace('=', '%3D')
            col_table += '&seqno=1'
      else:
        col_table = "상세조회참조"   
      # 샘플파일은 없음
      col_sample = NULL
    else:
      # 단가표
      # document.querySelector("#listType > div:nth-child(4) > div.summary > ul > li:nth-child(3) > a")
      item_query = '#listType > div:nth-child(' + str(item_index) + ') > div.summary > ul > li:nth-child(3) > a'
      if (soup.select(item_query)):
        query_table = soup.select(item_query)[0]['onclick'].split('\'')
        col_table = URL_FILE
        for i in query_table:
          if '=' in i:
            col_table += i.replace('=', '%3D')
            col_table += '&seqno=1'
            break
      else:
        col_table = NULL
      # 샘플파일
      # document.querySelector("#sampleBtn2")
      item_query = '#listType > div:nth-child(' + str(item_index) + ') > div.summary > ul > li:nth-child(2) > a'
      if (soup.select(item_query)):
        query_sample = soup.select(item_query)[0]['onclick'].split('\'')
        col_sample = URL_FILE
        for i in query_sample:
          if '=' in i:
            col_sample += i.replace('=', '%3D')
            col_sample += '&seqno=2'
            break
        # document.querySelector("#listType > div:nth-child(3) > div.summary > ul > li:nth-child(2) > span")
        item_query = '#listType > div:nth-child(' + str(item_index) + ') > div.summary > ul > li:nth-child(2) > span'
        col_format = soup.select(item_query)[0].text.strip()
        col_section = col_section + '_' + col_format
      else:
        col_sample = col_format = NULL

    # 5. 설명추출
    # document.querySelector("#listType > div:nth-child(3) > div.contents > div.gr_explanation > p")
    if col_section != "가공":
      item_query =  '#listType > div:nth-child(' + str(item_index) + ') > div.contents > div.gr_explanation > p'
      col_desc_before_resolve = soup.select(item_query)[0].text.strip().split()
      temp_string = []
      for i in col_desc_before_resolve:
        if i == '\x9f':
          continue
        else:
          temp_string.append(i)
      col_desc = " ".join(temp_string)
    else:
      col_desc = NULL
    
    # 6. 건별 저장
    data = [col_section, col_company, col_item, col_attribute, col_table, col_sample, col_reg_date, col_desc]

    df = pd.DataFrame(data)
    df = df.transpose()
    # df.rename(columns=df.iloc[0], inplace=True)
    # df = df.drop(df.index[0])
    df.columns = ['분류', '기업명', '상품명', '태그', '가격정책_단가표', '샘플파일', '등록일', '설명']
    if file_flag == 1 & True != os.path.exists(file_datetime):
      df.to_csv(file_datetime, index=False, mode='w', encoding='utf-8-sig')
      file_flag = 0
      print("======Write OKAY=======")
    else:
      df.to_csv(file_datetime, index=False, mode='a', header=False, encoding='utf-8-sig')
      print("======Append OKAY=======")
    
    
    

    

  