"""
Orbital shaker belt length calculation
"""
from __future__ import print_function
import math

distBigToBigPulley = 7.5
distBigToSmallPulleyMin = 4.0
distBigToSmallPulleyMax = 5.5
diamBigPulley = 1.765
diamSmallPulley = 0.87

circBigPulley = math.pi*diamBigPulley
circSmallPulley = math.pi*diamSmallPulley

# Find minimum belt length
beltLengthMin  = 2*distBigToBigPulley
beltLengthMin += 2*distBigToSmallPulleyMin
beltLengthMin += 3*0.5*circBigPulley
beltLengthMin += 0.5*circSmallPulley

# Find maximum belt length
beltLengthMax  = 2*distBigToBigPulley
beltLengthMax += 2*distBigToSmallPulleyMax
beltLengthMax += 3*0.5*circBigPulley
beltLengthMax += 0.5*circSmallPulley

print('minimum belt length: ', beltLengthMin)
print('maximum belt legnth: ', beltLengthMax)


print(3*distBigToBigPulley + 3*0.5*circBigPulley)




