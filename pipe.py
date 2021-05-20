from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flappybird import FlappyBird


class Pipe():
    def __init__(self, game: "FlappyBird", y, height):
        self.game = game
        self.position = [
            self.game.settings["width"],
            y
        ]
        self.height = height

        self.isRemoved = False

    def update(self):
        self.position[0] -= self.game.settings["speed"] * self.game.delta

        if(self.position[0] + self.game.settings["pipeWidth"] < 0):
            # self.game.pipes.remove(self)
            self.isRemoved = True

    def render(self):
        if(self.isRemoved):
            return
        x1 = self.position[0]
        y1 = self.position[1]
        x2 = x1 + self.game.settings["pipeWidth"]
        y2 = y1 + self.height

        self.game.canvas.create_rectangle(x1, y1, x2, y2, fill=self.game.color["pipe"], outline=self.game.color["pipeStroke"])
