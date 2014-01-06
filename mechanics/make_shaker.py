from __future__ import print_function
import math
import scipy
from py2scad import *
from params import params

class OrbitalShaker(object):

    """ Base class for orbital shaker """

    def __init__(self, params):
        self.params = params
        self.addHoles()
        self.createPart()

    def addHoles(self):
        self.holeList = []

    def createPart(self):
        pass

    def getBearingHolePosList(self):
        x,y,z = self.params['baseSize']
        holeDiam = self.params['bearingHoleDiameter']
        pulleyDiam = self.params['pulleyDiameter']
        margin = self.params['pulleyMargin']
        numBearing = self.params['numBearing']
        angle = (math.pi/180.0)*360.0/float(numBearing)
        phase = (math.pi/180.0)*00.0
        radius = 0.5*min([x,y]) - 0.5*pulleyDiam*(1.0+margin)

        holeXList, holeYList = [], [] 
        for i in range(numBearing):
            holeX = radius*math.cos(i*angle + phase)
            holeY = radius*math.sin(i*angle + phase)
            holeX = round(holeX,5)
            holeY = round(holeY,5)
            holeXList.append(holeX)
            holeYList.append(holeY)

        holeXMean = scipy.array(list(set(holeXList))).mean()
        holeYMean = scipy.array(list(set(holeYList))).mean()
        holeXList = [val - holeXMean for val in holeXList]
        holeYList = [val - holeYMean for val in holeYList]
        holePosList = zip(holeXList, holeYList)
        return holePosList

    def getSwivelHubMountHoleRelPosList(self):
        numMountHole = self.params['swivelHubNumMountHole']
        mountHoleRingDiam = self.params['swivelHubMountRingDiameter']
        holeAngleStep = (math.pi/180.0)*(360.0/numMountHole)
        relPosList = []
        for i in range(numMountHole):
            holeAngle = i*holeAngleStep
            xPos = 0.5*mountHoleRingDiam*math.cos(holeAngle)
            yPos = 0.5*mountHoleRingDiam*math.sin(holeAngle)
            relPosList.append((xPos,yPos))
        return relPosList

    def __str__(self):
        return self.part.__str__()

    def projection(self):
        return Projection(self.part)


class BasePlate(OrbitalShaker):

    """ Obrital shaker base plate """

    def __init__(self,params):
        super(BasePlate,self).__init__(params)
       
    def createPart(self):
        super(BasePlate,self).createPart()
        x,y,z = self.params['baseSize']
        radius = self.params['baseCornerRadius']
        self.part = plate_w_holes(x,y,z,self.holeList,radius=radius)

    def addHoles(self):
        super(BasePlate,self).addHoles()
        self.addStandoffHoles()
        self.addBearingHoles()

    def addStandoffHoles(self):
        x,y,z = self.params['baseSize']
        standoffDiam = self.params['standoffDiameter']
        margin = self.params['standoffMargin']
        holeDiam = self.params['standoffHoleDiameter']
        for i in (-1,1):
            for j in (-1,1):
                delta = 0.5*standoffDiam*(1.0 + margin)
                holeX = i*(0.5*x - delta)
                holeY = j*(0.5*y - delta)
                hole = (holeX, holeY, holeDiam)
                self.holeList.append(hole)

    def addBearingHoles(self):
        holeDiam = self.params['bearingHoleDiameter']
        for holeX, holeY in self.getBearingHolePosList():
            hole = (holeX, holeY, holeDiam)
            self.holeList.append(hole)

class BasePlateLower(BasePlate):

    """ Orbital Shaker lower base plate """

    def __init__(self,params):
        super(BasePlateLower,self).__init__(params)
        self.createStepperSlots()

    def createStepperSlots(self):
        x,y,z = self.params['baseSize']
        holeDiam = self.params['bearingHoleDiameter']
        width = self.params['stepperSlotWidth'] 
        length = self.params['stepperSlotLength'] 
        spacing = self.params['stepperHoleSpacing']

        slotCube = Cube(size=(length + spacing,width, 2*z))
        slotCyl = Cylinder(r1=0.5*width, r2=0.5*width, h=2*z)
        slotCylPos = Translate(slotCyl,v=(0.5*(length+spacing),0,0))
        slotCylNeg = Translate(slotCyl,v=(-0.5*(length+spacing),0,0))
        slotCutBase = Union([slotCube, slotCylPos, slotCylNeg])

        slotCutList = []
        for j in (-1,1):
            xPos = 0.0
            yPos = 0.5*j*spacing
            slotCut = Translate(slotCutBase,v=(xPos,yPos,0))
            slotCutList.append(slotCut)

        diffList = [self.part] + slotCutList
        self.part = Difference(diffList)
            

