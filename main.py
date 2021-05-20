from flappybird import FlappyBird
from tkinter import Tk


def main():
    root = Tk()
    game = FlappyBird(root)
    root.mainloop()


if __name__ == '__main__':
    main()
