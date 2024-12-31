import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []
        self.scores = {"X": 0, "O": 0}
        
        # Configure styles
        self.window.configure(bg='#2c3e50')
        self.window.resizable(False, False)
        
        # Create score labels
        self.score_frame = tk.Frame(self.window, bg='#2c3e50')
        self.score_frame.pack(pady=10)
        
        self.label_x = tk.Label(self.score_frame, text="Player X: 0", font=('Arial', 12, 'bold'), 
                               bg='#2c3e50', fg='#e74c3c')
        self.label_x.pack(side=tk.LEFT, padx=10)
        
        self.label_o = tk.Label(self.score_frame, text="Player O: 0", font=('Arial', 12, 'bold'), 
                               bg='#2c3e50', fg='#3498db')
        self.label_o.pack(side=tk.LEFT, padx=10)
        
        # Create game board
        self.game_frame = tk.Frame(self.window, bg='#2c3e50')
        self.game_frame.pack()
        
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.game_frame, text="", font=('Arial', 24, 'bold'),
                                 width=5, height=2, command=lambda row=i, col=j: self.button_click(row, col))
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(button)
                self.configure_button(button)
        
        # Reset button
        self.reset_button = tk.Button(self.window, text="New Game", font=('Arial', 12, 'bold'),
                                    command=self.reset_board, bg='#27ae60', fg='white',
                                    activebackground='#2ecc71')
        self.reset_button.pack(pady=10)

    def configure_button(self, button):
        button.configure(bg='#34495e', fg='white', activebackground='#2c3e50')
        
    def button_click(self, row, col):
        index = 3 * row + col
        if self.board[index] == "":
            self.board[index] = self.current_player
            self.buttons[index].configure(text=self.current_player,
                                        fg='#e74c3c' if self.current_player == 'X' else '#3498db')
            
            if self.check_winner():
                self.scores[self.current_player] += 1
                self.update_score()
                messagebox.showinfo("Winner!", f"Player {self.current_player} wins!")
                self.reset_board()
            elif "" not in self.board:
                messagebox.showinfo("Draw!", "It's a draw!")
                self.reset_board()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                
    def check_winner(self):
        # Winning combinations
        lines = [(0,1,2), (3,4,5), (6,7,8),  # Rows
                (0,3,6), (1,4,7), (2,5,8),  # Columns
                (0,4,8), (2,4,6)]           # Diagonals
        
        for line in lines:
            if (self.board[line[0]] == self.board[line[1]] == self.board[line[2]] != ""):
                # Highlight winning combination
                for i in line:
                    self.buttons[i].configure(bg='#27ae60')
                return True
        return False
    
    def update_score(self):
        self.label_x.configure(text=f"Player X: {self.scores['X']}")
        self.label_o.configure(text=f"Player O: {self.scores['O']}")
        
    def reset_board(self):
        self.board = [""] * 9
        self.current_player = "X"
        for button in self.buttons:
            button.configure(text="", bg='#34495e')
            
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
