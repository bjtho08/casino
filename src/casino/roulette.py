"""Roulette module simulates a game of roulette
"""
import random
from os import urandom

class Outcome:
    """Class Outcome stores the name of a particular outcome along
    with the associated odds for that outcome

    >>> oc1 = Outcome("red", 2)
    >>> oc1.win_amount(500)
    1000
    """
    def __init__(self, name, odds):
        self.name = name
        self.odds = odds

    def win_amount(self, amount):
        """Multiply this Outcome's odds by the given amount

        >>> oc1 = Outcome("red", 2)
        >>> oc1.win_amount(100)
        200
        >>> oc1.win_amount(0)
        0
        >>> oc1.win_amount(-100)
        Traceback (most recent call last):
          ...
        AssertionError: Negative amounts not allowed
        """
        assert amount >= 0, "Negative amounts not allowed"
        return amount * self.odds

    def __eq__(self, other):
        """Compare the name attributes of self and other

        >>> Outcome("red", 2) == Outcome("red", 2)
        True
        >>> Outcome("red", 2) == Outcome("black", 2)
        False
        >>> Outcome("red", 2) == 'red'
        True
        """
        if isinstance(other, str):
            return self.name == other
        if isinstance(other, self.__class__):
            return self.name == other.name
        return False

    def __ne__(self, other):
        """Compare the name attributes of self and other

        >>> oc1 = Outcome("red", 2)
        >>> oc2 = Outcome("red", 2)
        >>> oc3 = Outcome("black", 2)
        >>> oc1 != oc2
        False
        >>> oc1 != oc3
        True
        >>> oc1 != 'red'
        False
        """
        return not self.__eq__(other)

    def __lt__(self, other):
        """ Allow sorting by name
        """
        return str(self).__lt__(str(other))

    def __hash__(self):
        """Hash value for this Outcome

        >>> oc1 = Outcome("red", 2)
        >>> oc2 = Outcome("red", 2)
        >>> oc3 = Outcome("black", 2)
        >>> hash(oc1) == hash(oc2)
        True
        >>> hash(oc1) == hash(oc3)
        False
        """
        return hash(self.name)

    def __str__(self):
        """Easy-to-read representation of this Outcome

        >>> oc1 = Outcome("red", 2)
        >>> str(oc1)
        'red (2:1)'
        """
        return '{name:s} ({odds:d}:1)'.format_map(vars(self))

    def __repr__(self):
        """Detailed representation of this Outcome

        >>> oc1 = Outcome("red", 2)
        >>> repr(oc1)
        "Outcome('red', 2)"
        """
        return '{class_:s}({name!r}, {odds!r})'.format(
            class_=type(self).__name__, **vars(self))

class Bin(frozenset):
    """Contains a collection of Outcomes which reflect the
    winning bets for a particular bin on a Roulette Wheel.

    >>> ocred = Outcome("red", 1)
    >>> ocodd = Outcome("odd", 1)
    >>> oceven = Outcome("even", 1)
    >>> bin1 = Bin([ocred, ocodd])
    >>> ocodd in bin1
    True
    >>> oceven in bin1
    False
    """
    pass

