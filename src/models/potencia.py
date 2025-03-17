class Scomplex():
    def __init__(self,ybus,barras):
        self.__ybus = ybus
        self.__barras = barras

    def correntes(self):
        Ib = []
        barras = self.__barras.bars
        yy = self.__ybus
        for k in range(self.__barras.nb):
            Ik = 0
            for m in range(self.__barras.nb):
               if yy[k][m] != 0:
                Ikm = barras[m].Eb() * yy[k][m] 
                Ik += Ikm
            Ib.append(Ik)
        return Ib
    
    def pots(self):
        Ik = self.correntes()
        Sb = [0 for ç in range(len(Ik))]
        dbar = self.__barras.bars

        for k in range(self.__barras.nb):
            Sb[k] = dbar[k].Eb() * Ik[k].conjugate()
        return Sb

    def erros(self): 
        potout = []
        pots = self.pots() 
        dbar = self.__barras.bars
        for barra in dbar:
            if barra.tipo == 1 or barra.tipo == 0:
                pot = barra.spq.real - pots[barra.indx].real
                potout.append(pot)
        for barra in dbar:
            if barra.tipo == 0:
                pot = barra.spq.imag - pots[barra.indx].imag
                potout.append(pot)
        return potout
    
    def erros2(self): 
        potout = [0j for ç in range(self.__barras.nb)]
        pots = self.pots() 
        dbar = self.__barras.bars
        for k in range(self.__barras.nb):
            potout[k] = dbar[k].spq - pots[k]
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
            if barras[k].tipo == 1 or barras[k].tipo == 0:
                dp.append(barras[k].indx)
        return dp
    
    def qbars(self):
        barras = self.__barras.bars
        rnb = range(self.__barras.nb)
        dq = []
        for k in rnb:
            if barras[k].tipo == 0:
                dq.append(barras[k].indx)
        return dq