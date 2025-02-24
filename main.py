from src.functions.leitura import lerAna, lerY
from src.models.potencia import  Scomplex
from numpy import linalg

epslon = 0.001
barras,linhas = lerAna("IEEE_03B")
ybus = linhas.ybus(barras)
potencia = Scomplex(ybus,barras)
    
# print("###")
# print(lerY(ybus))

print("###")
print(barras)

for i in range(100):
    variacoes = potencia.erros()
    # print(f"{i}: {potencia.erros()}")
    if max(abs(var) for var in variacoes) < epslon: break
    jac = potencia.jacob()
    # print(lerY(jac))
    sol = linalg.solve(jac,variacoes).tolist()
    barras.updatebar(sol)
barras.update2(potencia.pots())

# print(potencia.erros())
# print("###")
    
print(barras)
print("###")