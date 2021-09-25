from __future__ import print_function
import pickle
import os.path
import requests
import time
from PIL import Image
from PIL import UnidentifiedImageError
from requests.exceptions import ConnectionError
from urllib3 import util
import socket
import pickle
import fastbook
fastbook.setup_book()
from fastbook import *
from fastai.vision.widgets import *
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from gtts import gTTS
from gtts import gTTSError

def get_ys(r): 
  return (r.parent.name).split(' ')

learn=load_learner("/home/pi/project_folder/env/lib/python3.7/site-packages/esp32cam/finalized_model10", cpu=True)
dls=['ankur', 'chandan', 'courier', 'dhobi', 'ekam', 'garbage-collector', 'goldy-maam', 'maali', 'meko', 'milk-man', 'mom', 'papa', 'parkash', 'sabji', 'sahil', 'sahil_family', 'sanket', 'swiggy', 'zomato']

print(len(dls))

import pyttsx3
engine = pyttsx3.init() # object creation

""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate
engine.setProperty('rate', 150)     # setting up new voice rate


"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty('voices') #getting details of current voice
#print(voices)
print("voices="+str(len(voices)))#12
engine.setProperty('voice', voices[16].id)  #changing index, changes voices. o for male
#engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

engine.say("Hello World!")
engine.say('My current speaking rate is ' + str(rate))
engine.runAndWait()
engine.stop()

"""Saving Voice to a file"""
# On linux make sure that 'espeak' and 'ffmpeg' are installed
engine.save_to_file('Hello World', 'test.mp3')
engine.runAndWait()
i=1

while(1):
    try:
        #i=1 #remove to save multiple photos in click folder
        #URL = "http://192.168.68.101/capture"
        #location = "capture"
        #PARAMS = {'address':location}
        #r = requests.get(url = URL, params = PARAMS,timeout=5)
        #time.sleep(20)
        response = requests.get("http://192.168.68.101/saved-photo",timeout=5)
        #x = requests.get('https://w3schools.com')
        print(response.status_code)
        
        if response.status_code==200:
            #x = datetime.datetime.now()
            #i=x.strftime("%f")
            op="/home/pi/project_folder/env/lib/python3.7/site-packages/click/ring_"
            file = open(op+str(i)+'.jpg','wb')
            file.write(response.content)
            file.close()    

            img = Image.open(op+str(i)+'.jpg')
            print(op+str(i)+'.jpg')
            if img.format=='JPEG':
                #feedback=upload(f'ring_{i}.jpg')
                #time.sleep(3)
                #print(feedback)
                os.system("rm -rf /var/www/html/*.jpg")
                img.save(f'/var/www/html/myphoto{i}.jpg', 'JPEG')
                predsi,_,vals=learn.predict(tensor(np.array(PILImage.create(op+str(i)+'.jpg').to_thumb(224))))
                #img.save('/home/pi/Desktop/myphoto.jpg', 'JPEG')
                for j in torch.where(vals>0.75):
                    a=array(j)
                b=""
                for j in a:
                    print(dls[j],"\t\t",array(vals[j]))
                    b=b+dls[j]+" "
                print(b)
                i=i+1
                #Path("/var/www/html/bell.mp3").unlink()
                if b:
                    language = 'en'
                    myobj = gTTS(text="bahaar"+b+"hai", lang=language, slow=False)
                    
                    myobj.save("/var/www/html/bell.mp3")
                    os.system("mpg321 /var/www/html/bell.mp3")
                    os.system("rm -rf /var/www/html/*.jpg")
                    img.save(f'/var/www/html/myphoto{i}_{b}.jpg', 'JPEG')
            response = requests.get("http://192.168.68.101/delete?delete_photo=true",timeout=5)
            if str(response.status_code)=='200':
                print("Memory made for new image")
        else:
            print("Bell not ringed")
            time.sleep(3)
            
    except UnidentifiedImageError:
        continue;
    except requests.exceptions.ReadTimeout:
        print("read out error")
        continue;
    except requests.ConnectTimeout:
        print("Connect timeout error")
        time.sleep(3)
        continue;
    except ConnectionError as e:    # This is the correct syntax
        print("hello")
        r = "No response"
        time.sleep(3)
        continue;
    except socket.timeout as err:
        print("socket error retrying")
        time.sleep(3)
        continue;
    except gTTSError as err:
        print("internet not reachable")
        engine.say(b+"is outside")
        engine.runAndWait()
        engine.stop()
        time.sleep(3)
        continue;