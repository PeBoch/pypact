import os
import pypact as pp
import matplotlib.pyplot as plt

# the standard output file from FISPACT-II
# test files exist in 'references' directory

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '..', 'reference', 'test127.out')

times = []
values = []

with pp.Reader(filename) as output:
    for t in output.inventory_data:
        for n in t.nuclides:
            print(n.name)
      