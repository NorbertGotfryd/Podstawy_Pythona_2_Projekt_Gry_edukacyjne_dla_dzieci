# Projekt Dokumentacji: Gry Edukacyjne dla Dzieci

## Wprowadzenie

### Projekt zatytułowany "Gry Edukacyjne dla Dzieci" obejmuje trzy różne gry zaimplementowane przy użyciu biblioteki Pygame w języku Python. Celem gier jest edukacja i angażowanie młodych użytkowników. Projekt obejmuje następujące gry:

    Zapamiętywanie obrazków
    Gra Labirynt
    Połącz cienie

### Głównym celem jest stworzenie interaktywnych i wizualnie atrakcyjnych gier, które pomagają rozwijać pamięć, umiejętności rozwiązywania problemów oraz rozpoznawanie wzorców u dzieci.

## echnologie i Biblioteki Użyte
### Python i Pygame

    Python: Język programowania użyty do całego projektu.
    Pygame: Zestaw modułów Pythona zaprojektowany do tworzenia gier wideo, oferujący funkcje takie jak obsługa obrazów, zarządzanie zdarzeniami i kontrola pętli gry.

### Inne Biblioteki

    os: Używany do operacji na plikach i katalogach.
    random: Używany do losowego wyboru i tasowania, co jest kluczowe dla logiki gry.

## Struktura Projektu
### Organizacja Plików

### Projekt jest zorganizowany w różnych katalogach, aby utrzymać zasoby i kod w modułowej i zarządzalnej formie:

    Backgrounds: Zawiera obrazy tła dla różnych ekranów gry.
    Labyrinth game assets: Zawiera specyficzne zasoby, takie jak kafelki startowe i wyjściowe dla gry labirynt.
    Memory game assets: Zawiera obrazy używane jako kafelki w grze pamięciowej.
    Match the shadow assets: Zawiera obrazy kształtów i ich cieni dla gry "Dopasuj Cienie".
    Documentation: Zawiera dokumentację do projektu w formatach Markdown oraz .pdf.
    Scripts: Zawiera pliki skryptów potrzebnych do projektu, w tym przypadku jest to jeden plik.

## Kluczowe Moduły i Funkcje

    load_images: Ładuje i skalują obrazy, aby pasowały do kafelków gry.

        ```python
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
        ```

    create_board: Generuje planszę do gry pamięciowej.

        ```python
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

        ```

    draw_board: Renderuje planszę gry pamięciowej na ekranie.

        ```python
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

        ```

    generate_labyrinth: Tworzy proceduralny labirynt za pomocą algorytmu DFS (Przeszukiwanie w Głąb).

        ```python


        ```

    draw_labyrinth: Renderuje labirynt na ekranie.

        ```python
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
        ```

    create_game_pieces: Przygotowuje elementy gry i ich odpowiednie cienie dla gry "Dopasuj Cienie".

        ```python
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

        ```

    main_menu: Wyświetla główne menu do wyboru gry.

        ```python
        def main_menu(screen, background_image):
            font = pygame.font.Font(None, FONT_SIZE)
            menu_items = ["Zapamiętywanie obrazków", "Labirynt", "Połącz cienie", "Wyjście z gry"]
            menu_rects = []

        ```

    memory_game: Zarządza główną w zapamiętywanie obrazków.

        ```python
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

        ```

    labyrinth_game: Zarządza główną pętlą gry labirynt.

        ```python
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
        ```

    match_the_shadows_game: Zarządza główną pętlą gry "Dopasuj Cienie".

        ```python
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
        ```


## Szczegółowe Opisy Gier
### Gra Pamięciowa

Gra Pamięciowa polega na planszy wypełnionej parami ukrytych obrazów. Zadaniem gracza jest odkrycie pasujących par. Rozmiar planszy można wybrać spośród kilku opcji (2x2, 4x4, 6x6, 8x8).
Najważniejsze Funkcje

    create_board: Losowo wybiera i układa obrazy w pary na planszy.
    draw_board: Obsługuje renderowanie kafelków, pokazując albo obraz, albo symbol zastępczy w zależności od działań gracza.
    all_tiles_matched: Sprawdza, czy wszystkie pary zostały prawidłowo dopasowane.


### Gra Labirynt

