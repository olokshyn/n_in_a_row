import pickle
from copy import copy

import redis

from solver.game_state import GameState
from config import load_config


class GameStateProxy:

    def __init__(
            self,
            game_state_id: int,
            game_state_vault: 'GameStateVault'
    ):
        self.game_state = None
        self.game_state_id = game_state_id
        self.vault = game_state_vault

    def _load_game_state(self) -> None:
        if self.game_state is None:
            self.game_state = self.vault.load_game_state(self.game_state_id)

    def __getattr__(self, item):
        self._load_game_state()
        return getattr(self.game_state, item)

    def __hash__(self):
        self._load_game_state()
        return hash(self.game_state)


class GameStateVault:

    def __init__(self):
        config = load_config()
        self.redis = redis.Redis(
            host=config['redis']['host'],
            port=config['redis']['port']
        )

    def save_game_state(self, game_state: GameState) -> int:
        game_state_id = hash(game_state)
        if game_state_id in self.redis:
            return game_state_id

        game_state = copy(game_state)
        if game_state.parent is not None:
            game_state.parent = hash(game_state.parent)
        game_state.children = [
            self.save_game_state(child) for child in game_state.children
        ]

        data = pickle.dumps(game_state)
        if not self.redis.set(game_state_id, data):
            raise RuntimeError(f'Redis: Failed to save GameState {game_state_id}')
        return game_state_id

    def load_game_state(self, game_state_id: int) -> GameState:
        data = self.redis.get(game_state_id)
        if data is None:
            raise RuntimeError(f'GameState with id f{game_state_id} is not found')
        game_state: GameState = pickle.loads(data)
        if game_state.parent is not None:
            game_state.parent = GameStateProxy(game_state.parent, self)
        game_state.children = [
            GameStateProxy(child, self) for child in game_state.children
        ]
        return game_state