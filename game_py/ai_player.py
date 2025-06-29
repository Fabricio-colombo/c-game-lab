# game_py/ai_player.py
import numpy as np

class AIPlayer:
    def __init__(self, input_size=3):
        self.input_size = input_size
        self.output_size = 2 
        self.weights = np.random.randn(input_size, self.output_size)
        self.fitness = 0

    def decide(self, inputs):
        """
        inputs: [dist_obstaculo, altura_obstaculo, velocidade]
        saída:
            0 = pular
            1 = abaixar
        """
        result = np.dot(inputs, self.weights)
        return np.argmax(result)

    def mutate(self, rate=0.1):
        """Aplica uma mutação aleatória nos pesos."""
        mutation = np.random.randn(*self.weights.shape) * rate
        self.weights += mutation

    def crossover(self, other):
        """Gera um novo AIPlayer combinando os pesos de dois pais."""
        child = AIPlayer(self.input_size)
        mask = np.random.rand(*self.weights.shape) > 0.5
        child.weights = np.where(mask, self.weights, other.weights)
        return child
