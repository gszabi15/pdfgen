import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil import BlobMedia
import anvil.media
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
import json
import binascii
@anvil.server.callable
def retgenpdf(data,name):
      instance = genpdf(data)
      return instance(name)
class genpdf:
    def __init__(self, data:dict):
        self.kepz = 0
        print(dir(anvil.media))
        self.url1 = BytesIO(anvil.URLMedia(anvil.server.get_app_origin() + "/_/theme/karakterlap1.jpg").get_bytes())
        #asd = anvil.media.open("karakterlap1.jpg")
        self.url2 = BytesIO(anvil.URLMedia(anvil.server.get_app_origin() + "/_/theme/karakterlap2.jpg").get_bytes())
        
        self.lap = [Image.open(self.encode_text_in_image(json.dumps(data))).convert("RGB"), Image.open(self.url2)]
        self.editlap = []
        print(data)
        for x in list(data.keys()):
                elap = None
                self.editlap += [self.lap[0].copy()]
                self.editlap += [self.lap[1].copy()]
                elap = ImageDraw.Draw(self.editlap[(list(data.keys()).index(x))*2])

                self.alap(elap, data[x]['alap'])
                self.stat(elap, data[x]['stat'])
                self.szazalek(elap, data[x]['szazalek'])
                self.elony(elap, data[x]['elony'])
                self.hatrany(elap, data[x]['hatrany'])
                self.varazstargyak(elap, data[x]['varazstargyak'])
                self.fegyver_nelkuli(elap, data[x]['fegyver_nelkuli'])
                #for z in range(len(data[x]["fegyver1"]) if len(data[x]["fegyver1"]) < 4 else 3):
                #    self.fegyver(elap,z+1,data[x]["fegyver1"][z])
                for z in range(len(data[x]["fegyver"]) if len(data[x]["fegyver"]) < 4 else 3):
                    self.fegyver(elap, z+1, data[x]["fegyver"][z])

                self.pszi(elap, data[x]["pszi"])
                self.varazsero(elap, data[x]["varazsero"])
                self.vert(elap, data[x]["vert"])
                    
                elap = ImageDraw.Draw(self.editlap[(list(data.keys()).index(x)+1)*2-1])
                self.levonasok(elap, data[x]['levonasok'])
                self.penz(elap, data[x]['penz'])
                self.nyelv(elap, data[x]['nyelv'])
                self.felszereles(elap, data[x]['felszereles'])
                self.kepzettseg(elap, data[x]['kepzettseg'])
                self.mergek(elap, data[x]['mergek'])
                self.tarsak(elap, data[x]['tarsak'])
                self.talalkozok(elap, data[x]['talalkozok'])
                self.tp(elap, str(data[x]['tp']))
                #for z in range(len(data[x]["fegyver2"]) if len(data[x]["fegyver2"]) < 3 else 2):
                #    self.fegyver(elap, z+4, data[x]['fegyver2'][z])
                if len(data[x]["fegyver"]) > 3:
                    if len(data[x]["fegyver"]) >= 4:
                        self.fegyver(elap, 4, data[x]['fegyver'][3])
                    if len(data[x]["fegyver"]) >= 5:
                        self.fegyver(elap, 5, data[x]['fegyver'][4])
                self.zsakmany(elap, data[x]['zsakmany'])
    def encode_text_in_image(self, text):
      img = Image.open(self.url1)
      if img.mode != 'RGB':
          img = img.convert('RGB')
      
      # Convert text to binary and add a delimiter to indicate the end of text
      binary_text = ''.join(format(ord(char), '08b') for char in text) + '1111111111111110'
      binary_iter = iter(binary_text)
      
      # Encode text into the image
      pixels = list(img.getdata())
      new_pixels = []
      
      for pixel in pixels:
          new_pixel = []
          for value in pixel:
              try:
                  bit = next(binary_iter)
                  new_value = (value & ~1) | int(bit)  # Modify the LSB
              except StopIteration:
                  new_value = value  # No more bits to encode, keep the pixel unchanged
              new_pixel.append(new_value)
          new_pixels.append(tuple(new_pixel))
      
      # Create a new image with modified pixels
      img.putdata(new_pixels)
      img_save = BytesIO()
      img.save(img_save, format="JPEG")
      img_save.seek(0)
      return img_save
    def __call__(self, filename):
      pdf_bytes = BytesIO()
      self.editlap[0].save(pdf_bytes,  format="PDF", save_all=True, append_images=self.editlap[1:],quality=100, subsampling=0)
      pdf_bytes.seek(0)
      
      return BlobMedia("application/pdf", pdf_bytes.read(), name=filename+".pdf")
    def font(self, size: int, bold=False):
        if bold:
            return ImageFont.truetype('DejaVuSans-Bold.ttf', size)
        else:
            return ImageFont.truetype('DejaVuSans.ttf', size)
    def getsize(self, text:str, size:int, bold=False):
        l,t,r,b = self.font(size,bold).getbbox(str(text))
        return (r-l, b-t)
    def wtext(self, edit, x, y,text, size=16, bold = False, max=0):
        if text == None:
          text = ''
        if max == 0:
            edit.text((x,y-size-1),str(text),(0, 0, 0), self.font(size,bold))
        else:
            size2 = size
            while 1:
                w = self.getsize(text,size2,bold)[0]
                if w < max:
                    break
                else:
                    size2 -= 1
            edit.text((x,y-size2-1),text,(0, 0, 0), self.font(size2,bold))
    def wchtext(self, edit, x, y,text, size=16,bold=False):
        if text == None:
          text = ''
        w,h = self.getsize(str(text),size,bold)
        self.wtext(edit, x, y+h/2, str(text), size, bold)
    def wcwtext(self, edit, x, y,text, size=16,bold=False):
        if text == None:
          text = ''
        w,h = self.getsize(str(text),size,bold)
        self.wtext(edit, x-w/2, y, str(text), size, bold)
    def wcatext(self, edit, x, y,text, size=16,bold=False):
        if text == None:
          text = ''
        w,h = self.getsize(str(text),size,bold)
        self.wtext(edit, x-w/2, y+h/2, str(text), size, bold)
    def wcircle(self, edit, x,y):
        edit.ellipse((x-11, y-11, x+11, y+11), outline ='black', width=3)

    def alap(self, edit, text=["","","","","","","","","","","","","","","",""]): #nev,kor,kaszt,faj,vallas,szarmazas,csillagjegy,rend,rang,csapat,falka,jemondat1,jelmondat2,szint,jellem1,jellem2
        if text != []:
            self.wchtext(edit, 132/724*1225,50/1024*1732+1,text[0], 25, True)

            self.wtext(edit, 76/724*1225+2,82/1024*1732+1,text[1], 16)
            self.wtext(edit, 90/724*1225+2,105/1024*1732,text[2], 16)
            self.wtext(edit, 73/724*1225+1,128/1024*1732+2,text[3], 16)
            self.wtext(edit, 91/724*1225+2,151/1024*1732+1,text[4], 16)
            self.wtext(edit, 127/724*1225+2,174/1024*1732+1,text[5], 16)
            self.wtext(edit, 120/724*1225+1,197/1024*1732,text[6], 16)

            self.wtext(edit, 344/724*1225+2,81/1024*1732+1,text[7], 16)
            self.wtext(edit, 304/724*1225+2,103/1024*1732+2,text[8], 16)
            self.wtext(edit, 316/724*1225+1,126/1024*1732+2,text[9], 16)
            self.wtext(edit, 306/724*1225+1,149/1024*1732+1,text[10], 16)
            self.wtext(edit, 338/724*1225+1,172/1024*1732+1,text[11], 16)
            self.wtext(edit, 259/724*1225+1,196/1024*1732+1,text[12], 16)

            self.wcatext(edit, 69/724*1225+1,264/1024*1732,text[13],30, True) #szint
            if text[15] != "":
                self.wchtext(edit, 432/724*1225,252/1024*1732,text[14]+",",23) #jellem
                self.wchtext(edit, 432/724*1225,274/1024*1732,text[15],23) #jellem
            else:
                self.wchtext(edit, 432/724*1225,252/1024*1732,text[14],23)

    def elony(self, edit, text=["","","","",""]):
        if text != []:
            self.wtext(edit, 62/724*1225-1,(784+26*0)/1024*1732+2,text[0], 16, False, 316)
            self.wtext(edit, 62/724*1225-1,(784+26*1)/1024*1732+1,text[1], 16, False, 316)
            self.wtext(edit, 62/724*1225-1,(784+26*2)/1024*1732+2,text[2], 16, False, 316)
            self.wtext(edit, 62/724*1225-1,(784+26*3)/1024*1732+1,text[3], 16, False, 316)
            self.wtext(edit, 62/724*1225-1,(784+26*4)/1024*1732+1,text[4], 16, False, 316)

    def hatrany(self, edit, text=["","","","",""]):
        if text != []:
            self.wtext(edit, 269/724*1225,(784+26*0)/1024*1732+2,text[0], 16, False, 316)
            self.wtext(edit, 269/724*1225,(784+26*1)/1024*1732+1,text[1], 16, False, 316)
            self.wtext(edit, 269/724*1225,(784+26*2)/1024*1732+2,text[2], 16, False, 316)
            self.wtext(edit, 269/724*1225,(784+26*3)/1024*1732+1,text[3], 16, False, 316)
            self.wtext(edit, 269/724*1225,(784+26*4)/1024*1732+1,text[4], 16, False, 316)

    #xy=(509, 90) fegyver1
    #xy=(509,228) fegyver2
    #xy=(509,366) fegyver3
    #xy=(59,1459)
    def fegyver(self, edit, index: int,text=["","","","","","","", False, False]): #edit, fegyver index, nev,ke,te,ve,tam,sabzes,pajzs,magikus,aldott
        xy = (509,366)
        if index == 1:
            xy = (509, 90)
        elif index == 2:
            xy = (509,228)
        elif index == 3:
            xy = (509,366)
        elif index == 4:
            xy = (59/1225*724,1459/1732*1024)
        elif index == 5:
            xy = (380/1225*724,1459/1732*1024)
        x = 0
        y = 0
        z = 0
        if index < 3:
            y = index
        elif index == 3:
            y = index -1
        elif index > 3:
            y = 1
        self.wtext(edit, (xy[0]+63)/724*1225+2,(xy[1]+18)/1024*1732-1+y,text[0],18, False, 188)
        y = 0
        if index == 2:
            y = -1
        elif index == 4 or index == 5:
            y = -2
            z = -1
        self.wcatext(edit, (xy[0]+32)/724*1225, (xy[1]+51)/1024*1732+1+y,text[1])
        self.wcatext(edit, (xy[0]+93)/724*1225, (xy[1]+51)/1024*1732+1+y,text[2])
        self.wcatext(edit, (xy[0]+152)/724*1225, (xy[1]+51)/1024*1732+1+y,text[3])
        self.wcatext(edit, (xy[0]+32)/724*1225, (xy[1]+86)/1024*1732+z,text[4])
        self.wcatext(edit, (xy[0]+123)/724*1225, (xy[1]+86)/1024*1732+z,text[5])
        self.wcatext(edit, (xy[0]+123)/724*1225, (xy[1]+121)/1024*1732+z,text[6])
        
        if text[7]:
            if index > 1:
                y = 1
            if index == 4:
                y = 0
                x = -1
            if index == 5:
                y = 0
            self.wtext(edit,(xy[0]+7)/724*1225+2+x,(xy[1]+108)/1024*1732-1+y,"x",15)
            y = 0
            x = 0
        if text[8]:
            if index == 3:
                y = 1
            if index == 4:
                y = -1
                x = -1
            self.wtext(edit,(xy[0]+7)/724*1225+2+x,(xy[1]+122)/1024*1732+1+y,"x",15)
            y = 0
            x = 0
    #/724*1225 /1024*1732
    def varazstargyak(self, edit, text=[["","","",""],["","","",""],["","","",""],["","","",""]]):
        # if len(text) > 0:
        #     self.wtext(edit, 28/724*1225, 938/1024*1732,text[0][0], 16, False, 365)
        #     self.wtext(edit, 28/724*1225, 957/1024*1732+1,text[0][1], 16, False, 365)
        #     self.wtext(edit, 28/724*1225, 977/1024*1732+2,text[0][2], 16, False, 365)
        #     self.wtext(edit, 28/724*1225, 996/1024*1732+1,text[0][3], 16, False, 365)
        # if len(text) > 1:
        #     self.wtext(edit, 248/724*1225-1, 938/1024*1732,text[1][0], 16, False, 299)
        #     self.wtext(edit, 248/724*1225-1, 957/1024*1732+1,text[1][1], 16, False, 299)
        #     self.wtext(edit, 248/724*1225-1, 977/1024*1732+2,text[1][2], 16, False, 299)
        #     self.wtext(edit, 248/724*1225-1, 996/1024*1732+1,text[1][3], 16, False, 299)
        # if len(text) > 2:
        #     self.wcwtext(edit, 444/724*1225+1, 938/1024*1732,text[2][0])
        #     self.wcwtext(edit, 444/724*1225+1, 957/1024*1732+1,text[2][1])
        #     self.wcwtext(edit, 444/724*1225+1, 977/1024*1732+2,text[2][2])
        #     self.wcwtext(edit, 444/724*1225+1, 996/1024*1732+1,text[2][3])
        # if len(text) > 3:
        #     self.wcwtext(edit, 477/724*1225+1, 938/1024*1732,text[3][0])
        #     self.wcwtext(edit, 477/724*1225+1, 957/1024*1732+1,text[3][1])
        #     self.wcwtext(edit, 477/724*1225+1, 977/1024*1732+2,text[3][2])
        #     self.wcwtext(edit, 477/724*1225+1, 996/1024*1732+1,text[3][3])

        if len(text) > 0:
            self.wtext(edit, 28/724*1225, 938/1024*1732,text[0][0], 16, False, 365)
            self.wtext(edit, 248/724*1225-1, 938/1024*1732,text[0][1], 16, False, 299)
            self.wcwtext(edit, 477/724*1225+1, 938/1024*1732,text[0][2])
            self.wcwtext(edit, 444/724*1225+1, 938/1024*1732,text[0][3])
            
        if len(text) > 1:
            self.wtext(edit, 28/724*1225, 957/1024*1732+1,text[1][0], 16, False, 365)
            self.wtext(edit, 248/724*1225-1, 957/1024*1732+1,text[1][1], 16, False, 299)
            self.wcwtext(edit, 477/724*1225+1, 957/1024*1732+1,text[1][2])
            self.wcwtext(edit, 444/724*1225+1, 957/1024*1732+1,text[1][3])
            
        if len(text) > 2:
            self.wtext(edit, 28/724*1225, 977/1024*1732+2,text[2][0], 16, False, 365)
            self.wtext(edit, 248/724*1225-1, 977/1024*1732+2,text[2][1], 16, False, 299)
            self.wcwtext(edit, 477/724*1225+1, 977/1024*1732+2,text[2][2])
            self.wcwtext(edit, 444/724*1225+1, 977/1024*1732+2,text[2][3])
            
        if len(text) > 3:
            self.wtext(edit, 28/724*1225, 996/1024*1732+1,text[3][0], 16, False, 365)
            self.wtext(edit, 248/724*1225-1, 996/1024*1732+1,text[3][1], 16, False, 299)
            self.wcwtext(edit, 477/724*1225+1, 996/1024*1732+1,text[3][2])
            self.wcwtext(edit, 444/724*1225+1, 996/1024*1732+1,text[3][3])

    def fegyver_nelkuli(self, edit, text=["","","",""]): #ke,te,ve,ce
        if text != []:
            self.wcwtext(edit, 540/724*1225, 72/1024*1732-2,text[0],20)
            self.wcwtext(edit, 583/724*1225, 72/1024*1732-2,text[1],20)
            self.wcwtext(edit, 626/724*1225, 72/1024*1732-2,text[2],20)
            self.wcwtext(edit, 669/724*1225, 72/1024*1732-2,text[3],20)

    def szazalek(self, edit, text=["","","","","","","","","",""]): #ugras,eses,maszas,zsebmetszes,zarnyitas,rejtozes,koteltanc,lopozas,titkosajto kereses, csapdafelfedezes
        if text != []:
            self.wcatext(edit, 51/724*1225+1,719/1024*1732-2,text[0],20)
            self.wcatext(edit, 112/724*1225+1,719/1024*1732-2,text[1],20)
            self.wcatext(edit, 172/724*1225+1,719/1024*1732-2,text[2],20)
            self.wcatext(edit, 233/724*1225+1,719/1024*1732-2,text[3],20)
            self.wcatext(edit, 293/724*1225+2,719/1024*1732-2,text[4],20)
            self.wcatext(edit, 354/724*1225+1,719/1024*1732-2,text[5],20)
            self.wcatext(edit, 414/724*1225+1,719/1024*1732-2,text[6],20)
            self.wcatext(edit, 475/724*1225,719/1024*1732-2,text[7],20)
            self.wcatext(edit, 77/724*1225+1,658/1024*1732,text[8],20)
            self.wcatext(edit, 449/724*1225,658/1024*1732,text[9],20)

    #lap = [Image.open("karakterlap1.jpg").convert('RGB'),Image.open("karakterlap2.jpg").convert('RGB')]

    def pszi(self, edit, text=["","","","","","","","","", False,False,False,False,False,False]): # pszi,asztral termeszetes, asztral statikus, asztral dinamikus, asztral ME, mental termeszetes, mental statikus, mental dinamikus, manetal ME, diszciplinak AF, diszciplinak MF, Pyarroni, Slan, Kyr, Siopa
        if text != []:
            self.wcatext(edit, 656/724*1225 ,590/1024*1732,text[0],20)
            for x in range(4):
                y = 0
                if x == 0 or x == 4:
                    y = 3
                elif x == 1 or x == 5:
                    y = 2
                self.wcatext(edit,612/724*1225,(647+19*x)/1024*1732+y,text[x+1],17)
                self.wcatext(edit,666/724*1225,(647+19*x)/1024*1732+y,text[x+5],17)
            if text[9]:
                self.wcwtext(edit,612/724*1225+5,552/1024*1732,"x",15)
            if text[10]:
                self.wcwtext(edit,648/724*1225+5,552/1024*1732,"x",15)
            if text[11]:
                self.wcwtext(edit,508/724*1225+5,578/1024*1732,"x",15)
            if text[12]:
                self.wcwtext(edit,575/724*1225+6,578/1024*1732,"x",15)
            if text[13]:
                self.wcwtext(edit,508/724*1225+5,602/1024*1732,"x",15)
            if text[14]:
                self.wcwtext(edit,577/724*1225+5,602/1024*1732,"x",15)

    def varazsero(self, edit, text=["","","",False,False,False,False]): #mana,od,verpont,elet,lelek,termeszet,halal
        if text != []:
            self.wcatext(edit,561/724*1225,786/1024*1732-2,text[0],20)
            self.wcatext(edit,648/724*1225,790/1024*1732-1,text[1],18)
            self.wcatext(edit,648/724*1225,844/1024*1732,text[2],18)
            if text[3]:
                self.wtext(edit, 533/724*1225+1,809/1024*1732,"x",15)
            if text[4]:
                self.wtext(edit, 533/724*1225,822/1024*1732+1,"x",15)
            if text[5]:
                self.wtext(edit, 533/724*1225,835/1024*1732+2,"x",15)
            if text[6]:
                self.wtext(edit, 533/724*1225,849/1024*1732,"x",15)

    def vert(self, edit, text=["","","","",False,False]): #vert, ep, fp, sfe, mgt, af, mf
        if text != []:
            self.wtext(edit, 570/724*1225+2,915/1024*1732-1,text[0],17, False, 200)
            self.wcatext(edit, 535/724*1225,929/1024*1732,text[1],23)
            self.wcatext(edit, 674/724*1225,969/1024*1732,text[2],23)
            self.wcatext(edit, 561/724*1225,977/1024*1732,text[3],23)
            self.wcatext(edit, 613/724*1225,977/1024*1732,text[4],23)
            if text[5]:
                self.wtext(edit, 571/724*1225+2,931/1024*1732,"x",15)
            if text[6]:
                self.wtext(edit, 604/724*1225+1,931/1024*1732,"x",15)
    #/724*1225 /1024*1732

    def stat(self, edit, stat=[10,10,10,10,10,10,10,10,10,10]):
        if stat != []:
            #ero
            {
            18: lambda: self.wcircle(edit, 207/724*1225+1,293/1024*1732+2),
            17: lambda: self.wcircle(edit, 212/724*1225+1,309/1024*1732+2),
            16: lambda: self.wcircle(edit, 217/724*1225+1,326/1024*1732+1),
            15: lambda: self.wcircle(edit, 222/724*1225+1,342/1024*1732+3),
            14: lambda: self.wcircle(edit, 227/724*1225+1,359/1024*1732+1),
            13: lambda: self.wcircle(edit, 232/724*1225+1,375/1024*1732+2),
            12: lambda: self.wcircle(edit, 237/724*1225+1,392/1024*1732+1),
            11: lambda: self.wcircle(edit, 242/724*1225+1,409/1024*1732+1),
            10: lambda: self.wcircle(edit, 247/724*1225+1,425/1024*1732+2)
            }[stat[0]]() if 19>stat[0]>9 else []
            #gyorsasag
            {
            18: lambda: self.wcircle(edit, 315/724*1225+2,294/1024*1732),
            17: lambda: self.wcircle(edit, 310/724*1225+1,310/1024*1732+1),
            16: lambda: self.wcircle(edit, 305/724*1225,326/1024*1732+2),
            15: lambda: self.wcircle(edit, 299/724*1225+2,343/1024*1732+1),
            14: lambda: self.wcircle(edit, 294/724*1225+1,359/1024*1732+1),
            13: lambda: self.wcircle(edit, 289/724*1225+1,375/1024*1732+2),
            12: lambda: self.wcircle(edit, 283/724*1225+3,392/1024*1732+1),
            11: lambda: self.wcircle(edit, 278/724*1225+1,408/1024*1732+1),
            10: lambda: self.wcircle(edit, 273/724*1225+1,425/1024*1732+1)
            }[stat[1]]() if 19>stat[1]>9 else []
            #ugyesseg
            {
            18: lambda: self.wcircle(edit, 405/724*1225,360/1024*1732+1),
            17: lambda: self.wcircle(edit, 391/724*1225,370/1024*1732+1),
            16: lambda: self.wcircle(edit, 377/724*1225+1,380/1024*1732+1),
            15: lambda: self.wcircle(edit, 363/724*1225,390/1024*1732+1),
            14: lambda: self.wcircle(edit, 349/724*1225+1,400/1024*1732+1),
            13: lambda: self.wcircle(edit, 335/724*1225+1,410/1024*1732+1),
            12: lambda: self.wcircle(edit, 321/724*1225,420/1024*1732+1),
            11: lambda: self.wcircle(edit, 307/724*1225,430/1024*1732+1),
            10: lambda: self.wcircle(edit, 292/724*1225+2,440/1024*1732+1)
            }[stat[2]]() if 19>stat[2]>9 else []
            #allokepesseg
            {
            18: lambda: self.wcircle(edit, 439/724*1225,468/1024*1732),
            17: lambda: self.wcircle(edit, 422/724*1225,468/1024*1732),
            16: lambda: self.wcircle(edit, 404/724*1225+1,468/1024*1732),
            15: lambda: self.wcircle(edit, 387/724*1225+1,468/1024*1732),
            14: lambda: self.wcircle(edit, 370/724*1225,468/1024*1732),
            13: lambda: self.wcircle(edit, 353/724*1225+1,468/1024*1732),
            12: lambda: self.wcircle(edit, 335/724*1225+2,468/1024*1732),
            11: lambda: self.wcircle(edit, 318/724*1225+2,468/1024*1732),
            10: lambda: self.wcircle(edit, 301/724*1225+1,468/1024*1732)
            }[stat[3]]() if 19>stat[3]>9 else []
            #egeszseg
            {
            18: lambda: self.wcircle(edit, 404/724*1225,575/1024*1732+2),
            17: lambda: self.wcircle(edit, 390/724*1225+1,565/1024*1732+1),
            16: lambda: self.wcircle(edit, 376/724*1225,555/1024*1732+1),
            15: lambda: self.wcircle(edit, 362/724*1225+1,545/1024*1732),
            14: lambda: self.wcircle(edit, 348/724*1225+2,534/1024*1732+1),
            13: lambda: self.wcircle(edit, 334/724*1225+2,524/1024*1732+1),
            12: lambda: self.wcircle(edit, 320/724*1225+2,514/1024*1732+1),
            11: lambda: self.wcircle(edit, 307/724*1225+1,503/1024*1732+2),
            10: lambda: self.wcircle(edit, 293/724*1225+1,494/1024*1732)
            }[stat[4]]() if 19>stat[4]>9 else []
            #szepseg
            {
            18: lambda: self.wcircle(edit, 313/724*1225+1,638/1024*1732+2),
            17: lambda: self.wcircle(edit, 308/724*1225,622/1024*1732+1),
            16: lambda: self.wcircle(edit, 302/724*1225+2,606/1024*1732+1),
            15: lambda: self.wcircle(edit, 297/724*1225+1,589/1024*1732+1),
            14: lambda: self.wcircle(edit, 292/724*1225,573/1024*1732+1),
            13: lambda: self.wcircle(edit, 287/724*1225+1,556/1024*1732+2),
            12: lambda: self.wcircle(edit, 281/724*1225+2,540/1024*1732+1),
            11: lambda: self.wcircle(edit, 276/724*1225+2,524/1024*1732+1),
            10: lambda: self.wcircle(edit, 271/724*1225,507/1024*1732+2)
            }[stat[5]]() if 19>stat[5]>9 else []
            #inteligencia
            {
            18: lambda: self.wcircle(edit, 204/724*1225,639/1024*1732+1),
            17: lambda: self.wcircle(edit, 209/724*1225+1,623/1024*1732+1),
            16: lambda: self.wcircle(edit, 214/724*1225,606/1024*1732+2),
            15: lambda: self.wcircle(edit, 219/724*1225+2,590/1024*1732+1),
            14: lambda: self.wcircle(edit, 224/724*1225+2,573/1024*1732+2),
            13: lambda: self.wcircle(edit, 230/724*1225+1,557/1024*1732),
            12: lambda: self.wcircle(edit, 235/724*1225+2,540/1024*1732+1),
            11: lambda: self.wcircle(edit, 240/724*1225+1,524/1024*1732+1),
            10: lambda: self.wcircle(edit, 245/724*1225+1,507/1024*1732+2)
            }[stat[6]]() if 19>stat[6]>9 else []
            #akaratero
            {
            18: lambda: self.wcircle(edit, 112/724*1225+1,572/1024*1732),
            17: lambda: self.wcircle(edit, 126/724*1225,561/1024*1732+3),
            16: lambda: self.wcircle(edit, 140/724*1225+1,551/1024*1732+1),
            15: lambda: self.wcircle(edit, 154/724*1225,541/1024*1732),
            14: lambda: self.wcircle(edit, 167/724*1225+1,530/1024*1732+2),
            13: lambda: self.wcircle(edit, 181/724*1225+1,520/1024*1732+2),
            12: lambda: self.wcircle(edit, 195/724*1225+1,510/1024*1732+1),
            11: lambda: self.wcircle(edit, 209/724*1225+1,500/1024*1732+1),
            10: lambda: self.wcircle(edit, 223/724*1225+1,490/1024*1732+1)
            }[stat[7]]() if 19>stat[7]>9 else []
            #asztral
            {
            18: lambda: self.wcircle(edit, 78/724*1225+2,465/1024*1732),
            17: lambda: self.wcircle(edit, 95/724*1225+1,465/1024*1732),
            16: lambda: self.wcircle(edit, 113/724*1225,465/1024*1732),
            15: lambda: self.wcircle(edit, 130/724*1225+1,465/1024*1732),
            14: lambda: self.wcircle(edit, 147/724*1225+1,465/1024*1732),
            13: lambda: self.wcircle(edit, 164/724*1225+1,465/1024*1732),
            12: lambda: self.wcircle(edit, 182/724*1225+1,465/1024*1732),
            11: lambda: self.wcircle(edit, 199/724*1225,465/1024*1732),
            10: lambda: self.wcircle(edit, 216/724*1225+1,465/1024*1732)
            }[stat[8]]() if 19>stat[8]>9 else []
            #eszleles
            {
            18: lambda: self.wcircle(edit, 114/724*1225+2,357/1024*1732+2),
            17: lambda: self.wcircle(edit, 128/724*1225+1,368/1024*1732),
            16: lambda: self.wcircle(edit, 142/724*1225+1,378/1024*1732),
            15: lambda: self.wcircle(edit, 156/724*1225+1,388/1024*1732+1),
            14: lambda: self.wcircle(edit, 170/724*1225+1,398/1024*1732+1),
            13: lambda: self.wcircle(edit, 184/724*1225+1,408/1024*1732+1),
            12: lambda: self.wcircle(edit, 198/724*1225,418/1024*1732+1),
            11: lambda: self.wcircle(edit, 212/724*1225,429/1024*1732+1),
            10: lambda: self.wcircle(edit, 226/724*1225+1,439/1024*1732+1)
            }[stat[9]]() if 19>stat[9]>9 else []

            for x in range(10):
                if stat[x] != 0 and stat[x] <10:
                    [
                    lambda: self.wcatext(edit,250/724*1225,443/1024*1732,str(stat[x]),17,True), #ero
                    lambda: self.wcatext(edit,267/724*1225,443/1024*1732,str(stat[x]),17,True), #gyors
                    lambda: self.wcatext(edit,280/724*1225,452/1024*1732,str(stat[x]),17,True), #ugyesseg
                    lambda: self.wcatext(edit,285/724*1225,469/1024*1732,str(stat[x]),17,True), # all
                    lambda: self.wcatext(edit,280/724*1225,483/1024*1732,str(stat[x]),17,True), #egeszseg
                    lambda: self.wcatext(edit,267/724*1225,492/1024*1732,str(stat[x]),17,True), #szepseg
                    lambda: self.wcatext(edit,250/724*1225,492/1024*1732,str(stat[x]),17,True), #int
                    lambda: self.wcatext(edit,238/724*1225,483/1024*1732,str(stat[x]),17,True), #akarat
                    lambda: self.wcatext(edit,233/724*1225,467/1024*1732,str(stat[x]),17,True), #asztral 
                    lambda: self.wcatext(edit,238/724*1225,452/1024*1732,str(stat[x]),17,True) #eszleles
                    ][x]()
                elif stat[x] > 18:
                    [
                    lambda: self.wcatext(edit,203/724*1225,278/1024*1732,str(stat[x]),17,True), #ero
                    lambda: self.wcatext(edit,320/724*1225,279/1024*1732,str(stat[x]),17,True), #gyors
                    lambda: self.wcatext(edit,420/724*1225,352/1024*1732,str(stat[x]),17,True), #ugy
                    lambda: self.wcatext(edit,457/724*1225,469/1024*1732,str(stat[x]),17,True), # all
                    lambda: self.wcatext(edit,417/724*1225,587/1024*1732,str(stat[x]),17,True), #egeszs
                    lambda: self.wcatext(edit,318/724*1225,657/1024*1732,str(stat[x]),17,True), #szeps
                    lambda: self.wcatext(edit,201/724*1225,657/1024*1732,str(stat[x]),17,True), #int
                    lambda: self.wcatext(edit,99/724*1225,584/1024*1732,str(stat[x]),17,True), #akarat
                    lambda: self.wcatext(edit,61/724*1225,467/1024*1732,str(stat[x]),17,True), #asztral
                    lambda: self.wcatext(edit,99/724*1225,350/1024*1732,str(stat[x]),17,True) #eszleles
                    ][x]()


    def felszereles (self, edit, text=[[["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""]],[["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""]]]):
        for oszlop in range(len(text) if len(text) < 3 else 2):
            for sor in range(len(text[oszlop]) if len(text[oszlop]) < 16 else 15):
                [
                lambda: self.wtext(edit,61+272*oszlop,365,text[oszlop][sor][0], 16, False, 220),
                lambda: self.wtext(edit,61+272*oszlop,393,text[oszlop][sor][0], 16, False, 220),
                lambda: self.wtext(edit,61+272*oszlop,422,text[oszlop][sor][0], 16, False, 220),
                lambda: self.wtext(edit,61+272*oszlop,450,text[oszlop][sor][0], 16, False, 220),
                lambda: self.wtext(edit,61+272*oszlop,479,text[oszlop][sor][0], 16, False, 220),
                lambda: self.wtext(edit,61+272*oszlop,508,text[oszlop][sor][0], 16, False, 220),
                lambda: self.wtext(edit,61+272*oszlop,536,text[oszlop][sor][0], 16, False, 220),
                lambda: self.wtext(edit,61+272*oszlop,565,text[oszlop][sor][0], 16, False, 220),
                lambda: self.wtext(edit,61+272*oszlop,594,text[oszlop][sor][0], 16, False, 220),
                lambda: self.wtext(edit,61+272*oszlop,622,text[oszlop][sor][0], 16, False, 220),
                lambda: self.wtext(edit,61+272*oszlop,651,text[oszlop][sor][0], 16, False, 220),
                lambda: self.wtext(edit,61+272*oszlop,679,text[oszlop][sor][0], 16, False, 220),
                lambda: self.wtext(edit,61+272*oszlop,708,text[oszlop][sor][0], 16, False, 220),
                lambda: self.wtext(edit,61+272*oszlop,737,text[oszlop][sor][0], 16, False, 220),
                lambda: self.wtext(edit,61+272*oszlop,765,text[oszlop][sor][0], 16, False, 220)
                ][sor]()
                [
                lambda: self.wcwtext(edit,307+275*oszlop,365, text[oszlop][sor][1]),
                lambda: self.wcwtext(edit,307+275*oszlop,393, text[oszlop][sor][1]),
                lambda: self.wcwtext(edit,307+275*oszlop,422, text[oszlop][sor][1]),
                lambda: self.wcwtext(edit,307+275*oszlop,450, text[oszlop][sor][1]),
                lambda: self.wcwtext(edit,307+275*oszlop,479, text[oszlop][sor][1]),
                lambda: self.wcwtext(edit,307+275*oszlop,508, text[oszlop][sor][1]),
                lambda: self.wcwtext(edit,307+275*oszlop,536, text[oszlop][sor][1]),
                lambda: self.wcwtext(edit,307+275*oszlop,565, text[oszlop][sor][1]),
                lambda: self.wcwtext(edit,307+275*oszlop,594, text[oszlop][sor][1]),
                lambda: self.wcwtext(edit,307+275*oszlop,622, text[oszlop][sor][1]),
                lambda: self.wcwtext(edit,307+275*oszlop,651, text[oszlop][sor][1]),
                lambda: self.wcwtext(edit,307+275*oszlop,679, text[oszlop][sor][1]),
                lambda: self.wcwtext(edit,307+275*oszlop,708, text[oszlop][sor][1]),
                lambda: self.wcwtext(edit,307+275*oszlop,737, text[oszlop][sor][1]),
                lambda: self.wcwtext(edit,307+275*oszlop,765, text[oszlop][sor][1])
                ][sor]()
    def kepzettseg(self, edit, text=[[["", False, False]],[["", False, False]]]):
        for oszlop in range(len(text) if len(text) < 3 else 2):
            for sor in range(len(text[oszlop]) if len(text[oszlop]) < 22 else 21):
                if oszlop == 0:
                    if sor in [2,3,5,6,7,8,10,12,13,15,16,18,20]:
                        self.kepz = [2,3,5,6,7,8,10,12,13,15,16,18,20].index(sor) +1
                    self.wtext(edit, 630,364+28*sor+self.kepz,text[oszlop][sor][0], 16, False, 205)
                    z = 0
                    if sor in [4,5,11,19]:
                        z = 1
                    if text[oszlop][sor][1]:
                        self.wtext(edit, 857,357+28*sor+self.kepz+z,"x",15)
                    if text[oszlop][sor][2]:
                        self.wtext(edit, 883,357+28*sor+self.kepz+z,"x",15) 
                elif oszlop == 1:
                    if sor in [2,3,5,6,7,8,10,12,13,15,16,18,20]:
                        self.kepz = [2,3,5,6,7,8,10,12,13,15,16,18,20].index(sor) +1
                    self.wtext(edit, 909,364+28*sor+self.kepz,text[oszlop][sor][0], 16, False, 205)
                    z = 0
                    if sor in [4,5,11,19]:
                        z = 1
                    if text[oszlop][sor][1]:
                        self.wtext(edit, 1135,357+28*sor+self.kepz+z,"x",15)
                    if text[oszlop][sor][2]:
                        self.wtext(edit, 1160,357+28*sor+self.kepz+z,"x",15)
            self.kepz = 0
    def penz(self, edit, text=[["","","",""],["","","",""],["","","",""]]):
            for sor in range(len(text) if len(text) < 4 else 3):
                self.wcatext(edit, 498,141+44*sor,text[sor][0],20,True)
                self.wcatext(edit, 571,141+44*sor,text[sor][1],20,True)
                self.wcatext(edit, 643,141+44*sor,text[sor][2],20,True)
                self.wtext(edit, 675,160+44*sor,text[sor][3],18)

    def nyelv(self, edit, text=[[["","","","",""],["","","","",""]],[["","","","",""],["","","","",""]]]):
        for oszlop in range(len(text) if len(text) < 3 else 2):

            self.wtext(edit,849+176*oszlop,115,text[oszlop][0][0])
            self.wtext(edit,849+176*oszlop,145,text[oszlop][0][1])
            self.wtext(edit,849+176*oszlop,174,text[oszlop][0][2])
            self.wtext(edit,849+176*oszlop,203,text[oszlop][0][3])
            self.wtext(edit,849+176*oszlop,232,text[oszlop][0][4])

            self.wcwtext(edit,965+176*oszlop,115,text[oszlop][1][0])
            self.wcwtext(edit,965+176*oszlop,145,text[oszlop][1][1])
            self.wcwtext(edit,965+176*oszlop,174,text[oszlop][1][2])
            self.wcwtext(edit,965+176*oszlop,203,text[oszlop][1][3])
            self.wcwtext(edit,965+176*oszlop,232,text[oszlop][1][4])

    def talalkozok(self, edit, text=[["","","","","",""],["","","","","",""],["","","","","",""],["","","","","",""],["","","","","",""],["","","","","",""]]):
            oszlop = [47,275,504,732,961]
            for sor in range(len(text) if len(text) < 7 else 6):
                if sor < 5:
                    for x in range(len(oszlop)):
                        self.wtext(edit, oszlop[x],1214+32*sor,text[sor][x], 16, False, 222)
                elif sor == 5:
                    for x in range(len(oszlop)):
                        self.wtext(edit, oszlop[x],1214+32*5-1,text[sor][x], 16, False, 222)
            
    def tarsak(self, edit, text=[["","","","","","","","","","",""],["","","","","","","","","","",""]]):
        for sor in range(len(text) if len(text) < 3 else 2):
            self.wtext(edit,269,1026+36*sor,text[sor][0], 16, False, 105)
            self.wtext(edit,381,1026+36*sor,text[sor][1], 16, False, 105)
            self.wcwtext(edit,515,1026+36*sor,text[sor][2])
            self.wcwtext(edit,564,1026+36*sor,text[sor][3])
            self.wcwtext(edit,613,1026+36*sor,text[sor][4])
            self.wcwtext(edit,661,1026+36*sor,text[sor][5])
            self.wcwtext(edit,710,1026+36*sor,text[sor][6])
            self.wcwtext(edit,781,1026+36*sor,text[sor][7])
            self.wcwtext(edit,874,1026+36*sor,text[sor][8])
            self.wcwtext(edit,968,1026+36*sor,text[sor][9])
            self.wtext(edit,1017,1026+36*sor,text[sor][10], 16, False, 165)

    def mergek(self, edit, text=[["","","",""],["","","",""],["","","",""],["","","",""]]):
        for sor in range(len(text) if len(text) < 5 else 4):
            [
            lambda: self.wtext(edit,84,852,text[sor][0], 16, False, 197),
            lambda: self.wtext(edit,84,881,text[sor][0], 16, False, 197),
            lambda: self.wtext(edit,47,909,text[sor][0], 16, False, 235),
            lambda: self.wtext(edit,47,938,text[sor][0], 16, False, 235)
            ][sor]()
            [
            lambda: self.wcwtext(edit,308,852,text[sor][1]),
            lambda: self.wcwtext(edit,308,881,text[sor][1]),
            lambda: self.wcwtext(edit,308,909,text[sor][1]),
            lambda: self.wcwtext(edit,308,938,text[sor][1])
            ][sor]()
            [
            lambda: self.wtext(edit,333,852,text[sor][2], 16, False, 138),
            lambda: self.wtext(edit,333,881,text[sor][2], 16, False, 138),
            lambda: self.wtext(edit,333,909,text[sor][2], 16, False, 138),
            lambda: self.wtext(edit,333,938,text[sor][2], 16, False, 138)
            ][sor]()
            [
            lambda: self.wtext(edit,478,852,text[sor][3], 16, False, 138),
            lambda: self.wtext(edit,478,881,text[sor][3], 16, False, 138),
            lambda: self.wtext(edit,478,909,text[sor][3], 16, False, 138),
            lambda: self.wtext(edit,478,938,text[sor][3], 16, False, 138)
            ][sor]()

    def zsakmany(self, edit, text=[["",""],["",""],["",""],["",""],["",""],["",""],["",""]]):
        for sor in range(len(text) if len(text) < 8 else 7):
            if sor < 6:
                self.wtext(edit,747,1474+29*sor,text[sor][0], 16, False, 345)
                self.wcwtext(edit,1126,1474+29*sor,text[sor][1])
            elif sor == 6:
                self.wtext(edit,762,1474+29*6+1,text[sor][0], 16, False, 330)
                self.wcwtext(edit,1126,1474+29*6+1,text[sor][1])
    def tp(self, edit, text):
        if text == None:
          text = ''
        self.wcatext(edit,598,1412,text,20)
    def levonasok(self, edit, text=[["","","",""],["","","",""]]):
        if text != []:
            self.wchtext(edit,120,115-17,text[0][0])
            self.wchtext(edit,120,159-17,text[0][1])
            self.wchtext(edit,120,203-17,text[0][2])
            self.wchtext(edit,120,246-17,text[0][3])

            self.wcatext(edit,396,115-17,text[1][0])
            self.wcatext(edit,396,159-17,text[1][1])
            self.wcatext(edit,396,203-17,text[1][2])
            self.wcatext(edit,396,246-17,text[1][3])

