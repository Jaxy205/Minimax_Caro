"""
board.py - Class Board quản lý trạng thái bàn cờ.

Chức năng:
- Quản lý mảng 2D lưu trạng thái bàn cờ
- Kiểm tra nước đi hợp lệ
- Phát hiện người thắng (tối ưu: chỉ kiểm tra xung quanh nước đi mới nhất)
- Theo dõi các ô đã đánh để tối ưu hóa AI
"""

from typing import Optional
from consts import (
    BOARD_SIZE, WIN_CONDITION, EMPTY, DIRECTIONS
)


class Board:
    """
    Class quản lý bàn cờ Caro.
    
    Attributes:
        _grid: Mảng 2D lưu trạng thái các ô
        _played_cells: Set các ô đã được đánh (để truy xuất nhanh)
        _last_move: Nước đi gần nhất (row, col)
        _move_count: Số nước đã đánh
    """
    
    __slots__ = ('_grid', '_played_cells', '_last_move', '_move_count')
    
    def __init__(self) -> None:
        """Khởi tạo bàn cờ trống."""
        self._grid: list[list[str]] = [
            [EMPTY for _ in range(BOARD_SIZE)] 
            for _ in range(BOARD_SIZE)
        ]
        self._played_cells: set[tuple[int, int]] = set()
        self._last_move: Optional[tuple[int, int]] = None
        self._move_count: int = 0
    
    # =========================================================================
    # PROPERTIES (Encapsulation)
    # =========================================================================
    
    @property
    def grid(self) -> list[list[str]]:
        """Trả về bàn cờ (read-only reference)."""
        return self._grid
    
    @property
    def played_cells(self) -> set[tuple[int, int]]:
        """Trả về set các ô đã đánh (read-only reference)."""
        return self._played_cells
    
    @property
    def last_move(self) -> Optional[tuple[int, int]]:
        """Trả về nước đi gần nhất."""
        return self._last_move
    
    @property
    def move_count(self) -> int:
        """Trả về số nước đã đánh."""
        return self._move_count
    
    # =========================================================================
    # BASIC OPERATIONS
    # =========================================================================
    
    def get_cell(self, row: int, col: int) -> str:
        """
        Lấy giá trị ô tại vị trí (row, col).
        
        Args:
            row: Chỉ số hàng
            col: Chỉ số cột
            
        Returns:
            Giá trị ô (EMPTY, HUMAN, hoặc AI)
        """
        return self._grid[row][col]
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """
        Kiểm tra nước đi có hợp lệ không.
        
        Args:
            row: Chỉ số hàng
            col: Chỉ số cột
            
        Returns:
            True nếu ô trống và nằm trong bàn cờ
        """
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return False
        return self._grid[row][col] == EMPTY
    
    def make_move(self, row: int, col: int, player: str) -> bool:
        """
        Thực hiện nước đi.
        
        Args:
            row: Chỉ số hàng
            col: Chỉ số cột
            player: Người chơi (HUMAN hoặc AI)
            
        Returns:
            True nếu đánh thành công, False nếu ô đã có quân
        """
        if not self.is_valid_move(row, col):
            return False
        
        self._grid[row][col] = player
        self._played_cells.add((row, col))
        self._last_move = (row, col)
        self._move_count += 1
        return True
    
    def undo_move(self, row: int, col: int) -> None:
        """
        Hoàn tác nước đi (dùng cho AI backtracking).
        
        Args:
            row: Chỉ số hàng
            col: Chỉ số cột
        """
        self._grid[row][col] = EMPTY
        self._played_cells.discard((row, col))
        self._move_count -= 1
        # Không cập nhật _last_move vì AI sẽ restore sau
    
    def reset(self) -> None:
        """Reset bàn cờ về trạng thái ban đầu."""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self._grid[row][col] = EMPTY
        self._played_cells.clear()
        self._last_move = None
        self._move_count = 0
    
    def is_full(self) -> bool:
        """Kiểm tra bàn cờ đã đầy chưa (hòa)."""
        return self._move_count >= BOARD_SIZE * BOARD_SIZE
    
    # =========================================================================
    # WIN DETECTION (Optimized)
    # =========================================================================
    
    def check_winner(self, last_row: int, last_col: int) -> Optional[str]:
        """
        Kiểm tra người thắng dựa trên nước đi cuối cùng.
        
        Tối ưu: Chỉ kiểm tra 4 hướng đi qua ô vừa đánh thay vì
        quét toàn bộ bàn cờ.
        
        Args:
            last_row: Hàng của nước đi cuối
            last_col: Cột của nước đi cuối
            
        Returns:
            Symbol của người thắng (HUMAN/AI) hoặc None
        """
        player = self._grid[last_row][last_col]
        if player == EMPTY:
            return None
        
        for dr, dc in DIRECTIONS:
            count = 1  # Đếm ô hiện tại
            
            # Đếm theo hướng thuận (dr, dc)
            count += self._count_direction(last_row, last_col, dr, dc, player)
            
            # Đếm theo hướng nghịch (-dr, -dc)
            count += self._count_direction(last_row, last_col, -dr, -dc, player)
            
            if count >= WIN_CONDITION:
                return player
        
        return None
    
    def _count_direction(
        self, 
        row: int, 
        col: int, 
        dr: int, 
        dc: int, 
        player: str
    ) -> int:
        """
        Đếm số quân liên tiếp theo một hướng.
        
        Args:
            row: Hàng bắt đầu
            col: Cột bắt đầu
            dr: Delta row (hướng di chuyển)
            dc: Delta col (hướng di chuyển)
            player: Người chơi cần đếm
            
        Returns:
            Số quân liên tiếp (không tính ô bắt đầu)
        """
        count = 0
        r, c = row + dr, col + dc
        
        while (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE 
               and self._grid[r][c] == player):
            count += 1
            r += dr
            c += dc
        
        return count
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    def clone(self) -> 'Board':
        """
        Tạo bản sao của bàn cờ (deep copy).
        
        Returns:
            Bản sao mới của Board
        """
        new_board = Board()
        new_board._grid = [row[:] for row in self._grid]
        new_board._played_cells = self._played_cells.copy()
        new_board._last_move = self._last_move
        new_board._move_count = self._move_count
        return new_board
    
    def __repr__(self) -> str:
        """Hiển thị bàn cờ dạng text (debug)."""
        lines = []
        for row in self._grid:
            line = ' '.join(cell if cell else '.' for cell in row)
            lines.append(line)
        return '\n'.join(lines)
