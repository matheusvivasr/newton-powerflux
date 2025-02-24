import cmath as cm
class Scomplex():
    def __init__(self,ybus,barras):
        self.__ybus = ybus
        self.__barras = barras
        
    def pots(self):
        Sb = []
        dbar = self.__barras.bars
        for bk in dbar:
            pot = 0j
            for bm in dbar:
                pot += bk.vb*bm.vb*self.__ybus[bk.indx][bm.indx]*cm.exp(-1j*(bk.ab-bm.ab))
            Sb.append(pot.conjugate())
            
        return Sb

    def erros(self): 
        potout = []
        pots = self.pots() 
        dbar = self.__barras.bars
        for barra in dbar:
            if barra.oetg == 1 or barra.oetg == 0:
                pot = barra.pot - pots[barra.indx].real
                potout.append(pot)
        for barra in dbar:
            if barra.oetg == 0:
                pot = barra.qot - pots[barra.indx].imag
                potout.append(pot)
        return potout
    
    def jacob(self):
        barras = self.__barras.bars
        rnb = range(self.__barras.nb)

        dp = []
        dq = []
        for k in rnb:
            if barras[k].oetg == 1 or barras[k].oetg == 0:
                dp.append(k)
        for k in rnb:
            if barras[k].oetg == 0:
                dq.append(k)

        sda = [[0 for ç in rnb] for ç in rnb]
        for k in rnb:
            skk = 0
            for m in rnb:
                sk = 0
                if not k == m:
                    sk = (-1j) *barras[k].vb*barras[m].vb *self.__ybus[k][m] *cm.exp((-1j)*(barras[k].ab - barras[m].ab))
                skk -= sk.conjugate()
                sda[k][m] = sk.conjugate()
            sda[k][k] = skk

        sdv = [[0 for ç in rnb] for ç in rnb]
        for k in rnb:
            skk = 0
            for m in rnb:
                sk = 0
                if not k == m:
                    sk = -barras[k].vb *self.__ybus[k][m] *cm.exp((-1j)*(barras[k].ab - barras[m].ab))
                else: 
                    sk = -2*barras[k].vb*self.__ybus[k][k]

                sdv[k][m] = -sk.conjugate()
                skk += sk
            sdv[k][k] = skk.conjugate()

        jacs = []
        for k in dp:
            lin = []
            for m in dp:
                lin.append(sda[k][m].real)
            for m in dq:
                lin.append(sdv[k][m].real)
            jacs.append(lin)
        for k in dq:
            lin = []
            for m in dp:
                lin.append(sda[k][m].imag)
            for m in dq:
                lin.append(sdv[k][m].imag)
            jacs.append(lin)
        return jacs        
    