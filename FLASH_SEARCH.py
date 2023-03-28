import requests

from selenium import webdriver #since Youtube has anti-scraping measures, selenium allows us to create Chrome browser but controlled with python
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By#for driver.get('By.CSS)
#from openpyxl import Workbook

#for ignoring certificate error
from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager

#for HEADLESS
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument('--ignore-certificate-errors')
#-----

#import pandas as pd

import xlsxwriter

from selenium import webdriver

from bs4 import BeautifulSoup #works fine, ignore squigly red

from datetime import datetime, timedelta
#from webdriver_manager.chrome import ChromeDriverManager

import time
from time import sleep
def formatDate4XL(str2):
    return (str2[2:4] +'.'+str2[0:2] + '.20'+str2[4:])    
#end of def2    


mobi_url = 'https://www.flashscore.mobi/'
com_url = 'https://www.flashscore.com/'

#^OLD CODE

#NEW TRY with pressing buttons -- true automation

sudo_dataFrame =[ ['Date','Competition','Match(Home vs Away)','Last 5 results HOME','Last 5 results AWAY'] ]
#OPEN CALENDAR
driver = webdriver.Chrome()
driver.get(com_url)


num = 0

#open days and make list of their links? NO, just go to the day chosen
calendar = driver.find_element(By.ID,'calendarMenu')
calendar.click()
time.sleep(10)


today_index = 7


dias = driver.find_elements(By.CLASS_NAME,'calendar__day')
dias_strings = ['']*len(dias)

#print(len(dias_strings))

for z in range(len(dias)):
    #print("Text before at index" + str(z) + " is "+dias[z].text)
    #if dias[z].text == 'Today' or dias[z].text == 'TODAY':
        #dias_strings[z] = (datetime.now()).strftime('%d%') + "/"+ datetime.now().strftime('%y%')
    #else:    
    dias_strings[z] = dias[z].text.split(' ')[0].strip()
    #print("Text after at index" +  str(z) + " is "+dias_strings[z])
    #if dias[z].text == 'Today' or dias[z].text == 'TODAY':
    #    dias1[z] = (datetime.now()).strftime('%d%')#.strftime('%d%') + "/"+ datetime.now().strftime('%y%')
    #    today_index = z
    #else:
    #dias1[z] = dias[z].text.split(' ')[0].strip()
    #print(dias1[z])

desired_date = ''    

##desired_date = '28/03' #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#index_of_desired_date = dias_strings.index(desired_date)
#print('Desried Date: '+desired_date)
#for 
#match choice:
   # case 0:
       # print()
menu_options = {}
for z in range((len(dias_strings)) - today_index):
    menu_options[z + 1] = dias_strings[today_index + z]

#print(menu_options[7])
done_choosing = False
#menu_options['3']
while done_choosing == False:
    print("AVAILABLE DATES( Format is Day/Month")
    print("----------------")
    for key, value in menu_options.items():
        print(str(key) + '.' + value)
    choice = input("CHOOSE A DATE (select corresponding #):") #choice is string but in menu_options it is int
    #print menu_options
    


    #print ("type of number", type(choice))
    if int(choice) in menu_options:
        print("You chose "+menu_options[int(choice)])
        done_choosing = True
        desired_date = menu_options[int(choice)] 
    else:
        print("That is not a valid choice!")   
    print(choice)
    #if done_


#desired_date = '28/03' #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

index_of_desired_date = dias_strings.index(desired_date)
print('Desired Date: '+desired_date)
#GET TO DESIRED PAGE
#print("# of days: " + str(len(dias)))

#for z in range(len(dias)):#have to repeat the calender clicks because cant store buttons/links
    #if z > today_index:

#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), ) 
driver = webdriver.Chrome()
driver.get(com_url)

calendar = driver.find_element(By.ID,'calendarMenu')
time.sleep(5)#faux pause

calendar.click()
time.sleep(15)
#dias2 = 
dias2 = driver.find_elements(By.CLASS_NAME,'calendar__day')
#print(len(dias2))

#driver.execute_script("arguments[0].scrollIntoView();",dias2[index_of_desired_date])
time.sleep(15)

(dias2[index_of_desired_date]).click()
#get to todays date
time.sleep(15)
#Open Closed DROPDOWNS 
closed_dropdowns = driver.find_elements(By.CLASS_NAME,'arrow.event__expander.event__expander--close')

#"""""
#print("OPENING DROPDOWNS")
time.sleep(5)#faux pause
for auto in closed_dropdowns:#open all closed dropdowns
  
        driver.execute_script("arguments[0].scrollIntoView();",auto)
       
        time.sleep(15)
        auto.click()
        time.sleep(15)
      
