# Copyright (c) 2020 Patrick Hart, Julian Bernhard,
# Klemens Esterle, Tobias Kessler
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import unittest
import numpy as np
import os
import gym
import matplotlib
import time

# BARK imports
from bark_project.modules.runtime.commons.parameters import ParameterServer

# BARK-ML imports
from bark_ml.environments.blueprints import ContinuousHighwayBlueprint, \
  DiscreteHighwayBlueprint, ContinuousMergingBlueprint, DiscreteMergingBlueprint
from bark_ml.environments.single_agent_runtime import SingleAgentRuntime
import bark_ml.environments.gym
from bark_ml.library_wrappers.tf_agents.agents.ppo_agent import PPOAgent
from bark_ml.library_wrappers.tf_agents.agents.sac_agent import SACAgent


class PyLibraryWrappersTFAgentTests(unittest.TestCase):
  # make sure the agent works
  def test_agent_wrapping(self):
    params = ParameterServer()
    env = gym.make("highway-v0")
    env.reset()
    agent = PPOAgent(environment=env,
                     params=params)
    agent = SACAgent(environment=env,
                     params=params)

  # assign as behavior model (to check if trained agent can be used)
  def test_behavior_wrapping(self):
    # create scenario
    params = ParameterServer()
    bp = ContinuousHighwayBlueprint(params,
                                    number_of_senarios=10,
                                    random_seed=0)
    env = SingleAgentRuntime(blueprint=bp,
                             render=True)
    ml_behaviors = []
    ml_behaviors.append(
      PPOAgent(environment=env,
               params=params))
    ml_behaviors.append(
      SACAgent(environment=env,
               params=params))
    
    for ml_behavior in ml_behaviors:
      #! HACK
      env._ml_behavior = ml_behavior
      env.reset()
      done = False
      while done is False:
        action = np.random.uniform(low=-0.1, high=0.1, size=(2, ))
        observed_next_state, reward, done, info = env.step(action)
        print(f"Observed state: {observed_next_state}, Reward: {reward}, Done: {done}")


  # agent + runner
  def test_agent_and_runner(self):
    pass

  # test in gym environment
  @unittest.skip("for now skipping")
  def test_gym_wrapping(self):
    # highway-v0: continuous
    env = gym.make("highway-v0")
    env.reset()
    for _ in range(0, 10):
      action = np.random.uniform(low=-0.1, high=0.1, size=(2, ))
      observed_next_state, reward, done, info = env.step(action)
      print(f"Observed state: {observed_next_state}, Reward: {reward}, Done: {done}")


if __name__ == '__main__':
  unittest.main()