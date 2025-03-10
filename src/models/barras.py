from math import pi
import cmath as cm
class Barra():
    sb = 100
    vbs = 1000
    zb = 100
    
    def __init__(self,dados, ref = [1.0 ,0.0]):
        self.__dados = dados if dados is not None else []
        self.indx = int(self.__dados[0]) -1
        self.oetg = self.__dados[1]
        self.nome = self.__dados[2]
        
        self.operac:int
        self.estado:int
        self.tipo:int
        self.tpo:int
        self.vb:float
        self.ab:float
        self.sh:complex

        self.bartipo()
        self.nilton(ref)
        self.rngQ = self.limitQ()
        self.spq = self.sbar()/self.sb
        
    def bartipo(self): # tratamento do OETGb
        oetgb = self.oetg
        if isinstance(oetgb,float): oetgb = "  "+str(int(oetgb))+"  "

        operac = oetgb[0]
        if operac == " ": operac = 0
        else: operac = 1
        self.operac = operac

        estado = oetgb[1]
        if estado == "L" or estado == " ": estado = 1
        else: estado = 0
        self.estado = estado

        tipo = oetgb[2]
        if tipo.isdigit(): tipo = int(tipo)
        else: tipo = 0
        self.tipo = tipo
        self.tpo = tipo
        pass

    def nilton(self,ref):
        vsh = self.__dados[13]
        if vsh is None: vsh = 0
        self.sh = (1j)* vsh/self.zb 

        match self.tipo:
            case 0:
                self.vb = ref[0]
                self.ab = ref[1]
            case 1:
                self.vb = self.__dados[4]/self.vbs if self.__dados[4] is not None else 1
                self.ab = ref[1]
            case 2:
                self.vb = self.__dados[4]/self.vbs if self.__dados[4] is not None else 1
                self.ab = pi*(self.__dados[5])/180 if self.__dados[5] is not None else 0
        pass

    def Eb(self): return self.vb*cm.exp(1j*self.ab)

    def sbar(self):
        Pger = self.__dados[6] if self.__dados[6] is not None else 0
        Qger = self.__dados[7] if self.__dados[7] is not None else 0
        Pdem = self.__dados[11] if self.__dados[11] is not None else 0
        Qdem = self.__dados[12] if self.__dados[12] is not None else 0
        potencia = (Pger-Pdem) +1j*(Qger-Qdem)
        return potencia

    def limitQ(self):
        limmin = self.__dados[8] if self.__dados[8] is not None else -9999
        limmax = self.__dados[9] if self.__dados[9] is not None else 9999
        return [limmin/self.sb, limmax/self.sb]

    def __str__(self,r=4):
        return f"({self.indx+1})\t[{round(self.vb,r)} {round(self.ab,r)} {round(self.spq.real,r)} {round(self.spq.imag,r)}]"

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
            if bar.tipo == 2: 
                bref = [bar.vb, bar.ab]
                break
        for ddbar in self.__dbar:
            bar = Barra(ddbar,bref)
            nBar.append(bar)

        return nBar
    def __str__(self,r=1):
        tx = ''
        for barra in self.bars:
            tx += f"({barra.indx+1})\t[{round(barra.vb*barra.vbs,r)} {round(180*(barra.ab)/pi,1)} {round(barra.spq.real*barra.sb,r)} {round(barra.spq.imag*barra.sb,r)}]\n"
        return tx       
    def updatebar(self,vec:list):
        ctt = 0
        for k in range(self.nb):
            if self.bars[k].tipo == 1 or self.bars[k].tipo == 0:
                self.bars[k].ab += vec[ctt]
                ctt+=1
        vec = vec[ctt:]        
        ctt = 0
        for k in range(self.nb):
            if self.bars[k].tipo == 0:
                self.bars[k].vb += vec[ctt]
                ctt+=1
        return self.bars
    def update2(self,vec2:list):
        for k in range(self.nb):
            if self.bars[k].tipo == 1:
                self.bars[k].spq = self.bars[k].spq.real + 1j*(vec2[k].imag)
            if self.bars[k].tipo == 2:
                self.bars[k].spq = vec2[k]
        return self.bars
                