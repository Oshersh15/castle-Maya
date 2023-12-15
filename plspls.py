import maya.cmds as cmds
import math as m
import random


def create_terrain(*args):
    chosenTerrain = cmds.radioButtonGrp(terrainType, q=True, select=True)
    if chosenTerrain == 1:
        height = 50
    elif chosenTerrain == 2:
        height = 25
    elif chosenTerrain == 3:
        height = 10
    else:
    #in case when none of the options are selected
        cmds.confirmDialog(title='Warning', message='Please choose a terrain type', button='OK', defaultButton='OK', bgc=(0.8, 0.8, 1.0))
    width = 150
    depth = 150
    #Create a new polygon plane with the specified dimensions
    terrain = cmds.polyPlane(width=width, height=depth, subdivisionsWidth=7, subdivisionsHeight=7, name='terrain')
    if chosenTerrain == 0:
        cmds.delete(terrain)
    
    plane_name = cmds.ls(selection=True)[0]
    
    #Get the vertices of the polygon plane
    vertices = cmds.ls("{0}.vtx[*]".format(plane_name), flatten=True)
    
    #Set a random height value for each vertex
    for vertex in vertices:
        x, y, z = cmds.pointPosition(vertex, world=True)
        height_value = random.uniform(0, height)
        cmds.move(x, height_value, z, vertex, absolute=True)
    
    #Smooth the terrain to make it look more natural
    cmds.polySmooth(plane_name, dv=3)
   


def createCastle(*args):
    #select all towers
    cmds.select('finalTower*')
    selected_objects = cmds.ls(selection=True)
    if (len(selected_objects))/2<3:
        #warning popup message
        cmds.confirmDialog(title='Warning', message='There should be at least 3 towers', button='OK', defaultButton='OK', bgc=(0.8, 0.8, 1.0))
    else:
        curves(selected_objects)


def createTower(*args):
    radius = cmds.intSliderGrp(radiusValue, query=True, value=True)
    levels = cmds.intSliderGrp(levelValue, query=True, value=True)
    translateX = cmds.intSliderGrp(positionX, query=True, value=True)
    translateZ = cmds.intSliderGrp(positionZ, query=True, value=True)
    translateY = verLocation(translateX, translateZ)
    castle(radius, levels, translateX, translateZ, translateY)
    
    
def castle(radius, levels, translateX, translateZ, translateY):
    #kept these constant because that way it seems to be the most aesthetic
    numBricks = 15
    brickHeight = 1
    brickThickness = 0.5
    tower = cmds.polyPipe(sa=numBricks*2, h=brickHeight, r=radius, t=brickThickness, name="tower")
    #for loop that runs until level-1 because the last level will be modeled seperately and diferentaly
    for i in range (1, levels-1):
        newLevel=cmds.instance(tower)
        cmds.move(0,i*brickHeight/2, 0, newLevel)
        cmds.rotate(0, 90*i, 0, newLevel)
    top = cmds.polyPipe(sa=numBricks*2, h=brickHeight, r=radius, t=brickThickness, name="lastLevel")
    lastLevel = cmds.instance(top)
    cmds.delete(top)
    cmds.move(0, (levels-1)*brickHeight/2, 0, lastLevel)
    #after understanding the logic of faces names, i figured that if i want to choose every other top face then this is the loop i should do.
    for x in range(numBricks*2, numBricks*4, 2):
        cmds.select(lastLevel[0] + ".f[%d]" % x, add=True)
        mySel = cmds.ls(selection=True, tail=1)
        cmds.select(clear=True)
        cmds.polyExtrudeFacet(mySel, ty=1)
   
    ceiling = cmds.polyDisc(r=radius-brickThickness)
    cmds.move(0, (levels-1.5)*brickHeight/2, 0, ceiling)
    cmds.polySoftEdge(ceiling, a=180, ch=0)
    #selecting all objects that belong to this tower and combining them
    cmds.select('tower*')
    towerGrp = cmds.group(name="towerGrp")
    cmds.select('pDisc*')
    cmds.group(parent='towerGrp')
    cmds.select('lastLevel*')
    cmds.group(parent='towerGrp')
    cmds.select('%s*' % towerGrp, replace=True)
    finalTower = cmds.polyUnite(ch=False, mergeUVSets=True, centerPivot=True, n='finalTower')
    cmds.delete(towerGrp)
    cmds.move(translateX, translateY, translateZ)
    
def verLocation(translateX, translateZ):
    chosen_location = (translateX, 25, translateZ) 
    
    #Get the vertices of the terrain
    vertices = cmds.ls('terrain' + ".vtx[*]", flatten=True)
    
    #Set an initial minimum distance and closest vertex
    min_distance = float("inf")
    closest_vertex = None
    
    #Iterate over the vertices and find the closest one
    for vertex in vertices:
        vertex_pos = cmds.pointPosition(vertex, world=True)
        distance = m.sqrt(sum((v1 - v2) ** 2 for v1, v2 in zip(chosen_location, vertex_pos)))
        if distance < min_distance:
            min_distance = distance
            closest_vertex = vertex
        if closest_vertex:
            cmds.select(closest_vertex)
    selected_vertex = cmds.ls(selection=True)[0]

