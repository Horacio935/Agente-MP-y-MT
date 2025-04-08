# === Funciones base ===
import itertools

mapa_proposiciones = {}

def resetear_mapa():
    global mapa_proposiciones
    mapa_proposiciones = {}

def detectar_conector(enunciado):
    enunciado = enunciado.lower()
    if "si y solo si" in enunciado:
        return "↔"
    elif "si" in enunciado and "entonces" in enunciado:
        return "→"
    elif " y " in enunciado:
        return "∧"
    elif " o " in enunciado:
        return "∨"
    else:
        return None
    
def evaluar_formula_logica(formula, proposiciones):
    formula = formula.replace("∧", " and ").replace("∨", " or ").replace("→", " <= ").replace("↔", " == ")

    resultados = []
    variables = sorted(proposiciones)
    combinaciones = list(itertools.product([True, False], repeat=len(variables)))

    for valores in combinaciones:
        contexto = dict(zip(variables, valores))
        try:
            resultado = eval(formula, {}, contexto)
            resultados.append(resultado)
        except:
            return "Error al evaluar"

    if all(resultados):
        return "Tautología"
    elif not any(resultados):
        return "Contradicción"
    elif resultados.count(True) > 0 and resultados.count(False) > 0:
        return "Contingencia"
    else:
        return "Falacia"

def extraer_proposiciones(enunciado):
    enunciado = enunciado.lower().strip()
    conector = detectar_conector(enunciado)

    if conector == "→":
        partes = enunciado.replace("si", "").split("entonces")
        if len(partes) != 2:
            return None, None, None
        antecedente = partes[0].strip().capitalize()
        consecuente = partes[1].strip().capitalize()
        return antecedente, consecuente, conector
    elif conector in ["∧", "∨", "↔"]:
        if conector == "↔":
            partes = enunciado.split("si y solo si")
        elif conector == "∧":
            partes = enunciado.split(" y ")
        elif conector == "∨":
            partes = enunciado.split(" o ")
        if len(partes) == 2:
            prop1 = partes[0].strip().capitalize()
            prop2 = partes[1].strip().capitalize()
            return prop1, prop2, conector
        else:
            return None, None, None
    else:
        return None, None, None

def negar_enunciado(frase):
    palabras = frase.split()
    if len(palabras) > 1:
        palabras.insert(1, "no")
        return " ".join(palabras)
    else:
        return "No " + frase

def es_negacion(frase1, frase2):
    return frase2.lower() == negar_enunciado(frase1).lower()

def aplicar_inferencia(antecedente, consecuente, segunda_premisa):
    segunda_premisa = segunda_premisa.strip().capitalize()
    if segunda_premisa == antecedente:
        print(f"\nPremisa 1: Si {antecedente} entonces {consecuente}")
        print(f"Premisa 2: {segunda_premisa}")
        print(f"Conclusión: Por lo tanto, {consecuente} (MP)")
    elif es_negacion(consecuente, segunda_premisa):
        neg_antecedente = negar_enunciado(antecedente)
        print(f"\nPremisa 1: Si {antecedente} entonces {consecuente}")
        print(f"Premisa 2: {segunda_premisa}")
        print(f"Conclusión: Por lo tanto, {neg_antecedente} (MT)")
    else:
        print("No se pudo determinar la regla de inferencia a partir de la segunda premisa.")

def aplicar_modus_ponens(antecedente, consecuente):
    print(f"\nPremisa 1: Si {antecedente} entonces {consecuente}")
    print(f"Premisa 2: {antecedente}")
    print(f"Conclusión: Por lo tanto, {consecuente}")

def aplicar_modus_tollens(antecedente, consecuente):
    neg_consecuente = negar_enunciado(consecuente)
    neg_antecedente = negar_enunciado(antecedente)
    print(f"\nPremisa 1: Si {antecedente} entonces {consecuente}")
    print(f"Premisa 2: {neg_consecuente}")
    print(f"Conclusión: Por lo tanto, {neg_antecedente}")

def asignar_simbolo(proposicion):
    global mapa_proposiciones
    for simbolo, texto in mapa_proposiciones.items():
        if texto == proposicion:
            return simbolo
    if len(mapa_proposiciones) >= 3:
        return "?"
    nuevo_simbolo = chr(80 + len(mapa_proposiciones))  # P, Q, R
    mapa_proposiciones[nuevo_simbolo] = proposicion
    return nuevo_simbolo

