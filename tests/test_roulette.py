""" Test module for roulette game simulation
"""
import unittest
from roulette import *

class NotUsed:
    """ Does nothing
    """
    def __init__(self):
        self.rand = random
        self.doct = doctest
        self.bin_b = BinBuilder()
        self.sim = SIM
        self.res = RESULTS

    def trow(self):
        """ trow
        """
        return vars(self)

class TestOutcome(unittest.TestCase):
    """ Unittest for class Outcome
    """
    def setUp(self):
        self.oc1 = Outcome("Straight 8", RouletteOdds.straightbet)
        self.oc2 = Outcome("Straight 8", RouletteOdds.straightbet)
        self.oc3 = Outcome("Straight 5", RouletteOdds.straightbet)

    def test_init(self):
        """ Test that the class properly inits an instance
        """
        self.assertIsInstance(self.oc1, Outcome)

    def test_win_amount(self):
        """ Test that method win_amount returns the result of
        (amount_bet * odds) + amount_bet
        """
        self.assertEqual(self.oc1.win_amount(100), 3500)
        self.assertRaises(AssertionError, self.oc1.win_amount, -100)

    def test_eq(self):
        """ Test that comparison only compares the name attribute
        """
        self.assertTrue(self.oc1 == self.oc2)
        self.assertFalse(self.oc1 == self.oc3)

    def test_ne(self):
        """ Test that comparison only compares the name attribute
        """
        self.assertTrue(self.oc1 != self.oc3)
        self.assertFalse(self.oc1 != self.oc2)

    def test_hash(self):
        """ Verify that the hash of two identical instances
        are in fact also identical
        """
        self.assertEqual(hash(self.oc1), hash(self.oc2))
        self.assertNotEqual(hash(self.oc1), hash(self.oc3))

    def test_str(self):
        """ Verify that str() returns an easy-to-red string representation
        """
        self.assertEqual('Straight 8 (35:1)', str(self.oc1))

    def test_repr(self):
        """ Verify that repr() returns a detailed string representation
        """
        self.assertEqual("Outcome('Straight 8', 35)", repr(self.oc1))

class TestBin(unittest.TestCase):
    """ Unit test of the Bin class. The Bin class should be able
    to hold an Outcomes.
    """
    def setUp(self):
        self.oc1 = Outcome("Straight 8", RouletteOdds.straightbet)
        self.oc2 = Outcome("Black", RouletteOdds.evenmoneybet)
        self.oc3 = Outcome("Straight 5", RouletteOdds.straightbet)
        self.bin = Bin([self.oc1, self.oc2])

    def test_bin(self):
        """ Verify that a Bin can hold an Outcome
        """
        self.assertIsInstance(self.bin, frozenset)
        self.assertIn(self.oc1, self.bin)
        self.assertNotIn(self.oc3, self.bin)

class TestWheel(unittest.TestCase):
    """Unit test of the Wheel class. The Wheel should create 38 Bins
    and be able to pick a Bin at random as well as add Outcomes to a Bin.
    Additionally, then Wheel can return a specific Bin and return an
    existing Outcome.
    """
    def setUp(self):
        self.wheel = Wheel()
        self.ocm = Outcome("Mock outcome", 42)
        self.rand = [8, 36, 4, 16, 7, 31, 28, 30, 24, 13]

    def test_wheel(self):
        """ Verify that the wheel does in fact have 38 Bins.
        Test that the wheel can produce random numbers in a given interval.
        """
        self.wheel.rng.seed(1)
        wheel_rand = [self.wheel.rng.randint(0, 37) for i in range(10)]
        self.assertEqual(len(self.wheel.bins), 38)
        self.assertListEqual(wheel_rand, self.rand)

    def test_add(self):
        """Verify that an Outcome is added to an existing Bin in a Roulette Wheel
        """
        self.wheel.add(0, self.ocm)
        self.assertIn(self.ocm, self.wheel.bins[0])
        self.assertIn(self.ocm, self.wheel.all_outcomes)

    def test_next(self):
        """ Verify that the wheel can reutrn a random Bin
        """
        self.wheel.rng.seed(1)
        self.assertEqual(self.wheel.next(), self.wheel.bins[8])

    def test_get(self):
        """ Verify that the wheel can return a specific Bin on request
        """
        self.assertTrue(any(outcome == 'Straight 1' for outcome in self.wheel.get(1)))

    def test_get_outcome(self):
        """ Verify that the wheel can return a specific Outcome based on its name.
        """
        self.assertEqual(self.wheel.get_outcome('straight 8'),
                         'Straight 8')

