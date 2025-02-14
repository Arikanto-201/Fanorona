import pygame
import random

# Initialisation de Pygame
pygame.init()
pygame.font.init()

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
GRAY  = (200, 200, 200)

# Dimensions de la fenêtre
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fanorona Telo")

# Définir une police pour afficher les messages
font = pygame.font.SysFont(None, 48)

# Positions des nœuds du plateau
nodes = {
    1: (100, 100), 2: (200, 100), 3: (300, 100),
    4: (100, 200), 5: (200, 200), 6: (300, 200),
    7: (100, 300), 8: (200, 300), 9: (300, 300)
}

# Connexions entre les nœuds (lignes du plateau)
edges = [
    (1, 2), (2, 3), (4, 5), (5, 6), (7, 8), (8, 9),
    (1, 4), (4, 7), (2, 5), (5, 8), (3, 6), (6, 9),
    (1, 5), (5, 9), (3, 5), (5, 7)
]

# Position de départ :
# - Le joueur Rouge a ses pions en haut (positions 1, 2, 3)
# - Le joueur Bleu (bot) a ses pions en bas (positions 7, 8, 9)
pieces = {
    1: "R",
    2: "R",
    3: "R",
    7: "B",
    8: "B",
    9: "B"
}

# Ensembles pour suivre quels pions n'ont pas encore bougé
unmoved_R = {1, 2, 3}
unmoved_B = {7, 8, 9}

selected_piece = None    # Pion actuellement sélectionné
current_player = "R"     # Le joueur qui commence

# Variables pour le délai et le loader du bot
bot_delay = 2000         # Délai de 2 secondes (2000 ms) pour le coup du bot
bot_thinking = False
bot_start_time = 0

clock = pygame.time.Clock()

def draw_board():
    screen.fill(WHITE)
    # Dessiner les arêtes
    for edge in edges:
        pygame.draw.line(screen, BLACK, nodes[edge[0]], nodes[edge[1]], 3)
    # Dessiner les nœuds
    for node in nodes:
        pygame.draw.circle(screen, GRAY, nodes[node], 20)
        pygame.draw.circle(screen, BLACK, nodes[node], 5)
    # Dessiner les pions
    for pos, player in pieces.items():
        color = RED if player == "R" else BLUE
        pygame.draw.circle(screen, color, nodes[pos], 18)

def get_closest_node(pos):
    for node, coord in nodes.items():
        if (coord[0] - pos[0])**2 + (coord[1] - pos[1])**2 <= 20**2:
            return node
    return None

def is_valid_move(start, end):
    return (start, end) in edges or (end, start) in edges

def check_win():
    winning_lines = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],      # Lignes horizontales
        [1, 4, 7], [2, 5, 8], [3, 6, 9],      # Lignes verticales
        [1, 5, 9], [3, 5, 7]                  # Diagonales
    ]
    for line in winning_lines:
        # Pour le joueur Rouge : la victoire n'est valide que si aucun pion de la ligne n'est resté dans sa position initiale
        if all(pos in pieces and pieces[pos] == "R" for pos in line):
            if not any(pos in unmoved_R for pos in line):
                return "R"
        # Pour le bot (Bleu)
        if all(pos in pieces and pieces[pos] == "B" for pos in line):
            if not any(pos in unmoved_B for pos in line):
                return "B"
    return None

def bot_move():
    global unmoved_B
    possible_moves = []
    for start, player in pieces.items():
        if player == "B":  # Tour du bot
            for end in nodes:
                if end not in pieces and is_valid_move(start, end):
                    possible_moves.append((start, end))
    if possible_moves:
        start, end = random.choice(possible_moves)
        # Si le pion du bot part d'une position initiale, on le retire de unmoved_B
        if start in unmoved_B:
            unmoved_B.remove(start)
        pieces[end] = pieces.pop(start)
        return True
    return False

running = True
winner = None

while running:
    draw_board()
    
    # Vérifier la victoire
    winner = check_win()
    if winner:
        message = f"Le joueur {winner} a gagné !"
        text = font.render(message, True, BLACK)
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(WHITE)
        screen.blit(overlay, (0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)  # Afficher le message 3 secondes
        running = False
        continue

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Tour du joueur humain (R) : déplacement instantané
        if current_player == "R":
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
                node = get_closest_node(click_pos)
                if node:
                    if selected_piece is None and node in pieces and pieces[node] == "R":
                        selected_piece = node
                    elif selected_piece is not None and node not in pieces and is_valid_move(selected_piece, node):
                        # Si le pion part d'une position initiale, le retirer de unmoved_R
                        if selected_piece in unmoved_R:
                            unmoved_R.remove(selected_piece)
                        pieces[node] = pieces.pop(selected_piece)
                        selected_piece = None
                        # Passe immédiatement le tour au bot et démarre le délai
                        current_player = "B"
                        bot_thinking = False  # Réinitialisation du flag du bot

    # Tour du bot avec délai de 2 secondes après le coup de l'utilisateur
    if current_player == "B":
        if not bot_thinking:
            bot_start_time = pygame.time.get_ticks()
            bot_thinking = True
        else:
            elapsed = pygame.time.get_ticks() - bot_start_time
            if elapsed >= bot_delay:
                bot_move()
                current_player = "R"
                bot_thinking = False
            else:
                # Affichage du loader pendant le délai
                num_dots = (elapsed // 300) % 4
                loader_text = "Miketrika ny Bot" + "." * num_dots
                text_surface = font.render(loader_text, True, BLACK)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(text_surface, text_rect)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
