from src.functions.leitura import lerAna, lerY
from src.models.potencia import  Scomplex
from numpy import linalg

epslon = 0.001
barras,linhas = lerAna("IEEE_14B")
ybus = linhas.ybus(barras)
potencia = Scomplex(ybus,barras)

for i in range(13):
    err = potencia.erros()
    if max(abs(var) for var in err) < epslon: break
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

print(barras)
print()
print(f"{i+1}: {max(abs(var) for var in err)}")
