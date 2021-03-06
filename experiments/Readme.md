# Experiment Runner
To ease tracking and training configurations, the experiment runner converts the json into a runnable experiment.
To avoid mismatching training and execution runs, the experiment runner additionally hashes the json-file (to provide reproducibility to some extent).

## Usage
For training, run the following command:
`bazel run //experiments:experiment_runner -- --exp_json=/ABSOLUTE_PATH/bark-ml/experiments/configs/highway_interaction_network.json --mode=train`

To visualize the current checkpoint, run:
`bazel run //experiments:experiment_runner -- --exp_json=/ABSOLUTE_PATH/bark-ml/experiments/configs/highway_interaction_network.json`

And to evaluate the performance of the agent, use:
`bazel run //experiments:experiment_runner -- --exp_json=/ABSOLUTE_PATH/bark-ml/experiments/configs/highway_interaction_network.json --mode=evaluate`