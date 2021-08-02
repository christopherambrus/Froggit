"""
Models module for Froggit

This module contains the model classes for the Frogger game. Anything that you
interact with on the screen is model: the frog, the cars, the logs, and so on.

Just because something is a model does not mean there has to be a special class for
it. Unless you need something special for your extra gameplay features, cars and logs
could just be an instance of GImage that you move across the screen. You only need a new
class when you add extra features to an object.

That is why this module contains the Frog class.  There is A LOT going on with the
frog, particularly once you start creating the animation coroutines.

If you are just working on the main assignment, you should not need any other classes
in this module. However, you might find yourself adding extra classes to add new
features.  For example, turtles that can submerge underneath the frog would probably
need a custom model for the same reason that the frog does.

If you are unsure about  whether to make a new class or not, please ask on Piazza. We
will answer.

#Christopher Ambrus caa66
# DATE COMPLETED HERE
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from a lane or level object, then it
# should be a parameter in your method.


class Frog(GSprite):         # You will need to change this by Task 3
    """
    A class representing the frog

    The frog is represented as an image (or sprite if you are doing timed animation).
    However, unlike the obstacles, we cannot use a simple GImage class for the frog.
    The frog has to have additional attributes (which you will add).  That is why we
    make it a subclass of GImage.

    When you reach Task 3, you will discover that Frog needs to be a composite object,
    tracking both the frog animation and the death animation.  That will like caused
    major modifications to this class.
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE
    # Attribute _x: The x (horizontal) postion of the frog
    # Invariant: x is a number (float)

    # Attribute _y: The y (vertical) postion of the frog
    # Invariant: y is a number (float)

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO SET FROG POSITION
    def __init__(self,x,y,hitboxes):
        """
        Initializes the Frog object.

        Intializes the frog, including its direction and x and y positions.

        Parameter x: The x (horizontal) postion of the frog
        Precondition: x is a number (float)

        Parameter y: The y (vertical) postion of the frog
        Precondition: y is a number (float)

        Parameter hitboxes:The frog's hitbox
        Precondtion: A tuple of tuples
        """
        self._x = x
        self._y = y
        super().__init__(x=x,y=y,source=FROG_SPRITE+'.png',\
        angle=FROG_NORTH,format=(1,5))
        self.hitboxes=hitboxes
    # ADDITIONAL METHODS (DRAWING, COLLISIONS, MOVEMENT, ETC)

# IF YOU NEED ADDITIONAL LANE CLASSES, THEY GO HERE
