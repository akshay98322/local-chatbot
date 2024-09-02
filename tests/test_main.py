import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from main import handle_conversation

class TestHandleConversation(unittest.TestCase):

    @patch('builtins.input', side_effect=['Hello', 'How are you?', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_handle_conversation_flow(self, mock_stdout, mock_input):
        handle_conversation()
        output = mock_stdout.getvalue()
        self.assertIn("Welcome to the Jarvis ChatBot!", output)
        self.assertIn("Jarvis:", output)
        self.assertEqual(mock_input.call_count, 3)

    @patch('builtins.input', side_effect=['exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_handle_conversation_exit(self, mock_stdout, mock_input):
        handle_conversation()
        output = mock_stdout.getvalue()
        self.assertIn("Welcome to the Jarvis ChatBot!", output)
        self.assertNotIn("Jarvis:", output)
        self.assertEqual(mock_input.call_count, 1)

    @patch('builtins.input', side_effect=['Hello', 'exit'])
    @patch('main.chain.invoke')
    def test_chain_invoke_called(self, mock_chain_invoke, mock_input):
        mock_chain_invoke.return_value = "Hello! How can I assist you today?"
        handle_conversation()
        mock_chain_invoke.assert_called_once_with({"context": "", "question": "Hello"})

    @patch('builtins.input', side_effect=['Question 1', 'Question 2', 'exit'])
    @patch('main.chain.invoke')
    def test_context_accumulation(self, mock_chain_invoke, mock_input):
        mock_chain_invoke.side_effect = ["Answer 1", "Answer 2"]
        handle_conversation()
        self.assertEqual(mock_chain_invoke.call_count, 2)
        expected_context = "\nUser: Question 1\nAI: Answer 1"
        mock_chain_invoke.assert_called_with({"context": expected_context, "question": "Question 2"})

if __name__ == '__main__':
    unittest.main()