class BinBuilder:
    """binBuilder creates the Outcomes for all of the 38 individual Bins

    >>> wheel = Wheel()
    >>> Outcome("Red", RouletteOdds.evenmoneybet) in wheel.bins[1]
    True
    >>> Outcome("00-0-1-2-3", RouletteOdds.fivebet) in wheel.bins[37]
    True
    """
    def __init__(self):
        pass

    def build_bins(self, wheel):
        """Populate Bins with the associated Outcomes
        """
        self.straight(wheel)
        self.five(wheel)
        self.split_bets(wheel)
        self.street_bets(wheel)
        self.corner_bets(wheel)
        self.line_bets(wheel)
        self.dozen_bets(wheel)
        self.column_bets(wheel)
        self.even_money_bets(wheel)

    def straight(self, wheel):
        """ Create all Straight bets
        """
        for i in range(37):
            outcome = Outcome("Straight {}".format(i), RouletteOdds.straightbet)
            wheel.add(i, outcome)
        outcome = Outcome("Straight 00", RouletteOdds.straightbet)
        wheel.add(37, outcome)

    def five(self, wheel):
        """ Create the Five bets
        """
        outcome = Outcome("00-0-1-2-3", RouletteOdds.fivebet)
        wheel.add(37, outcome)
        for straight in range(4):
            wheel.add(straight, outcome)

    def split_bets(self, wheel):
        """ Create Split bets
        """
        for row in range(12):
            col1 = 3 * row + 1
            col2 = 3 * row + 2
            outcome = Outcome("{}, {} Split".format(col1, col1 + 1),
                              RouletteOdds.splitbet)
            wheel.add(col1, outcome)
            wheel.add(col1 + 1, outcome)
            outcome = Outcome("{}, {} Split".format(col2, col2 + 1),
                              RouletteOdds.splitbet)
            wheel.add(col2, outcome)
            wheel.add(col2 + 1, outcome)
        for num in range(1, 34):
            lower = num
            upper = num + 3
            outcome = Outcome("{}, {} Split".format(lower, upper),
                              RouletteOdds.splitbet)
            wheel.add(lower, outcome)
            wheel.add(upper, outcome)

    def street_bets(self, wheel):
        """ Create Street bets
        """
        for row in range(12):
            num = 3 * row + 1
            outcome = Outcome('{}, {}, {} Street'.format(num, num+1, num+2),
                              RouletteOdds.streetbet)
            wheel.add(num, outcome)
            wheel.add(num+1, outcome)
            wheel.add(num+2, outcome)

    def corner_bets(self, wheel):
        """ Create Corner bets
        """
        corner = [0, 1, 3, 4]
        for row in range(11):
            col1 = 3 * row + 1
            col2 = 3 * row + 2
            outcome1 = Outcome('{}, {}, {}, {} Corner'.format(
                *[col1 + i for i in corner]),
                               RouletteOdds.cornerbet)
            outcome2 = Outcome('{}, {}, {}, {} Corner'.format(
                *[col2 + j for j in corner]),
                               RouletteOdds.cornerbet)
            for k in corner:
                wheel.add(col1 + k, outcome1)
                wheel.add(col2 + k, outcome2)

    def line_bets(self, wheel):
        """ Create Line bets
        """
        line = range(6)
        for row in range(11):
            num = 3 * row + 1
            outcome = Outcome('{}, {}, {}, {}, {}, {} Line'.format(
                *[num + i for i in line]
            ), RouletteOdds.linebet)
            for j in line:
                wheel.add(num + j, outcome)

    def dozen_bets(self, wheel):
        """ Create Dozen bets
        """
        for dozen in range(3):
            outcome = Outcome('Dozen {}'.format(dozen+1), RouletteOdds.dozenbet)
            for straight in range(12):
                wheel.add(dozen*12 + straight + 1, outcome)

    def column_bets(self, wheel):
        """ Create Column bets
        """
        for col in range(3):
            outcome = Outcome('Column {}'.format(col + 1), RouletteOdds.columnbet)
            for row in range(12):
                wheel.add(row * 3 + col + 1, outcome)

    def even_money_bets(self, wheel):
        """ Create all Even-money bets (Low, High, Even, Odd, Red, and Black)
        """
        red = list((*range(1, 10, 2),
                    *range(12, 19, 2),
                    *range(19, 28, 2),
                    *range(30, 37, 2)))
        for straight in range(1, 37):
            if 1 <= straight < 19:
                outcome = Outcome('Low', RouletteOdds.evenmoneybet)
                wheel.add(straight, outcome)
            if 19 <= straight < 37:
                outcome = Outcome('High', RouletteOdds.evenmoneybet)
                wheel.add(straight, outcome)
            if straight % 2 == 0:
                outcome = Outcome('Even', RouletteOdds.evenmoneybet)
                wheel.add(straight, outcome)
            if straight % 2 != 0:
                outcome = Outcome('Odd', RouletteOdds.evenmoneybet)
                wheel.add(straight, outcome)
            if straight in red:
                outcome = Outcome('Red', RouletteOdds.evenmoneybet)
                wheel.add(straight, outcome)
            if straight not in red:
                outcome = Outcome('Black', RouletteOdds.evenmoneybet)
                wheel.add(straight, outcome)

