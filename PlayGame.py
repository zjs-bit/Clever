from Environment import GameEnvironment
from ActionSpace import ActionSpace
from Player import Player
from TurnStage import TurnStage


def run_epoch(end_stage=TurnStage.GAMEOVER, verbose=False, max_iters=250):

    Agent = Player(0, "Learning")
    Env = GameEnvironment(players=[Agent])
    A = ActionSpace()

    iter = 0
    while Env.stage is not end_stage and iter < max_iters:

        if verbose:
            print(
                f"Round: {Env.round}, Stage: {Env.stage}, Player: {Env.player_num}, Bonus: {Env.bonus_processing}"
            )

        # Get feasible action:
        feas_acts = Agent.get_feasible_actions(
            A, Env.stage, Env.bonus_processing, Env.dice
        )

        if Env.bonus_processing:
            print(Agent.board.pending_bonuses)
            A.display(feas_acts)

        act = Agent.choose_action(feas_acts)
        Agent.execute_action(act, Env.dice, Env.stage, Env.bonus_processing)
        if verbose:
            act.print_action()
            print(Agent.get_reward())

        # Advance the turn stage:
        Env.advance(last_action=act)
        if verbose:
            print(Env.state())

        iter += 1

    if verbose:
        print(f"Final score: {Agent.board.final_score()}")


def main():
    run_epoch(verbose=True)


if __name__ == "__main__":
    main()