if __name__ == "__main__":
    import sys
    pdf = genpdf(json.load(open(sys.argv[1], mode="r", encoding="utf-8")))
    pdf(sys.argv[2])

    """
    def __init__(self, data):
        self.kepz = 0
        self.lap = [Image.open("karakterlap1.jpg"), Image.open("karakterlap2.jpg")]
        self.editlap = []
        for x in list(data.keys()):
            for y in range(2):
                elap = None
                if int(list(data[str(x)].keys())[y]) == 0:
                    self.editlap += [self.lap[0].copy()]
                    elap = ImageDraw.Draw(self.editlap[(list(data.keys()).index(x))*2])
                    self.alap(elap, data[x]['alap'])
                    self.stat(elap, data[x]['stat'])
                    self.szazalek(elap, data[x]['szazalek'])
                    self.elony(elap, data[x]['elony'])
                    self.hatrany(elap, data[x]['hatrany'])
                    self.varazstargyak(elap, data[x]['varazstargyak'])
                    self.fegyver_nelkuli(elap, data[x]['fegyver_nelkuli'])
                    for z in range(len(data[x]["fegyver"]) if len(data[x]["fegyver"]) < 4 else 3):
                        self.fegyver(elap,z+1,data[x]["fegyver"][y])
                    self.pszi(elap, data[x]["pszi"])
                    self.vert(elap, data[x]["vert"])
                elif int(list(data[str(x)].keys())[y]) == 1:
                    self.editlap += [self.lap[1].copy()]
                    elap = ImageDraw.Draw(self.editlap[(list(data.keys()).index(x)+1)*2-1])
                    self.levonasok(elap, data[x]['levonasok'])
                    self.penz(elap, data[x]['penz'])
                    self.nyelv(elap, data[x]['nyelv'])
                    self.felszereles(elap, data[x]['felszereles'])
                    self.kepzettseg(elap, data[x]['kepzettseg'])
                    self.mergek(elap, data[x]['mergek'])
                    self.tarsak(elap, data[x]['tarsak'])
                    self.talalkozok(elap, data[x]['talalkozok'])
                    self.tp(elap, str(data[x]['tp']))
                    for z in range(len(data[x]["fegyver"]) if len(data[x]["fegyver"]) < 3 else 2):
                        self.fegyver(elap, z+4, data[x]['fegyver'][y])
                    self.zsakmany(elap, data[x]['zsakmany'])
    """