class Wheel:
    """Wheel contains 38 individual Bins on a Roulette wheel, plus a
    random number generator. It can select a Bin at random, simulating the
    spin of the Roulette wheel.

    >>> wheel = Wheel()
    >>> len(wheel.bins)
    38
    >>> wheel.rng.seed(1)
    >>> [wheel.rng.randint(0, 37) for i in range(10)]
    [8, 36, 4, 16, 7, 31, 28, 30, 24, 13]
    """
    def __init__(self):
        self.bins = tuple(Bin() for i in range(38))
        self.rng = random.Random()
        self.all_outcomes = set()
        BinBuilder().build_bins(self)

    def add(self, bin_, outcome):
        """Add an Outcome to an existing Bin in a Roulette Wheel

        >>> wheel = Wheel()
        >>> outcome = Outcome("Red", 1)
        >>> wheel.add(1, outcome)
        >>> outcome in wheel.bins[1]
        True
        >>> outcome in wheel.all_outcomes
        True
        """
        assert 0 <= bin_ < 38, "invalid bin number"
        assert isinstance(outcome, Outcome)
        bins = list(self.bins)
        the_bin = list(bins[bin_])
        the_bin.append(outcome)
        bins[bin_] = Bin(the_bin)
        self.bins = tuple(bins)

        if outcome not in self.all_outcomes:
            self.all_outcomes.add(outcome)

    def next(self):
        """Select a random Bin

        >>> wheel = Wheel()
        >>> wheel.rng.seed(1)
        >>> Outcome('Straight 8', 35) in wheel.next()
        True
        """
        return self.rng.choice(self.bins)

    def get(self, bin_):
        """Get a particular Bin from the Roulette Wheel

        >>> wheel = Wheel()
        >>> Outcome('Straight 8', 35) in wheel.get(8)
        True
        """
        return self.bins[bin_]

    def get_outcome(self, name):
        """ Get an existing outcome from any Bin in the Wheel by looking
        up the Outcome name (case-insensitive)

        >>> wheel = Wheel()
        >>> wheel.get_outcome("straight 8")
        Outcome('Straight 8', 35)
        """
        outcome, = [oc for oc in self.all_outcomes if name.casefold()
                    == oc.name.casefold()]
        return outcome

    def get_all_outcomes(self):
        """ Return a complete set of possible Outcomes
        """
        return self.all_outcomes

class Bet:
    """Bet class is used to keep track on how much a Player
    has wagered on a particular Outcome
    """
    def __init__(self, amount, outcome):
        self.amount_bet = amount
        self.outcome = outcome

    def win_amount(self):
        """ Returns the winnings of a particular Bet using
        the odds of the Outcome the Bet was placed on

        >>> bet1 = Bet(15, Outcome("Straight 1", 35))
        >>> bet1.win_amount()
        540
        """
        return self.outcome.win_amount(self.amount_bet) + self.amount_bet

    def loose_amount(self):
        """ Returns the loss from a loosing Bet

        >>> bet1 = Bet(15, Outcome("Straight 1", 35))
        >>> bet1.loose_amount()
        15
        """
        return self.amount_bet

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return repr(self) == repr(other)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.amount_bet, self.outcome))

    def __str__(self):
        """ String representation of this Bet with the form "amount on outcome"

        >>> bet1 = Bet(15, Outcome("Straight 1", 35))
        >>> str(bet1)
        '15 on Straight 1'
        """
        return '{amount_bet} on {outcome.name}'.format_map(vars(self))

    def __repr__(self):
        """ String representation of this Bet with the form "Bet(amount, outcome)"

        >>> bet1 = Bet(15, Outcome("Straight 1", 35))
        >>> repr(bet1)
        "Bet(15, Outcome('Straight 1', 35))"
        """
        return '{class_:s}({amount_bet!r}, {outcome!r})'.format(
            class_=type(self).__name__, **vars(self))

