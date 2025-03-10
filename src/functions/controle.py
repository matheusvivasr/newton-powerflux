

def tensoesQ(barrass):
        # se for uma barra PV que exede os limites de Q,
        # marcamos a barra como PQ e fixamos Q em seu limite
    for b in barrass:
        limi = b.rngQ[0]
        lima = b.rngQ[1]
        if   (b.tipo == 1) and (b.spq.imag < limi):
            b.tipo = 0
            b.spq = b.spq.real +1j* limi
        elif (b.tipo == 1) and (b.spq.imag > lima):
            b.tipo = 0
            b.spq = b.spq.real +1j* lima
    return barrass