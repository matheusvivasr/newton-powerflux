import re
from src.models.barras import  Barras
from src.models.linhas import Linhas
def lerAna(file:str='IEEE_TTB'):
    path = 'src/documents/'+file+'.txt'
    with open(path,'r') as arq:
        doc = arq.read()
    
    Dcte = constantes(doc)
    
    Dbar = Barras(barras(doc))
    
    Dlin = Linhas(linhas(doc))

    return Dbar, Dlin

def barras(conteudo):
    rgx = r"DBAR(.*?)99999\n"
    tabela = re.search(rgx, conteudo, re.DOTALL).group(1).split('\n')
    rgx = r"((\(\w*\))|((?<=\))\w+(?=\())|(\(\s*\w+\s*\)))"
    head = [len(a[0]) for a in re.findall(rgx,tabela[1])]

    tabela = tabela[2:-1]
    ntabela = []
    for linha in tabela:
        ini = 0
        nlinha = []
        for colw in head:
            fim = ini+colw
            v = linha[ini:fim].strip()
            try: v = float(v)
            except ValueError: 
                if v == '': v= None
                else: v = linha[ini:fim].strip()

            nlinha.append(v)
            ini = fim
        ntabela.append(nlinha)
    tabela = ntabela
    return tabela

def linhas(conteudo):
    rgx = r"DLIN(.*?)99999"
    tabela = re.search(rgx, conteudo, re.DOTALL).group(1).split('\n')

    rgx = r"((\(\w*\))|((?<=\))\w+(?=\())|((?<=\))\w+))"
    # FAVOR ATUALIZAR AQUI CASO DE MERDA \/
    head = "(aaa)aaaaa(aaa)aaaaa(aaaa)(aaaa)(aaaa)(aaa)(aaa)(aaa)(aaa)(aaaa)(aa)(aa)aa"
    # print(re.findall(rgx,head))
    head = [len(a[0]) for a in re.findall(rgx,head)]
    # print(head)
    
    tabela = tabela[2:-1]
    ntabela = []
    for linha in tabela:
        ini = 0
        nlinha = []
        for colw in head:
            fim = ini+colw
            v = linha[ini:fim].strip()
            try: v = float(v)
            except ValueError: 
                if v == '': v= None
                else: v = linha[ini:fim].strip()
            nlinha.append(v)
            ini = fim
            
        ntabela.append(nlinha)
    tabela = ntabela
    return tabela

def constantes(conteudo):
    rgx = r"DCTE(.*?)99999"
    tabela = re.search(rgx, conteudo, re.DOTALL).group(1).strip()

    ctes = []
    itens = ['BASE', 'DASE']
    for ct in itens:
        ctes.append(valor(ct, tabela))

    ctes[0] = int(ctes[0])*(10**6)
    ctes[1] = int(ctes[1])
    ctes.append((ctes[0]/ctes[1])**0.5)
    ctes.append((ctes[2]/ctes[1]))
    ctes[0] = ctes[0]/(10**6)
    # print(ctes)
    return ctes

def valor(nome:str, conteudo):
    rgx = r"(?<="+nome+r")\W*\d*"
    val = re.search(rgx,conteudo,re.DOTALL).group(0).strip()
    return val

def lerY(ybus):
    rnb = range(len(ybus))
    lin = ""
    for k in rnb:
        for m in rnb:
            if k <= m:
                lin += f"({k+1}, {m+1}): {ybus[k][m]}\n"
    return lin 