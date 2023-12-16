# castle-Maya
creating a castle using Python in Maya software

My code creates the outer part of a castle that is standing on top of a terrain. In my code I created a round building, a brick wall and a terrain that are being arranged based on the user’s choice. The user is presented with a user interface window and can determine the level of mountainous for the terrain and can determine the attributes of the round buildings such as radius, height and location on the terrain (x-axis and z-axis). The program will already know to determine the y-position based on the area of the terrain the building is standing on. After that the user can press on the ‘create castle’ button and the brick walls will arrange themselves appropriately


The code functions:

create_terrain:
The function receives the type of terrain the user wants. It checks also if the user didn’t choose any option which in that case a warning popup window will show, and no terrain will appear. The level of mountainous is influenced by the height attribute – the highest the value will be, the more mountainy it will be. The terrains’ vertices are positioned randomly within their defined limits.

createCastle:
The function checks if while clicking the button ‘create castle’ there are more than 3 towers (as there is not much to do with less than 3 towers). If there are, the function calls another function – curves, which I will explain later. If there are not enough towers, a warning popup window will show.

createTower:
The function receives the arguments from the GUI controls and then uses them to call two other functions – verLocation and castle, which will be explained later.

castle:
The function builds the round tower. When called, it receives the radius, levels (height), and position attributes. The tower is created from polyPipe. In addition, as the ceiling, a pDisc is created and as the last level of the tower, the ‘crenellation’ is also made out of polyPipe but some faces are extruded upwards. Every level is made separately and at the end all levels are combined.

verLocation:
The function searches for the closest vertex of the terrain to the position of the tower. As the user determines the attributes of z and x axis, it is not possible for him to determine the y-axis as it is changing depending to the terrain mountainous ‘ texture’. The function at the end returns the y attribute in order for the tower to ‘stand’ on the terrain.

get_object_position:
The function obtains the towers’ world space position.

Curves:
The function sorts all towers in the scene by their location. This is in order for them to be in an order that is not affected by the order of their creation because at the end, what we are building is a sort of a barrier and we need to connect all the towers with walls. After the towers are sorted in the list ‘sorted_objects’, they are listed again but this time only in pairs. This is in order to create a curve between two towers and not one curve that goes through all of them.

Build_walls:
The function creates the brick walls. It builds brick by brick and at the end combines them. When there is a wall ready, we align the wall to the curves between the towers.

Main function:
Specifies all the GUI controls and attributes that will be shown in the user interface window.


References
• In ‘castle’ function, I took the idea on how to build the tower from the slides in brightSpace: Gears Systems p.13
• In ‘build_walls’ function, I took the idea from brighSpace slides. Introduction to production tool->Functions->7_wall
• In ‘build_walls’ function, I took the code that was in the forum there. I was looking for a way to use warp deformer with python. (MASH1_ReproMesh, $selection[0]); - I changed the line for it to apply on python and to fit my needs. https://forums.autodesk.com/t5/maya- programming/scripting-curve-warp/td-p/9964799
• Wathed this video that helped me understand Maya GUI. https://www.google.com/search?q=maya+python+gui+examples&oq=maya+python+gui&aq s=chrome.0.69i59l2j69i57j0i22i30l2j69i60l3.4686j0j7&sourceid=chrome&ie=UTF- 8#fpstate=ive&vld=cid:1afeb39c,vid:n4i4F2fmK2M
• Autodesk website https://download.autodesk.com/us/maya/2010help/commandspython/cat_Windows.html
• In ‘verLocation’ function, lines 126-134, I found some codes on how to find coordinates of the closest point and took inspiration and reformed them a bit to fit my needs. https://stackoverflow.com/questions/24415806/coordinates-of-the-closest-points-of-two- geometries-in-shapely



