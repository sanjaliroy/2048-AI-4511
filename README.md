# 2048-AI
AI that plays 2048 puzzle using minimax and alpha-beta pruning.

Heuristics used:

* Monotonicity of board
* Smoothness of board
* Emptiness of board
* Maximum four tiles of board

Results of 10 trials:

Trials with max tile of 512: 60%
Trials with max tile of 1024: 30%
Trials with max tile of 2048: 10%

Execution:
```bash
$ python3 GameManager_3.py
```
