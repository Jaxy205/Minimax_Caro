"""
consts.py - Chứa toàn bộ hằng số cho game Caro (Gomoku).

Bao gồm: Kích thước bàn cờ, màu sắc GUI, độ sâu AI, và trọng số heuristic.
"""

from typing import Final

# =============================================================================
# BOARD CONFIGURATION
# =============================================================================
BOARD_SIZE: Final[int] = 15          # Kích thước bàn cờ 15x15
WIN_CONDITION: Final[int] = 5        # Số quân liên tiếp để thắng

# =============================================================================
# PLAYER SYMBOLS
# =============================================================================
EMPTY: Final[str] = ""               # Ô trống
HUMAN: Final[str] = "X"              # Ký hiệu người chơi
AI: Final[str] = "O"                 # Ký hiệu máy

# =============================================================================
# AI CONFIGURATION
# =============================================================================
AI_DEPTH: Final[int] = 2             # Độ sâu tìm kiếm (2-3 cho bàn 15x15)
NEIGHBOR_RADIUS: Final[int] = 2      # Bán kính neighbor limiting

# =============================================================================
# GUI CONFIGURATION
# =============================================================================
CELL_SIZE: Final[int] = 35           # Kích thước gọn cho bàn lớn
PADDING: Final[int] = 20
LINE_WIDTH: Final[int] = 2
PIECE_RADIUS: Final[int] = 12
FONT_STYLE_PIECE: Final[tuple[str, int, str]] = ("Constantia", 20, "bold") # Giả lập viết tay (comic/serif)

# =============================================================================
# COLOR PALETTE (Visual Style per User Image)
# =============================================================================
COLOR_BACKGROUND: Final[str] = "#FDFEFE"     # Trắng sáng (giấy)
COLOR_LINE: Final[str] = "#BDC3C7"           # Kẻ xám nhạt
COLOR_HUMAN: Final[str] = "#2874A6"          # Xanh mực (Handwritten Blue)
COLOR_AI: Final[str] = "#C0392B"             # Đỏ mực (Handwritten Red)
COLOR_HIGHLIGHT: Final[str] = "#3498DB"      # Viền xanh vuông chọn
COLOR_BUTTON_BG: Final[str] = "#2ECC71"
COLOR_BUTTON_FG: Final[str] = "#FFFFFF"

# =============================================================================
# HEURISTIC SCORES
# =============================================================================
SCORE_FIVE: Final[int] = 100_000_000
SCORE_OPEN_FOUR: Final[int] = 10_000_000
SCORE_CLOSED_FOUR: Final[int] = 1_000_000
SCORE_OPEN_THREE: Final[int] = 100_000
SCORE_CLOSED_THREE: Final[int] = 10_000
SCORE_OPEN_TWO: Final[int] = 1_000
SCORE_CLOSED_TWO: Final[int] = 100
SCORE_ONE: Final[int] = 10

DEFENSE_MULTIPLIER: Final[float] = 1.1

DIRECTIONS: Final[list[tuple[int, int]]] = [
    (0, 1), (1, 0), (1, 1), (1, -1)
]
