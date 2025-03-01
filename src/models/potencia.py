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
                ykm = self.__ybus[bk.indx][bm.indx]
                pot += bk.Eb().conjugate() * ykm * bm.Eb()
            Sb.append(pot.conjugate())
        return Sb

    def erros(self): 
        potout = []
        pots = self.pots() 
        dbar = self.__barras.bars
        for barra in dbar:
            if barra.oetg == 1 or barra.oetg == 0:
                pot = barra.spq.real - pots[barra.indx].real
                potout.append(pot)
        for barra in dbar:
            if barra.oetg == 0:
                pot = barra.spq.imag - pots[barra.indx].imag
                potout.append(pot)
        return potout
    
    def jacob(self):
        barras = self.__barras.bars
        rnb = range(self.__barras.nb)
        sda = [[0 for ç in rnb] for ç in rnb]
        sdv = [[0 for ç in rnb] for ç in rnb]
        for k in rnb:
            sda[k][k] = 0j
            sdv[k][k] = (2*barras[k].vb*self.__ybus[k][k])
            for m in rnb:
                if not k == m:
                    sda[k][m]  = ((1j)*self.__ybus[k][m]*(barras[k].Eb().conjugate())*(barras[m].Eb()))
                    sda[k][k] -= sda[k][m]
                    sdv[k][m]   = ((1/barras[k].vb)*self.__ybus[k][m]*(barras[k].Eb().conjugate())*(barras[m].Eb()))
                    sdv[k][k] += sdv[k][m]

        jacs = []
        for k in self.pbars():
            lin = []
            for m in self.pbars():
                lin.append(round(-sda[k][m].real,4))
            for m in self.qbars():
                lin.append(round(-sdv[k][m].real,4))
            jacs.append(lin)
            
        for k in self.qbars():
            lin = []
            for m in self.pbars():
                lin.append(round(sda[k][m].imag,4))
            for m in self.qbars():
                lin.append(round(sdv[k][m].imag,4))
            jacs.append(lin)
        return jacs     
       
    def pbars(self):
        barras = self.__barras.bars
        rnb = range(self.__barras.nb)

        dp = []
        for k in rnb:
            if barras[k].oetg == 1 or barras[k].oetg == 0:
                dp.append(barras[k].indx)
        return dp
    
    def qbars(self):
        barras = self.__barras.bars
        rnb = range(self.__barras.nb)
        dq = []
        for k in rnb:
            if barras[k].oetg == 0:
                dq.append(barras[k].indx)
        return dq