class Table:
    """Base Table class. Has all the basic functionality of a game table.
    Holds Bets and rejects invalid Bets. The Table sets the limits and
    minimum wagers for Players
    """
    def __init__(self, minimum: int, limit: int):
        self.limit = limit
        self.minimum = minimum
        self.bets = set()

    def table(self):
        """Fresh table without any Bets
        """
        self.bets = set()

    def place_bet(self, bet):
        """Place a Bet on the Table
        """
        # if not self.minimum <= bet.amount_bet <= self.limit:
        #     raise InvalidBet("The amount bet must be within Table limits.")
        self.bets.add(bet)

    def __iter__(self):
        """Return an iterable of the Bets on the Table
        """
        return self.bets.copy()

    def __str__(self):
        """ Easy-to-read string representation of all current bets

        >>> table = Table(10, 100)
        >>> table.place_bet(Bet(15, Outcome("Straight 1", 35)))
        >>> str(table)
        'Current bets:\\n    15 on Straight 1'
        >>> repr(table)
        "Table({Bet(15, Outcome('Straight 1', 35))})"
        """
        return 'Current bets:\n'+ '\n'.join(['{:>20}'.format(str(line))
                                             for line in self.bets])

    def __repr__(self):
        """Detailed representation of the Table instance
        """
        return '{class_:s}({bets!r})'.format(
            class_=type(self).__name__, **vars(self))

    def is_valid(self):
        """ Checks the validity of Bets placed

        >>> table = Table(10, 100)
        >>> table.place_bet(Bet(15, Outcome("Straight 1", 35)))
        >>> table.place_bet(Bet(10, Outcome("00-0-1-2-3", 6)))
        >>> table.is_valid()
        True
        >>> table.place_bet(Bet(100, Outcome("Red", 1)))
        >>> table.is_valid()
        Traceback (most recent call last):
            ...
        InvalidBet: Total betting amount exceeds Table limit (125 in 3 Bets)
        """
        if not sum([bet.amount_bet for bet in self.bets]) <= self.limit:
            raise InvalidBet(
                "Total betting amount exceeds Table limit ({} in {} Bets)".format(
                    sum([bet.amount_bet for bet in self.bets]), len(self.bets)))
        return True

class InvalidBet(Exception):
    """Raised when a Bet is not allowed by the Table rules
    """
    pass

class RouletteTable(Table):
    """Roulette Table subclass of Table
    """
    def __init__(self, minimum, limit, wheel):
        Table.__init__(self, minimum, limit)
        self.wheel = wheel

class Game:
    """The Game class controls the flow of a game.

    At the moment, a Game does not check if all bets are resolved before moving on.
    """
    def __init__(self, wheel=None, table=None):
        self.wheel = wheel
        self.table = table
        if wheel is None:
            self.wheel = Wheel()
        if table is None:
            self.table = RouletteTable(10, 100, self.wheel)

    def cycle(self, player):
        """Cycle through one round of the Game

        """
        self.table.table()
        playing = player.playing()
        if playing:
            player.place_bets()
            try:
                self.table.is_valid()
            except InvalidBet:
                for bet in self.table.bets:
                    player.set_stake(player.stake + bet.amount_bet)
                player.invalid_bet()
                self.table.table()

        winning_bin = self.wheel.next()
        player.winners(winning_bin)

        if playing:
            for bet in self.table.__iter__():
                if bet.outcome in winning_bin:
                    player.win(bet)
                if bet.outcome not in winning_bin:
                    player.loose(bet)
        player.rounds_to_go -= 1


