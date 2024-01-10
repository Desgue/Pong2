from scenes import *
class Scene_Manager():
    def __init__(self, current_scene = Menu_Scene()):
        self.go_to(current_scene)
    def go_to(self, scene):
        if hasattr(self, "scene"): del self.scene
        self.scene = scene
        self.scene.manager = self
