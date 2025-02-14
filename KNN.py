import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

# Correction de l'initialisation de la classe FanoronaTelo
class FanoronaTelo:
    def __init__(self, board=None, turn='X'):
        self.board = board if board else [[' ' for _ in range(3)] for _ in range(3)]
        self.turn = turn  # 'X' ou 'O'

    def get_successor(self):
        successors = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':  # Case vide
                    new_board = [row[:] for row in self.board]
                    new_board[i][j] = self.turn
                    successors.append(FanoronaTelo(new_board, 'O' if self.turn == 'X' else 'X'))
        return successors

# Génération du dataset pour un problème de classification binaire
def generate_dataset():
    X, y = [], []
    for _ in range(500):
        game = FanoronaTelo()
        board_state = np.random.choice(['X', 'O', ' '], (3, 3))
        game.board = board_state.tolist()

        # Encodage des cases en valeurs numériques
        board_encoded = np.array([[1 if cell == 'X' else -1 if cell == 'O' else 0 for cell in row] 
                                  for row in board_state])
        X.append(board_encoded.flatten())  # Transformation en vecteur 1D

        # Création d'une classe binaire à partir d'un score aléatoire
        score = random.uniform(-1, 1)
        y.append(1 if score > 0 else 0)
    
    return np.array(X), np.array(y)

# Génération des données
X, y = generate_dataset()

# Normalisation des données
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Séparation des données en ensemble d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modèle de régression logistique
logreg = LogisticRegression()
logreg.fit(X_train, y_train)

# Prédictions
y_pred = logreg.predict(X_test)

# Évaluation du modèle
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy du modèle de régression logistique : {accuracy:.4f}")

# Affichage de la matrice de confusion
cm = confusion_matrix(y_test, y_pred)
print("Matrice de confusion :")
print(cm)

# Visualisation des prédictions (comparaison des classes réelles et prédites)
plt.figure(figsize=(10, 5))
plt.scatter(range(len(y_test)), y_test, label="Classes réelles", color="blue", alpha=0.6)
plt.scatter(range(len(y_pred)), y_pred, label="Prédictions", color="red", alpha=0.6)
plt.xlabel("Échantillons")
plt.ylabel("Classe")
plt.title("Comparaison des Prédictions vs Réel (Régression Logistique)")
plt.legend()
plt.show()

# Remarque : Le graphe du taux de vrais positifs (ROC) a été supprimé.
