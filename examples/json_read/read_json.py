import os
import json
#python package for fispact output
import pypact as pp
import matplotlib.pyplot as plt

# read json output file
filename1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inventory.json')

with pp.JSONReader(filename1) as output:
    for t in output.inventory_data:             
        for n in t.nuclides:
            print(n.name, n.half_life)