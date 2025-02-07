import turtle
import random
import time

class MazeTurtle:
    def __init__(self, width=15, height=15):
        self.width = width
        self.height = height
        self.maze = [['X' for _ in range(width)] for _ in range(height)]
        self.ply = None
        self.end = None
        self.path = set()
        self.visited = set()
        self.stack = []
        self.generate_maze()
        self.set_start_end()
        self.setup_turtle()

    def isInBound(self, y, x):
        return 0 <= y < self.height and 0 <= x < self.width

    def generate_maze(self):
        for y in range(self.height):
            for x in range(self.width):
                self.maze[y][x] = " " if random.random() < 0.6 else "X"
        self.maze[1][1] = " "
        self.maze[self.height - 2][self.width - 2] = " "

    def set_start_end(self):
        self.ply = Pos(1, 1)
        self.end = Pos(self.height - 2, self.width - 2)
        self.path.add((self.ply.y, self.ply.x))
        self.visited.add((self.ply.y, self.ply.x))

    def setup_turtle(self):
        turtle.setup(600, 600)
        turtle.bgcolor("white")
        turtle.speed(0)
        turtle.tracer(0, 0)
        self.draw_maze()
        turtle.update()

    def draw_maze(self):
        turtle.clear()
        turtle.penup()
        for y in range(self.height):
            for x in range(self.width):
                screen_x = -200 + x * 20
                screen_y = 200 - y * 20
                turtle.goto(screen_x, screen_y)
                if self.maze[y][x] == "X":
                    turtle.color("black")
                    turtle.begin_fill()
                    for _ in range(4):
                        turtle.forward(20)
                        turtle.right(90)
                    turtle.end_fill()
        turtle.update()

    def draw_player(self):
        turtle.color("blue")
        screen_x = -200 + self.ply.x * 20
        screen_y = 200 - self.ply.y * 20
        turtle.penup()
        turtle.goto(screen_x + 10, screen_y + 10)
        turtle.dot(10, "blue")
        turtle.update()

    def move(self, direction):
        next_move = Pos(self.ply.y + direction[0], self.ply.x + direction[1])
        if self.isInBound(next_move.y, next_move.x) and self.maze[next_move.y][next_move.x] == " " and (next_move.y, next_move.x) not in self.visited:
            self.ply = next_move
            self.path.add((next_move.y, next_move.x))
            self.visited.add((next_move.y, next_move.x))
            self.stack.append((next_move.y, next_move.x))
            self.draw_maze()
            self.draw_player()
            time.sleep(0.1)
            return self.ply != self.end
        return False

    def auto_move(self):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        while self.ply != self.end:
            random.shuffle(directions)
            moved = False
            for direction in directions:
                if self.move(direction):
                    moved = True
                    break
            if not moved:
                if not self.stack:
                    print("No more moves available.")
                    return
                last_position = self.stack.pop()
                self.ply = Pos(last_position[0], last_position[1])
                self.draw_maze()
                self.draw_player()
                time.sleep(0.1)
        print("Maze completed!")
        turtle.done()

class Pos:
    def __init__(self, y, x):
        self.y = y
        self.x = x

if __name__ == '__main__':
    maze_game = MazeTurtle()
    maze_game.auto_move()
