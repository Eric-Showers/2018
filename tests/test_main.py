"""
Test game starting, responses, and validity of responses.
"""
import unittest
from unittest.mock import Mock
from boddle import boddle
import app.main as main

class TestMain(unittest.TestCase):
    """
    Parent class to run unittests.
    """

    def setUp(self):
        """
        Clear the game dictionary between tests.
        """
        main.gameDict = {}

    def test_start_response(self):
        """
        Test required responses to `/start` POST
        """
        paramData = {
            'game_id': 'game1',
            'width': 20,
            'height': 20
        }
        headers = {
            'Content-Type': 'application/json'
        }
        with boddle(json=paramData, headers=headers):
            response = main.start()
            self.assertIn('color', response)
            self.assertIn('head_url', response)
            self.assertIn('name', response)
            self.assertIn('taunt', response)

    def test_optional_start_responses(self):
        """
        Test optional responses to '/start' POST
        """
        paramData = {
            'width': 20,
            'height': 20,
            'game_id': 'game1'
        }
        headers = {
            'Content-Type': 'application/json'
        }
        with boddle(json=paramData, headers=headers):
            response = main.start()
            self.assertIn('head_type', response)
            self.assertIn('tail_type', response)

    def test_emergency_start_method(self):
        """
        Test method to confirm it will add a new game object to game dictionary.
        """
        main.emergencyStart('game_id_1', 10, 10)
        self.assertNotEqual(main.gameDict, {})

    def test_log_invalid_level(self):
        """
        Test log method, given an invalid level.
        Test for thrown errors.
        """
        fail_msg = 'Log threw an error'
        try:
            main.log('Test level higher than specified.', 4)
            main.log('Test level lower than specified.', -1)
        except Exception:
            self.fail(fail_msg)

    def test_get_game_decision(self):
        """
        Test game decision method during nominal gameplay.
        """
        game_id = 'game_id_test'
        taunt = 'hi there friend'
        moves = ['up', 'down', 'right', 'left']
        mock_battle = Mock()
        # Default move in getGameDecision is up, so need to pick something else for the mock
        mock_battle.getNextMove.return_value = 'down'
        mock_battle.getTaunt.return_value = taunt

        main.gameDict[game_id] = mock_battle
        next_move, next_taunt = main.getGameDecisions(game_id)
        self.assertIn(next_move, moves)
        self.assertEqual(next_taunt, taunt)

    def test_get_game_decision_exception(self):
        """
        Test game decision method when an error is thrown internally.
        """
        game_id = 'game_id_test'
        default_move = 'up'
        default_taunt = 'oh_noes!'
        mock_battle = Mock()
        # Test getNextMove throwing an error internally
        mock_battle.getNextMove.side_effect = KeyError('Value not found on board')

        main.gameDict[game_id] = mock_battle
        next_move, next_taunt = main.getGameDecisions(game_id)
        self.assertEqual(next_move, default_move)    # up is the default move if an error is thrown
        self.assertEqual(next_taunt, default_taunt)

    def test_move_responses(self):
        """
        Test required fields in respones to `/move` POST.
        """
        game_id = '1'
        paramData = {
            'snakes': [
                {
                    'taunt': 'git gud',
                    'name': 'my-snake',
                    'id': '25229082-f0d7-4315-8c52-6b0ff23fb1fb',
                    'health_points': 93,
                    'coords': [[0, 0], [0, 1], [0, 2]]
                },
                {
                    'taunt': 'cash me outside',
                    'name': 'angry-whitegirl',
                    'id': 'ex-uuid',
                    'health_points': 93,
                    'coords': [[15, 14], [15, 13], [15, 12]]
                }
            ],
            'width': 20,
            'height': 20,
            'game_id': game_id,
            'food': [[4, 5], [8, 9]],
            'you': {
                'id': '25229082-f0d7-4315-8c52-6b0ff23fb1fb',
                'taunt': '1-800-267-2001 ALARMFORCE',
                'name': 'sneakysnake',
                'health_points': 100,
                'coords': [
                    [3, 3],
                    [3, 4],
                    [4, 4]
                ]
            },
            'turn': 0
        }
        headers = {
            'Content-Type': 'application/json'
        }
        moves = ['up', 'down', 'left', 'right']

        # Create a mock Battle in the game dictionary so games seem to be in progress
        mock_battle = Mock()
        mock_battle.getNextMove.return_value = 'down'
        mock_battle.getTaunt.return_value = 'hi there friend'
        main.gameDict[game_id] = mock_battle

        with boddle(json=paramData, headers=headers):
            response = main.move()
            self.assertIn('move', response)
            self.assertIn('taunt', response)
            self.assertIn(response['move'], moves)

    def test_move_no_game_id(self):
        """
        Test catching a lack of 'game_id' value in the request.
        """
        paramData = {
            'snakes': [],
            'width': 20,
            'height': 20,
            'food': [[4, 5], [8, 9]],
            'you': {},
            'turn': 0
        }
        headers = {
            'Content-Type': 'application/json'
        }

        with boddle(json=paramData, headers=headers):
            response = main.move()
            # Current defined behaviour is to return no response if game_id missing
            self.assertEqual(response, None)

    def test_move_game_not_started(self):
        """
        Test required fields in respones to `/move` POST.
        """
        game_id = '1'
        paramData = {
            'snakes': [
                {
                    'taunt': 'git gud',
                    'name': 'my-snake',
                    'id': '25229082-f0d7-4315-8c52-6b0ff23fb1fb',
                    'health_points': 93,
                    'coords': [[0, 0], [0, 1], [0, 2]]
                },
                {
                    'taunt': 'cash me outside',
                    'name': 'angry-whitegirl',
                    'id': 'ex-uuid',
                    'health_points': 93,
                    'coords': [[15, 14], [15, 13], [15, 12]]
                }
            ],
            'width': 20,
            'height': 20,
            'game_id': game_id,
            'food': [[4, 5], [8, 9]],
            'you': {
                'id': '25229082-f0d7-4315-8c52-6b0ff23fb1fb',
                'taunt': '1-800-267-2001 ALARMFORCE',
                'name': 'sneakysnake',
                'health_points': 100,
                'coords': [
                    [3, 3],
                    [3, 4],
                    [4, 4]
                ]
            },
            'turn': 0
        }
        headers = {
            'Content-Type': 'application/json'
        }
        moves = ['up', 'down', 'left', 'right']

        with boddle(json=paramData, headers=headers):
            response = main.move()
            self.assertIn('move', response)
            self.assertIn('taunt', response)
            self.assertIn(response['move'], moves)