#NOW to retrieve the match_ids : g_1_MATCHID but is this format consistent   
match_blocks = driver.find_elements(By.TAG_NAME,'div')
match_ids =[]
for auto in match_blocks:
    
    #hopefully no need for try block, and this process is agreeable
     if (auto.get_attribute('title') != None) and (auto.get_attribute('title') == 'Click for match detail!'): 
        m_ID = auto.get_attribute('id')  #= g_1_MATCHID
        m_ID = (m_ID.split('_')[-1]).strip()#just in case trailing/leading spaces
        #print(m_ID)
        match_ids.append(m_ID)

#print("Number of matches: " + str(len(match_ids)))
def list2string(list1):#w/ space
    str1 = ''
    for auto in list1:
        str1 += auto + ' '
    str1 = str1.strip()
    return str1  
#GETTING IMPORTANT CONTENT FOR EXCEL SPREADSHEET
game_date = ''

print("Total Games on " + desired_date + ": " + str(len(match_ids)))
for z in range(len(match_ids)):#len(match_ids)
   
    match_id = match_ids[z]       
    match_url = com_url + 'match/'+match_id+'/#/h2h/overall'#another /match-summary???
    

    driver = webdriver.Chrome()
    driver.get(match_url)
  
    competition = driver.find_elements(By.CLASS_NAME, 'tournamentHeader__country')[0].text
    competition = competition[0:competition.index(':')]
    competition = competition.lower().title()
    

    
    matchup = driver.find_elements(By.CLASS_NAME, 'participant__participantName')#
    home_name = matchup[0].text
    away_name = matchup[2].text


    h2h = home_name + ' - '+away_name


    date_of_game = driver.find_element(By.CLASS_NAME,'duelParticipant__startTime').text
    game_date = date_of_game


    l5home = []#getLast5( home_name,home_content)
    #rows[0] = home, rows[1] = away
    
    home_content = driver.find_elements(By.CLASS_NAME, 'rows')[0]
    #print(home_content.find_element(By.CLASS_NAME,'h2h__result').text)
    
    last_games_count = home_content.find_elements(By.CLASS_NAME,'h2h__result')#.text.split('\n') #or do elemst()[0].text which is what was done for getL% parameter
    #arr2 = home_content.find_elements(By.CLASS_NAME,'h2h__result__fulltime')#.text.split('\n')
    home_pts = ''
    away_pts = ''

    for z in range(len(last_games_count)):
        #print(home_content.find_elements(By.CLASS_NAME,'h2h__result')[z].find_element(By.TAG_NAME,'span')[0])
        arr1 = home_content.find_elements(By.CLASS_NAME,'h2h__result')[z].text.split('\n') #or do elemst()[0].text which is what was done for getL% parameter
        arr2 = home_content.find_elements(By.CLASS_NAME,'h2h__result__fulltime')[z].text.split('\n')
        #if z%2 == 0:
        try:
            if arr2[0] != '':#or maybe check if length is greater than 1
                home_pts = arr2[0]
                away_pts = arr2[1]
            else:
                home_pts = arr1[0]
                away_pts = arr1[1]
        except:
            print("Arr1[0] = " + arr1[0])

        score = home_pts + '-' + away_pts
        l5home.append(score) 
        #print(score)
    l5home = list2string(l5home)

    l5away = []#getLast5( home_name,home_content)
    #rows[0] = home, rows[1] = away
    
    away_content = driver.find_elements(By.CLASS_NAME, 'rows')[1]
    last_games_count = away_content.find_elements(By.CLASS_NAME,'h2h__result')#should be same as count of fulltimes
    

    for z in range(len(last_games_count)):
        arr3 = away_content.find_elements(By.CLASS_NAME,'h2h__result')[z].text.split('\n') #or do elemst()[0].text which is what was done for getL% parameter
        arr4 = away_content.find_elements(By.CLASS_NAME,'h2h__result__fulltime')[z].text.split('\n')
        #if z%2 == 0:
        if arr4[0] != '':#or maybe check if length is greater than 1
            home_pts = arr4[0]
            away_pts = arr4[1]
        else:
            home_pts = arr3[0]
            away_pts = arr3[1]   
        score = home_pts + '-' + away_pts
        l5away.append(score)
        #print(score)
    l5away = list2string(l5away)

    #print('Done')
    #print(match_id)
    sudo_dataFrame.append([date_of_game,competition,h2h,l5home,l5away])
    
print("FILLING SPREADSHEET")
#file_name = desired_date[]
#game_date = '29.03.2023'
file_arr = game_date.split('.')
name_of_file = file_arr[0] + '-' + file_arr[1] + '-' + file_arr[2]
workbook = xlsxwriter.Workbook('excel_files/'+name_of_file+'.xlsx')
wksht = workbook.add_worksheet()

row = 0
col = 0
for a,b,c,d,e in (sudo_dataFrame):
    wksht.write(row,col,a)
    wksht.write(row,col+1,b)
    wksht.write(row,col+2,c)
    wksht.write(row,col+3,d)
    wksht.write(row,col+4,e)
    row +=1
workbook.close() 


#pip install selenium
#pip install requests
#pip install BeautifulSoup4
#pip install xlsxwriter

