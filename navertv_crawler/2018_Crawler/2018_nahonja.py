#%%
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from datetime import datetime
import json
from collections import OrderedDict

class Naver_Crawler:

    def __init__(self):
        Naver_Crawler.self = self
        Naver_Crawler.in_list = True
        Naver_Crawler.list_order = 1
        Naver_Crawler.in_year = True
        Naver_Crawler.data_list = []

    def list_crawl(self) :
        while self.in_list == True:
            
            data_dict = {}
            heart_count = driver.find_element_by_xpath("//em[@class = 'u_cnt _cnt']").text
            reply_count = driver.find_element_by_xpath("//span[@class = 'count _commentCount']").text
            play_count = driver.find_element_by_xpath("//span[@class = 'play']").text
            is_jeon = jeon_name in driver.find_element_by_xpath("//h3[@class = '_clipTitle']").text   
            is_park = park_name in driver.find_element_by_xpath("//h3[@class = '_clipTitle']").text           
            title = driver.find_element_by_xpath("//*[@id='clipInfoArea']/div[1]/h3").text

            if ("예고" in title) or ("5주년" in title) :
                pass
            else :  
                try:
                    date =  driver.find_element_by_xpath('//*[@id="clipInfoArea"]/div[4]/div/dl/dd[3]').text
                    #date_strp = datetime.strptime(date, '%Y.%m.%d.')
                except Exception:
                    date = driver.find_element_by_xpath('//*[@id="clipInfoArea"]/div[1]/div/span[2]').text 
                except Exception :
                    date = driver.find_element_by_xpath('//*[@id="clipInfoArea"]/div[3]/div/dl/dd[3]').text
                finally :
                    try : 
                        date_strp = datetime.strptime(date, '%Y.%m.%d.')
                    except : 
                        date = date.replace('등록', '')
                        date_strp = datetime.strptime(date, '%Y.%m.%d.')

                data_dict['date'] =  date
                    
            reply_list = []
            replies = driver.find_elements_by_xpath("//span[@class = 'u_cbox_contents']")
            for a in replies:
                reply_list.append(a.text)

            data_dict['heart_count'] = heart_count
            data_dict['reply_count'] =  reply_count
            data_dict['play_count'] = play_count
            data_dict['is_jeon'] = is_jeon
            data_dict['is_park'] = is_park
            data_dict['reply_list'] =  reply_list            
            data_dict['order_in_list'] = int(self.list_order)
                
            self.data_list.append(data_dict)
            print(data_dict)

            try : 
                if (data_dict['date'] == '2018.12.07.') and (data_dict['order_in_list'] == 20) :
                    #2018년 크롤링 완료 시 완료 메시지 출력 및 json 파일 작성
                    print('크롤링이 완료됐습니다.')
                    with open('nahonja_2018.json', 'w', encoding="utf-8") as make_file:
                        json.dump(self.data_list, make_file, ensure_ascii=False, indent = '\t')
                    exit()
            except KeyError :
                pass
                        
            self.list_order += 1

            try : 
                #같은 회차 내 다음 영상으로 이동
                click_path = "//*[@id='playlistClip']/li[{}]/div/dl/dt/a".format(self.list_order)
                click_element = driver.find_element_by_xpath(click_path)
                click_element.click()
                time.sleep(3)
                
            except Exception : 

                # with open('naver_crawl.json', 'a', encoding="utf-8") as make_file:
                # json.dump(data_list, make_file, ensure_ascii=False)
                #while문 탈출
                self.in_list = False

                #변수초기화
                self.in_list = True
                self.list_order = 1

                #다음 재생목록으로 이동
                click_path2 = '//*[@id="playlistClipScrollBox"]/div[1]/div/div/ul/li[2]/a/div/strong'
                click_path_ex = '//*[@id="playlistClipScrollBox"]/div[1]/div/div/ul/li[2]/a/div'
                click_element2 = driver.find_element_by_xpath(click_path2)
                click_element_ex = driver.find_element_by_xpath(click_path_ex)
                try :
                    click_element2.click()
                except : 
                    click_element_ex.click()
                time.sleep(3)
                self.list_crawl()
                           

#MBC 나혼자산다 2018년 1화 네이버 tv 링크 

first_url = 'https://tv.naver.com/v/2509171/list/180650'
driver = webdriver.Chrome('C:\\Users\\bumso\\datajournalism-2018\\chromedriver_win32\\chromedriver.exe')
driver.get(first_url)
time.sleep(3)

jeon_name = "현무"
park_name = "나래"

nc = Naver_Crawler()
nc.list_crawl()