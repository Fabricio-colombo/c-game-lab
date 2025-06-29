# game_py/best_player.py
import pickle

def save_best(player, path="best_player.pkl"):
    with open(path, "wb") as f:
        pickle.dump(player.weights, f)

def load_best(input_size=3, path="best_player.pkl"):
    from ai_player import AIPlayer
    player = AIPlayer(input_size)
    try:
        with open(path, "rb") as f:
            player.weights = pickle.load(f)
        print("Melhor jogador carregado com sucesso!")
    except FileNotFoundError:
        print("Nenhum jogador salvo encontrado.")
    return player