class TestBinBuilder(unittest.TestCase):
    """Unit test of the binBuilder class.
    """
    def setUp(self):
        self.wheel = Wheel()

    def test_straight(self):
        """ Verify that all Straight bets are created
        """
        for bin_ in range(37):
            outcome = Outcome('Straight {}'.format(bin_), RouletteOdds.straightbet)
            self.assertIn(outcome, self.wheel.bins[bin_])
            self.assertIn(outcome, self.wheel.all_outcomes)
        self.assertIn(Outcome('Straight 00', RouletteOdds.straightbet),
                      self.wheel.bins[37])
        self.assertIn(Outcome('Straight 00', RouletteOdds.straightbet),
                      self.wheel.all_outcomes)

    def test_five(self):
        """ Verify that the Five bets are created
        """
        outcome = Outcome("00-0-1-2-3", RouletteOdds.fivebet)
        for bin_ in range(4):
            self.assertIn(outcome, self.wheel.bins[bin_])
            self.assertIn(outcome, self.wheel.all_outcomes)
        self.assertIn(outcome, self.wheel.bins[37])
        self.assertIn(outcome, self.wheel.all_outcomes)

    def test_split_bets(self):
        """ Verify that all Split bets are created
        """
        for row in range(12):
            col1 = 3*row + 1
            col2 = 3*row + 2
            outcome = Outcome(
                "{}, {} Split".format(col1, col1+1), RouletteOdds.splitbet
            )
            self.assertIn(outcome, self.wheel.bins[col1])
            self.assertIn(outcome, self.wheel.bins[col1+1])
            outcome = Outcome(
                "{}, {} Split".format(col2, col2+1), RouletteOdds.splitbet
            )
            self.assertIn(outcome, self.wheel.bins[col2])
            self.assertIn(outcome, self.wheel.bins[col2+1])
            self.assertIn(outcome, self.wheel.all_outcomes)
        for num in range(1, 34):
            lower = num
            upper = num+3
            outcome = Outcome(
                "{}, {} Split".format(lower, upper), RouletteOdds.splitbet
            )
            self.assertIn(outcome, self.wheel.bins[lower])
            self.assertIn(outcome, self.wheel.bins[upper])
            self.assertIn(outcome, self.wheel.all_outcomes)

    def test_street_bets(self):
        """ Verify that all Street bets are created
        """
        for row in range(12):
            num = 3*row + 1
            outcome = Outcome('{}, {}, {} Street'.format(num, num+1, num+2),
                              RouletteOdds.streetbet)
            for i in range(3):
                self.assertIn(outcome, self.wheel.bins[num+i])
                self.assertIn(outcome, self.wheel.all_outcomes)

    def test_corner_bets(self):
        """ Verify that all Corner bets are created
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
                self.assertIn(outcome1, self.wheel.bins[col1 + k])
                self.assertIn(outcome2, self.wheel.bins[col2 + k])
                self.assertIn(outcome1, self.wheel.all_outcomes)
                self.assertIn(outcome2, self.wheel.all_outcomes)

    def test_line_bets(self):
        """ Verify that all Line bets are created
        """
        line = range(6)
        for row in range(11):
            num = 3 * row + 1
            outcome = Outcome('{}, {}, {}, {}, {}, {} Line'.format(
                *[num + i for i in line]
            ), RouletteOdds.linebet)
            for j in line:
                self.assertIn(outcome, self.wheel.bins[num + j])
                self.assertIn(outcome, self.wheel.all_outcomes)

    def test_dozen_bets(self):
        """ Verify that all Dozen bets are created
        """
        for dozen in range(3):
            outcome = Outcome('Dozen {}'.format(dozen+1), RouletteOdds.dozenbet)
            for straight in range(12):
                self.assertIn(outcome, self.wheel.bins[dozen * 12 + straight + 1])
                self.assertIn(outcome, self.wheel.all_outcomes)

    def test_column_bets(self):
        """ Verify that all Column bets are created
        """
        for col in range(3):
            outcome = Outcome('Column {}'.format(col + 1), RouletteOdds.columnbet)
            for row in range(12):
                self.assertIn(outcome, self.wheel.bins[row * 3 + col + 1])
                self.assertIn(outcome, self.wheel.all_outcomes)

    def test_even_money_bets(self):
        """ Verify that all Even-money bets are created
        """
        red = list((*range(1, 10, 2),
                    *range(12, 19, 2),
                    *range(19, 28, 2),
                    *range(30, 37, 2)))
        for straight in range(1, 37):
            if 1 <= straight < 19:
                outcome = Outcome('Low', RouletteOdds.evenmoneybet)
                self.assertIn(outcome, self.wheel.bins[straight])
                self.assertIn(outcome, self.wheel.all_outcomes)
            if 19 <= straight < 37:
                outcome = Outcome('High', RouletteOdds.evenmoneybet)
                self.assertIn(outcome, self.wheel.bins[straight])
                self.assertIn(outcome, self.wheel.all_outcomes)
            if straight % 2 == 0:
                outcome = Outcome('Even', RouletteOdds.evenmoneybet)
                self.assertIn(outcome, self.wheel.bins[straight])
                self.assertIn(outcome, self.wheel.all_outcomes)
            if straight % 2 != 0:
                outcome = Outcome('Odd', RouletteOdds.evenmoneybet)
                self.assertIn(outcome, self.wheel.bins[straight])
                self.assertIn(outcome, self.wheel.all_outcomes)
            if straight in red:
                outcome = Outcome('Red', RouletteOdds.evenmoneybet)
                self.assertIn(outcome, self.wheel.bins[straight])
                self.assertIn(outcome, self.wheel.all_outcomes)
            if straight not in red:
                outcome = Outcome('Black', RouletteOdds.evenmoneybet)
                self.assertIn(outcome, self.wheel.bins[straight])
                self.assertIn(outcome, self.wheel.all_outcomes)


class TestBet(unittest.TestCase):
    """ Returns the winnings of a particular Bet using
    the odds of the Outcome the Bet was placed on
    """
    def setUp(self):
        self.oc1 = Outcome("Straight 1", RouletteOdds.straightbet)
        self.bet1 = Bet(15, self.oc1)

    def test_win_amount(self):
        """ Test that a Bet can properly call the win_amount()
        method from the associated Outcome
        """
        self.assertEqual(self.bet1.win_amount(), 540)

    def test_loose_amount(self):
        """ Verify that loose_amount returns the amount of the original bet
        """
        self.assertEqual(self.bet1.loose_amount(), 15)

    def test_eq(self):
        """ Test that Bets are compared by their repr
        """
        bet1 = Bet(15, Outcome('Black', RouletteOdds.evenmoneybet))
        bet2 = Bet(15, Outcome('Black', RouletteOdds.evenmoneybet))
        self.assertTrue(bet1 == bet2)

    def test_str(self):
        """ Verify that str() returns an easy-to-read string representation
        """
        self.assertEqual(str(self.bet1), '15 on Straight 1')

    def test_repr(self):
        """ Verify that repr() returns a detailed string representation
        """
        self.assertEqual(repr(self.bet1), "Bet(15, Outcome('Straight 1', 35))")


class TestTable(unittest.TestCase):
    """ Unit test of the Table class.
    """
    def setUp(self):
        self.oc1 = Outcome("Straight 1", RouletteOdds.straightbet)
        self.bet1 = Bet(15, self.oc1)
        self.table = Table(10, 100)
        self.table.place_bet(self.bet1)

    def test_place_bet(self):
        """ Test that the table can hold a Bet
        """
        self.assertIn(self.bet1, self.table.bets)

    def test_iter(self):
        """ Test that the Bets on the table can be iterated through
        """
        self.assertIn(self.bet1, self.table.__iter__())

    def test_str(self):
        """ Verify that str() returns an easy-to-read string representation
        """
        self.assertEqual(str(self.table), 'Current bets:\n    15 on Straight 1')

    def test_repr(self):
        """ Verify that repr() returns a detailed string representation
        """
        self.assertEqual(
            repr(self.table), "Table({Bet(15, Outcome('Straight 1', 35))})"
        )

    def test_is_valid(self):
        """ Checks the validity of Bets placed
        """
        ocfive = Outcome("00-0-1-2-3", RouletteOdds.fivebet)
        bet2 = Bet(10, ocfive)
        self.table.place_bet(bet2)
        self.assertTrue(self.table.is_valid())
        ocred = Outcome("Red", RouletteOdds.evenmoneybet)
        bet4 = Bet(100, ocred)
        self.table.place_bet(bet4)
        self.assertRaises(InvalidBet, self.table.is_valid)

class TestPlayer(unittest.TestCase):
    """ Unit test of the Player metaclass
    """
    def setUp(self):
        self.wheel = Wheel()
        self.table = RouletteTable(10, 100, self.wheel)
        self.player = Player(self.table)

    def test_set_stake(self):
        """ Verify that the Player's stake can be set through
        set_stake() method
        """
        self.player.set_stake(530)
        self.assertEqual(self.player.stake, 530)

    def test_set_rounds(self):
        """ Verify that the Player's number of rounds left can be set through
        set_rounds() method
        """
        self.player.set_rounds(23)
        self.assertEqual(self.player.rounds_to_go, 23)

    def test_playing(self):
        """ Verify that the Player can correctly decide if it is
        playing by using the playing() method
        """
        self.assertTrue(self.player.playing())
        self.player.set_stake(0)
        self.assertFalse(self.player.playing())
        self.player.set_stake(1000)
        self.assertTrue(self.player.playing())
        self.player.set_rounds(0)
        self.assertFalse(self.player.playing())

class TestPassenger57(unittest.TestCase):
    """ Unit test of the Passenger57 subclass.
    """
    def setUp(self):
        self.wheel = Wheel()
        self.table = RouletteTable(10, 100, self.wheel)
        self.player = Passenger57(self.table)

    def test_black(self):
        """ Verify that the player will bet on Black
        """
        self.assertEqual(self.player.black,
                         Bet(15, Outcome('Black', RouletteOdds.evenmoneybet)))

    def test_place_bets(self):
        """ Verify that the Player places a Bet on Black
        """
        self.player.place_bets()
        self.assertIn(self.player.black, self.table.bets)

    def test_win(self):
        """ Test that the win() method correctly increases the Player's stake
        """
        self.player.place_bets()
        self.player.win(self.player.black)
        self.assertEqual(self.player.stake, 1015)

    def test_loose(self):
        """ Test that the loose() method deducts from the stake
        """
        self.player.place_bets()
        self.player.loose(self.player.black)
        self.assertEqual(self.player.stake, 985)

class TestGame(unittest.TestCase):
    """ Unit test of the Game class.
    """
    def setUp(self):
        self.game = Game(None, None)
        self.player = Passenger57(self.game.table)

    def test_cycle(self):
        """ Test one playing cycle for a game of Roulette.

        1. Passenger57 places '15 on Black'
        2. Table verifies the Bet is valid
        3. Game spins the wheel (it lands on 8)
        4. Player wins and recieves 30 (stake is now 1015)
        5. Table clears all Bets
        6. Passenger57 places '15 on Black'
        7. Table verifies the Bet is valid
        8. Game spins the wheel (it lands on 36)
        9. Player looses

        """
        self.game.wheel.rng.seed(1)
        # Player wins first round
        self.game.cycle(self.player)
        self.assertEqual(self.player.stake, 1015)
        # Player loses second round
        self.game.cycle(self.player)
        self.assertEqual(self.player.stake, 1000)
        # Player withdraws before third round
        self.player.stake = 5
        self.game.cycle(self.player)
        self.assertSetEqual(self.game.table.bets, set())

class TestMartingale(unittest.TestCase):
    """ Unit test of the Martingale subclass.

    This player will only Bet on Black, but the amount bet doubles
    with each loss and is reset to minimum wager on each win.
    """
    def setUp(self):
        self.wheel = Wheel()
        self.table = RouletteTable(10, 100, self.wheel)
        self.player = Martingale(self.table)

    def test_place_bets(self):
        """ Verify that Player places the correct Bet
        """
        self.assertEqual(self.player.bet_multiple(), 1)
        self.player.place_bets()
        self.assertEqual(self.player.stake, 990)
        for bet in self.table.bets:
            self.assertEqual(bet.amount_bet, 10)

    def test_win(self):
        """ Test that a winning Bet will reset the loss_count to 0.
        """
        self.player.place_bets()
        bet = [_ for _ in self.table.bets][0]
        self.player.win(bet)
        self.assertEqual(self.player.stake, 1010)
        self.assertEqual(self.player.loss_count, 0)

    def test_loose(self):
        """ Test that a loosing bet will increase the loss_count by 1
        """
        self.player.place_bets()
        bet = [_ for _ in self.table.bets][0]
        self.player.loose(bet)
        self.assertEqual(self.player.stake, 990)
        self.assertEqual(self.player.loss_count, 1)

    def test_multiplier(self):
        """ Test that the bet_multiplier doubles with each loss
        """
        self.player.loss_count = 2
        self.assertEqual(self.player.loss_count, 2)
        self.assertEqual(self.player.bet_multiple(), 4)
        self.player.place_bets()
        self.assertEqual(self.player.stake, 960)

    def test_ten_game(self):
        """ Test the Player on 10 game cycles
        """
        self.wheel.rng.seed(1)
        self.assertEqual(self.player.stake, 1000)
        win = 0
        loss = 0
        stakes = []
        for bin_ in [self.wheel.next() for _ in range(10)]:
            self.table.table()
            self.player.place_bets()
            bet = [_ for _ in self.table.bets][0]
            self.assertEqual(bet.outcome,
                             Outcome('Black', RouletteOdds.evenmoneybet))
            if bet.outcome in bin_:
                self.player.win(bet)
                win += 1
            else:
                self.player.loose(bet)
                loss += 1
                self.assertNotEqual(self.player.loss_count, 0)
            stakes.append(self.player.stake)
        self.assertListEqual(
            stakes,
            [1010, 1000, 1020, 1010, 990, 1030, 1040, 1030, 1050, 1060]
        )
        self.assertEqual(win, 6)
        self.assertEqual(loss, 4)

    def test_set_rounds(self):
        """ Test that rounds can be set and that setting the
        rounds_to_to will also reset the loss_count to 0
        """
        self.player.loss_count = 3
        self.assertNotEqual(self.player.loss_count, 0)
        self.player.set_rounds(23)
        self.assertEqual(self.player.rounds_to_go, 23)
        self.assertEqual(self.player.loss_count, 0)

    def test_invalid_bet(self):
        """ Test that making an invalid Bet results in a reset of the loss_count
        """
        self.player.loss_count = 5
        self.player.invalid_bet()
        self.assertEqual(self.player.loss_count, 0)

class TestSevenReds(unittest.TestCase):
    """ Unit test of class SevenReds
    """
    def setUp(self):
        self.wheel = Wheel()
        self.table = RouletteTable(10, 100, self.wheel)
        self.player = SevenReds(self.table)

    def test_place_bets(self):
        """ Test that the Player will only place a Bet if red_count == 0
        """
        self.assertEqual(self.player.red_count, 7)
        self.player.place_bets()
        self.assertSetEqual(self.table.bets, set())
        self.player.red_count = 0
        self.player.place_bets()
        self.assertIn(Bet(10, Outcome('Black', RouletteOdds.evenmoneybet)),
                      self.table.bets)

    def test_winners(self):
        """ Test that winners() returns the winning bin and
        properly adjusts the red_Count
        """
        self.wheel.rng.seed(1)
        bin_ = self.wheel.next()
        self.player.winners(bin_)
        self.assertEqual(self.player.red_count, 7)
        bin_ = self.wheel.next()
        self.player.winners(bin_)
        self.assertEqual(self.player.red_count, 6)

class TestPlayerRandom(unittest.TestCase):
    """ Unit test for the PlayerRandom class.
    """
    def setUp(self):
        self.wheel = Wheel()
        self.table = RouletteTable(10, 100, self.wheel)
        self.player = PlayerRandom(self.table)

    def test_place_bets(self):
        """ Place a Bet on a random Outcome

        >>> table = RouletteTable(10, 100, Wheel())
        >>> player = PlayerRandom(table)
        >>> player.rng.seed(1)
        >>> outcomes = sorted(player.table.wheel.get_all_outcomes())
        >>> bet = Bet(10, player.rng.choice(outcomes))
        >>> str(bet.outcome)
        '19, 20, 21 Street (11:1)'
        """
        self.player.rng.seed(1)
        outcomes = sorted(self.player.table.wheel.get_all_outcomes())
        bet = Bet(10, self.player.rng.choice(outcomes))
        self.assertEqual(str(bet.outcome), '19, 20, 21 Street (11:1)')

class TestPlayer1326(unittest.TestCase):
    """ Unit test for Player1326 class.
    """
    def setUp(self):
        self.wheel = Wheel()
        self.table = RouletteTable(10, 100, self.wheel)
        self.player = Player1326(self.table)

    def test_states(self):
        """ Run a complete 1-3-2-6 strategy and one fail to
        verify proper function
        """
        self.assertIsInstance(self.player.state, Player1326NoWins)
        self.player.place_bets()
        self.assertEqual(self.table.bets, {Bet(10, Outcome('Black', 1))})
        self.player.win(self.table.bets.pop())
        self.assertIsInstance(self.player.state, Player1326OneWin)
        self.player.place_bets()
        self.assertEqual(self.table.bets, {Bet(30, Outcome('Black', 1))})
        self.player.win(self.table.bets.pop())
        self.assertIsInstance(self.player.state, Player1326TwoWins)
        self.player.place_bets()
        self.assertEqual(self.table.bets, {Bet(20, Outcome('Black', 1))})
        self.player.win(self.table.bets.pop())
        self.assertIsInstance(self.player.state, Player1326ThreeWins)
        self.player.place_bets()
        self.assertEqual(self.table.bets, {Bet(60, Outcome('Black', 1))})
        self.player.win(self.table.bets.pop())
        self.assertIsInstance(self.player.state, Player1326NoWins)
        self.player.place_bets()
        self.assertEqual(self.table.bets, {Bet(10, Outcome('Black', 1))})
        self.player.win(self.table.bets.pop())
        self.assertIsInstance(self.player.state, Player1326OneWin)
        self.player.place_bets()
        self.assertEqual(self.table.bets, {Bet(30, Outcome('Black', 1))})
        self.player.loose(self.table.bets.pop())
        self.assertIsInstance(self.player.state, Player1326NoWins)

class TestPlayerCancellation(unittest.TestCase):
    """Test the functions of PlayerCancellation

    """
    def setUp(self):
        self.wheel = Wheel()
        self.table = RouletteTable(10, 100, self.wheel)
        self.player = PlayerCancellation(self.table)

    def test_reset_sequence(self):
        """ Reset sequence for Player
        """
        self.player.reset_sequence()
        self.assertEqual(self.player.sequence, list(range(1, 7)))

    def test_place_bets(self):
        """
        >>> wheel = Wheel()
        >>> table = RouletteTable(10, 100, wheel)
        >>> player = PlayerCancellation(table)
        >>> player.place_bets()
        >>> table.bets
        {Bet(7, Outcome('Red', 1))}
        """
        self.player.place_bets()
        self.assertEqual(self.table.bets, {Bet(7, Outcome('Red', 1))})

    def test_win(self):
        """
        >>> wheel = Wheel()
        >>> table = RouletteTable(10, 100, wheel)
        >>> player = PlayerCancellation(table)
        >>> player.place_bets()
        >>> player.win(table.bets.pop())
        >>> player.sequence
        [2, 3, 4, 5]
        """
        self.player.place_bets()
        self.player.win(self.table.bets.pop())
        self.assertListEqual(self.player.sequence, [2, 3, 4, 5])

    def test_loose(self):
        """
        >>> wheel = Wheel()
        >>> table = RouletteTable(10, 100, wheel)
        >>> player = PlayerCancellation(table)
        >>> player.place_bets()
        >>> player.loose(table.bets.pop())
        >>> player.sequence
        [1, 2, 3, 4, 5, 6, 7]
        """
        self.player.place_bets()
        self.player.loose(self.table.bets.pop())
        self.assertListEqual(self.player.sequence, [1, 2, 3, 4, 5, 6, 7])

class TestFibonacciPlayer(unittest.TestCase):
    """ Unit test for the FibonacciPlayer class
    """
    def setUp(self):
        self.wheel = Wheel()
        self.table = RouletteTable(10, 100, self.wheel)
        self.player = FibonacciPlayer(self.table)

    def test_place_bets(self):
        """ Place a bet
        """
        self.player.place_bets()
        self.assertEqual(self.table.bets, {Bet(1, Outcome('Red', 1))})

    def test_win(self):
        """
        >>> wheel = Wheel()
        >>> table = RouletteTable(10, 100, wheel)
        >>> player = FibonacciPlayer(table)
        >>> player.place_bets()
        >>> player.win(table.bets.pop())
        >>> player.previous
        0
        """
        self.player.place_bets()
        self.player.win(self.table.bets.pop())
        self.assertEqual(self.player.previous, 0)

    def test_loose(self):
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
        [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
        """
        recent = []
        fibonacci = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
        for _ in range(10):
            self.player.place_bets()
            self.player.loose(self.table.bets.pop())
            recent.append(self.player.previous)
        self.assertListEqual(recent, fibonacci)

