import unicodedata

whitelistpovoleneznaky = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
cisla = ["XNULAX","XJEDNX","XDVAAX","XTRIIX","XCTYRX","XPETTX","XSESTX","XSEDUX","XOSMMX","XDEVEX"]


def UpravVstupUzivatele(textf, a, b):
    if (a > 25 or a < 1 or a==13 or a%2==0 or b < 0 or b > 25):
        return "1"
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

def zasifruj(textf, a, b):
    result = ""
    zasabeceda = []
    for x in range(26):
        zasabeceda.append(whitelistpovoleneznaky[(x*a+b)%26])
    count = 0
    for i in textf:
        if (count == 5):
            result += " "
            count = 0
        count+=1
        result += zasabeceda[whitelistpovoleneznaky.index(i)]
    return result, zasabeceda

def initzasifruj(text, a, b):
    text = UpravVstupUzivatele(text.upper(), a, b)
    if(text != "1"):
        text, sifrabc = zasifruj(text, a, b)
        return text, sifrabc
    else:
        return "A musí být z následujícího seznamu:\n{1,3,5,7,9,11,15,17,19,21,23,25} a zároveň B musí být celé číslo z intervalu <0, 25>", 1


def najdiinverzniprvek(a, b):
    for i in range(26):
        if (i*a % 26) == 1:
            return i
    return -1

def kontrola(textf, a, b):
    if (a > 25 or a < 1 or a==13 or a%2==0 or b < 0 or b > 25):
        return "1"
    textf = unicodedata.normalize('NFKD', textf)
    vetaBezDiakritiky = ''
    for c in textf:
        if (c in whitelistpovoleneznaky):
            vetaBezDiakritiky += c
    return vetaBezDiakritiky
    

def odsifruj(textf, inve, b):
    result = ""
    textf = textf.replace(" ", "")
    zasabeceda = []
    for x in range(26):
        zasabeceda.append(whitelistpovoleneznaky[(inve*(x-b))%26])
    for i in textf:
        result += zasabeceda[whitelistpovoleneznaky.index(i)]
    counter = 0
    for i in cisla:
        result = result.replace(i,str(counter))
        counter += 1
    result = result.replace("XMEZERAX"," ")
    return result, zasabeceda
        
def initodsifruj(text, a, b):
    text = kontrola(text.upper(), a, b)
    if(text == "1"):
        return "Zadané špatné vstupy",1
    invprvek = najdiinverzniprvek(a, b)
    if(invprvek>-1):
        text, zasabeceda = odsifruj(text, invprvek, b)
        return text, zasabeceda
    else:
        return "Zadané špatné údaje",1

