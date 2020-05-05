import pynput
from pynput.mouse import Button, Controller, Listener
import cv2
from bs4 import BeautifulSoup as bs
import requests as rs
import numpy as np
import urllib.request as urllib
import io
from time import sleep


class main():

    def process(self, img):
        ret, thresh4 = cv2.threshold(img, 120, 255, cv2.THRESH_TOZERO) 
        return thresh4
    
    def url_to_img(self, url):
        resp = urllib.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
        image = self.process(image)
        return image

    def get_google_img(self):
        search = 'https://www.google.com/search?q='+self.keyword+'+clipart&tbm=isch&ved=2ahUKEwj3977c_5vpAhXej0sFHfPTDK0Q2-cCegQIABAA&oq=dog+line+dra&gs_lcp=CgNpbWcQARgAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADoECAAQQ1C-A1jsD2CgF2gAcAB4AIABU4gBqwWSAQE5mAEAoAEBqgELZ3dzLXdpei1pbWc&sclient=img&ei=lPqwXvfdK96frtoP86ez6Ao&bih=665&biw=1396&rlz=1C1CHBD_enIN845IN845'
        res = rs.get(search)
        soup = bs(res.text, "html.parser")
        # print(soup)
        images = soup.find_all('img')
        url = ''
        for i in images:
            # print('heeee')
            if i.has_attr('src'):
                if 'http' in i['src']:
                    # print('HEE')
                    if i.has_attr('height'):
                        if int(i['height'])>100:
                            # print('HEEHEE')
                            url = i['src']
                            break
        print(url)
        urllib.urlretrieve(url, "image.png")
        return self.process(cv2.imread("image.png",0))
        
# https://www.google.com/search?q=dog&tbm=isch&chips=q:dog,g_1:drawing:U2qe5YUp82g%3D&rlz=1C1CHBD_enIN845IN845&hl=en&ved=2ahUKEwj3977c_5vpAhXej0sFHfPTDK0Q4lYoC3oECAEQKg&biw=1384&bih=665

    def get_color_pixels(self):
        img = cv2.resize(self.img, (int(self.width/self.pwidth),int(self.height/self.pheight)), interpolation = cv2.INTER_AREA)
        return img
    
    
    
    def draw(self):
        img = self.get_color_pixels()  
        mouse = Controller()
        # print(img.shape)
        sleep(3)
        x = self.startX
        y = self.startY
        mouse.position = (x, y)
        for i in range(len(img)):
            for j in range(len(img[i])):
                if img[i][j]<145:
                    mouse.press(Button.left)
                    if j<(len(img[i])-1):
                        if img[i][j+1]<145:
                            x+=self.pwidth
                            mouse.position = (x,y) 
                            continue
                    sleep(0.1)
                    mouse.release(Button.left)
                    x+=self.pwidth
                    mouse.position = (x,y)  
                else:
                     x+=self.pwidth
                     mouse.position = (x,y)
            x = self.startX
            y+=self.pheight
            mouse.position = (x,y)
        


    def __init__( self ):
        print('Starting...')
        self.startX = 500
        self.startY = 300
        self.height = 200
        self.width = 200
        self.pwidth = 3
        self.pheight = 3
        self.keyword = input('Enter what to draw')
        self.img = self.get_google_img()
        self.draw()
        

        

if __name__ == "__main__":
    main = main()

    