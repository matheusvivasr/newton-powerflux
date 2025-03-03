from src.models.potencia import  Scomplex
from numpy import linalg

def newt_raph(barras,linhas,eps):
    ybus = linhas.ybus(barras)
    potencia = Scomplex(ybus,barras)
    for i in range(19):
        err = potencia.erros()
        if max(abs(var) for var in err) < eps: break
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
    return barras