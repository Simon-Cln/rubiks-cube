import tkinter as tk
from tkinter import messagebox
import random
import time

class RubiksCube2D:
    def __init__(self, canvas):
        self.canvas = canvas
        self.size = 50  
        self.offset = 60  
        self.faces = {
            'U': [['white' for _ in range(3)] for _ in range(3)],  # Up face - White
            'D': [['yellow' for _ in range(3)] for _ in range(3)],  # Down face - Yellow
            'F': [['red' for _ in range(3)] for _ in range(3)],  # Front face - Red
            'B': [['orange' for _ in range(3)] for _ in range(3)],  # Back face - Orange
            'L': [['green' for _ in range(3)] for _ in range(3)],  # Left face - Green
            'R': [['blue' for _ in range(3)] for _ in range(3)],  # Right face - Blue
        }
        self.shuffled_moves = []  
        self.create_cube()

    def create_cube(self):
        self.canvas.delete('all')  
        self.draw_face('U', 200, 20)
        self.draw_face('D', 200, 360)
        self.draw_face('F', 200, 180)
        self.draw_face('B', 380, 180)
        self.draw_face('L', 20, 180)
        self.draw_face('R', 560, 180)
        self.canvas.update()

    def draw_face(self, face, start_x, start_y):
        for i in range(3):
            for j in range(3):
                x = start_x + j * self.size
                y = start_y + i * self.size
                color = self.faces[face][i][j]
                self.canvas.create_rectangle(x, y, x + self.size, y + self.size, fill=color, outline='black')

    def rotate_face_clockwise(self, face):
        self.faces[face] = [list(row) for row in zip(*self.faces[face][::-1])]
        self.create_cube()

    def rotate_face_counterclockwise(self, face):
        self.faces[face] = [list(row) for row in zip(*self.faces[face])][::-1]
        self.create_cube()

    def move(self, move):
        self.update_adjacent_faces(move)
        if move == "U":
            self.rotate_face_clockwise('U')
        elif move == "U'":
            self.rotate_face_counterclockwise('U')
        elif move == "D":
            self.rotate_face_clockwise('D')
        elif move == "D'":
            self.rotate_face_counterclockwise('D')
        elif move == "F":
            self.rotate_face_clockwise('F')
        elif move == "F'":
            self.rotate_face_counterclockwise('F')
        elif move == "B":
            self.rotate_face_clockwise('B')
        elif move == "B'":
            self.rotate_face_counterclockwise('B')
        elif move == "L":
            self.rotate_face_clockwise('L')
        elif move == "L'":
            self.rotate_face_counterclockwise('L')
        elif move == "R":
            self.rotate_face_clockwise('R')
        elif move == "R'":
            self.rotate_face_counterclockwise('R')

    def update_adjacent_faces(self, move):
        if move == "U":
            temp = self.faces['F'][0][:]
            self.faces['F'][0] = self.faces['R'][0][:]
            self.faces['R'][0] = self.faces['B'][0][:]
            self.faces['B'][0] = self.faces['L'][0][:]
            self.faces['L'][0] = temp
        elif move == "U'":
            temp = self.faces['F'][0][:]
            self.faces['F'][0] = self.faces['L'][0][:]
            self.faces['L'][0] = self.faces['B'][0][:]
            self.faces['B'][0] = self.faces['R'][0][:]
            self.faces['R'][0] = temp
        elif move == "D":
            temp = self.faces['F'][2][:]
            self.faces['F'][2] = self.faces['L'][2][:]
            self.faces['L'][2] = self.faces['B'][2][:]
            self.faces['B'][2] = self.faces['R'][2][:]
            self.faces['R'][2] = temp
        elif move == "D'":
            temp = self.faces['F'][2][:]
            self.faces['F'][2] = self.faces['R'][2][:]
            self.faces['R'][2] = self.faces['B'][2][:]
            self.faces['B'][2] = self.faces['L'][2][:]
            self.faces['L'][2] = temp
        # mm logique a faire pour la suite

    def shuffle(self, moves=20):
        possible_moves = ["U", "U'", "D", "D'", "F", "F'", "B", "B'", "L", "L'", "R", "R'"]
        self.shuffled_moves = []
        for _ in range(moves):
            move = random.choice(possible_moves)
            self.move(move)
            self.shuffled_moves.append(move)
            self.canvas.update()
            time.sleep(0.3) 

class Solver:
    def __init__(self, cube, move_label_var):
        self.cube = cube
        self.move_label_var = move_label_var

    def solve(self):
        if self.is_solved():
            print("Cube is already solved!")
        else:
            print("Solving is starting...")
            self.move_label_var.set("Solving is starting...")
            for move in reversed(self.cube.shuffled_moves):
                reversed_move = self.reverse_move(move)
                print(f"Performing move: {reversed_move}")
                self.move_label_var.set(f"Performing move: {reversed_move}")
                self.cube.move(reversed_move)
                self.cube.canvas.update()
                time.sleep(0.3) 
            print("Cube has been solved.")

    def is_solved(self):
        for face, grid in self.cube.faces.items():
            color = grid[0][0]
            if not all(cell == color for row in grid for cell in row):
                return False
        return True

    def reverse_move(self, move):
        if "'" in move:
            return move[0]
        else:
            return move + "'"

def main():
    root = tk.Tk()
    root.title("Rubik's Cube Simulator")
    canvas = tk.Canvas(root, width=1000, height=600, bg='white')
    canvas.pack()

    cube = RubiksCube2D(canvas)

    move_label_var = tk.StringVar()
    move_label = tk.Label(root, textvariable=move_label_var, font=("Helvetica", 14))
    move_label.pack(anchor='ne', padx=10, pady=10)

    def shuffle_cube():
        cube.shuffle()
        messagebox.showinfo("Shuffle", "Shuffle is complete. Solving is starting...")
        solver = Solver(cube, move_label_var)
        solver.solve()

    shuffle_button = tk.Button(root, text="Shuffle and Solve", command=shuffle_cube)
    shuffle_button.pack()

    root.mainloop()

if __name__ == '__main__':
    main()
