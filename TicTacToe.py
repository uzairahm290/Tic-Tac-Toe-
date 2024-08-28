import tkinter as tk
from tkinter import messagebox
import random
import pygame

class TicTacToeApp:
    def __init__(self, root):
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound('click.wav')
        self.win_sound = pygame.mixer.Sound('win.wav')
        self.tie_sound = pygame.mixer.Sound('tie.wav')
        self.lose_sound = pygame.mixer.Sound('lose.wav')
        self.comp_sound = pygame.mixer.Sound('comp.wav')

        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("600x650") 
        self.root.configure(bg='black')

        self.center_window()

        self.board = [' '] * 9
        self.player1_score = 0
        self.player2_score = 0
        self.tie_score = 0
        self.current_player = 'O' 
        self.is_2_player_mode = False
        self.computer_move_scheduled = False  

        self.create_widgets()
        self.update_scores()  
        if not self.is_2_player_mode:
            self.schedule_computer_move() 

    def center_window(self):
        self.root.update_idletasks()
        window_width = 600
        window_height = 650 

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Tic-Tac-Toe", font=('Helvetica', 24, 'bold'), 
                                    bg='black', fg='white')
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.player1_score_label = tk.Label(self.root, text=f"Player 1 (O): {self.player1_score}", 
                                            font=('Helvetica', 14), bg='black', fg='white')
        self.player2_score_label = tk.Label(self.root, text=f"{self.get_player2_label()}: {self.player2_score}", 
                                            font=('Helvetica', 14), bg='black', fg='white')
        self.tie_score_label = tk.Label(self.root, text=f"Ties: {self.tie_score}", 
                                        font=('Helvetica', 14), bg='black', fg='white')

        self.player1_score_label.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
        self.player2_score_label.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        self.tie_score_label.grid(row=1, column=2, padx=10, pady=5, sticky='ew')

        self.buttons = []
        for i in range(9):
            btn = tk.Button(self.root, text=' ', font=('Helvetica', 20, 'bold'), width=5, height=2, 
                            bg='black', fg='white', relief='raised', bd=3,
                            command=lambda i=i: self.on_button_click(i))
            btn.grid(row=i // 3 + 2, column=i % 3, padx=10, pady=10)
            self.buttons.append(btn)

        self.reset_button = tk.Button(self.root, text="Reset Scores", font=('Helvetica', 14), 
                                      bg='gray', fg='white', command=self.reset_scores)
        self.reset_button.grid(row=5, column=0, columnspan=3, pady=20)

        self.mode_button = tk.Button(self.root, text="Switch to Two-Player Mode", font=('Helvetica', 14), 
                                     bg='gray', fg='white', command=self.toggle_mode)
        self.mode_button.grid(row=6, column=0, columnspan=3, pady=10)

        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.root.grid_rowconfigure(i, weight=1)

    def on_button_click(self, index):
        if self.board[index] == ' ' and not self.check_winner('O') and not self.check_winner('X'):
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player, bg='lightblue' if self.current_player == 'O' else 'darkred')
            if self.current_player == 'O':
                self.click_sound.play()
            else:
                self.comp_sound.play()

            if self.check_winner(self.current_player):
                self.win_sound.play()
                winner = "Player 1" if self.current_player == 'O' else ("Player 2" if self.is_2_player_mode else "Computer")
                messagebox.showinfo("Game Over", f"Congratulations! {winner} wins!")
                if self.current_player == 'O':
                    self.player1_score += 1
                else:
                    self.player2_score += 1 
                self.update_scores()
                self.reset_board()
            elif self.is_board_full():
                self.tie_sound.play()
                messagebox.showinfo("Game Over", "It's a tie!")
                self.tie_score += 1
                self.update_scores()
                self.reset_board()
            else:
                if not self.is_2_player_mode:
                    self.schedule_computer_move() 
                else:
                    self.current_player = 'X' if self.current_player == 'O' else 'O'

    def computer_move(self):
        if not self.is_board_full() and not self.check_winner('O') and not self.check_winner('X'):
            available_moves = [i for i in range(9) if self.board[i] == ' ']
            if available_moves:
                move = random.choice(available_moves)
                self.board[move] = 'X'
                self.buttons[move].config(text='X', bg='darkred')
                self.comp_sound.play()
                if self.check_winner('X'):
                    self.lose_sound.play()
                    messagebox.showinfo("Game Over", "Computer wins!")
                    self.player2_score += 1 
                    self.update_scores()
                    self.reset_board()
                elif self.is_board_full():
                    self.tie_sound.play()
                    messagebox.showinfo("Game Over", "It's a tie!")
                    self.tie_score += 1
                    self.update_scores()
                    self.reset_board()
                else:
                    self.current_player = 'O' 
                self.computer_move_scheduled = False 

    def check_winner(self, sign):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  
            [0, 4, 8], [2, 4, 6]           
        ]
        for condition in win_conditions:
            if all(self.board[i] == sign for i in condition):
                return True
        return False

    def is_board_full(self):
        return all(cell != ' ' for cell in self.board)

    def reset_board(self):
        self.board = [' '] * 9
        for i in range(9):
            self.buttons[i].config(text=' ', bg='gray')
        if not self.is_2_player_mode and not self.computer_move_scheduled:
            self.schedule_computer_move()

    def update_scores(self):
        self.player1_score_label.config(text=f"Player 1 (O): {self.player1_score}")
        self.player2_score_label.config(text=f"{self.get_player2_label()}: {self.player2_score}")
        self.tie_score_label.config(text=f"Ties: {self.tie_score}")

    def reset_scores(self):
        self.player1_score = 0
        self.player2_score = 0
        self.tie_score = 0
        self.update_scores()
        self.reset_board()

    def toggle_mode(self):
        self.is_2_player_mode = not self.is_2_player_mode
        self.update_scores()
        self.reset_scores()
        if self.is_2_player_mode:
            self.mode_button.config(text="Switch to Single-Player Mode")
            self.current_player = 'O'
            self.computer_move_scheduled = False
        else:
            self.mode_button.config(text="Switch to Two-Player Mode")
            self.schedule_computer_move() 
        self.reset_board()

    def get_player2_label(self):
        return "Player 2 (X)" if self.is_2_player_mode else "Computer (X)"
    
    def schedule_computer_move(self):
        if not self.computer_move_scheduled:
            self.root.after(100, self.computer_move)
            self.computer_move_scheduled = True

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