#Convert the vertex that is selected to a vertex component
    vertex_component = cmds.polyListComponentConversion(selected_vertex, fromVertex=True, toVertex=True)

#Retrieve the world space position of the vertex
    vertex_position = cmds.pointPosition(vertex_component[0], world=True)
    return vertex_position[1]



def get_object_position(obj):
    try:
        return cmds.xform(obj, query=True, translation=True, worldSpace=True)
    except:
        return None

def curves(selected_objects):     
    #Filter and remove None values from the list
    valid_object_names = [obj for obj in selected_objects if get_object_position(obj)]
    
    #Sort the objects based on their location
    sorted_objects = sorted(valid_object_names, key=get_object_position)
    
    first_object = sorted_objects[0]
    
    #Append the first object to the end of the list
    sorted_objects.append(first_object)
    #insert 2 objects from the list to another list
    for i in range(len(sorted_objects) - 1):
        object1 = sorted_objects[i]
        object2 = sorted_objects[i + 1]
        another = [object1, object2]
    
        object_positions = []
        for obj in another:
            position = cmds.xform(obj, query=True, translation=True, worldSpace=True)
            object_positions.append(position)
    
        curve_name = cmds.curve(degree=1, point=object_positions)
        curve_length = cmds.arclen(curve_name)
        build_walls(curve_length, curve_name)


def build_walls(length, curve_name):
    #kept these constant because that way it seems to be the most aesthetic
    brickWidth=4
    brickHeight=1
    brickDepth=1
    numRows=9
    numColumns=int(length/brickWidth)
    objName=cmds.polyCube(w=brickWidth,h=brickHeight,d=brickDepth,n='brick')
    halfObjName=cmds.polyCube(w=brickWidth/2.0,h=brickHeight,d=brickDepth,n='halfBrick')
    for y in range(numRows):
        if y%2==1: # 1%2=1; 2%2=0; 3%2=1;4%2=0;5%2=1;6%2=0
            offset=brickWidth/2.0
        else:
            offset=0.0
        for x in range(numColumns):
            if x==0 and y%2==0:
                newObj = cmds.instance(halfObjName)
                xpos = x*brickWidth+offset+brickWidth/4.0
            elif x==numColumns-1 and y%2==1:
                newObj = cmds.instance(halfObjName)
                xpos = x*brickWidth+offset+brickWidth/4.0-brickWidth/2.0
            else:
                newObj = cmds.instance(objName)
                xpos = x*brickWidth+offset
            cmds.move(xpos,y*brickHeight,0,newObj)
    cmds.delete(objName)
    cmds.delete(halfObjName)
    cmds.select(clear=True)
    selected = cmds.ls("brick*")
    selected.append(cmds.ls("halfBrick*"))
    for i in selected:
        cmds.select(i, add=True)
    Grp = cmds.group(name='wall')
    
    # Select all objects in the group
    cmds.select('%s*' % Grp, replace=True)
    
    # Combine the objects into a single object
    united = cmds.polyUnite(ch=False, mergeUVSets=True, centerPivot=True, n='united')
    cmds.delete(Grp)
    cmds.select(clear=True)
    #make the wall align on the curve
    warp_deformer = cmds.createCurveWarp(united, curve_name)
    
window = cmds.window(title="My castle", widthHeight=(500, 500), bgc=(0.8, 0.8, 1.0))

cmds.columnLayout(adjustableColumn=True)
cmds.text('terrain')
terrainType = cmds.radioButtonGrp( label='Terrain type:', la3=['Dunes', 'Hills', 'Plains'], numberOfRadioButtons=3)
cmds.button(label='create terrain', command=create_terrain, bgc=(1.0, 1.0, 1.0))
cmds.separator(height=20)
cmds.text('round tower')
radiusValue = cmds.intSliderGrp(field=True, label='radius', minValue=2, maxValue=10, value=5)
levelValue = cmds.intSliderGrp(field=True, label='levels', minValue=15, maxValue=35, value=25)
frame_layout = cmds.frameLayout(label='translation', collapsable=True, collapse=True, borderVisible=True, marginWidth=5, marginHeight=5, bgc=(1.0, 1.0, 1.0))
cmds.separator(height=20)
positionX = cmds.intSliderGrp(field=True, label='Translate X', minValue=-60, maxValue=60, value=0)
positionZ = cmds.intSliderGrp(field=True, label='Translate Z', minValue=-60, maxValue=60, value=0)
#Close the frameLayout
cmds.setParent("..")
cmds.button(label='create tower', command=createTower, bgc=(1.0, 1.0, 1.0))
cmds.separator(height=20)
cmds.button(label='create castle', command=createCastle, bgc=(1.0, 1.0, 1.0))
cmds.showWindow(window)
    
    


    







