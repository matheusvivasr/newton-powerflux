from src.functions.leitura import lerAna
from src.functions.newtonit import newt_raph
from src.models.potencia import  Scomplex
from numpy import linalg


epslon = 0.001
barras,linhas = lerAna("IEEE_14B")
ybus = linhas.ybus(barras)
potencia = Scomplex(ybus,barras)
err = potencia.pots()
for i in err: print(i)
# print(barras)
# print(linhas)
print(barras)
newt_raph(barras,linhas,epslon)
print()
print(barras)
print()

# jac = potencia.jacob()
# ijac = -linalg.inv(jac)
# sol = []
# for lin in ijac.tolist():
#     ss = 0
#     for k in range(len(lin)):
#         ss+= lin[k]*err[k]
#     sol.append(ss)
# barras.updatebar(sol)