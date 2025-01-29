import unicodedata

whitelistpovoleneznaky = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
cisla = ["XNULAX","XEDNAX","XDVAAX","XTRIIX","XCTYRX","XPETTX","XSESTX","XSEDUX","XOSMMX","XDEVEX"]

def UpravVstupUzivatele(textf):
    textf = unicodedata.normalize('NFKD', textf)
    vetaBezDiakritiky = ''
    for c in textf:
        if not unicodedata.combining(c):
            if (c in whitelistpovoleneznaky):
                vetaBezDiakritiky += c
            elif (c == " "):
                vetaBezDiakritiky += "XMEZERAX"
            elif (c.isnumeric()):
                vetaBezDiakritiky += cisla[int(c)]
    return vetaBezDiakritiky

def UpravKlic(key):
    key = unicodedata.normalize('NFKD', key)
    vetaBezDiakritiky = ''
    pridaneznaky = []
    for c in key:
        if not unicodedata.combining(c):
            if (c in whitelistpovoleneznaky and c not in pridaneznaky):
                vetaBezDiakritiky += c
                pridaneznaky.append(c)
    if (len(vetaBezDiakritiky)==0):
        return 1
    else:
        return vetaBezDiakritiky

def UpravPredZasifrovanim(textf):
    counter = 0;
    upravtext = ""
    while(counter<len(textf)):
        temp = textf[counter:counter+2]
        if(len(temp)==2 and temp[0]==temp[1]):
            upravtext+=temp[0]
            if(temp[0]!="X"):
                upravtext+="X"
            else:
                upravtext+="Y"
            counter-=1
        else:
            upravtext+=temp
        counter+=2
    if(len(upravtext)%2==1):
        if(upravtext[-1]!="X"):
            upravtext+="X"
        else:
            upravtext+="Y"
    return upravtext
            
def zasifruj(text,zasabc):
    counter = 0
    result = ""
    while(counter<len(text)):
        temp = zasabc.index(text[counter])
        x1 = temp%5
        y1 = temp// 5
        
        temp1 = zasabc.index(text[counter+1])
        x2 = temp1%5
        y2 = temp1 // 5
        if (x1==x2):
            result+=zasabc[(temp+5)%25]+zasabc[(temp1+5)%25]
        elif (y1==y2):
            result+=zasabc[(x1+1)%5+y1*5]+zasabc[(x2+1)%5+y2*5]
        else:
            result+=zasabc[x1+y2*5]+zasabc[x2+y1*5]
        counter+=2
    res = ""
    counter=0
    for i in result:
        counter+=1
        res += i
        if counter == 5:
            counter = 0
            res+=" "
    return res

def initzasifruj(text,key,abeceda):
    klic = key.upper()
    text = UpravVstupUzivatele(text.upper())
    zbyvajici = []
    zbyvajici += whitelistpovoleneznaky
    if abeceda == 0:
        zbyvajici.remove("Q")
        text = text.replace("Q", "K")
        klic = klic.replace("Q", "K")
    else:
        zbyvajici.remove("J")
        text = text.replace("J", "I")
        klic = klic.replace("J", "I")  
    klic = UpravKlic(klic)
      
    if(klic==1):
        return "Zadán špatný klíč",1
    else:
        klic = list(klic)
        zasabc = klic
        for i in zbyvajici:
            if i not in klic:
                zasabc.append(i)
        text = UpravPredZasifrovanim(text)
        result = zasifruj(text,zasabc)
        return result, zasabc

def OdstranDiakritiku(vstup):
    vstup = unicodedata.normalize('NFKD', vstup)
    vetaBezDiakritiky = ''
    for c in vstup:
        if not unicodedata.combining(c):
            if (c in whitelistpovoleneznaky):
                vetaBezDiakritiky += c
    return vetaBezDiakritiky

def odsifruj(text,zasabc):
    counter = 0
    result = ""
    while(counter<len(text)):
        temp = zasabc.index(text[counter])
        x1 = temp%5
        y1 = temp// 5
        temp1 = zasabc.index(text[counter+1])
        x2 = temp1%5
        y2 = temp1 // 5
        if (x1==x2):
            result+=zasabc[(temp-5)%25]+zasabc[(temp1-5)%25]
        elif (y1==y2):
            result+=zasabc[(x1-1)%5+y1*5]+zasabc[(x2-1)%5+y2*5]
        else:
            result+=zasabc[x1+y2*5]+zasabc[x2+y1*5]
        counter+=2
    counter = 0
    result = result.replace("XMEZERAX"," ")
    for i in cisla:
        result = result.replace(i,str(counter))
        counter += 1
    return result

def initodsifruj(text,key,abeceda):
    text = text.replace(" ","")
    klic = key.upper()
    text = UpravVstupUzivatele(text.upper())
    zbyvajici = []
    zbyvajici += whitelistpovoleneznaky
    text = OdstranDiakritiku(text.upper())
    if abeceda == 0:
        zbyvajici.remove("Q")
        text = text.replace("Q", "K")
        klic = klic.replace("Q", "K")
    else:
        zbyvajici.remove("J")
        text = text.replace("J", "I")
        klic = klic.replace("J", "I")
    klic = UpravKlic(klic)
    if(klic==1):
        return "Zadán špatný klíč",1
    else:
        klic = list(klic)
        zasabc = klic
        for i in zbyvajici:
            if i not in klic:
                zasabc.append(i)
        if(len(text)%2==1):
            if(text[-1]!="X"):
                text+="X"
            else:
                text+="Y"
        result = odsifruj(text,zasabc)
        return result,zasabc
          
