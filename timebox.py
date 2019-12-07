import trello_retrieval
import sys
import os

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        cards = trello_retrieval.get_cards(os.getenv('BOARD_ID'))
        trello_retrieval.print_cards(trello_retrieval.sort_cards(cards))
        trello_retrieval.get_total_time_estimate(cards)
    else:
        if len(sys.argv) == 2:
            if int(sys.argv[1]) is not None:
                trello_retrieval.get_tasks_for_days(sys.argv[1])
