"""
inspired by playing elder sign the board game from Fantasy Flight Games and discussing
which tasks on a card should be attempted first.  Google for the rules to understand in
detail, but gist is you roll a pool of d6 dice and try to get a certain set of sides

Initially built to find the histogram counting the number of a given side you'd get
in a single role.  Need to expand to address the way the game actually works.  That is
it asks you to match n "face sets", e.g. you might have to match 2 sets in one case
and 4 sets in another.  For each match you have to remove those dice from the pool,
rolling the remaining to attempt to match the next set, and so on.  In some cases you
may match the sets in any order, and in others you must match them in a specific order.
NB there's no order when matching any given set - i.e. you don't have to get each
individual element in the match set in some specific order - you roll the (remaining)
dice as a single pool and pull out any that match (sorta, it's a bit harder b/c you
have to match the set all or none - though there are some game mechanics that make things
a bit easier - e.g. rerolls, etc.

As of now, this script can generate a histogram for the number of sides matching some
set in a single role.  To get a picture of the histogram for the actual game it needs
to expand to take account of the following:

    . three of the die faces are of the same "kind" (investigation) but
      count as 1, 2 or 3 investigations
    . match sets include a number of each face kind, e.g. 7 investigation &
      1 lore
    . some match sets require an order
    . you must match sets "all at once", and your dice pool decreases in size
      for each roll you don't match
    . game does allow you save a few dice if you've gotten the face you want
    . there are re-roll mechanisms
    . there are some dice with different sides and one has a "wild"

"""
from collections import Counter
import math
import random

# dice sides are:
# investigate-1,  investigate-2, investigate-3, peril, terror, lore
# lets' call that 1, 2, 3, 4, 5, 6?

die = [1, 2, 3, 4, 5, 6]
faces = {'investigate1': 1, 'investigate2': 2, 'investigate3': 3, 'peril': 4, 'terror': 5, 'lore': 6}


def roll_pool(die, pool_sz):
    """
    roll a pool of six dice, return as a list

    todo generalize for arbitrary die size
    :param die:
    :param pool_sz:
    :return:
    """
    return [random.choice(die) for _ in range(pool_sz)]


def count_results(roll, sides):
    """
    count the number of matching sides in a given roll of some number of dice

    number of dice is the length the roll array

    :param roll: an array w/the results of a roll of a pool of dice
    :param sides: which sides of a die do you want to count, assumes numbers
    """

    roll.sort()

    # extract only die results matching the sides of interest - i.e. filtered
    # is a list where all elements are the same value (or there aren't any elements)
    # the length of filtered is the number of die results matching side
    results = {}

    for side in sides:
        filtered = [e for e in roll if e == side]
        results[side] = len(filtered)

    return results


def get_hist(pool_sz=6, num_rolls=100, sides=[6]):
    """
    produce a hist of the the number of times the given die face came up in a
    single dice pool roll

    :param sides:
    :param pool_sz:
    :param num_rolls:
    :return:
    """

    # initialize the histogram, hist[i] = number of times a count of i came up, which can be 0 so + 1
    # hist = [0 for _ in range(pool_sz + 1)]
    # create a dict whose keys are from sides, the values are set to 0 and will become the counts for each side
    # todo fix this, the counter actually needs all possible values, plus 0, as it did when I used a list
    # this is only getting one count, for 6 for example, adding up all the 6's and dividing by the total rolls
    # but, what I want to know is how many  times did I get 0, 1, 2, ..., 6 6s in the number of rolls requested
    # I think this is close - I still need the key for 0 "sides"
    d = {k: 0 for k in die}
    d[0] = 0
    hist = Counter(d)  # creates a counter, which uses a dict to count things, which are the keys of the counter

    # sides.sort()

    for i in range(num_rolls):
        roll = roll_pool(die=die, pool_sz=pool_sz)
        count = count_results(roll, sides)
        print(f'Roll {i}: ', count, roll)
        # hist[count] += 1
        hist.update(count)

    # print('final hist: ', dict(hist))
    # return [(100 * e) / num_rolls for e in hist]  # get pct
    return {k: v/num_rolls for k, v in hist.items()}


get_hist(pool_sz=6, num_rolls=10, sides=[6])
