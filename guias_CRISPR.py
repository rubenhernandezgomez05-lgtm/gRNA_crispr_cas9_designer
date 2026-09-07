#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Definición de secuencia y contenedor de resultados

def obtencion_secuencia_diana():
    """Recibe la secuencia diana en forma de cadena de texto o como archivo .txt. 
    En ambos casos, estandariza a mayúsculas y devuelve la secuencia limpia."
    """

    entrada = input(
        """Pega aquí la secuencia de ADN o el nombre del archivo (.txt).
        Si deseas hacer un ejemplo rápido de prueba, introduce la siguiente secuencia
        obtenida de la base de datos SGD (DOG2, SGD:S000001085): 
ATGCCACAATTTTCAGTAGATCTTTGTCTTTTTGACCTAGATGGGACTATTGTCAGCACA
ACAACTGCAGCGGAAAGTGCCTGGAAAAAATTATGCCGTCAGCATGGGGTTGATCCTGTT
GAGTTATTCAAGCATTCCCATGGTGCAAGATCACAAGAAATGATGAAGAAATTTTTTCCA
AAATTGGACAATACCGATAATAAAGGTGTTCTTGCGTTAGAAAAGGATATGGCAGATAAT
TATTTGGACACAGTAAGCCTTATCCCTGGTGCAGAGAATTTATTGTTATCGTTAGATGTA
GATACTGAGACTCAAAAAAAGTTACCTGAAAGGAAATGGGCTATCGTTACCTCTGGTTCT
CCATATTTGGCATTTTCATGGTTCGAGACAATATTGAAAAATGTTGGAAAGCCCAAAGTT
TTCATTACTGGATTTGACGTGAAGAACGGTAAGCCTGATCCCGAGGGTTACTCAAGAGCT
CGTGATTTATTGCGTCAAGATTTGCAATTAACTGGTAAACAGGATCTGAAGTATGTTGTC
TTTGAAGATGCACCCGTGGGCATAAAGGCCGGCAAAGCAATGGGCGCAATTACTGTGGGT
ATAACATCCTCGTATGATAAGAGCGTTTTATTTGACGCAGGTGCAGATTATGTGGTCTGT
GATTTGACACAGGTTTCCGTGGTTAAGAACAATGAGAACGGTATCGTTATCCAGGTAAAC
AACCCTTTGACGAGAGATTAA.""").strip()



    if entrada.lower().endswith(".txt"):
        try:
            with open(entrada,"r") as archivo:
                secuencia_diana = archivo.read().replace("\n","").replace("\r","").strip().upper()
            print(f"Secuencia cargada exitosamente desde '{entrada}'.")
            return secuencia_diana

        except FileNotFoundError:
            raise FileNotFoundError(f"ERROR: No se encontró el archivo '{entrada}'. Deteniendo ejecución.")

    else:
        secuencia_diana = entrada.replace(" ","").upper()
        print("Secuencia recibida. Iniciando programa de diseño de guías CRISPR.")
        return secuencia_diana


secuencia_diana = obtencion_secuencia_diana()
guias_candidatas=[]

# Escaneo de la secuencia diana para buscar motivos PAM (NGG)

for i in range(len(secuencia_diana)-1):
    if secuencia_diana[i : i + 2] == "GG":
        if i >= 20:
            sec_guia = secuencia_diana[i - 20 : i]
            pam_sec = secuencia_diana[i : i + 3]
            guia = {
                "posicion": i - 20,
                "secuencia": sec_guia,
                "pam": pam_sec,
            }

            guias_candidatas.append(guia)
            print(f"PAM encontrada en posición {i}: {pam_sec}")
            print(f"Secuencia guía (20pb): {sec_guia}\n")
        else:
            print(f"PAM encontrada en posición {i}, pero no hay pares de bases previos suficientes.")

# En este bloque se define la función que evaluará cada guia posible de la lista creada anteriormente.
# Para ello, se calcula el porcentaje de Guanina-citosina (%GC), se comprueba que la guia no contiene
# una señal de terminación para la Pol III (esto es, tramos TTTT) y crea una variable booleana
# que adquiere el valor True en caso de que se cumpla que el porcentaje GC está entre el 40% y el 60%
# y si no contiene tramos TTTT. La función devuelve finalmente el porcentaje %GC y si la guia es válida o no.