class Player:
    """Base Player class. Has limited functionality, but implements
    the common Player elements.
    """
    def __init__(self, table):
        self.table = table
        self.stake = 1000
        self.rounds_to_go = 250

    def set_stake(self, stake):
        """Set the Player's available Stake
        """
        self.stake = stake

    def set_rounds(self, rounds):
        """Set the number of Rounds left before the Player leaves the Table
        """
        self.rounds_to_go = rounds

    def playing(self):
        """Returns True if the Player is still actively playing
        """
        if self.stake < self.table.minimum:
            self.set_rounds(0)
        if self.rounds_to_go > 0:
            return True
        return False

    def get_outcome(self, name):
        """ Return the requested Outcome from the Wheel of the Table
        """
        return self.table.wheel.get_outcome(name)

    def place_bets(self):
        """Placeholder method to be implemented in subclass
        """
        raise NotImplementedError('This method must be declared by the subclass')

    def win(self, bet):
        """Default win method. Will credit the Player's Stake with the amount won.
        """
        self.stake += bet.win_amount()

    def loose(self, bet):
        """Default loose method. The base method has no function
        """
        pass

    def winners(self, bin_):
        """ Called by game to inform Player of winning bin
        """
        pass

    def invalid_bet(self):
        """ Called by table if Bet is not valid
        """
        pass

class Passenger57(Player):
    """ Stub Player class. Will always Bet 15 on Black.
    """
    def __init__(self, table):
        Player.__init__(self, table)
        self.black = Bet(15, self.get_outcome('black'))

    def place_bets(self):
        """ Place '15 on Black',
        deduct 15 from stake
        and decrease rounds_to_go by 1
        """
        self.table.place_bet(self.black)
        self.stake -= 15

class Martingale(Player):
    """ The Martingale Player strategy.

    Doubles the amount wagered for every loss and resets to the
    initial wager upon a win.
    """
    def __init__(self, table):
        Player.__init__(self, table)
        self.loss_count = 0

    def set_rounds(self, rounds):
        """ Sets rounds to go equal to parameter 'rounds'
        """
        super().set_rounds(rounds)
        self.loss_count = 0

    def place_bets(self):
        """Place a Bet on Black,
        deduct the wager from Player stake
        and decrease rounds_to_go by 1.
        """
        wager = self.table.minimum * self.bet_multiple()
        black = Bet(wager, self.get_outcome('black'))
        self.table.place_bet(black)
        self.stake -= wager

    def bet_multiple(self):
        """Return the wager multiplier
        """
        return 2**self.loss_count

    def win(self, bet):
        """ In addition to adding the winnings to Player stake,
        also resets the loss count
        """
        super().win(bet)
        self.loss_count = 0

    def loose(self, bet):
        """Increase the loss count by 1
        """
        super().loose(bet)
        self.loss_count += 1

    def invalid_bet(self):
        """ Called by Table if Bet is not valid

        Resets the loss_count
        """
        self.loss_count = 0

class SevenReds(Martingale):
    """ Class SevenReds is a variant of Martingale that only places a Bet
    after observing seven Reds in a row.
    """
    def __init__(self, table):
        Martingale.__init__(self, table)
        self.red_count = 7

    def place_bets(self):
        """If Player has observed 7 Reds in a row, place a Bet on Black,
        deduct the wager from Player stake,
        decrease rounds_to_go by 1 and reset red_count.
        """
        if self.red_count is 0:
            wager = self.table.minimum * self.bet_multiple()
            black = Bet(wager, self.get_outcome('black'))
            self.table.place_bet(black)
            self.stake -= wager
            self.red_count = 7

    def winners(self, bin_):
        """ Called by the game to inform the player of the winning Bin.
        The Player examines the winning bin to determine if it was Red or Black:

        if it was Red, the red_count is decreased by 1;

        if it was Black, the red_count is reset to 7
        """
        if 'Red' in bin_:
            self.red_count -= 1
        if 'Black' in bin_:
            self.red_count = 7

    def invalid_bet(self):
        """ Called by Table if Bet is not valid

        Resets the loss_count
        """
        self.loss_count = 0

