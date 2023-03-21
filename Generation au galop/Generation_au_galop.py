import requests

import time
import os


from bs4 import BeautifulSoup
from random import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from tkinter import * 
from tkinter import messagebox
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
    else:
        wordsToReturn = words
    return wordsToReturn

def make_sentence(words):
    if len(words) > 1:
        sentence = words[0] +" "+words[1]
    else:
        sentence = words
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

def delete_images(urls):

    u=len(urls)
    if u>16:
        u=16

    for i in range(u):
        os.remove(str(i+1)+".jpg")


def changeImageTosablier():
    canvas.itemconfigure(image_container,image = sablier)

def generation():
   
    
    url = text.get()
    canvas.itemconfigure(image_container,image = sablier)
    canvas.update()
    
    try:
        page = requests.get(url)
    except Exception:
        messagebox.showerror("Erreur","There is a connexion problem \nGo to Help menu for more details")
        canvas.itemconfigure(image_container,image = profil)
        canvas.update()
        label.config(text="Try again!")
        label.update()
        return
        

    soup = BeautifulSoup(page.content,'html.parser')
    title = str.split(soup.title.string)
    
    words = returnTheWords(title)

    wordsToSearch =select_words(words)
    print(wordsToSearch)

    sentence = make_sentence(wordsToSearch)
    
    label.config(text="Initialise research")
    label.update()
    canvas.itemconfigure(image_container,image = sablierTurn)
    canvas.update()

    chrome_options = Options()
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

    canvas.itemconfigure(image_container,image = sablier)
    canvas.update()

    params = {'behavior': 'allow', 'downloadPath': currentFolder}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
    driver.get("https://images.google.com/")

    time.sleep(1)

    label.config(text="Research Begin")
    label.update()
    

    consent_button = driver.find_element(by=By.ID,value='L2AGLb')
    consent_button.click()

    search_bar = driver.find_element(by=By.CLASS_NAME,value="gLFyf")
    search_bar.send_keys(sentence)
    time.sleep(1)

    canvas.itemconfigure(image_container,image = sablierTurn)
    canvas.update()

    search_bar.send_keys(Keys.ENTER)
    time.sleep(1)

    canvas.itemconfigure(image_container,image = sablier)
    canvas.update()

    label.config(text="Urls are downloaded")
    label.update()    
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
    canvas.itemconfigure(image_container,image = sablier)
    canvas.update()
    time.sleep(1)
    driver.quit



    fileUrls = open(currentFolder+r"\urls.txt", "r")
    urls = fileUrls.readlines()
    fileUrls.close()

    os.remove(currentFolder+r"\urls.txt")
    label.config(text="Save images")
    label.update()
    canvas.itemconfigure(image_container,image = sablierTurn)
    canvas.update()
    record_images(urls)

    images = []

    create_images(images)
    resize_images(images)
    delete_images(urls)

    generationAuGalop = Image.new('RGB',(300*4,200*4),(250,250,250))
    creation_generationAuGalop(images,generationAuGalop)
   
    label.config(text="Creation of the image : Generation au Galop")
    label.update()
    canvas.itemconfigure(image_container,image = sablier)
    canvas.update()
    generationAuGalop.show()
    generationAuGalop.save("generationAuGalop.jpg","JPEG")

    canvas.itemconfigure(image_container,image = profil)
    canvas.update()
    label.config(text="Finished! The image has been saved")
    label.update()

def generationEvent(event):
    generation()

def Help():
    
    global windowsHelp 
    windowsHelp = Toplevel(fenetre)
    windowsHelp.geometry('800x400')
    global textHelp 
    textHelp = Text(windowsHelp,width=300)

    frameHelp = Frame(windowsHelp)
    frameHelp.pack(side=BOTTOM)

    boutonFrancais = Button(frameHelp, text ='Francais',command =HelpCommandFrancais ,height = 5, width = 10)
    boutonFrancais.pack(side=LEFT)
    boutonEnglish = Button(frameHelp, text ='English',command= HelpCommandEnglish ,height = 5, width = 10)
    boutonEnglish.pack(side=RIGHT)
    

def HelpCommandFrancais():
    fileHelpFrancais = open(currentFolder+r"\Interface\helpFrancais.help", "r", encoding='utf-8')
    helpsFrancais = fileHelpFrancais.read()
    fileHelpFrancais.close()
    textHelp.delete(1.0,"end")
    textHelp.insert(1.0,helpsFrancais)
    textHelp.pack(side = TOP)

def HelpCommandEnglish():
    fileHelpEnglish = open(currentFolder+r"\Interface\helpEnglish.help", "r")
    helpsEnglish = fileHelpEnglish.read()
    fileHelpEnglish.close()
    textHelp.delete(1.0,"end")
    textHelp.insert(1.0,helpsEnglish)
    textHelp.pack(side = TOP)


fenetre = Tk()
fenetre.title("Generation au Galop")
fenetre.geometry("900x300")

currentFolder =os.getcwd()
sablier = PhotoImage(file=currentFolder +r"\Interface\Sablier.gif")
sablierTurn = PhotoImage(file=currentFolder +r"\Interface\SablierTurn.gif")
profil = PhotoImage(file=currentFolder +r"\Interface\Galop.gif")



menubar = Menu(fenetre)

menuFile = Menu(menubar, tearoff=0)
menuFile.add_command(label="Quit", command=fenetre.destroy)
menubar.add_cascade(label="Quit",menu=menuFile) 

menuHelp = Menu(menubar, tearoff=0)
menuHelp.add_command(label="Help", command=Help)
menubar.add_cascade(label="Help",menu=menuHelp) 

fenetre.config(menu=menubar,bg ="white")

frame1 = Frame(fenetre)
frame1.pack(side=LEFT)

canvas = Canvas(frame1,width=309, height=163,bg="white")
image_container = canvas.create_image(0, 0, anchor=NW, image=profil)
canvas.pack(side=TOP, padx=5, pady=5)

saisie = Entry()
label = Label(frame1, text="Enter a website : ",font=("Courier", 20))
label.pack(side=TOP, padx=5, pady=5)


text = Entry(frame1, width=35)
text.pack(side=BOTTOM, padx=5, pady=20)
text.insert(0,"https://www.florian-djambazian.fr/")




frame2 = Frame(fenetre)
frame2.pack(side=RIGHT)

label_border = Frame(frame2, highlightbackground = "black", highlightthickness = 2, bd=0)
label = Label(label_border, text="Welcome",font=("Courier", 15), width = 60)
label.pack(side=TOP, padx=5, pady=5)
label_border.pack(side=TOP, padx=5, pady=31)

bouton_border = Frame(frame2, highlightbackground = "black", highlightthickness = 2, bd=0)
bouton = Button(bouton_border, text ='Generate \nImage',command = generation,height = 5, width = 10, bg ="DarkGoldenrod1",font=("Courier", 12))
bouton.pack(side=BOTTOM, padx=5, pady=5)
bouton_border.pack(side=BOTTOM, padx=5, pady=31)

fenetre.bind("<Return>",generationEvent)

fenetre.mainloop()

