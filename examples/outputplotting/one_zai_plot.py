import os
import pypact as pp
import matplotlib.pyplot as plt

# the standard output file from FISPACT-II
# test files exist in 'references' directory

filename1 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '..', 'reference', 'first.out')

filename2 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '..', 'reference', 'second_modif.out')

times1 = []
times2 = []
values1 = []
values2 = []

property1 = "atoms"

with pp.Reader(filename1) as output:

   
   for t in output.inventory_data:
                
        for n in t.nuclides:
            if(n.name=="Am241"):
                value1 = getattr(n, property1)
                times1.append(t.irradiation_time + t.cooling_time)
                values1.append(value1)
            if(n.name=="Cs137"):
                value2 = getattr(n, property1)
                times2.append(t.irradiation_time + t.cooling_time)
                values2.append(value2)

lastCumTime1 = times1[-1]

lastCumTime2 = times2[-1]

with pp.Reader(filename2) as output:
    
   for t in output.inventory_data:
                
        for n in t.nuclides:
            if(n.name=="Am241"):
                value1 = getattr(n, property1)
                times1.append(t.irradiation_time + t.cooling_time + lastCumTime1)
                values1.append(value1)    

            if(n.name=="Cs137"):
                value2 = getattr(n, property1)
                times2.append(t.irradiation_time + t.cooling_time + lastCumTime2)
                values2.append(value2)    


plt.loglog(times1, values1, "-b", label="Am241")
plt.loglog(times2, values2, "-g", label="Cs137")

plt.legend(loc="upper left")
plt.xlabel("time (s)")
plt.ylabel("atoms (-)")
plt.savefig("graph02.png")
plt.show() 