class PlayerRandom(Player):
    """ Class PlayerRandom. 'nuff said.
    """
    def __init__(self, table):
        Player.__init__(self, table)
        self.rng = random.Random()
        self.outcomes = sorted(self.table.wheel.get_all_outcomes())

    def place_bets(self):
        """ Place a Bet on a random Outcome

        >>> player = PlayerRandom(RouletteTable(10, 100, Wheel()))
        >>> player.rng.seed(1)
        >>> bet = Bet(10, player.rng.choice(player.outcomes))
        >>> str(bet.outcome)
        '19, 20, 21 Street (11:1)'
        """
        bet = Bet(10, self.rng.choice(self.outcomes))
        self.table.place_bet(bet)
        self.stake -= 10

class Player1326State:
    """ Superclass for the different state classes in the
    1-3-2-6 betting strategy.
    """
    def __init__(self, player):
        self.player = player
        self.minimum_bet = self.player.table.minimum
        self.multiplier = None
        self.next_state_win = None

    def current_bet(self):
        """ Returns a Bet with a given wager based on the current state
        """
        wager = self.minimum_bet * self.multiplier
        return Bet(wager, self.player.outcome)

    def next_won(self):
        """ Next state when winning a bet
        """
        self.player.state = self.player.factory.get(self.next_state_win)

    def next_lost(self):
        """ Next state when losing a bet
        """
        self.player.state = Player1326NoWins(self.player)

class Player1326NoWins(Player1326State):
    """ No Wins state subclass
    """
    def __init__(self, player):
        Player1326State.__init__(self, player)
        self.multiplier = 1
        self.next_state_win = 'Player1326OneWin'

class Player1326OneWin(Player1326State):
    """ One Win state subclass
    """
    def __init__(self, player):
        Player1326State.__init__(self, player)
        self.multiplier = 3
        self.next_state_win = 'Player1326TwoWins'

class Player1326TwoWins(Player1326State):
    """ Two Wins state subclass
    """
    def __init__(self, player):
        Player1326State.__init__(self, player)
        self.multiplier = 2
        self.next_state_win = 'Player1326ThreeWins'

class Player1326ThreeWins(Player1326State):
    """ Three Wins state subclass
    """
    def __init__(self, player):
        Player1326State.__init__(self, player)
        self.multiplier = 6
        self.next_state_win = 'Player1326NoWins'

class Player1326StateFactory(Player1326State):
    """ Player1326 factory
    """
    def __init__(self, player):
        Player1326State.__init__(self, player)
        self.values = {'Player1326NoWins'   : Player1326NoWins(player),
                       'Player1326OneWin'   : Player1326OneWin(player),
                       'Player1326TwoWins'  : Player1326TwoWins(player),
                       'Player1326ThreeWins': Player1326ThreeWins(player)}

    def get(self, name):
        """ Return the requested Player1326 state
        """
        return self.values[name]

class Player1326(Player):
    """ 1-3-2-6 Betting strategy Player class
    """
    def __init__(self, table):
        Player.__init__(self, table)
        self.outcome = self.get_outcome('black')
        self.factory = Player1326StateFactory(self)
        self.state = self.factory.get('Player1326NoWins')

    def place_bets(self):
        """
        >>> player = Player1326(RouletteTable(10, 100, Wheel()))
        >>> player.table.place_bets()
        >>> player.table.bets
        {Bet(10, Outcome('Black', 1))}
        """
        bet = self.state.current_bet()
        self.table.place_bet(bet)
        self.stake -= bet.amount_bet

    def win(self, bet):
        """
        >>> player = Player1326(RouletteTable(10, 100, Wheel()))
        >>> player.table.place_bets()
        >>> player.win(player.table.bets.pop())
        >>> player.state.__class__.__name__
        'Player1326OneWin'
        """
        super().win(bet)
        self.state.next_won()

    def loose(self, bet):
        """
        >>> player = Player1326(RouletteTable(10, 100, Wheel()))
        >>> player.table.place_bets()
        >>> player.loose(table.bets.pop())
        >>> player.state.__class__.__name__
        'Player1326NoWins'
        """
        super().loose(bet)
        self.state.next_lost()

