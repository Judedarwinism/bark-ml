# Copyright (c) 2020 fortiss GmbH
#
# Authors: Patrick Hart
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import pickle
from enum import Enum

class Tracer:
  def __init__(self):
    self._states = []
    self._trace_history = True
    self._total_episodes = 0  # increases with terminal count
    self._total_collisions = 0
    self._total_goals_reached = 0
    self._total_reward = 0
    self._total_steps = 0

  def EvalStateToDict(self, eval_state):
    """Converts an eval_state to a flat eval_dict"""
    eval_dict = {}
    if type(eval_state) is tuple:
      (state, reward, is_terminal, info) = eval_state
      eval_dict["state"] = state
      eval_dict["reward"] = reward
      eval_dict["is_terminal"] = is_terminal
      for info_key, info_value in info.items():
        eval_dict[info_key] = info_value
    if type(eval_state) is dict:
      for info_key, info_value in eval_state.items():
        eval_dict[info_key] = info_value
    return eval_dict

  def Trace(self, eval_state, **kwargs):
    """Traces and stores a state"""
    eval_dict = self.EvalStateToDict(eval_state)
    for key, value in kwargs.items():
      eval_dict[key] = value
    if self._trace_history:
      self._states.append(eval_dict)
    if "is_terminal" in eval_dict:
      if eval_dict["is_terminal"]:
        self._total_episodes += 1
    if "drivable_area" in eval_dict and "collision" in eval_dict:
      if eval_dict["drivable_area"] or eval_dict["collision"]:
        self._total_collisions += 1
    if "goal_reached" in eval_dict:
      if eval_dict["goal_reached"]:
        self._total_goals_reached += 1
    if "reward" in eval_dict:
      self._total_reward += eval_dict["reward"] 
    self._total_steps += 1
  
  @property
  def collision_rate(self):
    if self._total_episodes == 0:
      return 0
    return self._total_collisions/self._total_episodes
  
  @property
  def success_rate(self):
    if self._total_episodes == 0:
      return 0
    return self._total_goals_reached/self._total_episodes
  
  @property
  def mean_steps(self):
    if self._total_episodes == 0:
      return 0
    return self._total_steps/self._total_episodes

  @property
  def mean_reward(self):
    if self._total_episodes == 0:
      return 0
    return self._total_reward/self._total_episodes
  
  @property
  def episode_number(self):
    return self._total_episodes

  def Save(self, filepath="./"):
    """Saves trace as pandas dataframe"""
    filehandler = open(filepath, "wb")
    pickle.dump(self.__dict__, file=filehandler)
    filehandler.close()

  def Load(self, filepath="./"):
    filehandler = open(filepath, "wb")
    self.__dict__ = pickle.load(self, file=filehandler)
    filehandler.close()

  def Reset(self):
    self._states = []
    self._total_episodes = 0
    self._total_collisions = 0
    self._total_goals_reached = 0
    self._total_steps = 0
    self._total_reward = 0