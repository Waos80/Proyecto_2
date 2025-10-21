import analisis

def LeerArchivo(ruta: str) -> str:
    info = ""
    with open(ruta, "r") as f:
        info = f.read()

    return info


if __name__ == "__main__":
    digito = list("0123456789")
    OP = ["SUMA", "RESTA", "MULTIPLICACION", "DIVISION", "POTENCIA", "RAIZ", "INVERSO", "MOD"]
    
    automata = analisis.AFD()
    automata.crearEstados(
        [False, False, False, True, False, False, False, False, False, False, False, False, True, True, True, True, True]
    )

    automata.crearTransiciones({
        0: [
            (['<'], 1),
            (['-'], 2),
            (digito, 3),
        ],
        1: [
            (["Operacion= "], 4),
            (['/'], 5),
            (["Numero"], 6),
        ],
        2: [
            (digito, 3)
        ],
        3: [
            (digito, 3),
            (['.'], 7)
        ],
        4: [
            #([' '], 4),
            (OP, 8)
        ],
        5: [
            #([' '], 9),
            (["Operacion"], 10),
            (["Numero"], 11)
        ],
        6: [
            #([' '], 6),
            (['>'], 12)
        ],
        7: [
            (digito, 13)
        ],
        8: [
            #([' '], 8),
            (['>'], 14)
        ],
        9: [
            #([' '], 9),
            (["Operacion"], 10)
        ],
        10: [
            #([' '], 10),
            (['>'], 15)
        ],
        11: [
            #([' '], 11),
            (['>'], 16)
        ],
        13: [
            (digito, 13)
        ],
    })

    info = LeerArchivo("./Entrada1.txt")
    tabla = {
        3: "numero",
        12: "an",
        13: "numero",
        14: "ao",
        15: "co",
        16: "cn"
    }

    l = analisis.Lexico(automata, tabla)
    l.ProcesarEntrada(info)
    print(l.tokens)