from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import csv
import sys
import re


course_id = input("Enter the course id exactly as you see it on sis EX:'CSCI 1200' (capitalization is important): ").strip()
print(course_id)
output_file_name = input("Enter the output file name: ").strip()
print(output_file_name)


options = Options()
options.headless = True

transfer_course_url = "https://sis.rpi.edu/rss/yhwwkwags.P_Select_Inst"
driver = webdriver.Firefox(options=options)
driver.get(transfer_course_url)


output_data = []


def scrape_place(type):
    states_select = driver.find_element_by_name(type)
    states = [x.get_attribute('value') for x in states_select.find_elements_by_tag_name("option")]
    states_real_names = [x.text for x in states_select.find_elements_by_tag_name("option")]

    for i in range(len(states)):
        if(states[i] == ""):
            continue

        print("State/Nation:", states[i])
        Select(driver.find_element_by_name(type)).select_by_value(states[i]);#set the select box to the current state
        driver.find_element_by_css_selector("[value='Get Institutions']").click()#click button to load schools

        #get list of schools for this state
        schools_select = driver.find_element_by_name('sbgi_code')
        schools = [x.get_attribute('value') for x in schools_select.find_elements_by_tag_name("option")]

        scrape_school(schools,states[i],type,states_real_names[i])

        driver.get(transfer_course_url)    #go back to main page for next state




def save_data():
    with open(output_file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(output_data)


def scrape(real_name):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    school_name = soup.find("caption", {"class": "captiontext"}).find("strong").text


    table = soup.find("table", {"id": "TransArtTable"})
    table = table.find("tbody")
    rows = table.findAll('tr')
    for i in range(len(rows)):
        cells = rows[i].findAll('td')
        if(len(cells) > 3 ):
            if(cells[3].text.strip() == course_id):
                print("Found class at", school_name)
                #gets the offsets because some data actually fills more than one row
                row_offset_up=0
                while(len(rows[i-row_offset_up].findAll('td'))>1):
                    row_offset_up += 1
                row_offset_down=0
                while(len(rows[i+row_offset_down].findAll('td'))>1):
                    row_offset_down += 1

                # print(school_name, cells[3].text, row_offset_up, row_offset_down)

                #scrape data between the offsets
                start_cell_offset = 2

                output_line = [""] * (5+start_cell_offset)
                output_line[0]=real_name
                output_line[1] = school_name
                for offset in range(i-row_offset_up+1, i+row_offset_down):
                    # print(offset)
                    current_cells = rows[offset].findAll('td')
                    for j in range(start_cell_offset,min(len(current_cells)+start_cell_offset-1, (5+start_cell_offset))):
                        temp = current_cells[j-start_cell_offset+1].text.strip()
                        if(temp != ""):
                            output_line[j] += re.sub(' +', ' ', temp) + "\n"

                #remove extra \n at the end of a cell
                for j in range(len(output_line)):
                    output_line[j] = output_line[j].strip()

                output_data.append(output_line)

                save_data()

    # print(output_data)



#schools is the list of schoolsys.argv[s
#place is the state or the nation
#type is "stat_code" for a state or "natn_code" for a nation
def scrape_school(schools, place, type, real_name):
    for school in schools:
        if(school == ""):
            continue
        # print("Working on school number:", school)
        Select(driver.find_element_by_name('sbgi_code')).select_by_value(school)#set the select box to the current school
        driver.find_element_by_css_selector("[value='Get Courses']").click()#click to load the classes for the course

        scrape(real_name)

        driver.get(transfer_course_url)#go back to main page for next college

        Select(driver.find_element_by_name(type)).select_by_value(place);#repick the state
        select_button = driver.find_element_by_css_selector("[value='Get Institutions']").click()#reclick Get Institutions button

#scrape schools then nations
scrape_place('stat_code')
scrape_place('natn_code')
