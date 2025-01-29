import unicodedata

whitelistpovoleneznaky = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
cisla = ["XNULAX","XEDNAX","XDVAAX","XTRIIX","XCTYRX","XPETTX","XSESTX","XSEDUX","XOSMMX","XDEVEX"]

def UpravVstupUzivatele(textf,petznaku):
    textf = unicodedata.normalize('NFKD', textf)
    vetaBezDiakritiky = ''
    for c in textf:
        if not unicodedata.combining(c):
            if (c in whitelistpovoleneznaky):
                vetaBezDiakritiky += c
            elif (c == " "):
                vetaBezDiakritiky += "XMEZERAX"
            elif (c.isnumeric()):
                if petznaku:
                    vetaBezDiakritiky += cisla[int(c)]
                else:
                    vetaBezDiakritiky += c
    return vetaBezDiakritiky

def UpravKlic(key):
    key = unicodedata.normalize('NFKD', key)
    vetaBezDiakritiky = ''
    for c in key:
        if not unicodedata.combining(c):
            if (c in whitelistpovoleneznaky):
                vetaBezDiakritiky += c
    if (len(vetaBezDiakritiky)==0):
        return 1
    else:
        return vetaBezDiakritiky

            
def zasifruj(text,zasabc,pole):
    result = ""
    for i in text:
        temp = zasabc.index(i)
        result+=pole[temp//len(pole)]
        result+=pole[temp%len(pole)]
    return result

def zasifrujfinal(sifrovanytext,klic):
    klicsort = sorted(klic)
    result=""
    if len(klic)<len(sifrovanytext):
        for i in klicsort:
            index = klic.index(i)
            for q in range(index,len(sifrovanytext),len(klic)):
                result+=sifrovanytext[q]
            result+=" "
            klic[index]=""
        return result   
    else:
        return "Zadán dlouhý klíč. Musí se zvětšit vstupní data nebo zmenšit klíč."
    

def initzasifruj(text,key,abeceda,pole):
    klic = key.upper()
    if(len(pole)==5):
        text = UpravVstupUzivatele(text,True)
    else:
        text = UpravVstupUzivatele(text,False)
    klic = UpravKlic(klic)
      
    if(klic==1):
        return "Zadán špatný klíč"
    else:
        klic = list(klic)
        result = zasifruj(text,abeceda,pole)
        result = zasifrujfinal(result,klic)
        result = result.replace(" ","")
        counter = 0
        pomocna = ""
        for i in result:
            counter += 1
            pomocna += i
            if counter == 5:
                pomocna += " "
                counter = 0
            
        return pomocna

def OdstranDiakritiku(vstup):
    vstup = unicodedata.normalize('NFKD', vstup)
    vetaBezDiakritiky = ''
    for c in vstup:
        if not unicodedata.combining(c):
            if (c in whitelistpovoleneznaky):
                vetaBezDiakritiky += c
    return vetaBezDiakritiky

def odsifruj(sifrovanytext,klice):
    klic=[]
    klic+=klice
    klicsort = sorted(klic)
    result=""
    
    if len(klic)<len(sifrovanytext):
        mezery = [len(sifrovanytext)//len(klic)]*len(klic)
        pocetznakunavic=len(sifrovanytext)%len(klic)
        counter=0
        while counter < len(klic):
            i = klic[counter]
            index = klicsort.index(i)
            if(pocetznakunavic>klic.index(i)):
                mezery[index]+=1
            klicsort[index]=""
            klic[counter] = ""
            counter+=1
        startpismena = []
        klic=[]
        klic+=klice
        klicsort = sorted(klic)
        counter=0
        while counter < len(klic):
            i = klic[counter]
            index = klicsort.index(i)
            start = 0
            for q in range (0,index):
                start += mezery[q]
            startpismena.append(start)
            klicsort[index]=""
            klic[counter] = ""
            counter+=1
        for j in range(0,max(mezery)):
            for i in range(0,len(mezery)):
                if startpismena[i]+j < len(sifrovanytext) and (startpismena[i]+j not in startpismena or j==0):
                    result += sifrovanytext[startpismena[i]+j]
        return result   
    else:
        return "Zadán dlouhý klíč. Musí se zvětšit vstupní data nebo zmenšit klíč."

def odsifrujfinal(text,zasabc,pole):
    result = ""
    for i in range(0, len(text), 2):
        temp1 = pole.index(text[i])
        temp2 = pole.index(text[i+1])
        result+=zasabc[temp1*len(pole)+temp2]
    return result


def initodsifruj(text,key,abeceda,pole):
    pokracuj = True
    text = text.replace(" ","")
    klic = key.upper()
    text = OdstranDiakritiku(text.upper())
    klic = UpravKlic(klic)
    for i in text:
        if i not in pole:
            pokracuj=False
            break
    if(klic==1):
        return "Zadán špatný klíč"
    elif pokracuj==False:
        return "Zadán špatný vstup"
    else:
        klic = list(klic)
        result = odsifruj(text,klic)
        result = odsifrujfinal(result, abeceda, pole)
        counter = 0
        result = result.replace("XMEZERAX"," ")
        for i in cisla:
            result = result.replace(i,str(counter))
            counter += 1
        return result
          