class HubAdapterPlate(OrbitalShaker):

    def __init__(self, params):
        super(HubAdapterPlate,self).__init__(params)

    def addHoles(self):
        super(HubAdapterPlate,self).addHoles()
        self.addClampHubHoles()
        self.addSwivelHubHoles()

    def addClampHubHoles(self):
        x,y,z = self.getPlateSize()
        separation = self.params['clampToSwivelHubSeparation'] 
        mountHoleSpacing = self.params['clampHubMountHoleSpacing']  
        mountHoleDiam  = self.params['clampHubMounttHoleDiameter'] 
        centerHoleDiam = self.params['clampHubCenterHoleDiameter']

        # Mount holes
        for i in (-1,1):
            for j in (-1,1):
                xPos = -0.5*separation + i*0.5*mountHoleSpacing
                yPos = j*0.5*mountHoleSpacing
                hole = (xPos, yPos, mountHoleDiam)
                self.holeList.append(hole)

        # Center Hole
        xPos = -0.5*separation
        yPos = 0.0
        hole = (xPos, yPos, centerHoleDiam)
        self.holeList.append(hole)

    def addSwivelHubHoles(self):
        x,y,z = self.getPlateSize()
        separation = self.params['clampToSwivelHubSeparation'] 
        mountHoleDiam = self.params['swivelHubMountHoleDiameter']
        centerHoleDiam = self.params['swivelHubCenterHoleDiameter']

        for xPosRel, yPosRel in self.getSwivelHubMountHoleRelPosList():
            xPos = xPosRel + 0.5*separation
            yPos = yPosRel
            hole = (xPos, yPos, mountHoleDiam)
            self.holeList.append(hole)

        # Center hole
        xPos = 0.5*separation
        yPos = 0.0
        hole = (xPos, yPos, centerHoleDiam)
        self.holeList.append(hole)

    def createPart(self):
        super(HubAdapterPlate,self).createPart()
        radius = self.params['hubAdapterCornerRadius']
        x, y, z = self.getPlateSize()
        self.part = plate_w_holes(x,y,z,self.holeList,radius=radius)

    def getPlateSize(self):
        margin = self.params['hubAdapterSizeMargin']
        thickness = self.params['hubAdapterThickness']
        separation = self.params['clampToSwivelHubSeparation'] 
        clampHubMountHoleSpacing = self.params['clampHubMountHoleSpacing']  
        clampHubMountHoleDiam  = self.params['clampHubMounttHoleDiameter'] 
        swivelHubMountHoleDiam = self.params['swivelHubMountHoleDiameter'] 
        swivelHubMountRingDiam = self.params['swivelHubMountRingDiameter'] 
        x  = separation
        x += 0.5*clampHubMountHoleSpacing + 0.5*clampHubMountHoleDiam + margin
        x += 0.5*swivelHubMountRingDiam + 0.5*swivelHubMountHoleDiam + margin
        clampHubY = clampHubMountHoleSpacing + clampHubMountHoleDiam + 2*margin
        swivelHubY = swivelHubMountRingDiam + swivelHubMountHoleDiam + 2*margin
        y = max([clampHubY, swivelHubY])
        return x, y, thickness 


class OrbitalPlate(OrbitalShaker):

    def __init__(self,params):
        super(OrbitalPlate,self).__init__(params)

    def addHoles(self):
        super(OrbitalPlate,self).addHoles()
        self.addSwivelHubHoles()

    def addSwivelHubHoles(self):
        mountHoleDiam = self.params['swivelHubMountHoleDiameter']
        for xBearing, yBearing in self.getBearingHolePosList():
            for xPosRel, yPosRel in self.getSwivelHubMountHoleRelPosList():
                xPos = xPosRel + xBearing
                yPos = yPosRel + yBearing
                hole = (xPos, yPos, mountHoleDiam)
                self.holeList.append(hole)

    def createPart(self):
        super(OrbitalPlate,self).createPart()
        x,y,z = self.params['orbitalPlateSize']
        radius = self.params['orbitalPlateRadius']
        self.part = plate_w_holes(x,y,z,self.holeList,radius=radius)



# -----------------------------------------------------------------------------
if __name__ == '__main__':

    projection = True 

    if 1:
        # Upper base plate 
        basePlateUpper = BasePlate(params)
        prog = SCAD_Prog()
        prog.fn = 50
        if projection:
            prog.add(basePlateUpper.projection())
        else:
            prog.add(basePlateUpper)
        prog.write('base_plate_upper.scad')

    if 1:
        # Lower base plate
        basePlateLower = BasePlateLower(params)
        prog = SCAD_Prog()
        prog.fn = 50
        if projection:
            prog.add(basePlateLower.projection())
        else:
            prog.add(basePlateLower)
        prog.write('base_plate_lower.scad')

    if 1:
        # Hub adapter
        hubAdapter = HubAdapterPlate(params)
        prog = SCAD_Prog()
        prog.fn = 50
        if projection:
            prog.add(hubAdapter.projection())
        else:
            prog.add(hubAdapter)
        prog.write('hub_adapter.scad')

    if 1:
        # Orbital plate
        orbitalPlate = OrbitalPlate(params)
        prog = SCAD_Prog()
        prog.fn = 50
        if projection:
            prog.add(orbitalPlate.projection())
        else:
            prog.add(orbitalPlate)
        prog.write('orbital_plate.scad')


