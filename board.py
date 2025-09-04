# board.py
import numpy as np
import matplotlib.pyplot as plt

class Board:
    def __init__(self):
        # Initialize the overall 9x9 grid (9 sub-grids, each 3x3)
        self.board = np.zeros((9, 9), dtype=int)  # Overall 9x9 board
        self.subgrid_wins = [0] * 9  # Track wins for each subgrid: 0 = not won, 1 = Player 1, 2 = Player 2
        self.overall_winner = 0  # Track the overall winner: 0 = none, 1 = Player 1, 2 = Player 2
        self.next_subgrid = None  # Tracks the subgrid where the next move must be made

    def index_to_position(self, index, size):
        """
        Convert a flat index into row and column coordinates.
        For size = 3 (subgrid), index will be from 0-8.
        For size = 9 (full board), index will be from 0-80.
        """
        row = index // size
        col = index % size
        return row, col

    def get_subgrid(self, subgrid_index):
        """
        Get a specific 3x3 subgrid by index (0-8).
        """
        row_start = (subgrid_index // 3) * 3  # Row of the top-left corner of the subgrid
        col_start = (subgrid_index % 3) * 3   # Column of the top-left corner of the subgrid
        return self.board[row_start:row_start + 3, col_start:col_start + 3]

    def set_subgrid(self, subgrid_index, subgrid):
        """
        Set the values of a specific 3x3 subgrid.
        The subgrid should be a 3x3 numpy array.
        """
        if subgrid.shape != (3, 3):
            raise ValueError("Subgrid must be a 3x3 numpy array")

        row_start = (subgrid_index // 3) * 3
        col_start = (subgrid_index % 3) * 3
        self.board[row_start:row_start + 3, col_start:col_start + 3] = subgrid


    def is_valid_move(self, row, col):
        """
        Check if a move is valid by checking if the corresponding subgrid is available 
        and the cell is empty.
        """
        # Check if move is in the valid subgrid, unless it's a free move
        if self.next_subgrid is not None:
            subgrid_row, subgrid_col = row // 3, col // 3
            if subgrid_row * 3 + subgrid_col != self.next_subgrid:
                return False

        return self.board[row, col] == 0

    def update_cell(self, index, value):
        """
        Update a single cell in the 9x9 board using a flat index (0-80).
        This method ensures that updates to the overall board are reflected in the corresponding subgrid.
        """
        if not (0 <= index < 81):
            raise ValueError("Index must be between 0 and 80.")
        if value not in (0, 1, 2):  # Assuming 0 = empty, 1 = Player 1, 2 = Player 2
            raise ValueError("Cell value must be 0 (empty), 1 (Player 1), or 2 (Player 2).")

        # Convert the flat index (0-80) to a row and column
        row, col = self.index_to_position(index, 9)

        if not self.is_valid_move(row, col):
            raise ValueError(f"Invalid move: Cell at index {index} is already occupied.")
        
        # Update the main 9x9 board
        self.board[row, col] = value

        # Check the winner for the subgrid
        subgrid_index = (row // 3) * 3 + (col // 3)
        self.check_subgrid_winner(subgrid_index)

        # Update the next subgrid based on this move
        self.update_next_subgrid(row, col)

        # Check overall winner after every move
        self.check_winner(value)

    def update_cell_in_subgrid(self, subgrid_index, subgrid_index_flat, value):
        """
        Update a specific cell within a subgrid (3x3) by subgrid index (0-8) and 
        flat cell index (0-8), and reflect this change in the overall 9x9 board.
        
        subgrid_index: The index of the subgrid (0-8).
        subgrid_index_flat: The flat index within the subgrid (0-8).
        value: The value to set (0 = empty, 1 = Player 1, 2 = Player 2).
        """
        if not (0 <= subgrid_index < 9):
            raise ValueError("Subgrid index must be between 0 and 8.")
        if not (0 <= subgrid_index_flat < 9):
            raise ValueError("Subgrid cell index must be between 0 and 8.")
        if value not in (0, 1, 2):
            raise ValueError("Cell value must be 0 (empty), 1 (Player 1), or 2 (Player 2).")

        # Convert the flat index within subgrid (0-8) to local row and column
        local_row, local_col = self.index_to_position(subgrid_index_flat, 3)

        # Calculate the global row and column in the 9x9 board based on the subgrid index
        global_row = (subgrid_index // 3) * 3 + local_row
        global_col = (subgrid_index % 3) * 3 + local_col

        if not self.is_valid_move(global_row, global_col):
            raise ValueError(f"Invalid move: Cell in subgrid {subgrid_index}, index {subgrid_index_flat} is already occupied.")

        # Update the corresponding cell in the 9x9 board
        self.board[global_row, global_col] = value

        # Check the winner for the subgrid
        self.check_subgrid_winner(subgrid_index)

         # Update the next subgrid restriction based on the current move
        self.update_next_subgrid(global_row, global_col)

        # Check overall winner after every move
        self.check_winner(value)

    def check_winner(self, player):
        """
        Check if the given player has won the overall board or any subgrid.
        """
        # Check rows and columns for overall board
        for i in range(9):
            if all(self.board[i, j] == player for j in range(9)):  # Check row
                self.overall_winner = player
                return True
            if all(self.board[j, i] == player for j in range(9)):  # Check column
                self.overall_winner = player
                return True

        # Check diagonals for overall board
        if all(self.board[i, i] == player for i in range(9)):  # Main diagonal
            self.overall_winner = player
            return True
        if all(self.board[i, 8 - i] == player for i in range(9)):  # Anti-diagonal
            self.overall_winner = player
            return True

        return False

    def check_subgrid_winner(self, subgrid_index):
        """
        Check if there is a winner in a specific subgrid.
        """
        subgrid = self.get_subgrid(subgrid_index)

        for player in [1, 2]:
            # Check rows and columns for subgrid
            for i in range(3):
                if all(subgrid[i, j] == player for j in range(3)):  # Check row
                    self.subgrid_wins[subgrid_index] = player
                    return player
                if all(subgrid[j, i] == player for j in range(3)):  # Check column
                    self.subgrid_wins[subgrid_index] = player
                    return player

            # Check diagonals for subgrid
            if all(subgrid[i, i] == player for i in range(3)):  # Main diagonal
                self.subgrid_wins[subgrid_index] = player
                return player
            if all(subgrid[i, 2 - i] == player for i in range(3)):  # Anti-diagonal
                self.subgrid_wins[subgrid_index] = player
                return player

        return None  # No winner in this subgrid

    def is_subgrid_full(self, subgrid_index):
        """
        Check if a specific subgrid is full (i.e., no available moves).
        """
        subgrid = self.get_subgrid(subgrid_index)
        return np.all(subgrid != 0)
    
    def update_next_subgrid(self, row, col):
        """
        Update the next subgrid based on the position of the last move.
        """
        # Determine the subgrid index where the next move should be made
        next_subgrid = (row % 3) * 3 + (col % 3)
        if self.is_subgrid_full(next_subgrid) or self.subgrid_wins[next_subgrid] != 0:
            self.next_subgrid = None  # Free play if the next subgrid is full or won
        else:
            self.next_subgrid = next_subgrid

    def display_winners(self):
        """
        Display the winners for subgrids and the overall board.
        """
        print("Subgrid Winners:")
        for i, winner in enumerate(self.subgrid_wins):
            if winner == 0:
                print(f"Subgrid {i}: No winner")
            else:
                print(f"Subgrid {i}: Player {winner} wins")

        if self.overall_winner:
            print(f"\nOverall Winner: Player {self.overall_winner}")
        else:
            print("\nOverall Winner: None")

    def print_board(self):
        """
        Print the 9x9 overall board with separation between subgrids.
        """
        print("Ultimate Tic-Tac-Toe Board (9x9):\n")
        for i in range(3):  # Iterate over 3 rows of subgrids
            for row in range(3):  # Each row within subgrid
                row_display = ""
                for j in range(3):  # Iterate over 3 columns of subgrids
                    row_display += " ".join(map(str, self.board[i * 3 + row, j * 3:j * 3 + 3])) + " | "
                print(row_display)
            print("-" * 20)
    
    def plot_board(self):
        """
        Plot the current state of the 9x9 board using matplotlib.
        """
        plt.figure(figsize=(8, 8))
        plt.title("Ultimate Tic-Tac-Toe Board")

        # Create the grid
        for i in range(10):
            # Thicker lines for 3x3 subgrid borders
            linewidth = 2 if i % 3 == 0 else 0.5
            plt.axhline(i, color='black', linewidth=linewidth, linestyle='-')
            plt.axvline(i, color='black', linewidth=linewidth, linestyle='-')

        # Set the ticks and labels
        plt.xticks(np.arange(0.5, 9, 1), [])
        plt.yticks(np.arange(0.5, 9, 1), [])

        # Fill in the board with markers
        for i in range(9):
            for j in range(9):
                # Center the markers in their respective cells
                center_x = j + 0.5
                center_y = 8.45 - i
                if self.board[i, j] == 1:
                    plt.text(center_x, center_y, 'X', fontsize=40, ha='center', va='center', color='blue')
                elif self.board[i, j] == 2:
                    plt.text(center_x, center_y, 'O', fontsize=40, ha='center', va='center', color='red')

        plt.xlim(0, 9)
        plt.ylim(0, 9)
        plt.grid(False)
        plt.gca().set_aspect('equal', adjustable='box')  # Maintain aspect ratio
        plt.show()