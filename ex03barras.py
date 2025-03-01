from src.functions.leitura import lerAna
from src.models.potencia import  Scomplex
from numpy import linalg

epslon = 0.001
barras,linhas = lerAna("IEEE_03B")
ybus = linhas.ybus(barras)
potencia = Scomplex(ybus,barras)

for i in range(1):
    err = potencia.erros()
    if max(abs(var) for var in err) < epslon: break
    jac = potencia.jacob()
    if i == 0:
        for l in jac: print(l)
    ijac = -linalg.inv(jac)
    sol = (ijac @ err).tolist()
    barras.updatebar(sol)
barras.update2(potencia.pots())