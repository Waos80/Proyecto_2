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
        [False, False, False, True, 
         False, False, False, False, 
         False, False, False, True, 
         True, True, True, True]
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
            (OP, 8)
        ],
        5: [
            (["Operacion"], 9),
            (["Numero"], 10)
        ],
        6: [
            (['>'], 11)
        ],
        7: [
            (digito, 12)
        ],
        8: [
            (['>'], 13)
        ],
        9: [
            (['>'], 14)
        ],
        10: [
            (['>'], 15)
        ],
        12: [
            (digito, 12)
        ]
    })

    info = LeerArchivo("./Entrada1.txt")
    tabla = {
        3: "numero",
        11: "an",
        12: "numero",
        13: "ao",
        14: "co",
        15: "cn",
    }

    l = analisis.Lexico(automata, tabla)
    l.ProcesarEntrada(info)
    print(l.tokens)
