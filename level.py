"""
Subcontroller module for Froggit

This module contains the subcontroller to manage a single level in the Froggit game.
Instances of Level represent a single game, read from a JSON.  Whenever you load a new
level, you are expected to make a new instance of this class.

The subcontroller Level manages the frog and all of the obstacles. However, those are
all defined in models.py.  The only thing in this class is the level class and all of
the individual lanes.

This module should not contain any more classes than Levels. If you need a new class,
it should either go in the lanes.py module or the models.py module.

#Christopher Ambrus caa66
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from lanes  import *
from models import *

# PRIMARY RULE: Level can only access attributes in models.py or lanes.py using getters
# and setters. Level is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Level(object):
    """
    This class controls a single level of Froggit.

    This subcontroller has a reference to the frog and the individual lanes.  However,
    it does not directly store any information about the contents of a lane (e.g. the
    cars, logs, or other items in each lane). That information is stored inside of the
    individual lane objects.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lesson 27 for an example.  This class will be similar to that
    one in many ways.

    All attributes of this class are to be hidden.  No attribute should be accessed
    without going through a getter/setter first.  However, just because you have an
    attribute does not mean that you have to have a getter for it.  For example, the
    Froggit app probably never needs to access the attribute for the Frog object, so
    there is no need for a getter.

    The one thing you DO need a getter for is the width and height.  The width and height
    of a level is different than the default width and height and the window needs to
    resize to match.  That resizing is done in the Froggit app, and so it needs to access
    these values in the level.  The height value should include one extra grid square
    to suppose the number of lives meter.
    """

    # LIST ALL HIDDEN ATTRIBUTES HERE
    # Attribute _frog: The frog in each level (your playable character)
    # Invariant: _frog is a GImage object

    # Attribute _lanes: The lanes that appear in each level
    # Invariant: _lanes is a GTile object

    # Attribute _width: The width of the window size
    # Invariant: _width is a number (int)

    # Attribute _height: The height of the window
    # Invariant: _height is a number (int)

    # Attribute _cooldown: The time in between each of the frog's movements
    # Invariant: _cooldown is a number (float)

    # Attribute _lives: The amount of lives the player has left before losing
    # Invariant: _lives is a GImage object

    # Attribute _exitcount: The number of exits in the level
    # Invariant: _exitcount is a number (int)

    # Attribute _animating: Whether the frog's animation is active or not
    # Invariant: _animating is a boolean (True,False)

    # Attribute _updateDeath: Status of frog upon death (win,loss,death)
    # Invariant: _updateDeath is a number (int), can be 0, 1, -1

    # Attribute _safefrog: Contains the safe frog images on the exits
    # Invariant: _safefrog is a list of GImages

    # Attribute _input: The input handler to access keyboard information
    # Invariant: _input is a GInput object

    # Attribute _dead: Status of the frog (alive,dead)
    # Invariant: _dead is a number (int), 0 or 1

    # Attribute _death: The death sprite of the frog
    # Invariant: _death is a GSprite object

    # Attribute _startfrogx: The starting position of the frog
    # Invariant: _startfrogx is number (float)

    # Attribute _froghitbox: The frog's hitbox
    # Invariant: A tuple of tuples

    # Attribute _undead: An indication of when the death animation is complete
    # Invariant: _undead is a number (int), 0 or 1

    # Attribute _jumpSound: The jumpsound of the frog
    # Invariant: _jumpSound is a sound object

    # Attribute _winSound: The sound of getting to an exit
    # Invariant: _winSound is a sound object

    # Attribute _deathSound: The sound of the frog dying
    # Invariant: _deathSound is a sound object

    # Attribute _lastleafx: The x position of the last exit the frog was on
    # Invariant: _lastleafx is a number (float)

    # Attribute _lastleafy: The y position of the last exit the frog was on
    # Invariant: _lastleafy is a number (float)

    # Attribute _collidestatus: The status of the frog's collision
    # Invariant: _collidestatus is a number (int)

    # Attribute _animator: Handles the coroutine of animations
    # Invariant: _animator is the animation function

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getWidth(self):
        """
        Gets the width of the window screen of each level
        """
        return self._width

    def getHeight(self):
        """
        Gets the height of the window screen of each level
        """
        return self._height

    # INITIALIZER (standard form) TO CREATE THE FROG AND LANES
    def start(self,dict,width,height,input,hitbox):
        """
        Initializes the level.

        Initalizes the lanes, frog, and frog lives in the level.

        Parameter dict: The dictionary with each level's information
        Precondition: dict is a dictionary

        Parameter width: The width of the window size
        Precondtion: width is a number (int)

        Parameter height: The height of the window size
        Precondtion: height is a number (int)

        Parameter input: The input handler to access keyboard information
        Precondition: input is a GInput object

        Parameter hitbox: The dictionary containing the hitbox sizes of each object
        Precondition: hitbox is a dictionary
        """
        self._exitcount = 0
        self._animating = False
        self._updateDeath = 0
        self._safefrog = []
        self._width = width
        self._height = height
        self._cooldown = 0
        self._input = input
        lanes = dict['lanes']
        size = dict['size']
        objects = hitbox['images']
        self._lanes = []
        count=0.5
        for type in lanes:
            for value in type.values():
                if value == 'grass' or value == 'road' \
                or value == 'hedge' or value == 'water':
                    self._lanes.append(Lane(count,value,\
                    size,type,dict,objects))
            count = count + 1
        for lane in self._lanes:
            self._exitcount += lane.getexits()
        self.__starthelper__(dict,count,hitbox)

    # UPDATE METHOD TO MOVE THE FROG AND UPDATE ALL OF THE LANES
    def update(self,dt):
        """
        Updates the game objects each frame.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        lanes = self._lanes
        for lane in lanes:
            lane.update(dt,self._frog)
        onlogcount=0
        if not self._animator is None:
            try:
                self._animator.send(dt)
            except:
                self._animator = None
                self._dead=0
        elif(isinstance(self.__updateDeath__(),int)):
            return self._updateDeath
        elif self._frog != None:
            if(self.__updatecontinue__(lanes,onlogcount)==1):
                return
            elif(self.__inputcheck__(lanes)==1):
                return

    # DRAW METHOD TO DRAW THE FROG AND THE INDIVIDUAL LANES
    def draw(self,view):
        """
        Draw the lane and frog objects into view.

        Parameter view: The view to draw to
        Precondition: view is a GView object
        """
        for lane in self._lanes: #style points?
            lane.draw(view)
        if self._frog != None:
            self._frog.draw(view)
        for lives in self._lives:
            lives.draw(view)
        for frogs in self._safefrog:
            frogs.draw(view)
        if self._dead==1:
            self._death.draw(view)

    # ANY NECESSARY HELPERS (SHOULD BE HIDDEN)
    def __starthelper__(self,dict,count,hitbox):
        """
        Helps the start method initialize the level.

        Helps the start method to initalize the frog and the remaining lives.

        Parameter dict: The dictionary with each level's information
        Precondition: dict is a dictionary

        Parameter count: Number of lanes
        Precondition: count is a number (float)

        Parameter hitbox: The dictionary containing the hitbox sizes of each object
        Precondition: hitbox is a dictionary
        """
        self._startfrogx = (count+1.5)*GRID_SIZE/2
        self._froghitbox = hitbox['sprites'].get('frog').get('hitboxes')
        self._frog = Frog(x=(count+1.5)*GRID_SIZE/2,y=GRID_SIZE/2,\
        hitboxes=self._froghitbox)
        self._lives = [GImage(x=self.getWidth()-(0.5*GRID_SIZE),\
        y=count*GRID_SIZE,width=GRID_SIZE,height=GRID_SIZE,source=FROG_HEAD),\
        GImage(x=self.getWidth()-(1.5*GRID_SIZE),y=count*GRID_SIZE,\
        width=GRID_SIZE,height=GRID_SIZE,source=FROG_HEAD),\
        GImage(x=self.getWidth()-(2.5*GRID_SIZE),y=count*GRID_SIZE,\
        width=GRID_SIZE,height=GRID_SIZE,source=FROG_HEAD),\
        GLabel(text='LIVES:')]
        self._frog.dead=0
        self._undead=1
        self._lives[3].font_size = ALLOY_SMALL
        self._lives[3].font_name = ALLOY_FONT
        self._lives[3].linecolor = 'dark green'
        self._lives[3].x = self.getWidth()-(4.2*GRID_SIZE)
        self._lives[3].y = count*GRID_SIZE
        self._animator = None
        self._death=GSprite(x=-GRID_SIZE,y=0,source=DEATH_SPRITE+'.png',\
        angle=FROG_SOUTH,format=(2,4))
        self._dead=0
        self._jumpSound = Sound(CROAK_SOUND)
        self._deathSound = Sound(SPLAT_SOUND)
        self._winSound = Sound(TRILL_SOUND)
        self._lastleafx=0
        self._lastleafy=0
        self._collidestatus=0

    def __frogrejack__(self):
        """
        Draws frog in starting position.
        """
        self._frog = Frog(x=self._startfrogx,y=GRID_SIZE/2,\
        hitboxes=self._froghitbox)
        self._frog.dead=0
        self._undead=1
        self._death=GSprite(x=-GRID_SIZE,y=0,source=DEATH_SPRITE+'.png',\
        angle=FROG_SOUTH,format=(2,4))

    def __checkcollide__(self,lanes,direction):
        """
        Helper method of update.

        Checks for collisions of the frog object.

        Parameter lanes: The lanes in the level
        Precondtion: A list of objects

        Parameter direction: The direction to slide.
        Precondition: direction is a string
        """
        x = self._frog.x
        y = self._frog.y
        self.__directionmodifier__(direction)
        for lane in lanes:
            if self._frog.collides(lane._tile) == True:
                if lane._tile.source.find('hedge') != -1:
                    for i in range(len(lane._objs)+1):
                        if i == len(lane._objs):
                            self._frog.x = x
                            self._frog.y = y
                            return 2
                        if lane._objs[i].source.find('open') != -1 and \
                        self._frog.collides(lane._objs[i]) == True:
                            break
                        if lane._objs[i].source.find('exit') != -1 and \
                        self._frog.contains((lane._objs[i].x,\
                        lane._objs[i].y))\
                        == True and y <= lane._objs[i].y and \
                        lane._objs[i].blocked == 0:
                            lane._objs[i].blocked = 1
                            self._lastleafx=lane._objs[i].x
                            self._lastleafy=lane._objs[i].y
                            self._frog.x = x
                            self._frog.y = y
                            return 3
        self._frog.x = x
        self._frog.y = y

    def __directionmodifier__(self,direction):
        """
        Helper method of update.

        Modifies the direction of the frog.

        Parameter direction: The direction to slide.
        Precondition: direction is a string
        """
        if direction == 'up':
            self._frog.y+=GRID_SIZE
        if direction == 'down':
            self._frog.y-=GRID_SIZE
        if direction == 'left':
            self._frog.x-=GRID_SIZE
        if direction == 'right':
            self._frog.x+=GRID_SIZE

    def __inputcheck__(self,lanes):
        """
        Helper method of update.

        Checks for input of the arrow keys for frog movement.

        Parameter lanes: The lanes in the level
        Precondtion: A list of objects
        """
        if self._input.is_key_down('right'):
            self._frog.angle = FROG_EAST
            if(self.__checkcollide__(lanes,'right')==2): return 1
            self._animator = self.__animateslide__('right',self._frog)
            next(self._animator)
            self._jumpSound.play()
        elif self._input.is_key_down('left'):
            self._frog.angle = FROG_WEST
            if(self.__checkcollide__(lanes,'left')==2): return 1
            self._animator = self.__animateslide__('left',self._frog)
            next(self._animator)
            self._jumpSound.play()
        elif self._input.is_key_down('up'):
            self._frog.angle = FROG_NORTH
            self._collidestatus =self.__checkcollide__(lanes,'up')
            if(self._collidestatus==2): return 1
            self._animator = self.__animateslide__('up',self._frog)
            next(self._animator)
            self._jumpSound.play()
        elif self._input.is_key_down('down'):
            self._frog.angle = FROG_SOUTH
            if(self.__checkcollide__(lanes,'down')==2): return 1
            self._animator = self.__animateslide__('down',self._frog)
            next(self._animator)
            self._jumpSound.play()

    def __updatecontinue__(self,lanes,onlogcount):
        """
        A helper of the update method.

        Handles car collisions and log riding.

        Parameter lanes: The lanes in the level
        Precondtion: A list of objects

        Parameter onlogcount: The status of if the frog is on a log or not
        Precondtion: onlogcount is a number (int)
        """
        for lane in lanes:
            if self._frog.collides(lane._tile) == True:
                if lane._tile.source.find('water') != -1:
                    for i in range(len(lane._objs)):
                        if lane._objs[i].source.find('log') != -1:
                            for j in range(int(round(lane._objs[i].right))-\
                            int(round(lane._objs[i].left))-\
                            int(round(1.5*GRID_SIZE))):
                                tmp=GRID_SIZE/1.5+\
                                int(round(lane._objs[i].left+j+1))
                                angle = self._frog.angle
                                self._frog.angle=0
                                if self._frog.contains((tmp,lane._objs[i].y))\
                                ==True:
                                    lane._objs[i].onlog = 1
                                self._frog.angle=angle
                        onlogcount+=lane._objs[i].onlog
                    if(onlogcount==0):
                        self._dead=1
                        return 1
                if lane._tile.source.find('road') != -1:
                    for i in range(len(lane._objs)):
                        if (lane._objs[i].source.find('car') != -1 or \
                        lane._objs[i].source.find('truck') != -1 or \
                        lane._objs[i].source.find('trailer') != -1 or \
                        lane._objs[i].source.find('flatbed') != -1)and\
                        self._frog.collides(lane._objs[i]) == True:
                            self._dead=1
                            return 1

    def __updateDeath__(self):
        """
        Helper method of update.

        Handles the frog's death status. Updates the frog's death status.
        """
        if(self._collidestatus==3):
            self._collidestatus=0
            self._winSound.play()
            self._frog = None
            self._safefrog.append(GImage(x=self._lastleafx,y=self._lastleafy,\
            width=GRID_SIZE,height=GRID_SIZE,source=FROG_SAFE))
            if len(self._safefrog) == self._exitcount:
                self._updateDeath = 1
                return 1
            self._updateDeath = 0
            return 0
        elif self._dead==1:
            self._death.x=self._frog.x
            self._death.y=self._frog.y
            self._frog = None
            self._deathSound.play()
            self._animator=self.__animateslide__('dead',self._death)
            next(self._animator)
            self._undead=0
        elif self._undead==0:
            if len(self._lives) == 1:
                self._updateDeath = -1
                return -1
            self._lives.pop(0)
            self._updateDeath = 0
            return 0
        else:
            return 'none'

    def __animateslide__(self,direction,obj):
        """
        Helper method of update.

        Animates a  vertical up or down of the image over ANIMATION_SPEED seconds

        This method is a coroutine that takes a break (so that the game
        can redraw the image) every time it moves it. The coroutine takes
        the dt as periodic input so it knows how many (parts of) seconds
        to animate.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter direction: The direction to slide.
        Precondition: direction is a string

        Parameter obj: The frog's data
        Precondtion: obj is a list
        """
        self._animating,dtsum,notdeep=True,0,0
        if direction != 'dead':
            numberlist=self.__animationdirection__(direction,obj)
            curpos,nexpos,steps = numberlist[0],numberlist[1],numberlist[2]
            deeper = FROG_SPEED/8
            while self._animating:
                dt = (yield)
                dtsum+=dt
                if round(dtsum,5)>deeper:
                    dtsum=0
                    if(notdeep==0): obj.frame+=1
                    if(obj.frame==4): notdeep=1
                    if(notdeep==1):
                        obj.frame-=1
                        if(obj.frame==0): notdeep=0
                if self.__endanimation__(obj,direction,steps,dt,\
                curpos,nexpos)==2: continue
        else:
            deeper = DEATH_SPEED/8
            while self._animating:
                dt = (yield)
                dtsum+=dt
                if round(dtsum,5)>deeper:
                    dtsum=0
                    if(notdeep==0): obj.frame+=1
                    if(obj.frame==7): notdeep=1
                    if(notdeep==1):
                        obj.frame=0
                        self._animating=False

    def __animationdirection__(self,direction,obj):
        """
        Helper method of update.

        Updates the direction of the objects of the level.

        Parameter direction: The direction to slide.
        Precondition: direction is a string

        Parameter obj: The frog's data
        Precondtion: obj is a list
        """
        curpos=0
        nexpos=0
        steps=0
        if direction == 'up':
            curpos = obj.y
            nexpos = sorted([GRID_SIZE/2, obj.y+GRID_SIZE,self.getHeight()-\
            GRID_SIZE*1.5])[1]
            steps = abs((nexpos-curpos)/FROG_SPEED)
        if direction == 'down':
            curpos = obj.y
            nexpos = sorted([GRID_SIZE/2,obj.y-GRID_SIZE, self.getHeight()-\
            GRID_SIZE/2])[1]
            steps = abs((nexpos-curpos)/FROG_SPEED)
        if direction == 'left':
            curpos = obj.x
            nexpos = sorted([GRID_SIZE/2, obj.x-GRID_SIZE, self.getWidth()-\
            GRID_SIZE/2])[1]
            steps = abs((nexpos-curpos)/FROG_SPEED)
        if direction == 'right':
            curpos = obj.x
            nexpos = sorted([GRID_SIZE/2, obj.x+GRID_SIZE, self.getWidth()-\
            GRID_SIZE/2])[1]
            steps = abs((nexpos-curpos)/FROG_SPEED)
        return [curpos,nexpos,steps]

    def __endanimation__(self,obj,direction,steps,dt,curpos,nexpos):
        """
        Helper method of update.

        Concludes the animation of the frog's motion

        Parameter obj: The frog's data
        Precondtion: obj is a list

        Parameter direction: The direction to slide.
        Precondition: direction is a string

        Parameter steps: The velocity of the frog
        Precondtion: steps is a number (float)

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter curpos: The current position of the frog
        Precondtion: curpos is a number (float)

        Parameter nexpos: The next position of the frog
        Precondtion: nexpos is a number (float)
        """
        amount = steps*dt
        if steps==0:
            self._animating = False
            return 2
        if direction == 'up':
            obj.y +=amount
            if abs(obj.y-curpos) >= GRID_SIZE:
                obj.y = nexpos
                obj.frame=0
                self._animating = False
        if direction == 'down':
            obj.y -=amount
            if abs(obj.y-curpos) >= GRID_SIZE:
                obj.y = nexpos
                obj.frame=0
                self._animating = False
        if direction == 'left':
            obj.x -=amount
            if abs(obj.x-curpos) >= GRID_SIZE:
                obj.x = nexpos
                obj.frame=0
                self._animating = False
        if direction == 'right':
            obj.x +=amount
            if abs(obj.x-curpos) >= GRID_SIZE:
                obj.x = nexpos
                obj.frame=0
                self._animating = False