def evaluacion_calidad(sec_guia):
    """Evalúa la calidad de una guía CRISPR de 20pb.
    Devuele el porcentaje de GC y un booleano indicando si es válida.
    """
    conteo_g = sec_guia.count("G")
    conteo_c = sec_guia.count("C")
    percent_gc = round((conteo_g + conteo_c)/len(sec_guia)*100, 2)


    gc_valido = 40 <= percent_gc <= 60
    sin_poli_t = "TTTT" not in sec_guia 

    es_valida = gc_valido and sin_poli_t

    return percent_gc, es_valida

# Función para exportar los resultados a un archivo de texto.
def exportar_guias_aprobadas(guias_candidatas, nombre_archivo="guias_aprobadas.txt"):

    guias_aprobadas = [x for x in guias_candidatas if x["es_valida"]]

    if not guias_aprobadas:
        print(
        """\nNo hay guías aprobadas para exportar. El archivo no se ha creado.
        \n Revise la lista de guias no aprobadas en caso de que alguna pueda ser utilizada
        según las condiciones de su experimento.
        """)
        return

    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("=== INFORME DE GUÍAS CRISPR-Cas9 APROBADAS ===\n")
        archivo.write(f"Total de candidatos analizados: {len(guias_candidatas)}\n")
        archivo.write(f"Total de candidatos aprobados: {len(guias_aprobadas)}\n")
        archivo.write("=" * 48 + "\n\n")
        archivo.write(f"{"Posición":<10} | {"Guía (20 pb)":<22} | {"PAM":<5} | {"%GC":<7}\n")
        archivo.write("-" * 52 + "\n")

        for g in guias_aprobadas:
          archivo.write(f"{g["posicion"]:<10} | {g["secuencia"]:<22} | {g["pam"]:<5} |{g["porcentaje_gc"]}%\n")
    print(f"\n Éxito: Se han exportado {len(guias_aprobadas)} guías aprobadas en {nombre_archivo}.\n\n")

# Finalmente, este bloque extrae las variables de la función de evaluación y las añade a cada guia; otorga el valor de "aprobada" o "descartada" 
# según la variable de validez definida anteriormente. 

for guia in guias_candidatas:
    percent_gc, valida = evaluacion_calidad(guia["secuencia"])

    guia["porcentaje_gc"] = percent_gc
    guia["es_valida"] = valida

# Ordenación: las guias válidas aparecerán las primeras.

guias_candidatas.sort(key=lambda x: x["es_valida"], reverse=True)

# Imprime un informe final con las guías encontradas, informando de su posición en la secuencia
# inicial, la secuencia PAM, la secuencia de la guia, el porcentaje de GC y su estado (aprobada o descartada).

print ("=== INFORME DE GUÍAS CRISPR ENCONTRADAS ===\n")
for x in guias_candidatas:
    estado = "APROBADA" if x["es_valida"] else "DESCARTADA"
    print(f"Posición: {x['posicion']} | Guía: {x['secuencia']} | PAM: {x['pam']} |"
      f" %GC: {x['porcentaje_gc']}% | Estado: {estado}")

# Decisión sobre crear archivo con los resultados.

crear_doc = input("¡Muchas gracias por probar el programa!¿Deseas guardar las guías aprobadas en un archivo .txt? (S/N):").strip().lower()

if crear_doc == "s":
    nombre_archivo = input(
    "Nombre del archivo [Presiona Enter para 'guias_aprobadas.txt']: ").strip()
    if nombre_archivo:
        if not nombre_archivo.lower().endswith(".txt"):
            nombre_archivo += ".txt"
        exportar_guias_aprobadas(guias_candidatas, nombre_archivo)
    else:
        exportar_guias_aprobadas(guias_candidatas)
else:
    print("¡De acuerdo! Muchas gracias.")


# In[ ]:




