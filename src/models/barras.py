from math import pi
import cmath as cm
class Barra():
    sb = 100
    vbs = 1000
    zb = 100
    
    def __init__(self,dados, ref = [1.0 ,0.0]):
        self.__dados = dados if dados is not None else []
        self.indx = int(self.__dados[0]) -1
        self.oetg = int(self.__dados[1]) if self.__dados[1] != ' ' else 0
        self.nome = self.__dados[2]
        self.sh = (1j)*self.__dados[13]/(self.zb) if self.__dados[13] is not None else 0  
        self.vb:float
        self.ab:float
        self.nilton(ref)
        self.spq = self.sbar()/self.sb
        
    def nilton(self,ref):
        match self.oetg:
            case 0:
                self.vb = ref[0]
                self.ab = ref[1]
            case 1:
                self.vb = self.__dados[4]/self.vbs if self.__dados[4] is not None else 1
                self.ab = ref[1]
            case 2:
                self.vb = self.__dados[4]/self.vbs if self.__dados[4] is not None else 1
                self.ab = pi*(self.__dados[5])/180 if self.__dados[5] is not None else 0
        # self.vb = self.__dados[4]/self.vbs if self.__dados[4] is not None else 1
        # self.ab = pi*(self.__dados[5])/180 if self.__dados[5] is not None else 0
        pass

    def Eb(self): return self.vb*cm.exp(1j*self.ab)

    def sbar(self):
        Pger = self.__dados[6] if self.__dados[6] is not None else 0
        Qger = self.__dados[7] if self.__dados[7] is not None else 0
        Pdem = self.__dados[11] if self.__dados[11] is not None else 0
        Qdem = self.__dados[12] if self.__dados[12] is not None else 0
        potencia = (Pger-Pdem) +1j*(Qger-Qdem)
        return potencia


    def __str__(self,r=4):
        return f"({self.indx+1})\t[{round(self.vb,r)} {round(180*(self.ab)/pi,r)} {round(self.spq.real,r)} {round(self.spq.imag,r)}]"

class Barras():
    def __init__(self,dbar:list=None):
        self.__dbar = dbar if dbar is not None else []
        self.nb = len(self.__dbar)
        self.bars = self.novas_barras()
    def novas_barras(self):
        nBar = []
        bref = [1.0 ,0.0]
        for ddbar in self.__dbar:
            bar = Barra(ddbar,bref)
            if bar.oetg == 2: 
                bref = [bar.vb, bar.ab]
                break
        for ddbar in self.__dbar:
            bar = Barra(ddbar,bref)
            nBar.append(bar)

        return nBar
    def __str__(self,r=3):
        tx = ''
        for barra in self.bars:
            tx += f"({barra.indx+1})\t[{round(barra.vb,2)} {round(180*(barra.ab)/pi,1)} {round(barra.spq.real,r)} {round(barra.spq.imag,r)}]\n"
        return tx       
    def updatebar(self,vec:list):
        ctt = 0
        for k in range(self.nb):
            if self.bars[k].oetg == 1 or self.bars[k].oetg == 0:
                self.bars[k].ab += vec[ctt]
                ctt+=1
        vec = vec[ctt:]        
        ctt = 0
        for k in range(self.nb):
            if self.bars[k].oetg == 0:
                self.bars[k].vb += vec[ctt]
                ctt+=1
        return self.bars
    def update2(self,vec2:list):
        for k in range(self.nb):
            if self.bars[k].oetg == 1:
                self.bars[k].spq = self.bars[k].spq.real + 1j*(vec2[k].imag)
            if self.bars[k].oetg == 2:
                self.bars[k].spq = vec2[k]
        return self.bars
                