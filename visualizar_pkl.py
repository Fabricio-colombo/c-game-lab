import pickle
import numpy as np

def show_best_info(path="best_player.pkl"):
    try:
        with open(path, "rb") as f:
            weights = pickle.load(f)
        print("Pesos carregados:")
        print(weights)
        print(f"Media dos pesos: {np.mean(weights):.4f}")
        print(f"Maximo dos pesos: {np.max(weights):.4f}")
        print(f"Minimo dos pesos: {np.min(weights):.4f}")
    except Exception as e:
        print(f"Erro ao carregar: {e}")

show_best_info()
