"""
gui.py - Giao diện đồ họa game Caro (Style: Hand drawn on Paper).
"""

import tkinter as tk
from tkinter import messagebox
from consts import (
    BOARD_SIZE, CELL_SIZE, PADDING, LINE_WIDTH, PIECE_RADIUS, FONT_STYLE_PIECE,
    COLOR_BACKGROUND, COLOR_LINE, COLOR_HUMAN, COLOR_AI, COLOR_HIGHLIGHT,
    COLOR_BUTTON_BG, COLOR_BUTTON_FG, EMPTY, HUMAN, AI
)
from board import Board
from ai import AIEngine

class CaroGUI:
    def __init__(self, board: Board, ai_engine: AIEngine, human_first: bool = True) -> None:
        self._board = board
        self._ai_engine = ai_engine
        self._human_first = human_first
        self._is_game_over = False
        self._is_ai_thinking = False
        self._current_player = HUMAN if human_first else AI
        self._canvas_size = BOARD_SIZE * CELL_SIZE + 2 * PADDING
        
        self._root = tk.Tk()
        self._root.title("Cờ Caro (Gomoku) - Paper Style")
        self._root.resizable(False, False)
        self._create_widgets()
        
        if not human_first:
            self._root.after(100, self._ai_move)
            
    def _create_widgets(self):
        main_frame = tk.Frame(self._root, bg="#ECF0F1")
        main_frame.pack(padx=10, pady=10)
        
        self._canvas = tk.Canvas(
            main_frame, width=self._canvas_size, height=self._canvas_size,
            bg=COLOR_BACKGROUND, highlightthickness=1, highlightbackground="#BDC3C7"
        )
        self._canvas.pack(pady=(0, 10))
        self._canvas.bind("<Button-1>", self._on_canvas_click)
        self._draw_grid()
        
        control_frame = tk.Frame(main_frame, bg="#ECF0F1")
        control_frame.pack(fill=tk.X)
        self._status_label = tk.Label(control_frame, text="Lượt của bạn (X)", font=("Segoe UI", 12), bg="#ECF0F1")
        self._status_label.pack(side=tk.LEFT, padx=10)
        
        tk.Button(control_frame, text="Chơi lại", command=self._reset_game,
                 bg=COLOR_BUTTON_BG, fg=COLOR_BUTTON_FG).pack(side=tk.RIGHT, padx=10)
                 
    def _draw_grid(self):
        for i in range(BOARD_SIZE + 1):
            # Lines go from edge to edge of the grid area
            # Adjusted to ensure full grid enclose
            start = PADDING
            end = PADDING + BOARD_SIZE * CELL_SIZE
            pos = PADDING + i * CELL_SIZE
            
            # Horizontal
            self._canvas.create_line(start, pos, end, pos, fill=COLOR_LINE, width=LINE_WIDTH)
            # Vertical
            self._canvas.create_line(pos, start, pos, end, fill=COLOR_LINE, width=LINE_WIDTH)

    def _on_canvas_click(self, event):
        if self._is_game_over or self._is_ai_thinking or self._current_player != HUMAN: return
        
        col = (event.x - PADDING) // CELL_SIZE
        row = (event.y - PADDING) // CELL_SIZE
        
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self._board.is_valid_move(row, col):
            self._make_move(row, col, HUMAN)
            if self._check_game_end(row, col): return
            
            self._current_player = AI
            self._update_status("AI đang suy nghĩ...")
            self._is_ai_thinking = True
            self._root.after(50, self._ai_move)

    def _ai_move(self):
        if self._is_game_over: return
        best_move = self._ai_engine.get_best_move(self._board)
        if best_move:
            self._make_move(best_move[0], best_move[1], AI)
            if self._check_game_end(best_move[0], best_move[1]):
                self._is_ai_thinking = False
                return
        self._current_player = HUMAN
        self._update_status("Lượt của bạn (X)")
        self._is_ai_thinking = False

    def _make_move(self, row, col, player):
        self._board.make_move(row, col, player)
        self._canvas.delete("highlight")
        self._draw_piece(row, col, player)
        self._highlight_last_move(row, col)

    def _draw_piece(self, row, col, player):
        x = PADDING + col * CELL_SIZE + CELL_SIZE // 2
        y = PADDING + row * CELL_SIZE + CELL_SIZE // 2
        text = "X" if player == HUMAN else "O"
        color = COLOR_HUMAN if player == HUMAN else COLOR_AI
        
        # Draw text to simulate handwriting
        self._canvas.create_text(x, y, text=text, fill=color, font=FONT_STYLE_PIECE, tags="piece")

    def _highlight_last_move(self, row, col):
        x = PADDING + col * CELL_SIZE
        y = PADDING + row * CELL_SIZE
        # Square box highlight
        self._canvas.create_rectangle(
            x + 2, y + 2, x + CELL_SIZE - 2, y + CELL_SIZE - 2,
            outline=COLOR_HIGHLIGHT, width=2, tags="highlight"
        )

    def _check_game_end(self, row, col):
        winner = self._board.check_winner(row, col)
        if winner:
            self._is_game_over = True
            msg = "Bạn thắng!" if winner == HUMAN else "AI thắng!"
            variable_msg = "Chúc mừng!" if winner == HUMAN else "Cố gắng lần sau!"
            self._update_status(msg)
            messagebox.showinfo("Kết quả", f"{msg} {variable_msg}")
            return True
        if self._board.is_full():
            self._is_game_over = True
            self._update_status("Hòa!")
            messagebox.showinfo("Kết quả", "Ván cờ hòa!")
            return True
        return False

    def _update_status(self, msg):
        self._status_label.config(text=msg)

    def _reset_game(self):
        self._board.reset()
        self._is_game_over = False
        self._is_ai_thinking = False
        self._current_player = HUMAN if self._human_first else AI
        self._canvas.delete("piece")
        self._canvas.delete("highlight")
        if self._human_first: self._update_status("Lượt của bạn (X)")
        else:
            self._update_status("AI đang suy nghĩ...")
            self._root.after(100, self._ai_move)

    def run(self):
        self._root.mainloop()
