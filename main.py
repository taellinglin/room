#!/usr/bin/env python

# Author: Shao Zhang, Phil Saltzman, and Eddie Caanan
# Last Updated: 2015-03-13
#
# This tutorial shows how to play animations on models aka "actors".
# It is based on the popular game of "Rock 'em Sock 'em Robots".

from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import TextNode
from panda3d.core import LVector3
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import NodePath
from random import random
from random import shuffle
from math import sin
from motionBlur import MotionBlur
from colorcyle import ColorCycle
import sys


class Room(ShowBase):
    # Macro-like function used to reduce the amount to code needed to create the
    # on screen instructions

    def genLabelText(self, text, i):
        return OnscreenText(text=text, parent=base.a2dTopLeft, scale=.05,
                            pos=(0.1, - 0.1 -.07 * i), fg=(1, 1, 1, 1),
                            align=TextNode.ALeft)

    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self)

        # This code puts the standard title and instruction text on screen
        self.title = OnscreenText(text="Tael Ling Lin's Room",
                                  parent=base.a2dBottomRight, style=1,
                                  fg=(255, 255, 255, 1), pos=(-0.2, 0.1),
                                  align=TextNode.ARight, scale=.09)

        self.escapeEventText = self.genLabelText("ESC: Quit", 0)
        self.motionblur = MotionBlur()
        # Set the camera in a fixed position
        self.disableMouse()
        base.cam.setPosHpr(0,0,16,0,0,0)
        self.setBackgroundColor(0, 0, 0)

        # Add lighting so that the objects are not drawn flat
        self.setupLights()
        # Shader
        base.useTrackball()

        # Load the ring
        self.room = loader.loadModel('room/room00.bam')
        self.room.reparentTo(render)
        self.colorcycle = ColorCycle()
        self.timer = 1
        for n, node in enumerate(self.room.findAllMatches("**/*")):
            self.colorcycle.apply_hue_cycle(node, 0.1)
        
        # Now that we have defined the motion, we can define our key input.
        # Each fist is bound to a key. When a key is pressed, self.tryPunch checks to
        # make sure that the both robots have their heads down, and if they do it
        # plays the given interval
        self.accept('escape', sys.exit)
        self.taskMgr.add(self.update, "update")

    # tryPunch will play the interval passed to it only if
    # neither robot has 'resetHead' playing (a head is up) AND
    # the punch interval passed to it is not already playing

    # checkPunch will determine if a successful punch has been thrown

    # This function sets up the lighting
    def update(self, task):
        #self.room.set_h(self.room, 0.1)
        self.timer += 0.01
        base.cam.set_r(0)
        self.room.set_pos(self.render, 0,0,(sin(self.timer)*.1 + 0.125))
        

        return task.cont
    
    def setupLights(self):
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((.8, .8, .75, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(LVector3(0, 0, -2.5))
        directionalLight.setColor((0.9, 0.8, 0.9, 1))
        render.setLight(render.attachNewNode(ambientLight))
        render.setLight(render.attachNewNode(directionalLight))
    

app = Room()
app.run()
