"""
main.py - Entry point.
"""
from board import Board
from ai import AIEngine
from gui import CaroGUI
from consts import AI_DEPTH

def main() -> None:
    board = Board()
    ai_engine = AIEngine(depth=AI_DEPTH)
    gui = CaroGUI(board=board, ai_engine=ai_engine, human_first=True)
    
    print("=" * 50)
    print("       CỜ CARO (GOMOKU) - MINIMAX AI")
    print("=" * 50)
    print(f"  Kích thước: 15x15")
    print("  Style: Hand Drawn")
    print("=" * 50)
    
    gui.run()

if __name__ == "__main__":
    main()