class TestPlayerFactory(unittest.TestCase):
    """ Unit test of class PlayerFactory
    """
    def setUp(self):
        self.wheel = Wheel()
        self.table = RouletteTable(10, 100, self.wheel)

    def test_factory(self):
        """ Create an instance of a Player and verify that
        it belongs to the correct class
        """
        for player_class in [Passenger57, Martingale, SevenReds]:
            player = PlayerFactory.factory(self, player_class, self.table)
            self.assertIsInstance(player, player_class)

class TestSimulator(unittest.TestCase):
    """ Unit test for the Simulator class
    """
    def setUp(self):
        self.sim = Simulator(Martingale)

    def test_init(self):
        """ Verify instance init procedure
        """
        self.assertIsInstance(self.sim.player, Martingale)
        self.assertEqual(self.sim.game.table.limit, 100)

    def test_session(self):
        """ Test that a session completes and returns a list
        """
        self.sim.game.wheel.rng.seed(1)
        self.assertIsInstance(self.sim.session(), list)

    def test_gather(self):
        """ Test that the gather() method runs a number of sessions
        and gathers statistics on each session in a Dict.
        """
        self.sim.game.wheel.rng.seed(1)
        self.sim.samples = 10
        self.sim.gather()
        self.assertListEqual(self.sim.sessions['Maxima'],
                             [1130, 1640, 1380, 1180, 1030,
                              1020, 1160, 1040, 990, 1230])
        self.assertListEqual(self.sim.sessions['Duration'],
                             [250, 250, 250, 250, 250, 250, 250, 228, 250, 250])

if __name__ == '__main__':
    unittest.main(verbosity=2)