Gra Labirynt przedstawia proceduralnie generowany labirynt. Gracz musi nawigować od pozycji startowej do wyjścia, unikając ścian.
Najważniejsze Funkcje

    generate_labyrinth: Używa DFS do generowania losowego labiryntu.
    draw_labyrinth: Rysuje labirynt, pozycje startową i wyjściową oraz ścieżkę gracza
    is_valid_move: Waliduje ruchy gracza, zapewniając, że nie przechodzą przez ściany.

### Gra Dopasuj Cienie

W tej grze gracze dopasowują kształty do ich odpowiednich cieni. Gra ta ma na celu poprawę rozpoznawania wzorców i zdolności wizualnych.
Najważniejsze Funkcje

    create_game_pieces: Losowo łączy kształty i cienie.
    draw_board: Wyświetla kształty i cienie po przeciwnych stronach ekranu.
    is_valid_match: Sprawdza, czy wybrany kształt pasuje do wybranego cienia.

## Instalacja i Uruchamianie Projektu
Wymagania

    Python 3.11.9
    Biblioteka Pygame

Kroki Instalacji

    Sklonuj repozytorium z linku Git - https://github.com/NorbertGotfryd/Podstawy_Pythona_2_Projekt_Gry_edukacyjne_dla_dzieci
    Przejdź do katalogu projektu.
    Zainstaluj wymagane pakiety Pythona, używając:

bash

pip install pygame

    Uruchom główny skrypt, aby rozpocząć grę:

bash

python main.py

## Raport z Realizacji Projektu

### Realizacja projektu obejmowała kilka kluczowych kroków:

    Projektowanie Logiki Gry: Dla każdej gry szczegółowa logika została opracowana w celu zapewnienia angażującej rozgrywki.
    Proceduralne Generowanie Treści: Zaimplementowane dla gry labirynt, zapewniając unikalne doświadczenie za każdym razem.
        Dla pozostałych dwóch gier proceduralne generowanie treści ogranicza się do wyboru użytych obrazków.

### Napotkane Wyzwania

    Skalowanie Obrazów: Upewnienie się, że wszystkie obrazy są prawidłowo skalowane w celu utrzymania atrakcyjności wizualnej, było wyzwaniem.
    Generowanie Labiryntu: Tworzenie labiryntu, który był zarówno rozwiązywalny, jak i stanowiący wyzwanie, wymagało dostosowania algorytmu DFS.

### Przyszłe Ulepszenia

    Wsparcie dla Trybu Wieloosobowego: Dodanie funkcji dla wielu graczy, aby dzieci mogły grać razem.
    Elementy mierzalność sukcesu: Dodanie takich funkcji jak wskaźnik czasu oraz ilość ruchów potrzebny do ukończenia etapu.
    Zaawansowane Poziomy: Wprowadzenie wielu poziomów o rosnącym stopniu trudności.
    Interaktywne Samouczki: Dodanie samouczków w grze, aby pomóc graczom lepiej zrozumieć mechanikę gry.

## Wniosek

Projekt ten z demonstruje użycie Pygame do tworzenia edukacyjnych gier dla dzieci.
Gry są zaprojektowane tak, aby były zarówno zabawne, jak i edukacyjne, pomagając dzieciom rozwijać różne umiejętności poznawcze.

## Źródła Wiedzy

    https://www.pygame.org/docs/ - Dokumentacja pygame
    https://docs.python.org/pl/3/reference/index.html - Oficjalna Dokumentacja Pythona
    https://www.rawpixel.com - pobrane zdjecia, wszystkie poochodza z domeny publicznej lub są generoowane przez ai
    https://chatgpt.com - debugowanie, pomoc w rozwiazaniach problemów, generowanie obrazów
    https://coderslegacy.com/python/python-pygame-tutorial/ - zapoznanie z technologia pygame
    https://www.youtube.com/watch?v=PjcjkQZCXRI - pierwotny tutorial który dal mi koncepcje na pierwszą gre
    https://favtutor.com/blogs/depth-first-search-python - opis algorytmu DFS ktory zmodyfikowany zostal użyty w grze labirynt.
    https://www.youtube.com/watch?v=sTRK9mQgYuc&themeRefresh=1 - tutorial funkcjonowania algorytmu DFS