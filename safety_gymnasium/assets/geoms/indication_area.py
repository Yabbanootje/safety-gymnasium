# Copyright 2022-2023 OmniSafe Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Hazard."""

from dataclasses import dataclass, field

import numpy as np

from safety_gymnasium.assets.color import COLOR
from safety_gymnasium.assets.group import GROUP
from safety_gymnasium.bases.base_object import Geom


@dataclass
class IndicationArea(Geom):  # pylint: disable=too-many-instance-attributes
    """
    
    """
    name: str = 'indication_area'
    num: int = 8
    x_width: float = 1.0
    y_width: float = 2.0
    placements: list = None
    locations: list = field(default_factory=list)  # Fixed locations to override placements
    keepout: float = 0.0

    color: np.array = COLOR['sigwall']
    alpha: float = 0.1
    group: np.array = GROUP['sigwall']
    is_lidar_observed: bool = False
    is_constrained: bool = False
    is_meshed: bool = False
    mesh_name: str = name

    def get_config(self, xy_pos, rot):  # pylint: disable=unused-argument
        """To facilitate get specific config for this object."""
        body = {
            'name': self.name,
            'pos': np.r_[xy_pos, 0.25],
            'rot': 0,
            'geoms': [
                {
                    'name': self.name,
                    'size': np.array([self.x_width, self.y_width, 0.05]),
                    'type': 'box',
                    'contype': 0,
                    'conaffinity': 0,
                    'group': self.group,
                    'rgba': self.color * np.array([1, 1, 1, self.alpha]),
                },
            ],
        }
        if self.is_meshed:
            body['geoms'][0].update(
                {
                    'type': 'mesh',
                    'mesh': self.mesh_name,
                    'material': self.mesh_name,
                    'euler': [0, 0, 0],
                },
            )
        return body

    def cal_cost(self):
        return 0

    @property
    def pos(self):
        """Helper to get list of Sigwalls positions."""
