"""
Lanes module for Froggit

This module contains the lane classes for the Frogger game. The lanes are the vertical
slice that the frog goes through: grass, roads, water, and the exit hedge.

Each lane is like its own level. It has hazards (e.g. cars) that the frog has to make
it past.  Therefore, it is a lot easier to program frogger by breaking each level into
a bunch of lane objects (and this is exactly how the level files are organized).

You should think of each lane as a secondary subcontroller.  The level is a subcontroller
to app, but then that subcontroller is broken up into several other subcontrollers, one
for each lane.  That means that lanes need to have a traditional subcontroller set-up.
They need their own initializer, update, and draw methods.

There are potentially a lot of classes here -- one for each type of lane.  But this is
another place where using subclasses is going to help us A LOT.  Most of your code will
go into the Lane class.  All of the other classes will inherit from this class, and
you will only need to add a few additional methods.

If you are working on extra credit, you might want to add additional lanes (a beach lane?
a snow lane?). Any of those classes should go in this file.  However, if you need additional
obstacles for an existing lane, those go in models.py instead.  If you are going to write
extra classes and are now sure where they would go, ask on Piazza and we will answer.

#Christopher Ambrus caa66
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *

# PRIMARY RULE: Lanes are not allowed to access anything in any level.py or app.py.
# They can only access models.py and const.py. If you need extra information from the
# level object (or the app), then it should be a parameter in your method.

class Lane(object):         # You are permitted to change the parent class if you wish
    """
    Parent class for an arbitrary lane.

    Lanes include grass, road, water, and the exit hedge.  We could write a class for
    each one of these four (and we will have classes for THREE of them).  But when you
    write the classes, you will discover a lot of repeated code.  That is the point of
    a subclass.  So this class will contain all of the code that lanes have in common,
    while the other classes will contain specialized code.

    Lanes should use the GTile class and to draw their background.  Each lane should be
    GRID_SIZE high and the length of the window wide.  You COULD make this class a
    subclass of GTile if you want.  This will make collisions easier.  However, it can
    make drawing really confusing because the Lane not only includes the tile but also
    all of the objects in the lane (cars, logs, etc.)
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE
    # Attribute _objs: The objects on the lanes
    # Invariant: _objs is a list that contains only GImage objects

    # Attribute _tile: The lanes of each level
    # Invariant: _tile is a GTile object

    # Attribute _exitcount: The number of exits in the level
    # Invariant: _exitcount is a number (int)

    # Attribute _offscreen: The offscreen buffer for each moving object in the level
    # Invariant: _offscreen is a number (int)

    # Attribute _objs: The objects in the level
    # Invariant: _objs is a list (may be empty)

    # Attribute _objspeed: The speed of the moving objects
    # Invariant: _objspeed is a number (float)

    # Attribute _width: The width of the window screen
    # Invariant: _width is a number (int)

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getexits(self):
        """
        Gets the exit count of each level
        """
        return self._exitcount
    # INITIALIZER TO SET LANE POSITION, BACKGROUND,AND OBJECTS
    def __init__(self,count,type,size,objtype,dict,objects):
        """
        Initializes the lanes and objects.

        Initalizes the grass, road, water, and hedges.
        Initalizes the log and car objects onto the lanes.
        Initalizes the hitboxes of each object.

        Parameter count: Number of lanes
        Precondition: count is a number (float)

        Parameter type: The background surface of each lane
        Precondtion: type is a string ("grass","road","water","hedge")

        Parameter size: The window's scaling when playing the game
        Precondition: size is a number (int)

        Parameter objtype: The object being rendered onto the lanes
        Precondition: objtype is a string i.e. "log1","car3"

        Parameter dict: The dictionary with all the information pretaining to each level
        Precondition: dict is a dictionary

        Parameter objects: The objects and their information for each level
        Preconiditon: objects is a dictionary
        """
        hardhitbox, objangle = None, 0
        self._exitcount = 0
        self._offscreen = dict['offscreen']
        self._objs = []
        self._objspeed = 0
        self._width = size[0]*GRID_SIZE
        self._tile = GTile(x=0,y=count*GRID_SIZE,width=2*size[0] *GRID_SIZE,\
        height=GRID_SIZE,source=str(type)+'.png')
        for i in objtype.values():
            if isinstance(i,int):
                objspeed = i
                self._objspeed = i
                if objspeed < 0: objangle= 180
            if not isinstance(i,list): continue
            for j in i:
                for k in j.values():
                    if isinstance(k,str): objecttype=k
                    if isinstance(k,float) or isinstance(k,int): objectpos = k
                for i in objects.values():
                    if (list(i.items())[0][1])==(objecttype+'.png'):
                        hardhitbox=tuple(list(i.items())[2][1])
                self._objs.append(GImage(x=(objectpos+0.5)*GRID_SIZE,\
                y=count*GRID_SIZE,source=objecttype+'.png',angle=objangle))
                self._objs[len(self._objs)-1].blocked = 0
                if hardhitbox!=None:
                    self._objs[len(self._objs)-1].hitbox = hardhitbox
                self._objs[len(self._objs)-1].onlog = 0
                if objecttype == 'exit': self._exitcount += 1

    def update(self,dt,frog):
        """
        Updates the game objects each frame.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter frog: The frog in each level (your playable character)
        Precondition: frog is a GImage object
        """
        for obj in self._objs:
            obj.x += dt*self._objspeed
            if obj.onlog==1:
                frog.x += dt*self._objspeed
                if (frog.x<=0 or frog.x>=self._width):
                    frog.dead=1
                obj.onlog = 0
            if self._objspeed < 0:
                if obj.right <= -self._offscreen*GRID_SIZE:
                    obj.right = self._width + self._offscreen*GRID_SIZE
            else:
                if obj.left >= self._width + self._offscreen*GRID_SIZE:
                    obj.left = -self._offscreen*GRID_SIZE


    def draw(self,view):
        """
        Draw the lane and frog objects.

        Parameter view: The view to draw to
        Precondition: view is a GView object
        """
        self._tile.draw(view)
        for obj in self._objs:
            obj.draw(view)
    # ADDITIONAL METHODS (DRAWING, COLLISIONS, MOVEMENT, ETC)


