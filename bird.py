from typing import TYPE_CHECKING
from utils import clamp
if TYPE_CHECKING:
    from flappybird import FlappyBird
    from pipe import Pipe


class Bird():
    def __init__(self, game: "FlappyBird"):
        self.game = game

        self.position = [
            self.game.settings["width"] * 0.25,
            self.game.settings["height"] * 0.25
        ]
        self.velocity = 0
        self.score = 0
        self.isAlive = True

    def jump(self):
        if(self.isAlive):
            self.velocity = -self.game.settings["lift"]

    def update(self):
        # Do not update if the player is died
        # if(not self.isAlive):
        #    return False

        # Update score
        if(self.isAlive):
            self.score += 1 * self.game.delta

        # Update position
        self.velocity += self.game.settings["gravity"] * self.game.delta
        self.position[1] += self.velocity * self.game.delta

        # y < 0 handling
        if(self.position[1] < 0):
            self.position[1] = 0
            self.velocity = 0

        # Collision (falling on the ground)
        if(self.position[1] > self.game.settings["height"] - self.game.settings["groundHeight"]):
            self.isAlive = False

        # Collision (with pipes)
        for pipe in self.game.pipes:
            if(self.collision(pipe)):
                self.isAlive = False

        # Player death
        if(not self.isAlive and self.position[1] > self.game.settings["height"] - self.game.settings["birdRadius"] - self.game.settings["groundHeight"]):
            self.position[1] = self.game.settings["height"] - self.game.settings["birdRadius"] - self.game.settings["groundHeight"]
            self.game.isPaused = True

    def render(self):
        x = self.position[0]
        y = self.position[1]
        r = self.game.settings["birdRadius"]

        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        self.game.canvas.create_oval(x0, y0, x1, y1, fill=self.game.color["bird"], outline=self.game.color["birdStroke"])

    def collision(self, pipe: "Pipe"):
        closestX = clamp(self.position[0], pipe.position[0], pipe.position[0] + self.game.settings["pipeWidth"])
        closestY = clamp(self.position[1], pipe.position[1], pipe.position[1] + pipe.height)

        # Calculate the distance between the circle's center and this closest point
        distanceX = self.position[0] - closestX
        distanceY = self.position[1] - closestY

        # If the distance is less than the circle's radius, an intersection occurs
        distanceSquared = (distanceX * distanceX) + (distanceY * distanceY)
        return distanceSquared < (self.game.settings["birdRadius"] * self.game.settings["birdRadius"])
