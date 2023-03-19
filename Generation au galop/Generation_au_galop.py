
import requests
import os


import time
import os

from bs4 import BeautifulSoup
from random import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from PIL import Image




def returnTheWords(sentence):
    words =[]
    for word in sentence:
        if len(word)>2:
            words.append(word)
    return words

def select_words(words):
    wordsToReturn = []
    if len(words) > 2:
        number = randint(0,len(words)-1)
        wordsToReturn.append(words[number])
        words.pop(number)
        number = randint(0,len(words)-1)
        wordsToReturn.append(words[number])
    return wordsToReturn

def make_sentence(words):
    sentence = words[0] +" "+words[1]
    return sentence

def record_images(urls):
    i = 0
    for url in urls:
        i+=1
        if i == 17:
            return i
        
        url = url.strip('\n')
        filename = str(i) + ".jpg"
        try:
            r = requests.get(url, allow_redirects=True)
            open(filename, 'wb').write(r.content)
        except Exception:
            image = Image.new('RGB',(300,200),(250,250,250))
            image.save(filename,"JPEG")


    return i

def create_images(images):


    for i in range(16):
        try:
            images.append(Image.open(str(i+1)+".jpg"))
        except Exception:
            images.append(Image.new('RGB',(300,200),(250,250,250)))

def resize_images(images):
    
    for i in range(16):
        images[i] = images[i].resize((300,200))

def creation_generationAuGalop(images,generationAuGalop):
    
    i=0
    j=0
    k=0
    while(i<16):

        generationAuGalop.paste(images[i],(j,k))
        j+=300
        if(j==1200):
            j=0
            k+=200
        i+=1

def delete_images():
 
    for i in range(16):
        os.remove(str(i+1)+".jpg")


url = "https://www.florian-djambazian.fr"
currentFolder =os.getcwd()

page = requests.get(url)
soup = BeautifulSoup(page.content,'html.parser')
title = str.split(soup.title.string)

words = returnTheWords(title)
print(words)

wordsToSearch =select_words(words)
print(wordsToSearch)

sentence = make_sentence(wordsToSearch)
print(sentence)

print("Ouverture de chrome !")
chrome_options = Options()
#prefs = {'profile.default_content_setting_values.automatic_downloads': 1}
#chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument('headless')
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')
chrome_options.add_argument("download.default_directory=C/:")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer') 
prefs = {'profile.default_content_setting_values.automatic_downloads': 1}
chrome_options.add_experimental_option("prefs", prefs)


driver = webdriver.Chrome(chrome_options = chrome_options)



params = {'behavior': 'allow', 'downloadPath': currentFolder}
driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
driver.get("https://images.google.com/")

time.sleep(1)

consent_button = driver.find_element(by=By.ID,value='L2AGLb')
consent_button.click()

search_bar = driver.find_element(by=By.CLASS_NAME,value="gLFyf")
search_bar.send_keys(sentence)
time.sleep(1)
search_bar.send_keys(Keys.ENTER)
time.sleep(5)

script = """
var urls = [];
var count = 0;
var toReturn;
[...document.querySelectorAll('.rg_i')].forEach((element, index) => {
let el = element.parentElement.parentElement;
el.click();
count++;
setTimeout(() => {
let google_url = el.href;
let start = google_url.indexOf('=' , google_url.indexOf('imgurl'))+1;
let encoded = google_url.substring(start, google_url.indexOf('&', start));
let url = decodeURIComponent(encoded);
urls.push(url);
console.log(count);
console.log(url);
if(--count == 0) {
   let textToSave = urls.join('\\n');
    let hiddenElement = document.createElement('a');
    hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);
    hiddenElement.target = '_blank';
    hiddenElement.download = 'urls.txt';
    hiddenElement.click();
}
}, 50);
});
"""
driver.execute_script(script)
time.sleep(1)
driver.quit



fileUrls = open(currentFolder+r"\urls.txt", "r")
urls = fileUrls.readlines()
fileUrls.close()

os.remove(currentFolder+r"\urls.txt")

print("record images !")
record_images(urls)

images = []

create_images(images)
resize_images(images)
delete_images()

generationAuGalop = Image.new('RGB',(300*4,200*4),(250,250,250))
creation_generationAuGalop(images,generationAuGalop)


generationAuGalop.show()
generationAuGalop.save("generationAuGalop.jpg","JPEG")