class Grass(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a 'safe' grass area.

    You will NOT need to actually do anything in this class.  You will only do anything
    with this class if you are adding additional features like a snake in the grass
    (which the original Frogger does on higher difficulties).
    """
    pass

    # ONLY ADD CODE IF YOU ARE WORKING ON EXTRA CREDIT EXTENSIONS.


class Road(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a roadway with cars.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, roads are different
    than other lanes as they have cars that can kill the frog. Therefore, this class
    does need a method to tell whether or not the frog is safe.
    """
    pass

    # DEFINE ANY NEW METHODS HERE


class Water(Lane):
    """
    A class representing a waterway with logs.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, water is very different
    because it is quite hazardous. The frog will die in water unless the (x,y) position
    of the frog (its center) is contained inside of a log. Therefore, this class needs a
    method to tell whether or not the frog is safe.

    In addition, the logs move the frog. If the frog is currently in this lane, then the
    frog moves at the same rate as all of the logs.
    """
    pass

    # DEFINE ANY NEW METHODS HERE


class Hedge(Lane):
    """
    A class representing the exit hedge.

    This class is a subclass of lane because it does want to use a lot of the features
    of that class. But there is a lot more going on with this class, and so it needs
    several more methods.  First of all, hedges are the win condition. They contain exit
    objects (which the frog is trying to reach). When a frog reaches the exit, it needs
    to be replaced by the blue frog image and that exit is now "taken", never to be used
    again.

    That means this class needs methods to determine whether or not an exit is taken.
    It also need to take the (x,y) position of the frog and use that to determine which
    exit (if any) the frog has reached. Finally, it needs a method to determine if there
    are any available exits at all; once they are taken the game is over.

    These exit methods will require several additional attributes. That means this class
    (unlike Road and Water) will need an initializer. Remember to user super() to combine
    it with the initializer for the Lane.
    """
    pass
    # LIST ALL HIDDEN ATTRIBUTES HERE

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO SET ADDITIONAL EXIT INFORMATION

    # ANY ADDITIONAL METHODS


# IF YOU NEED ADDITIONAL LANE CLASSES, THEY GO HERE
