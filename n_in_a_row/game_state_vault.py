from __future__ import annotations

import pickle
from copy import copy, deepcopy
from typing import cast

import redis

from n_in_a_row.game_state import GameState
from n_in_a_row.config import load_config


class GameStateProxy:

    def __init__(
            self,
            game_state_id: int,
            game_state_vault: GameStateVault
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

    def __hash__(self) -> int:
        self._load_game_state()
        return hash(self.game_state)

    def __copy__(self):
        self._load_game_state()
        return copy(self.game_state)

    def __deepcopy__(self, memodict):
        self._load_game_state()
        return deepcopy(self.game_state)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.game_state_id == other
        self._load_game_state()
        return self.game_state == other

    def __ne__(self, other):
        if isinstance(other, int):
            return self.game_state_id != other
        self._load_game_state()
        return self.game_state != other

    def __repr__(self) -> str:
        self._load_game_state()
        return repr(self.game_state)


class GameStateVault:

    def __init__(self):
        config = load_config()
        self.redis = redis.Redis(
            host=config['redis']['host'],
            port=config['redis']['port']
        )

    def save_game_state(
            self,
            game_state: GameState,
            *,
            overwrite: bool = True
    ) -> int:
        game_state_id = hash(game_state)
        if not overwrite and game_state_id in self.redis:
            return game_state_id

        game_state = copy(game_state)
        if game_state.parents:
            game_state.parents = [hash(parent) for parent in game_state.parents]
        game_state.children = [hash(child) for child in game_state.children]

        data = pickle.dumps(game_state)
        if not self.redis.set(game_state_id, data):
            raise RuntimeError(f'Redis: Failed to save GameState {game_state_id}')
        return game_state_id

    def load_game_state(self, game_state_id: int) -> GameState:
        data = self.redis.get(game_state_id)
        if data is None:
            raise GameStateNotInVaultError(game_state_id)
        game_state: GameState = pickle.loads(data)
        if game_state.parents:
            game_state.parents = [GameStateProxy(cast(int, parent), self) for parent in game_state.parents]
        game_state.children = [
            GameStateProxy(cast(int, child), self) for child in game_state.children
        ]
        return game_state


class GameStateNotInVaultError(Exception):

    def __init__(self, game_state_id: int, *args):
        if not args:
            args = [f'GameState with id f{game_state_id} is not found']
        super().__init__(*args)
        self.game_state_id = game_state_id
