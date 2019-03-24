
#======================================================================
#Author: Rahul Prajapati                File: download_script.py
#Package: os, urllib.parse, requests, tqdm and bs4 
#Date modified: 03/23/2019 
#Link Used: https://github.com/j2kun/imsdb_download_all_scripts
#Description: This script can download all latest script from imsdb.com
#======================================================================

#Imports
import os

try:
    from urllib.parse import quote
except IndexError:
    print("quotes package needed!!!!!")
    exit()
try:
    from bs4 import BeautifulSoup
except IndexError:
    print("Beautiful Soup package needed!!!!")
    exit()

try:
    import requests
except IndexError:
    print("requests package needed!!!!")
    exit()

try:
    from tqdm import tqdm as loader
except IndexError:
    print("tqdm package needed!!!!")
    exit()

#Constant defination
BASE_URL = 'http://www.imsdb.com'
ALL_SCRIPT_URL = BASE_URL + '/all%20scripts/'

#Save file with name of title
def save_file(title, script_text):
    path = os.path.join(title.strip('.html')+'.txt')
    with open(path, 'w+') as outfile:
        outfile.write(script_text)

#Filter the scipt by cleaning some unused text 
def clean_script(text):
    text = text.replace('Back to IMSDb', '')
    text = text.replace('''<b><!--
</b>if (window!= top)
top.location.href=location.href
<b>// -->
</b>
''', '')
    text = text.replace('''          Scanned by http://freemoviescripts.com
          Formatting by http://simplyscripts.home.att.net
''', '')
    return text.replace(r'\r', '')

#Parse url response 
def get_response_text(url):
    respose = requests.get(url)
    url_text = respose.text
    soup = BeautifulSoup(url_text, "html.parser")
    return soup

#Filter the soup with text needed 
def soup_find_all(soup, option):
    try:
        if option is 'all_script':
            soup_text = soup.find_all('p')
        elif option is 'movie_page':
            soup_text = soup.find_all('p', align="center")[0].a['href']
        elif option is 'script_page':
            soup_text = soup.find_all('td', {'class': "scrtext"})[0].get_text()
        else:
            return None
    except IndexError:
        return None 
    return soup_text

#Get results from the text response and fetchinh title and script 
def movie_scripts(movie_url):
    movie_url_soup = get_response_text(movie_url)
    script_link = soup_find_all(movie_url_soup, 'movie_page')
    try: 
        if script_link is not None and script_link.endswith('.html'):
            title = script_link.split('/')[-1].split(' Script')[0]
            script_soup = get_response_text(BASE_URL + script_link)
            script_text = soup_find_all(script_soup, 'script_page')
            return title, script_text
        else:
            return None, None 
    except IndexError:
        return None, None

#Main funtion starting from all script page to each movie page getting script
#calculating error file which are unable to fetch
def main_function():
    number_of_file_downloaded = 0
    soup = get_response_text(ALL_SCRIPT_URL)
    paragraphs = soup_find_all(soup, 'all_script')
    for i in loader(range(850, len(paragraphs))):
        #print(each_paragraph, end="\n")
        relative_link = paragraphs[i].a['href']
        each_movie_url = BASE_URL + quote(relative_link)
        title, script = movie_scripts(each_movie_url)
        #print(title)
        if script is not None:
            number_of_file_downloaded += 1
            save_file(title, script)
    print('Error fetching: '+ (int(len(number_of_file_downloaded)) - int(number_of_file_downloaded)))
            
if __name__ == "__main__":
    main_function()
