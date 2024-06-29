import pygame
import os
import random

# Inicjalizacja Pygame
pygame.init()

# Stałe
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
FPS = 30
TILE_SIZE = 100
PADDING = 10
FONT_SIZE = 40

# Dostosuj rozmiar okna w oparciu o maksymalny rozmiar planszy (8x8)
MAX_BOARD_SIZE = 8
WINDOW_WIDTH = MAX_BOARD_SIZE * (TILE_SIZE + PADDING) + PADDING
WINDOW_HEIGHT = MAX_BOARD_SIZE * (TILE_SIZE + PADDING) + PADDING

# Załaduj obrazy (zaktualizowane, aby zwracały słownik dla kształtów i cieni)
def load_images(path, tile_size):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Katalog {path} nie istnieje.")
    
    images = {}
    for filename in os.listdir(path):
        if filename.endswith('.png'):
            img = pygame.image.load(os.path.join(path, filename)).convert_alpha()
            img = scale_image_to_fit_tile(img, tile_size)
            image_name = os.path.splitext(filename)[0]
            images[image_name] = img
    
    if not images:
        raise FileNotFoundError(f"Nie znaleziono obrazów PNG w katalogu {path}.")
    
    return images

# Skaluj obraz, aby zmieścił się w kafelku, zachowując współczynnik proporcji
def scale_image_to_fit_tile(image, tile_size):
    image_rect = image.get_rect()
    scale_factor = min(tile_size / image_rect.width, tile_size / image_rect.height)
    new_size = (int(image_rect.width * scale_factor), int(image_rect.height * scale_factor))
    return pygame.transform.smoothscale(image.convert_alpha(), new_size)

# Skaluj obraz tła, aby wypełnić rozmiar okna
def scale_background_image(image, window_width, window_height):
    return pygame.transform.scale(image, (window_width, window_height))

# Utwórz nową planszę do gry
def create_board(size, images):
    num_tiles = (size * size) // 2
    if num_tiles > len(images):
        raise ValueError(f"Za mało unikatowych obrazów, aby zapełnić planszę {size}x{size}. Wymagana liczba obrazów {num_tiles}, ale dostępna jest tylko liczba {len(images)}.")
    
    selected_images = random.sample(list(images.values()), num_tiles)
    tiles = selected_images * 2
    random.shuffle(tiles)
    
    board = []
    for i in range(size):
        row = []
        for j in range(size):
            if tiles:  # Upewnij się, że lista kafelków nie jest pusta
                row.append(tiles.pop())
            else:
                raise IndexError("Za mało kafelek, aby zapełnić planszę.")
        board.append(row)
    return board

# Narysuj planszę do gry
def draw_board(screen, board, revealed, offset_x, offset_y):
    for i, row in enumerate(board):
        for j, tile in enumerate(row):
            x = offset_x + j * (TILE_SIZE + PADDING)
            y = offset_y + i * (TILE_SIZE + PADDING)
            pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE)) # Dodaj białe tło do każdego kafelka
            if revealed[i][j]:
                tile_rect = tile.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                screen.blit(tile, tile_rect.topleft)
            else:
                pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 2)

# Sprawdź, czy wszystkie kafelki są dopasowane
def all_tiles_matched(revealed):
    for row in revealed:
        if False in row:
            return False
    return True

# Wygeneruj proceduralny labirynt używając algorytmu "Depth-First Search"
def generate_labyrinth(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]

    def carve_passages_from(cx, cy, grid):
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)
        for (dx, dy) in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == 1:
                grid[cy + dy // 2][cx + dx // 2] = 0
                grid[ny][nx] = 0
                carve_passages_from(nx, ny, grid)

    maze[1][1] = 0
    carve_passages_from(1, 1, maze)
    return maze

# Tworzenie tęczowego tła
def draw_rainbow_walls(screen, maze, cell_size):
    width = len(maze[0])
    height = len(maze)
    colors = []
    for i in range(height):
        color = pygame.Color(0)
        color.hsva = (i / height * 360, 100, 100)
        colors.append(color)
    
    for y in range(height):
        for x in range(width):
            if maze[y][x] == 1:
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, colors[y], rect)
                pygame.draw.rect(screen, BLACK, rect, 1)

