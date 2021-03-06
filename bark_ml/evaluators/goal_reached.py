# Copyright (c) 2020 Patrick Hart, Julian Bernhard,
# Klemens Esterle, Tobias Kessler
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from bark.core.world.evaluation import \
  EvaluatorGoalReached, EvaluatorCollisionEgoAgent, \
  EvaluatorStepCount, EvaluatorDrivableArea, CaptureAgentStates
from bark.runtime.commons.parameters import ParameterServer

from bark_ml.evaluators.evaluator import StateEvaluator


class GoalReached(StateEvaluator):
  def __init__(self,
               params=ParameterServer(),
               eval_agent=None):
    StateEvaluator.__init__(self, params)
    self._goal_reward = \
      self._params["ML"]["GoalReachedEvaluator"]["GoalReward",
        "Reward for reaching the goal.",
        1.]
    self._col_penalty = \
      self._params["ML"]["GoalReachedEvaluator"]["CollisionPenalty",
        "Reward given for a collisions.",
        -1.]
    self._max_steps = \
      self._params["ML"]["GoalReachedEvaluator"]["MaxSteps",
        "Maximum steps per episode.",
        60]
    self._eval_agent = eval_agent

  def _add_evaluators(self):
    evaluators = {}
    evaluators["goal_reached"] = EvaluatorGoalReached()
    evaluators["collision"] = EvaluatorCollisionEgoAgent()
    evaluators["step_count"] = EvaluatorStepCount()
    evaluators["drivable_area"] = EvaluatorDrivableArea()
    return evaluators

  def _evaluate(self, observed_world, eval_results, action):
    """Returns information about the current world state
    """
    done = False
    success = eval_results["goal_reached"]
    step_count = eval_results["step_count"]
    collision = eval_results["collision"] or eval_results["drivable_area"] or (step_count > self._max_steps)
    # for agent_id, agent in observed_world.agents.items():
    #   eval_results[agent_id] = agent.state
    # determine whether the simulation should terminate
    if success or collision or step_count > self._max_steps:
      done = True
    if collision:
      success = 0
    # calculate reward
    reward = collision * self._col_penalty + \
      success * self._goal_reward
    return reward, done, eval_results
    
  def Reset(self, world):
    return super(GoalReached, self).Reset(world)