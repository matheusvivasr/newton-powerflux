## colunas do dbar
# 0 (Num)
# 1 OETGb
# 2 (   nome   )
# 3 Gl
# 4 ( V)
# 5 ( A)
# 6 ( Pg)
# 7 ( Qg)
# 8 ( Qn)
# 9 ( Qm)
# 0 (Bc  )
# 1 ( Pl)
# 2 ( Ql)
# 3 ( Sh)
# 4 Are
# 5 (Vf)

class Barra():
    def __init__(self, dados):
        for chave, valor in dados.items():
            setattr(self, chave, valor)
        self.updt

    def updt(self, chave, novo_valor):
        if hasattr(self, chave):
            setattr(self, chave, novo_valor)
        else:
            print(f"Atributo '{chave}' não encontrado.")


