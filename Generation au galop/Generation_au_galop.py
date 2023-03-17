from logging import exception
from xml.etree.ElementTree import tostring
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
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
    
         


    return i

urltest = "https://www.florian-djambazian.fr"
url ="https://www.1538mediterranee.com/"
page = requests.get(url)
soup = BeautifulSoup(page.content,'html.parser')
title = str.split(soup.title.string)

words = returnTheWords(title)
print(words)

wordsToSearch =select_words(words)
print(wordsToSearch)

sentence = make_sentence(wordsToSearch)
print(sentence)

chrome_options = Options()
#chrome_options.add_argument("--headless")
prefs = {'profile.default_content_setting_values.automatic_downloads': 1}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')
chrome_options.add_experimental_option("prefs", {
        "download.default_directory": "c:/",
        "download.prompt_for_download": True,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
})
#chrome_options.add_argument('--disable-gpu')
#chrome_options.add_argument('--disable-software-rasterizer')
prefs = {'profile.default_content_setting_values.automatic_downloads': 1}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(executable_path = 'C:/Users/Flordjam/Downloads/chromedriver.exe' ,chrome_options = chrome_options)
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
driver.quit()

fileUrls = open("C:/Users/Flordjam/Downloads/urls.txt", "r")

urls = fileUrls.readlines()
print(urls)
fileUrls.close()

os.remove("C:/Users/Flordjam/Downloads/urls.txt")

record_images(urls)

image1 = Image.open("1.jpg")
image2 = Image.open("2.jpg")
image3 = Image.open("3.jpg")
image4 = Image.open("4.jpg")
image5 = Image.open("5.jpg")
image6 = Image.open("6.jpg")
image7 = Image.open("7.jpg")
image8 = Image.open("8.jpg")
image9 = Image.open("9.jpg")
image10 = Image.open("10.jpg")
image11 = Image.open("11.jpg")
image12 = Image.open("12.jpg")
image13 = Image.open("13.jpg")
image14 = Image.open("14.jpg")
image15 = Image.open("15.jpg")
image16 = Image.open("16.jpg")

image1 = image1.resize((300,200))
image2 =image2.resize(((300,200)))
image3 =image3.resize((300,200))
image4 =image4.resize((300,200))
image5 =image5.resize((300,200))
image6 =image6.resize((300,200))
image7 =image7.resize((300,200))
image8 =image8.resize((300,200))
image9 =image9.resize((300,200))
image10 =image10.resize((300,200))
image11 =image11.resize((300,200))
image12 =image12.resize((300,200))
image13 =image13.resize((300,200))
image14 =image14.resize((300,200))
image15 =image15.resize((300,200))
image16 =image16.resize((300,200))



generationAuGalop = Image.new('RGB',(300*4,200*4),(250,250,250))

generationAuGalop.paste(image1,(0,0))
generationAuGalop.paste(image2,(300,0))
generationAuGalop.paste(image3,(600,0))
generationAuGalop.paste(image4,(900,0))

generationAuGalop.paste(image5,(0,200))
generationAuGalop.paste(image6,(300,200))
generationAuGalop.paste(image7,(600,200))
generationAuGalop.paste(image8,(900,200))
   
generationAuGalop.paste(image9,(0,400))
generationAuGalop.paste(image10,(300,400))
generationAuGalop.paste(image11,(600,400))
generationAuGalop.paste(image12,(900,400))

generationAuGalop.paste(image13,(0,600))
generationAuGalop.paste(image14,(300,600))
generationAuGalop.paste(image15,(600,600))
generationAuGalop.paste(image16,(900,600))

generationAuGalop.show()
generationAuGalop.save("generationAuGalop.jpg","JPEG")





