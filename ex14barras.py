from src.functions.leitura import lerAna
from src.functions.newtonit import newt_raph

epslon = 0.001
barras,linhas = lerAna("IEEE_30B")

print(barras)
newt_raph(barras,linhas,epslon)
print(barras)
