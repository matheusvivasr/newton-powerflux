class Barra():
    sb = 100
    vb = 1000
    zb = 100
    def __init__(self,dados:list=None):
        self.__dados = dados if dados is not None else []
        self.indx = int(self.__dados[0]) -1
        self.oetg = int(self.__dados[1])
        self.nome = self.__dados[2]
        self.vb = self.__dados[4]/self.vb if self.__dados[4] is not None else 1
        self.ab = self.__dados[5] if self.__dados[5] is not None else 0
        self.pot = self.__dados[11]/self.sb if self.__dados[11] is not None else 0
        self.qot = self.__dados[12]/self.sb if self.__dados[12] is not None else 0
        self.sh = 1j*self.__dados[13]/(self.zb) if self.__dados[13] is not None else 0  
    def __str__(self,r=4):
        return f"({self.indx+1})\t[{round(self.vb,r)} {round(self.ab,r)} {round(self.pot,r)} {round(self.qot,r)}]"

class Barras():
    def __init__(self,dbar:list=None):
        self.__dbar = dbar if dbar is not None else []
        self.nb = len(self.__dbar)
        self.bars = self.novas_barras()
    def novas_barras(self):
        nBar = []
        for ddbar in self.__dbar:
            bar = Barra(ddbar)
            nBar.append(bar)
        return nBar
    def __str__(self,r=4):
        tx = ''
        for barra in self.bars:
            tx += f"({barra.indx+1})\t[{round(barra.vb,r)} {round(barra.ab,r)} {round(barra.pot,r)} {round(barra.qot,r)}]\n"
        return tx       
    def updatebar(self,vec:list):
        ctt = 0
        for k in range(self.nb):
            if self.bars[k].oetg == 1 or self.bars[k].oetg == 0:
                self.bars[k].ab -= vec[ctt]
                ctt+=1
        vec = vec[ctt:]        
        ctt = 0
        for k in range(self.nb):
            if self.bars[k].oetg == 0:
                self.bars[k].vb -= vec[ctt]
                ctt+=1
        return self.bars
    def update2(self,vec2:list):
        for k in range(self.nb):
            if self.bars[k].oetg == 1:
                self.bars[k].qot = vec2[k].imag
            if self.bars[k].oetg == 2:
                self.bars[k].pot = vec2[k].real
                self.bars[k].qot = vec2[k].imag
        return self.bars