# Narysuj labirynt
def draw_labyrinth(screen, maze, path, cell_size, start_pos, exit_pos, start_image, exit_image):
    width = len(maze[0])
    height = len(maze)
    colors = []
    for i in range(width):
        color = pygame.Color(0)
        color.hsva = (i / width * 360, 100, 100)
        colors.append(color)
    
    for y in range(height):
        for x in range(width):
            if maze[y][x] == 1:
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, colors[x], rect)
                pygame.draw.rect(screen, BLACK, rect, 1)
            else:
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)

    # Narysuj obraz początkowy w pozycji początkowej
    sx, sy = start_pos
    start_rect = start_image.get_rect(center=(sx * cell_size + cell_size // 2, sy * cell_size + cell_size // 2))
    screen.blit(start_image, start_rect.topleft)

    # Rysowanie obrazu wyjścia
    ex, ey = exit_pos
    exit_rect = exit_image.get_rect(center=(ex * cell_size + cell_size // 2, ey * cell_size + cell_size // 2))
    screen.blit(exit_image, exit_rect.topleft)

    if len(path) > 1:
        pygame.draw.lines(screen, RED, False, path, 2)

# Sprawdzenie czy ścieżka przecina ścianę
def is_valid_move(maze, path, cell_size):
    if len(path) < 2:
        return True
    x1, y1 = path[-2]
    x2, y2 = path[-1]
    cx1, cy1 = x1 // cell_size, y1 // cell_size
    cx2, cy2 = x2 // cell_size, y2 // cell_size
    if abs(cx2 - cx1) + abs(cy2 - cy1) > 1:
        return False
    if maze[cy2][cx2] == 1:
        return False
    return True

# Ładowanie obrazów cieni
def load_shadow_images(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Katalog {path} nie istnieje.")
    
    shadows = {}
    for filename in os.listdir(path):
        if filename.endswith('.png'):
            shadow_name = filename.split('.')[0]
            img = pygame.image.load(os.path.join(path, filename)).convert_alpha()
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            img.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
            shadows[shadow_name] = img
    
    if not shadows:
        raise FileNotFoundError(f"Nie znaleziono obrazów PNG w katalogu {path}.")
    
    return shadows

# Tworzenie elementów gry i cieni do gry w dopasowywanie cieni
def create_game_pieces(shapes, shadows, num_pieces):
    pieces = []
    shadows_list = []
    
    for _ in range(num_pieces):
        shape_name = random.choice(list(shapes.keys()))
        pieces.append((shape_name, shapes[shape_name]))
        shadows_list.append((shape_name, shadows[shape_name]))
    
    random.shuffle(pieces)
    random.shuffle(shadows_list)
    return pieces, shadows_list

# Tworzenie menu głównego
def main_menu(screen, background_image):
    font = pygame.font.Font(None, FONT_SIZE)
    menu_items = ["Zapamiętywanie obrazków", "Labirynt", "Połącz cienie", "Wyjście z gry"]
    menu_rects = []

    # Dostosowanie przesunięcia pionowego
    initial_y_offset = WINDOW_HEIGHT // 2 - 120  # Przesuń elementy w górę
    vertical_spacing = 75  # Odstępy między elementami menu

    for idx, item in enumerate(menu_items):
        text = font.render(item, True, BLACK)
        rect = text.get_rect(center=(WINDOW_WIDTH // 2, initial_y_offset + idx * vertical_spacing))
        menu_rects.append((text, rect))

    while True:
        screen.fill(WHITE)
        bg_rect = background_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(background_image, bg_rect.topleft)

        for text, rect in menu_rects:
            screen.blit(text, rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "Wyjście z gry"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for idx, (text, rect) in enumerate(menu_rects):
                    if rect.collidepoint(event.pos):
                        return menu_items[idx]

        pygame.time.Clock().tick(FPS)

# Menu wyboru gry z dodatkowym tekstem
def game_selection_menu(screen, background_image, game_type):
    font = pygame.font.Font(None, FONT_SIZE)
    
    # Dodatkowy tekst wyświetlany nad pozycjami menu
    if game_type == "Zapamiętywanie obrazków":
        menu_items = ["2x2", "4x4", "6x6", "8x8"]
        menu_values = [2, 4, 6, 8]
        instruction = "Połącz obrazki w pary."
        additional_text = "Wybierz rozmiar planszy:"
    elif game_type == "Połącz cienie":
        menu_items = ["3 objects", "6 objects", "9 objects", "12 objects"]
        menu_values = [3, 6, 9, 12]
        instruction = "Połącz zwierzęta z ich cieniem."
        additional_text = "Wybierz liczbę zwierząt:"
    
    menu_rects = []
    
    # Tekst dodatkowy 
    additional_text_surf = font.render(additional_text, True, BLACK)
    additional_text_rect = additional_text_surf.get_rect(center=(WINDOW_WIDTH // 2 + 5, WINDOW_HEIGHT // 2 - 50))
    instruction_surf = font.render(instruction, True, BLACK)
    instruction_rect = instruction_surf.get_rect(center=(WINDOW_WIDTH // 2 + 5, WINDOW_HEIGHT // 2 - 110))

    # Dostosowywanie pozycji elementów menu
    for idx, item in enumerate(menu_items):
        text = font.render(item, True, BLACK)
        rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2+ idx * 50))
        menu_rects.append((text, rect))
    
    while True:
        screen.fill(WHITE)
        bg_rect = background_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(background_image, bg_rect.topleft)
        
        # Rysowanie dodatkowego tekstu
        screen.blit(additional_text_surf, additional_text_rect)
        screen.blit(instruction_surf, instruction_rect)
        
        for text, rect in menu_rects:
            screen.blit(text, rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for idx, (text, rect) in enumerate(menu_rects):
                    if rect.collidepoint(event.pos):
                        return menu_values[idx]
        
        pygame.time.Clock().tick(FPS)


# Wyświetlanie ekranu z gratulacjami
def display_congratulations(screen, background_image):
    font = pygame.font.Font(None, 60)
    text = font.render("Gratulacje!", True, BLACK)
    rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    
    while True:
        screen.fill(WHITE)
        bg_rect = background_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(background_image, bg_rect.topleft)
        screen.blit(text, rect)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return

# Pętla gry w zapamiętywanie obrazków
def memory_game(screen, board_size, images, background_image, congratulations_image):
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    # Oblicz przesunięcia w celu wyśrodkowania płytki 
    offset_x = (WINDOW_WIDTH - (board_size * (TILE_SIZE + PADDING) - PADDING)) // 2
    offset_y = (WINDOW_HEIGHT - (board_size * (TILE_SIZE + PADDING) - PADDING)) // 2

    try:
        board = create_board(board_size, images)
    except ValueError as e:
        print(e)
        return
    
    revealed = [[False] * board_size for _ in range(board_size)]
    first_selection = None
    running = True
    show_mismatched = False
    mismatched_tiles = []
    mismatch_time = 0

    while running:
        screen.fill(WHITE)
        bg_rect = background_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(background_image, bg_rect.topleft)
        draw_board(screen, board, revealed, offset_x, offset_y)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not show_mismatched:
                x, y = event.pos
                col = (x - offset_x) // (TILE_SIZE + PADDING)
                row = (y - offset_y) // (TILE_SIZE + PADDING)
                if 0 <= row < board_size and 0 <= col < board_size and not revealed[row][col]:
                    revealed[row][col] = True
                    if first_selection is None:
                        first_selection = (row, col)
                    else:
                        r1, c1 = first_selection
                        if board[r1][c1] != board[row][col]:
                            show_mismatched = True
                            mismatched_tiles = [(r1, c1), (row, col)]
                            mismatch_time = pygame.time.get_ticks()
                        first_selection = None

        if show_mismatched and pygame.time.get_ticks() - mismatch_time > 1000:
            for (r, c) in mismatched_tiles:
                revealed[r][c] = False
            show_mismatched = False
        
        if all_tiles_matched(revealed):
            display_congratulations(screen, congratulations_image)
            return
        
        pygame.time.Clock().tick(FPS)
    
    pygame.quit()

# Pętla gry w labiryncie
def labyrinth_game(screen, background_image, congratulations_image, start_image, exit_image):
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    maze_size = 21
    cell_size = WINDOW_WIDTH // maze_size
    
    maze = generate_labyrinth(maze_size, maze_size)
    
    path = []
    drawing = False
    start_pos = (maze_size // 2, maze_size // 2)
    start_pixel = (start_pos[0] * cell_size + cell_size // 2, start_pos[1] * cell_size + cell_size // 2)
    path.append(start_pixel)
    
    # Ustaw pozycję wyjściową losowo wybraną z ostatnich rzędów 
    exit_pos = (random.randint(maze_size - 3, maze_size - 1), random.randint(0, maze_size - 1))
    while maze[exit_pos[1]][exit_pos[0]] == 1:
        exit_pos = (random.randint(maze_size - 3, maze_size - 1), random.randint(0, maze_size - 1))
    
    running = True
    while running:
        screen.blit(background_image, (0, 0))
        draw_labyrinth(screen, maze, path, cell_size, start_pos, exit_pos, start_image, exit_image)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    pos = event.pos
                    if path[-1] != pos:
                        path.append(pos)
                        if not is_valid_move(maze, path, cell_size):
                            path.pop()  # Usuń nieprawidłowy ruch 

        # Sprawdzanie czy gracz dotarł do wyjścia
        if path[-1][0] // cell_size == exit_pos[0] and path[-1][1] // cell_size == exit_pos[1]:
            display_congratulations(screen, congratulations_image)
            return
        
        pygame.time.Clock().tick(FPS)
    
    pygame.quit()

# Pętla gry w dopasowanie cieni
def match_the_shadows_game(screen, num_pieces, shapes, shadows, background_image, congratulations_image):
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Obliczanie wysokości każdego objektu w celu zmieszczenia wszystkich obiektów w planszy
    max_object_height = (WINDOW_HEIGHT - (num_pieces + 1) * PADDING) // num_pieces
    piece_size = min(TILE_SIZE, max_object_height)

    # Skalowanie objektów i cieni w razie potrzeby
    scaled_shapes = {name: pygame.transform.scale(img, (piece_size, piece_size)) for name, img in shapes.items()}
    scaled_shadows = {name: pygame.transform.scale(img, (piece_size, piece_size)) for name, img in shadows.items()}

    pieces, shadows_list = create_game_pieces(scaled_shapes, scaled_shadows, num_pieces)
    piece_positions = [(50, i * (piece_size + PADDING) + PADDING) for i in range(num_pieces)]
    shadow_positions = [(WINDOW_WIDTH - 50 - piece_size, i * (piece_size + PADDING) + PADDING) for i in range(num_pieces)]

    selected_piece = None
    lines = []

    running = True
    while running:
        screen.fill(WHITE)
        bg_rect = background_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(background_image, bg_rect.topleft)

        for (name, image), pos in zip(pieces, piece_positions):
            pygame.draw.rect(screen, WHITE, (pos[0] - PADDING // 2, pos[1] - PADDING // 2, piece_size + PADDING, piece_size + PADDING))  # Dodaj białe kwadratowe tło
            screen.blit(image, pos)

        for (name, shadow), pos in zip(shadows_list, shadow_positions):
            pygame.draw.rect(screen, WHITE, (pos[0] - PADDING // 2, pos[1] - PADDING // 2, piece_size + PADDING, piece_size + PADDING))  # Dodaj białe kwadratowe tło
            screen.blit(shadow, pos)

        for line in lines:
            pygame.draw.line(screen, BLACK, line[0], line[1], 2)

        # Rysowanie liniy podczas przeciągania obiektu do cienia
        if selected_piece is not None:
            pygame.draw.line(screen, BLACK, selected_piece[1], pygame.mouse.get_pos(), 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, pos in enumerate(piece_positions):
                    x, y = pos
                    if x <= event.pos[0] <= x + piece_size and y <= event.pos[1] <= y + piece_size:
                        selected_piece = (i, event.pos)
                        break
            elif event.type == pygame.MOUSEBUTTONUP:
                if selected_piece is not None:
                    for i, pos in enumerate(shadow_positions):
                        x, y = pos
                        if x <= event.pos[0] <= x + piece_size and y <= event.pos[1] <= y + piece_size:
                            if pieces[selected_piece[0]][0] == shadows_list[i][0]:
                                # Sprawdź, czy ten cień jest już dopasowany, zabezpieczenie przed wielokrotnym dopasowywaniu tej samej pary
                                if all(line[1] != pos for line in lines):
                                    lines.append((selected_piece[1], pos))
                                break
                    selected_piece = None

        if len(lines) == num_pieces:
            display_congratulations(screen, congratulations_image)
            return

    pygame.quit()

def main():
    script_dir = os.path.dirname(__file__)
    base_dir = os.path.abspath(os.path.join(script_dir, os.pardir))

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Gry edukacyjne dla dzieci")
    
    backgrounds_path = os.path.join(base_dir, 'Backgrounds')
    menu_background = scale_background_image(pygame.image.load(os.path.join(backgrounds_path, 'menu_background.png')), WINDOW_WIDTH, WINDOW_HEIGHT)
    memory_game_background = scale_background_image(pygame.image.load(os.path.join(backgrounds_path, 'memory_game_background.png')), WINDOW_WIDTH, WINDOW_HEIGHT)
    labyrinth_game_background = scale_background_image(pygame.image.load(os.path.join(backgrounds_path, 'labyrinth_game_background.png')), WINDOW_WIDTH, WINDOW_HEIGHT)
    shape_game_background = scale_background_image(pygame.image.load(os.path.join(backgrounds_path, 'shape_game_background.png')), WINDOW_WIDTH, WINDOW_HEIGHT)
    congratulations_image = scale_background_image(pygame.image.load(os.path.join(backgrounds_path, 'congratulations_background.png')), WINDOW_WIDTH, WINDOW_HEIGHT)

    labyrinth_assets_path = os.path.join(base_dir, 'Labyrinth game assets')
    start_image = pygame.image.load(os.path.join(labyrinth_assets_path, 'start_tile.png'))
    start_image = pygame.transform.scale(start_image, (40, 40))
    exit_image = pygame.image.load(os.path.join(labyrinth_assets_path, 'exit_tile.png'))
    exit_image = pygame.transform.scale(exit_image, (40, 40))
    
    shapes_path = os.path.join(base_dir, 'Match the shadow assets')
    shapes = load_images(shapes_path, TILE_SIZE)
    shadows = load_shadow_images(shapes_path)
    
    while True:
        game_choice = main_menu(screen, menu_background)
        if game_choice == "Zapamiętywanie obrazków":
            board_size = game_selection_menu(screen, memory_game_background, "Zapamiętywanie obrazków")
            if board_size:
                images_path = os.path.join(base_dir, 'Memory game assets')
                try:
                    images = load_images(images_path, TILE_SIZE)
                except FileNotFoundError as e:
                    print(e)
                    continue
                
                memory_game(screen, board_size, images, memory_game_background, congratulations_image)
        elif game_choice == "Labirynt":
            labyrinth_game(screen, labyrinth_game_background, congratulations_image, start_image, exit_image)
        elif game_choice == "Połącz cienie":
            num_pieces = game_selection_menu(screen, shape_game_background, "Połącz cienie")
            if num_pieces:
                match_the_shadows_game(screen, num_pieces, shapes, shadows, shape_game_background, congratulations_image)
        elif game_choice == "Wyjście z gry":
            pygame.quit()
            return
    
if __name__ == "__main__":
    main()
