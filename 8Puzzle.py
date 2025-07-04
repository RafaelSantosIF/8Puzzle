import customtkinter
import heapq
from tkinter import Toplevel, Text, END

#==============================================================================
# CLASSE DO SOLUCIONADOR (LÓGICA DO BACK-END)
#==============================================================================
class PuzzleSolver:
    def __init__(self, initial_state, goal_state):
        self.initial_state = tuple(map(tuple, initial_state))
        self.goal_state = tuple(map(tuple, goal_state))
        self.goal_pos = self._get_goal_positions()

    def _get_goal_positions(self):
        positions = {}
        for r, row in enumerate(self.goal_state):
            for c, tile in enumerate(row):
                if tile != 0:
                    positions[tile] = (r, c)
        return positions

    def _count_inversions(self, state):
        flat_list = [num for row in state for num in row if num != 0]
        inversions = 0
        for i in range(len(flat_list)):
            for j in range(i + 1, len(flat_list)):
                if flat_list[i] > flat_list[j]:
                    inversions += 1
        return inversions

    def is_solvable(self):
        initial_inversions = self._count_inversions(self.initial_state)
        goal_inversions = self._count_inversions(self.goal_state)
        return (initial_inversions % 2) == (goal_inversions % 2)

    def calculate_manhattan_distance(self, state):
        distance = 0
        for r, row in enumerate(state):
            for c, tile in enumerate(row):
                if tile != 0:
                    goal_r, goal_c = self.goal_pos[tile]
                    distance += abs(r - goal_r) + abs(c - goal_c)
        return distance

    def get_neighbors(self, state):
        neighbors = []
        blank_pos = next((r, c) for r, row in enumerate(state) for c, val in enumerate(row) if val == 0)
        r, c = blank_pos
        moves = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

        for move_r, move_c in moves:
            if 0 <= move_r < 3 and 0 <= move_c < 3:
                new_state_list = [list(row) for row in state]
                new_state_list[r][c], new_state_list[move_r][move_c] = new_state_list[move_r][move_c], new_state_list[r][c]
                neighbors.append(tuple(map(tuple, new_state_list)))
        return neighbors

    def solve(self):
        if not self.is_solvable():
            return None, "Este quebra-cabeças não tem solução (paridade de inversões incompatível)."

        open_set = []
        initial_h = self.calculate_manhattan_distance(self.initial_state)
        heapq.heappush(open_set, (initial_h, 0, self.initial_state))

        came_from = {}
        g_score = {self.initial_state: 0}

        while open_set:
            _, current_g, current_state = heapq.heappop(open_set)
            if current_state == self.goal_state:
                return self._reconstruct_path(came_from, current_state), "Solução encontrada!"

            for neighbor in self.get_neighbors(current_state):
                tentative_g_score = current_g + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current_state
                    g_score[neighbor] = tentative_g_score
                    h_score = self.calculate_manhattan_distance(neighbor)
                    f_score = tentative_g_score + h_score
                    heapq.heappush(open_set, (f_score, tentative_g_score, neighbor))
        return None, "Falha ao encontrar solução."

    def _reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]

#==============================================================================
# CLASSE DA INTERFACE GRÁFICA (FRONT-END)
#==============================================================================
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Solucionador de Quebra-Cabeças 8-Puzzle")
        self.geometry("600x450")
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.grid_columnconfigure((0, 1), weight=1)
        
        # --- Widgets Principais ---
        self.title_label = customtkinter.CTkLabel(self, text="Preencha as Matrizes Inicial e Objetivo", font=("Roboto", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))

        # Listas para armazenar os campos de entrada
        self.initial_entries = []
        self.goal_entries = []

        # --- Criação dos Formulários ---
        self.initial_frame = self._create_matrix_frame("Matriz Inicial", self.initial_entries)
        self.initial_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        self.goal_frame = self._create_matrix_frame("Matriz Objetivo", self.goal_entries)
        self.goal_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        # --- Botão e Status ---
        self.solve_button = customtkinter.CTkButton(self, text="Resolver", font=("Roboto", 16), command=self.solve_puzzle)
        self.solve_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

        self.status_label = customtkinter.CTkLabel(self, text="Aguardando entrada...", font=("Roboto", 14))
        self.status_label.grid(row=3, column=0, columnspan=2, padx=20, pady=(10, 20))

    def _create_matrix_frame(self, title_text, entry_list):       
        frame = customtkinter.CTkFrame(self)
        frame.grid_columnconfigure((0, 1, 2), weight=1)

        label = customtkinter.CTkLabel(frame, text=title_text, font=("Roboto", 18))
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        for r in range(3):
            row_entries = []
            for c in range(3):
                entry = customtkinter.CTkEntry(frame, width=50, height=50, font=("Roboto", 20), justify='center')
                entry.grid(row=r+1, column=c, padx=5, pady=5)
                row_entries.append(entry)
            entry_list.append(row_entries)
        
        return frame

    def _get_matrix_from_entries(self, entries):        
        matrix = []
        try:
            for r in range(3):
                row = [int(entries[r][c].get()) for c in range(3)]
                matrix.append(row)
            return matrix
        except (ValueError, TypeError):           
            return None

    def solve_puzzle(self):        
        self.status_label.configure(text="Lendo e validando matrizes...")
        self.update_idletasks() 

        initial_matrix = self._get_matrix_from_entries(self.initial_entries)
        goal_matrix = self._get_matrix_from_entries(self.goal_entries)

        # --- Validações ---
        if initial_matrix is None or goal_matrix is None:
            self.status_label.configure(text="Erro: Preencha todos os campos com números.", text_color="orange")
            return
        
        initial_tiles = sorted([n for r in initial_matrix for n in r])
        goal_tiles = sorted([n for r in goal_matrix for n in r])

        if initial_tiles != goal_tiles:
            self.status_label.configure(text="Erro: As peças das matrizes inicial e objetivo não correspondem.", text_color="orange")
            return

        self.status_label.configure(text="Resolvendo...", text_color="white")
        self.update_idletasks()

        # --- Resolução ---
        solver = PuzzleSolver(initial_matrix, goal_matrix)
        path, message = solver.solve()
        
        self.status_label.configure(text=message, text_color="lightgreen" if path else "yellow")
        
        if path:
            self.show_solution_window(path)

    def show_solution_window(self, path):        
        solution_window = customtkinter.CTkToplevel(self)
        solution_window.title("Caminho da Solução")
        solution_window.geometry("300x500")

        textbox = customtkinter.CTkTextbox(solution_window, width=300, height=500, font=("Consolas", 14))
        textbox.pack(expand=True, fill="both")

        for i, state in enumerate(path):
            textbox.insert(END, f"--- Passo {i} ---\n")
            for row in state:
                textbox.insert(END, f" {list(row)}\n")
            textbox.insert(END, "\n")
        
        textbox.configure(state="disabled") 


if __name__ == "__main__":
    app = App()
    app.mainloop()