class PlayerCancellation(Player):
    """ PlayerCancellation betting strategy.
    """
    def __init__(self, table):
        Player.__init__(self, table)
        self.sequence = list(range(1, 7))
        self.outcome = self.get_outcome('Red')

    def reset_sequence(self):
        """
        >>> player = PlayerCancellation(RouletteTable(10, 100, Wheel()))
        >>> player.table.place_bets()
        >>> player.reset_sequence()
        >>> player.sequence
        [1, 2, 3, 4, 5, 6]
        """
        self.sequence = list(range(1, 7))

    def place_bets(self):
        """
        >>> player = PlayerCancellation(RouletteTable(10, 100, Wheel()))
        >>> player.table.place_bets()
        >>> player.table.bets
        {Bet(7, Outcome('Red', 1))}
        """
        amount = self.sequence[0] + self.sequence[-1]
        self.table.place_bet(Bet(amount, self.outcome))
        self.stake -= amount

    def win(self, bet):
        """
        >>> player = PlayerCancellation(RouletteTable(10, 100, Wheel()))
        >>> player.table.place_bets()
        >>> player.win(table.bets.pop())
        >>> player.sequence
        [2, 3, 4, 5]
        """
        super().win(bet)
        del self.sequence[0]
        if self.sequence == []:
            self.set_rounds(0)
        else:
            del self.sequence[-1]
        if self.sequence == []:
            self.set_rounds(0)

    def loose(self, bet):
        """
        >>> player = PlayerCancellation(RouletteTable(10, 100, Wheel()))
        >>> player.table.place_bets()
        >>> player.loose(table.bets.pop())
        >>> player.sequence
        [1, 2, 3, 4, 5, 6, 7]
        """
        super().loose(bet)
        self.sequence.append(bet.amount_bet)

    def invalid_bet(self):
        """ Called by Table if Bet is not valid

        Resets the loss_count
        """
        self.reset_sequence()

class FibonacciPlayer(Player):
    """ Variation on the Martingale system using
    the Fibonacci sequence to increase bets
    """
    def __init__(self, table):
        Player.__init__(self, table)
        self.recent = 1
        self.previous = 0

    def place_bets(self):
        """
        >>> player = FibonacciPlayer(RouletteTable(10, 100, Wheel()))
        >>> player.table.place_bets()
        >>> table.bets
        {Bet(10, Outcome('Red', 1))}
        """
        wager = self.recent + self.previous
        self.table.place_bet(Bet(wager * 10, self.get_outcome('Red')))
        self.stake -= wager * 10

    def win(self, bet):
        """
        >>> player = FibonacciPlayer(RouletteTable(10, 100, Wheel()))
        >>> player.table.place_bets()
        >>> player.win(table.bets.pop())
        >>> player.previous
        0
        """
        super().win(bet)
        self.recent = 1
        self.previous = 0

    def loose(self, bet):
        """
        >>> wheel = Wheel()
        >>> table = RouletteTable(10, 100, wheel)
        >>> player = FibonacciPlayer(table)
        >>> recent = []
        >>> for _ in range(10):
        ...     player.place_bets()
        ...     player.loose(table.bets.pop())
        ...     recent.append(player.previous)
        >>> recent
        [1, 1, 2, 3, 5, 0, 1, 1, 2, 3]
        """
        super().loose(bet)
        next_ = self.recent + self.previous
        if next_ * 10 > self.table.limit:
            self.recent = 1
            self.previous = 0
        else:
            self.previous = self.recent
            self.recent = next_

    def invalid_bet(self):
        """ Called by Table if Bet is not valid

        Resets the loss_count
        """
        self.recent = 1
        self.previous = 0

