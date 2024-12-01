key_switch_camera = 'c' # the camera is bounded to the hero or not
key_switch_mode = 'z' # can get past obstacles or not

key_forward = 'w' #step forward (in the direction the camera is facing)
key_back = 's' # step back
key_left = 'a' # step left (sideways from the camera)
key_right = 'd' # step right
key_up = 'e' # step up
key_down = 'q' # step down

key_turn_left = 'arrow_left' # turn the camera to the right (the world is to the left)
key_turn_right = 'arrow_right' # turn the camera to the left (the world is to the right)

key_build = 'b' # build a block
key_destroy = 'x' # destroy a block

key_savemap = 'k' # save the map
key_loadmap = 'l' # load the map

class Hero():
    def __init__(self,pos,land):
        self.mode = True # can get past obstacles or not
        self.land = land
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setH(180)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()
    
    def cameraBind(self):
        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True 

    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2] - 3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False

    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    def turnLeft(self):
        self.hero.setH((self.hero.getH() + 5) % 360)

    def turnRight(self):
        self.hero.setH((self.hero.getH() - 5) % 360)

    def look_at(self, angle):
        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())

        dx, dy = self.check_dir(angle) #check_dir is a function that returns the dx and dy for the angle
        x_to = x_from + dx
        y_to = y_from + dy
        return (x_to, y_to, z_from)

    def just_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            # check if there is a free space in front of you. Perhaps you need to move down
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            # if there is no free space, if possible, climb up the block
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos) # unable to climb up

    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)

    def check_dir(self, angle):
        ''' returns the rounded changes in the X and Y coordinates
        corresponding to the movement towards the angle.
        The Y coordinate decreases if the hero is looking at a 0-degree angle,
        and increases when they look at a 180-degree angle.   
        The X coordinate increases if the hero is looking at a 90-degree angle,
        and decreases when they look at a 270-degree angle.   
            0-degree angle (from 0 to 20)      ->        Y - 1
            45-degree angle (from 25 to 65)    -> X + 1, Y - 1
            90-degree angle (from 70 to 110) -> X + 1
            from 115 to 155 -> X + 1, Y + 1
            from 160 to 200 -> Y + 1
            205 to 245 -> X - 1, Y + 1
            from 250 to 290 -> X - 1
            from 290 to 335 -> X - 1, Y - 1
            from 340 -> Y - 1 '''
        if angle >= 0 and angle <= 20:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (-1, 0)
        elif angle <= 335:
            return (-1, -1)
        else:
            return (0, -1)

    def forward(self):
        angle = (self.hero.getH()) % 360
        self.move_to(angle)

    def back(self):
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)

    def left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)
    
    def right(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)

    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.getZ() + 1)

    def down(self):
        if self.mode and self.hero.getZ() > 1:
            self.hero.setZ(self.hero.getZ() - 1)

    def changeMode(self):
        if self.mode:
            self.mode = False
        else:
            self.mode = True

    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)

    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.deleteBlock(pos)
        else:
            self.land.deleteBlockFrom(pos)     

    def accept_events(self):
        base.accept(key_switch_camera, self.changeView)
        base.accept(key_switch_mode, self.changeMode)

        base.accept(key_forward, self.forward)
        base.accept(key_forward + '-repeat', self.forward)

        base.accept(key_back, self.back)
        base.accept(key_back + '-repeat', self.back)

        base.accept(key_left, self.left)
        base.accept(key_left + '-repeat', self.left)

        base.accept(key_right, self.right)
        base.accept(key_right + '-repeat', self.right)

        base.accept(key_up, self.up)
        base.accept(key_up + '-repeat', self.up)

        base.accept(key_down, self.down)
        base.accept(key_down + '-repeat', self.down)

        base.accept(key_turn_left, self.turnLeft)
        base.accept(key_turn_left + '-repeat', self.turnLeft)

        base.accept(key_turn_right, self.turnRight)
        base.accept(key_turn_right + '-repeat', self.turnRight)

        base.accept(key_build, self.build)
        base.accept(key_destroy, self.destroy)

        base.accept(key_savemap, self.land.saveMap )
        base.accept(key_loadmap, self.land.loadMap )
