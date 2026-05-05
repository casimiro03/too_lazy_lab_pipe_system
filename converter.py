import csv
import math
from typing import TypedDict, Generator
from functools import reduce

"""
n = number of divitions of the movile ruler
A = instrument apreciation
LP = principal lecture
"""

# we stablish the global contract for the measurement lecture
class Measurement(TypedDict):
    LP: float
    A: float
    n: int

def calculate_measurement(m: Measurement) -> float:
    """ Calculate the measurement using caliber formula """
    return m['LP'] + (m['A']) * m['n']

def parse_row(row):
    # We convert into float the value of the row
    return {
        'LP': float(row['Lp']),
        'A': float(row['A']),
        'n': float(row['n']),

    }

def compositor(*functions):
    "Create a function composing other ones f(g(x)) like in blender"
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

pipeline_logic = compositor(calculate_measurement, parse_row)

def get_processed_stream(filepath: str):
    """ Extract each row element using a mouting line"""
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Shield it's a generator. shield avoid the memory overflow when we have a big csv file, because it will read one row at a time and yield the result, instead of loading the entire file into memory. its like a cinta transportadora
            yield pipeline_logic(row)

# 7. El Sink: Persistencia en TXT [LO QUE TE FALTABA]
def save_to_txt(stream: Generator, output_path: str):
    """Consume el generador y persiste los datos en un archivo plano"""
    with open(output_path, mode='w', encoding='utf-8') as file:
        file.write("--- RESULTADOS LABORATORIO FÍSICA ---\n")
        for i, val in enumerate(stream, 1):
            file.write(f"Medición {i:02}: {val:.3f} mm\n")
    print(f"✅ Pipeline completado. Resultados en: {output_path}")

path = '/home/casimirx/Projects/too_lazy_lab_pipe_system/data/sample.csv'
target_path = '/home/casimirx/Projects/too_lazy_lab_pipe_system/data/results.txt'

# Ejecución de Arquitecto
if __name__ == "__main__":
    try:
        data_stream = get_processed_stream(path)
        save_to_txt(data_stream, target_path)
    except FileNotFoundError:
        print(f"❌ Error: No encontré el archivo {target_path}")
    except Exception as e:
        print(f"⚠️ Glitch en la matriz: {e}")


  

"""
choose datalcass or typedict 
what's messing the pipiline parts that read the headers, extract each and
operate writing over each row and paste it into a txt file

i want implement an algorithm that operate over each header using function composition

"""
