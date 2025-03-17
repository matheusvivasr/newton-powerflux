import cmath as cm
from math import pi
class Linha():
    zb = 100 # impedancia base
    def __init__(self,dados:list=None):
        self.__dados = dados if dados is not None else []

        self.nome = self.__dados[2]
        self.lin = [int(self.__dados[0])-1, int(self.__dados[2])-1]
        self.zl = self.impedancia()
        self.yl = self.admitancia()
        self.tap = self.trafo()[1]
        self.ph = self.trafo()[0]
        self.sh = 1j*self.__dados[6]/(self.zb*2) if self.__dados[6] is not None else 0
        pass

    def __str__(self):
        return f"({self.lin}):\t[{self.yl}]"

    def impedancia(self):
        rl = self.__dados[4] if self.__dados[4] is not None else 0
        xl = self.__dados[5] if self.__dados[5] is not None else 0
        zlin = (rl + 1j*xl)/self.zb
        return zlin
    
    def trafo(self):
        phs = pi*(self.__dados[10])/180 if self.__dados[10] is not None else 0
        ang = cm.exp(-1j*phs)
        tap = 1/self.__dados[7] if self.__dados[7] is not None else 1
        tf = [ang, tap]
        return tf

    def admitancia(self,r=4):
        admit = (1/self.zl)
        admit = admit.real +1j*admit.imag
        return admit


class Linhas():
    def __init__(self,dlin:list=None):
        self.__dlin = dlin if dlin is not None else []
        self.nl = len(self.__dlin)
        self.lins = self.novas_linhas()
        pass

    def novas_linhas(self):
        nLin = []
        for ddlin in self.__dlin:
            lin = Linha(ddlin)
            nLin.append(lin)
        return nLin

    def ybus(self,barras:list=None):
        self.barras = barras
        rnb = range(barras.nb)
        barras = barras.bars if barras is not None else []
        ybuss = [[0j for _ in rnb] for _ in rnb]
        for linha in self.lins:
            k,m = linha.lin
            ybuss[k][m] = -linha.ph*linha.tap*linha.yl
            ybuss[m][k] = -linha.ph*linha.tap*linha.yl
            ybuss[k][k] += (linha.tap*linha.tap*linha.yl + linha.sh)
            ybuss[m][m] += (linha.tap*linha.tap*linha.yl + linha.sh)
        for bar in barras:
            k = bar.indx
            ybuss[k][k] += bar.sh
        return ybuss
    
    def __str__(self):
        out =  ''
        for linm in self.lins:
            out += f"{[ind+1 for ind in linm.lin]}: {redondo(linm.yl)}, {round(linm.tap,4)}, {redondo(linm.sh)}\n"
        return out
    
def redondo(num=0):
    nr = round(num.real,4)
    ni = round(num.imag,4)
    return nr+1j*ni