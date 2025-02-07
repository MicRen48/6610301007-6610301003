import os
import time
import random

class Maze:
    def __init__(self, width=15, height=15) -> None:
        self.width = width
        self.height = height
        self.maze = [['X' for _ in range(width)] for _ in range(height)]
        self.ply = None
        self.end = None
        self.path = set()
        self.stack = []
        self.generate_maze()
        self.set_start_end()

    def isInBound(self, y, x):
        return 0 <= y < self.height and 0 <= x < self.width

    def print(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("\n\n\n")
        for row in self.maze:
            for col in row:
                print(col, " ", end="")
            print("")
        print("\n\n\n")

    def printEND(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("\n\n\n")
        print(" ผ่านแล้ว!!! ")
        print("\n\n\n")

    def move(self, direction):
        next_move = Pos(self.ply.y + direction[0], self.ply.x + direction[1])
        if self.isInBound(next_move.y, next_move.x):
            if self.maze[next_move.y][next_move.x] in [" ", "E"] and (next_move.y, next_move.x) not in self.path:
                self.maze[self.ply.y][self.ply.x] = " "
                self.maze[next_move.y][next_move.x] = "P"
                self.ply = next_move
                self.path.add((next_move.y, next_move.x))
                self.stack.append((next_move.y, next_move.x))
                self.print()
                print(f"Moved to: ({next_move.y}, {next_move.x})")
                time.sleep(1)
                return self.maze[next_move.y][next_move.x] != "E"
        return False

    def auto_move(self):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        while True:
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
                self.maze[self.ply.y][self.ply.x] = " "
                self.maze[last_position[0]][last_position[1]] = "P"
                self.ply = Pos(last_position[0], last_position[1])
                self.print()
                print(f"Backtracked to: ({last_position[0]}, {last_position[1]})")
                time.sleep(1)

            if (self.ply.y, self.ply.x) == (self.end.y, self.end.x):
                self.printEND()
                return

    def generate_maze(self):
        # สร้างเขาวงกตแบบสุ่ม
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < 0.9:  
                    self.maze[y][x] = " "
                else:
                    self.maze[y][x] = "X"

        # กำหนดจุดเริ่มและจบ
        self.maze[1][1] = " "  
        self.maze[self.height - 2][self.width - 2] = " "  

    def set_start_end(self):
        self.ply = Pos(1, 1)  # กำหนดตำแหน่งผู้เล่นเริ่มต้น
        self.end = Pos(self.height -2, self.width - 2)  # กำหนดตำแหน่งจุดสิ้นสุด
        self.save_maze_to_file()
        #ทำ.txt
    def save_maze_to_file(self):
        with open("maze.txt", "w") as f:
            for row in self.maze:
                f.write("".join(row) + "\n")
            f.write(f"Start: ({self.ply.y}, {self.ply.x})\n")
            f.write(f"End: ({self.end.y}, {self.end.x})\n")

class Pos:
    def __init__(self, y, x) -> None:
        self.y = y
        self.x = x

if __name__ == '__main__':
    
    m = Maze()  
    m.print()  
    m.auto_move()  