from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionNode, CollisionSphere, CollisionHandlerEvent, CollisionPlane, Plane, Point3, Vec3
from panda3d.physics import ForceNode, LinearVectorForce,  ActorNode
import common

target_window_w, target_window_h = 1600, 900


class Application(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        common.setup_window(self, target_window_w, target_window_h)

        self.cam.setPos(0, -50, 10)
        self.setup_collision()
        self.setup_physics()
        self.add_smiley()
        self.add_floor()

        common.add_sky_box(self, sky_box_name="blue")
        common.add_directional_light(self)
        common.add_ambient_light(self)

        self.camLens.setFov(90)
        self.setFrameRateMeter(True)

    def setup_collision(self):
        self.cTrav = CollisionTraverser()
        self.cTrav.showCollisions(self.render)
        self.notifier = CollisionHandlerEvent()
        self.notifier.addInPattern("%fn-in-%in")
        self.notifier.addOutPattern("%fn-out-%in")
        self.accept("smiley-in-floor", self.on_collision_start)
        self.accept("smiley-out-floor", self.on_collision_end)

    def setup_physics(self):
        self.enableParticles()
        gravity_node = ForceNode("gravity")
        self.render.attachNewNode(gravity_node)
        gravityForce = LinearVectorForce(0, 0, -9.81)
        gravity_node.addForce(gravityForce)
        self.physicsMgr.addLinearForce(gravityForce)

    def add_smiley(self):
        actor = ActorNode("physics")
        actor.getPhysicsObject().setMass(10)
        self.phys = self.render.attachNewNode(actor)
        self.physicsMgr.attachPhysicalNode(actor)
        self.smiley = self.loader.loadModel("smiley")
        self.smiley.reparentTo(self.phys)
        self.phys.setPos(0, 0, 10)
        thrustNode = ForceNode("thrust")
        self.phys.attachNewNode(thrustNode)
        # self.thrustForce = LinearVectorForce(0, 0, 400)
        # self.thrustForce.setMassDependent(1) # Mass dependent force
        self.thrustForce = LinearVectorForce(0, 0, 100)
        self.thrustForce.setMassDependent(0)  # Mass independent
        thrustNode.addForce(self.thrustForce)
        col = self.smiley.attachNewNode(CollisionNode("smiley"))
        col.node().addSolid(CollisionSphere(0, 0, 0, 1.1))
        col.show()
        self.cTrav.addCollider(col, self.notifier)

    def add_floor(self):
        floor = self.render.attachNewNode(CollisionNode("floor"))
        floor.node().addSolid(CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0))))
        floor.show()

    def on_collision_start(self, entry):
        self.physicsMgr.addLinearForce(self.thrustForce)

    def on_collision_end(self, entry):
        self.physicsMgr.removeLinearForce(self.thrustForce)


common.load_prc_file()
game = Application()
game.run()
