from src.models.potencia import  Scomplex
from numpy import linalg

def newt_raph(barras,linhas,eps):
    ybus = linhas.ybus(barras)
    potencia = Scomplex(ybus,barras)

    err = potencia.erros()
    jac = potencia.jacob()
    ijac = -linalg.inv(jac)
    sol = []
    for lin in ijac.tolist():
        ss = 0
        for k in range(len(lin)):
            ss+= lin[k]*err[k]
        sol.append(ss)
    barras.updatebar(sol)

    for ç in range(1000):
        proba = barras.controlar()
        err = potencia.erros()
        probb = (max(abs(var) for var in err)< eps)
        
        if   probb and proba: break
        
        jac = potencia.jacob()
        ijac = -linalg.inv(jac)
        sol = []
        for lin in ijac.tolist():
            ss = 0
            for k in range(len(lin)):
                ss+= lin[k]*err[k]
            sol.append(ss)
        
        barras.updatebar(sol)
        barras.update2(potencia.pots())
        
        if ç == 998: print("maximo de iteracoes")
    return barras