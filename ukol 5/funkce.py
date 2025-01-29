from PIL import *
from PyQt5 import  QtGui

ukoncovacitextvb = "000011001000000110100000001100111000011101000000110110100001101100"
    
def pil2pixmap(im):
    if im.mode == "RGB":
        r, g, b = im.split()
        im = Image.merge("RGB", (b, g, r))
    elif  im.mode == "RGBA":
        r, g, b, a = im.split()
        im = Image.merge("RGBA", (b, g, r, a))
    elif im.mode == "L":
        im = im.convert("RGBA")
        im = Image.merge("RGB", (b, g, r))
    im3 = im.convert("RGBA")
    data = im3.tobytes("raw", "RGBA")
    qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
    pixmap = QtGui.QPixmap.fromImage(qim)
    return pixmap

def ziskejtext(data):
    result = ""
    for x in data:
        for q in x[:3]:
            result += str(q%2)
    result = result.split(ukoncovacitextvb)
    if len(result) == 2:
        result = result[0]
    else:
        return "V tomto obrázku se nenašly žádné data",1
    res = ""
    for i in range(len(result)//11):
        t = int(result[i*11:(i+1)*11],2)
        res += chr(t)
    return res,0

def upravrRGB(data, textkzapisu):
    
    finres = []
    result = ""
    for i in textkzapisu:
        b = str(bin(ord(i)))[2:]
        result += "0"*(11-len(b))+b
    result += ukoncovacitextvb
    result = list(result)
    counter = 0
    for i in data:
        temp = []
        tmp = 0
        for z in i:
            tmp+=1
            p = z
            if tmp <=3:
                counter += 1
                if counter<=len(result):
                    if z%2 == 1 and int(result[counter-1]) %2 ==1:
                        True
                    elif z%2 == 1 and int(result[counter-1]) %2 ==0:
                        p+=1
                        if p > 255:
                            p-=2
                    else:
                        p += int(result[counter-1])
            temp.append(p)
        finres.append(tuple(temp))
    while len(finres)<len(data):
        finres.append(tuple(data[len(finres)]))
    return finres