import math
from py2scad import *

# Base size
baseX = 11.0*INCH2MM
baseY = 11.0*INCH2MM
baseZ = 6.0

params = { 
        'baseSize'                    : (11.0*INCH2MM, 11.0*INCH2MM, 6.0), 
        'baseCornerRadius'            : 0.25*INCH2MM,
        'pulleyDiameter'              : 2.0*INCH2MM, 
        'bearingHoleDiameter'         : 0.5*INCH2MM,
        'numBearing'                  : 3, 
        'standoffDiameter'            : (5.0/8.0)*INCH2MM,
        'standoffMargin'              : 0.2,
        'standoffHoleDiameter'        : 0.2570*INCH2MM,
        'pulleyMargin'                : 0.2,
        'stepperHoleSpacing'          : 1.85*INCH2MM,
        'stepperSlotWidth'            : 0.196*INCH2MM,
        'stepperSlotLength'           : 1.5*INCH2MM,
        'clampHubMountHoleSpacing'    : (0.77/math.sqrt(2.0))*INCH2MM,
        'clampHubMounttHoleDiameter'  : 0.144*INCH2MM,
        'clampHubCenterHoleDiameter'  : 0.5*INCH2MM,
        'swivelHubNumMountHole'       : 8, 
        'swivelHubMountHoleDiameter'  : 0.144*INCH2MM,
        'swivelHubMountRingDiameter'  : 0.77*INCH2MM,
        'swivelHubCenterHoleDiameter' : 0.5*INCH2MM,
        'clampToSwivelHubSeparation'  : 1.0*INCH2MM,
        'hubAdapterCornerRadius'      : 0.25*INCH2MM,
        'hubAdapterSizeMargin'        : 0.15*INCH2MM,              
        'hubAdapterThickness'         : 6.0,
        'orbitalPlateSize'            : (11.0*INCH2MM, 11.0*INCH2MM, 6.0), 
        'orbitalPlateRadius'          : 0.25*INCH2MM,
        }


"""
Notes:

    bearingHoleDiameter - needs to be just a tiny bit smaller so that the bearing fit is tighter.

"""

