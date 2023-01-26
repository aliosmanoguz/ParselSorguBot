from PyQt5.QtWidgets import *
from giris_ui import Ui_MainWindow
from harita import HaritaOlustur
import RotaAlg
import requests

sayac = 0
coordlist = []
coord = []
url = "https://cbsapi.tkgm.gov.tr/megsiswebapi.v3/api/"
class girisPencere(QMainWindow):
    def __init__(self) ->None:
        super().__init__()
        self.giris = Ui_MainWindow()
        self.giris.setupUi(self)

        self.giris.pushButton_koordinat.clicked.connect(self.GonderKoor)
        self.giris.pushButton_Tasinmaz.clicked.connect(self.GonderTasinmaz)
        self.giris.pushButton.clicked.connect(self.haritaGoster)
        self.giris.pushButton_2.clicked.connect(self.haritaGoster)
        self.giris.TAMAMLA_2.clicked.connect(self.KodlariAktar)

    def KoorSplit(self, urlyeni):

        global sayac
        urlHtml = requests.get(urlyeni)
        strjson = urlHtml.text  # url ile bir sorgu yaptık ve gelen veriyi string e dönüştürdük
        print(strjson[2])
        if(strjson[2] == 'M'):
            self.giris.textBrowser.append("Mevcut Bilgiler İle Bir Kayıt Bulunamadı")
        else:
            coord.clear()
            coordlist.clear()
            strjson = strjson.split("[[")  # json içeriğindeki koordinat noktalarını ayırdık ve strj3 dizisinin içine koyduk
            strj2 = strjson[1]
            strj2 = strj2.split("]]")
            strj3 = strj2[0]
            strj3 = strj3.split(",")

            for i in range(len(strj3)):
                strj3[i] = strj3[i].removeprefix('[')
                strj3[i] = strj3[i].removesuffix(']')

            for i in range(len(strj3)):
                self.giris.textBrowser.append(strj3[i])

            while (sayac < len(strj3)):
                a = float(strj3[sayac+1])
                b = float(strj3[sayac])
                coordlist.append([a,b])
                sayac = sayac+2
            coord.append(float(strj3[1]))
            coord.append(float(strj3[0]))
            print(coord)
            print(coordlist)
            self.haritaYap = HaritaOlustur(coord,coordlist,len(strj3))

    def haritaGoster(self):
        self.haritaYap.showMaximized()
    def GonderKoor(self):
        paralel = self.giris.lineEdit_Paralel.text()
        meridyen = self.giris.lineEdit_Meridyen.text()

        url2 = url+"parsel/"+paralel+"/"+meridyen
        self.KoorSplit(url2)

    def GonderTasinmaz(self):
        tasinmazNo = self.giris.lineEdit_Tasinmaz.text()
        url2 = url+"zemin//"+tasinmazNo
        self.KoorSplit(url2)
    def KodlariAktar(self):

        x = []
        y = []

        for i in range(len(coordlist)):
            x.append(coordlist[i][0])
            y.append(coordlist[i][1])

        path = RotaAlg.rotaHesapla(x,y)

        path00 = path[0][0]
        path01 = path[0][1]

        for i in range(len(path)):

            if i < len(path) - 1:
                path[i][0] = int(((path[i][0] / 100000) - (path00 / 10000)) * 111000000)
                path[i][1] = int(((path[i][1] / 100000) - (path01 / 10000)) * 111000000)

        hafiza = 0
        path2 = []

        for i in range(1, len(path) - 1):
            if path[i][0] == path[i + 1][0]:
                if hafiza == 1:
                    pass
                else:
                    ara = [path[i][0], path[i][1]]
                    path2.append(ara)
                    hafiza = 1
            else:
                hafiza = 0
                ara = [path[i][0], path[i][1]]
                path2.append(ara)

        gonderi = ""
        for i in range(len(path2)):
            gonderi = gonderi + str(path2[i][0]) + " " + str(path2[i][1]) + ","

        dosya = open("sinirlar.txt", "w")
        dosya.write(gonderi)
        dosya.close()
        print("TAMAMLANDI")