class RouletteOdds:
    """Container class for Roulette betting odds
    """
    straightbet = 35
    splitbet = 17
    streetbet = 11
    cornerbet = 8
    linebet = 5
    dozenbet = 2
    columnbet = 2
    evenmoneybet = 1
    fivebet = 6

class PlayerFactory:
    """The PlayerFactory class can create instances of the available Player strategies
    """
    def factory(self, typ_, *args):
        """Used to create the available Player strategies
        """
        table, = args
        if typ_ == Passenger57:
            return Passenger57(table)
        if typ_ == Martingale:
            return Martingale(table)
        if typ_ == SevenReds:
            return SevenReds(table)
        if typ_ == PlayerRandom:
            return PlayerRandom(table)
        if typ_ == Player1326:
            return Player1326(table)
        if typ_ == PlayerCancellation:
            return PlayerCancellation(table)
        if typ_ == FibonacciPlayer:
            return FibonacciPlayer(table)

    staticmethod(factory)

class IntegerStatistics(list):
    """ Extension of the list class, which can calculate basic statistics of the list
    """
    def mean(self):
        """ Calculate the average of all elements in self

        >>> mylist = IntegerStatistics([1, 2, 3, 4, 5, 6 ,7 ,8 , 9, 10])
        >>> mylist.mean()
        5.5
        """
        return round(sum(self)/len(self), 6)

    def stdev(self):
        """ Calculate the standard deviation of all elements in self

        >>> mylist = IntegerStatistics([1, 2, 3, 4, 5, 6 ,7 ,8 , 9, 10])
        >>> mylist.stdev()
        2.692582
        """
        from math import sqrt
        mean = self.mean()
        try:
            return round(sqrt(sum((x - mean)**2 for x in self)/len(self) - 1), 6)
        except ValueError:
            return 0

class Simulator:
    """The Simulator class handles the actual simulation and data gathering.
    """
    def __init__(self, player):
        self.init_duration = 250
        self.init_stake = 100
        self.samples = 50
        self.game = self.create_game()
        self.player = PlayerFactory.factory(self, player, self.game.table)
        self.sessions = {'Maxima'   : IntegerStatistics(),
                         'Duration' : IntegerStatistics()
                        }

    def create_game(self):
        """Create a new instance of Game with associated Table and Wheel
        complete with populated Bins
        """
        wheel = Wheel()
        table = RouletteTable(10, 100, wheel)
        return Game(wheel, table)

    def session(self):
        """ Simulate a single gambling session and collect data on the
        Player's stake throughout the session.

        Returns a list of stakes (int)
        """
        self.player.set_stake(self.init_stake * self.game.table.minimum)
        self.player.set_rounds(self.init_duration)
        stake_history = []
        #stake_history.append(self.player.stake)
        while self.player.playing():
            self.game.wheel.rng.seed(urandom(8))
            self.game.table.table()
            self.game.cycle(self.player)
            stake_history.append(self.player.stake)
        return stake_history

    def gather(self):
        """ Gather statistics from several gambling sessions.
        """
        for _ in range(self.samples):
            stakes = self.session()
            self.sessions['Maxima'].append(max(stakes))
            self.sessions['Duration'].append(len(stakes))
        return self.sessions

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    SIM = Simulator(FibonacciPlayer)
    RESULTS = SIM.gather()
    print(SIM.player.__class__.__name__)
    print('Maxima: {Maxima}\nDuration: {Duration}'.format(**RESULTS))
    print('Mean and st. dev of Maxima: {}, {}'.format(
        RESULTS['Maxima'].mean(), RESULTS['Maxima'].stdev()))
    print('Mean and st. dev of Duration: {}, {}'.format(
        RESULTS['Duration'].mean(), RESULTS['Duration'].stdev()))
