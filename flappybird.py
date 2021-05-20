from random import randint
import time

from tkinter import Canvas, Frame
from tkinter.constants import BOTH

from bird import Bird
from pipe import Pipe


class FlappyBird(Frame):
    def __init__(self, root):
        super().__init__()

        # Internal
        self.root = root

        # Timing
        self.timestamp = time.time() * 1000
        self.lastFrame = self.timestamp
        self.delta = 16

        # Timers
        self.timer1 = self.timestamp

        # Settings
        self.settings = {
            "width": 400,
            "height": 600,
            "pipegap": 50,
            "gravity": 0.6,
            "lift": 12,
            "birdRadius": 15,
            "pipeWidth": 80,
            "groundHeight": 50,
            "gapSize": 150,
            "minPipeHeight": 100,
            "fps": 60,
            "speed": 6,
            "richness": 6000
        }

        self.color = {
            "bird": "#934536",
            "birdStroke": "#ff6446",
            "pipe": "#464646",
            "pipeStroke": "",
            "background": "#262626",
            "ground": "#3d3d3d",
            "scoreText": "white"
        }

        self.delay = round(1000 / self.settings["fps"])

        # Game variables
        self.pipes: list[Pipe] = []
        self.player: Bird = Bird(self)

        self.isPaused = False
        self.bestScore = 0

        # Setup
        self.root.title("FlappyBird")
        self.setupCanvas()

        # Start the game loop
        self.reset()
        self.tick()

    # Draw function
    def animationFrame(self):
        # Timer1 handler (Create new pipes)
        if(self.timestamp > self.timer1 + self.settings["richness"] / self.settings["speed"]):
            self.timer1 = self.timestamp

            gap = randint(self.settings["minPipeHeight"], self.settings["height"] - self.settings["gapSize"] - self.settings["minPipeHeight"])
            self.pipes.append(Pipe(self, 0, gap))
            self.pipes.append(Pipe(self, gap + self.settings["gapSize"], self.settings["height"] - gap - self.settings["gapSize"]))

        # Update and render pipes
        for pipe in self.pipes:
            if(self.player.isAlive):
                pipe.update()
            pipe.render()

        # Remove pipes which are out of the view (Has to do it in separate loop to prevent flashing)
        for pipe in self.pipes:
            if(pipe.isRemoved):
                self.pipes.remove(pipe)

        # Render ground
        self.renderGround()

        # Update and render player
        self.player.update()
        self.player.render()

        # Render text
        self.renderScore()
        self.canvas.create_text(15, 20, text=round(self.bestScore), anchor="w", font=("Consolas", 12), fill="white")

    # onclick event handler
    def onClick(self, evnet):
        if(self.isPaused):
            self.isPaused = False

            if(not self.player.isAlive):
                print(self.player.score > self.bestScore, self.player.score, self.bestScore)
                if(self.player.score > self.bestScore):
                    self.bestScore = self.player.score
                self.reset()
        self.player.jump()

    # Tick in game loop
    def tick(self):
        self.timestamp = time.time() * 1000
        self.deltaTime = (self.timestamp - self.lastFrame) or self.delay
        self.delta = self.deltaTime / self.delay
        self.lastFrame = self.timestamp

        self.root.title("FlappyBird | FPS: " + str(round(1000 / self.deltaTime)))

        self.canvas.delete("all")
        self.animationFrame()

        self.canvas.update()
        self.canvas.after(self.delay, self.tick)

    # Wrapper function for setting up the canvas
    def setupCanvas(self):
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self, width=self.settings["width"], height=self.settings["height"])
        self.canvas.configure(bg=self.color["background"])
        self.canvas.bind("<Button-1>", self.onClick)
        self.canvas.pack(fill=BOTH, expand=1)

    def renderGround(self):
        x1 = 0
        y1 = self.settings["height"] - self.settings["groundHeight"]
        x2 = self.settings["width"]
        y2 = self.settings["height"]

        self.canvas.create_rectangle(x1, y1, x2, y2, outline="", fill=self.color["ground"])

    def renderScore(self):
        text = self.canvas.create_text(0, 0, text=round(self.player.score), anchor="w", font=("Consolas", 18), fill="white")

        coords = self.canvas.bbox(text)
        xOffset = (coords[2] - coords[0]) / 2

        self.canvas.move(text, self.settings["width"] * 0.5 - xOffset, self.settings["height"] * 0.15)

    def reset(self):
        # Timing
        self.timestamp = time.time() * 1000
        self.lastFrame = self.timestamp
        self.delta = 16

        # Timers
        self.timer1 = self.timestamp

        # Game variables
        self.pipes: list[Pipe] = []
        self.player: Bird = Bird(self)

        self.isPaused = False