def traducir_a_logica(enunciado):
    conector = detectar_conector(enunciado)
    enunciado = enunciado.strip().lower()

    if not conector:
        simbolo = asignar_simbolo(enunciado.capitalize())
        return simbolo, None

    if conector == "→":
        if "si" not in enunciado or "entonces" not in enunciado:
            return None, None
        partes = enunciado.split("entonces", 1)
        if len(partes) != 2:
            return None, None
        izquierda = partes[0].strip()
        if izquierda.startswith("si "):
            izquierda = izquierda[3:].strip()
        derecha = partes[1].strip()
    elif conector == "↔":
        partes = enunciado.split("si y solo si", 1)
    elif conector == "∧":
        partes = enunciado.split(" y ", 1)
    elif conector == "∨":
        partes = enunciado.split(" o ", 1)
    else:
        return None, None

    if len(partes) != 2:
        return None, None

    izquierda = partes[0].strip()
    derecha = partes[1].strip()
    simbolo_izq = asignar_simbolo(izquierda.capitalize())
    simbolo_der = asignar_simbolo(derecha.capitalize())
    return f"({simbolo_izq} {conector} {simbolo_der})", conector

# ==== Agente en ejecución continua ====

print("Agente de inferencia lógica (MP / MT / Traducción simbólica)")
print("Escribe 'salir' en cualquier momento para finalizar.\n")

while True:
    resetear_mapa()

    premisa1 = input("Introduce una premisa (Ej: 'Si A entonces B', 'A y B', 'A o B', 'A si y solo si B'):\n> ").strip()
    if premisa1.lower() == "salir":
        break

    if "por lo tanto" in premisa1.lower():
        print("Por favor, introduce las premisas antes de la conclusión.")
        continue

    premisa2 = input("Introduce 'MP', 'MT' o la segunda premisa directamente:\n> ").strip()
    if premisa2.lower() == "salir":
        break

    conector_detectado = detectar_conector(premisa1)

    if premisa2.upper() in ["MP", "MT"]:
        if conector_detectado != "→":
            print("❌ Error: Solo puedes aplicar MP o MT si la premisa es una implicación.")
            continue

        antecedente, consecuente, conector = extraer_proposiciones(premisa1)
        if not antecedente or not consecuente or not conector:
            print("❌ La premisa no tiene el formato correcto para MP/MT (debe ser 'Si A entonces B').")
            continue

        if premisa2.upper() == "MP":
            aplicar_modus_ponens(antecedente, consecuente)
        elif premisa2.upper() == "MT":
            aplicar_modus_tollens(antecedente, consecuente)

    else:
        tercera = input("¿Deseas escribir la conclusión manualmente o escribir 'confirmar' para que el agente determine si es MP o MT?\n> ").strip().lower()
        if tercera == "salir":
            break

        if tercera.startswith("por lo tanto"):
            conclusion = tercera[len("por lo tanto"):].strip().capitalize()

            f1, c1 = traducir_a_logica(premisa1)
            f2, c2 = traducir_a_logica(premisa2)
            f3, c3 = traducir_a_logica(conclusion)

            if not f1 or not f2 or not f3:
                print("No se pudo traducir una de las oraciones.")
                continue

            formula_final = f"({f1} ∧ {f2}) → {f3}"

            print("\n🔍 Traducción simbólica:")
            for simbolo, frase in mapa_proposiciones.items():
                print(f"{simbolo} ↔ {frase}")
            print(f"\nFórmula lógica completa:\n{formula_final}")
            propos = set([ch for ch in formula_final if ch in "PQR"])
            tipo_formula = evaluar_formula_logica(formula_final, propos)
            print(f"\n🧠 Clasificación lógica: {tipo_formula}")


        elif tercera == "confirmar":
            if conector_detectado != "→":
                print("❌ Solo puedes confirmar inferencia automática si la primera premisa es una implicación.")
            else:
                antecedente, consecuente, conector = extraer_proposiciones(premisa1)
                if not antecedente or not consecuente or not conector:
                    print("❌ La premisa no tiene el formato correcto para MP/MT (debe ser 'Si A entonces B').")
                    continue
                aplicar_inferencia(antecedente, consecuente, premisa2)

        else:
            print(f"\nPremisa 1: {premisa1}")
            print(f"Premisa 2: {premisa2}")
            print(f"Conclusión: Por lo tanto, {tercera.capitalize()}")
            print("Nota: No se verificó si la conclusión es válida.")

    print("\n---------------------------------------------\n")

