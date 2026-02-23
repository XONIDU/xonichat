import unittest
import sys
import os
import tempfile
from unittest.mock import patch, MagicMock
import io

# Import the XONICHAT class from start.py
try:
    # Try to import directly from start.py
    sys.path.insert(0, os.path.dirname(__file__))
    from start import XONICHAT
except ImportError as e:
    print(f"ERROR: Could not import XONICHAT from start.py: {e}")
    print("Make sure start.py is in the current directory")
    sys.exit(1)


class TestXONICHATKeyManagement(unittest.TestCase):
    """Test API key management functionality"""
    
    def setUp(self):
        """Set up test environment before each test"""
        self.app = XONICHAT()
        # Use a test keys file
        self.test_keys_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.app.keys_file = self.test_keys_file.name
    
    def tearDown(self):
        """Clean up after each test"""
        if hasattr(self, 'test_keys_file'):
            try:
                os.unlink(self.test_keys_file.name)
            except FileNotFoundError:
                pass
    
    def write_keys_file(self, content):
        """Helper to write content to keys file"""
        with open(self.test_keys_file.name, 'w') as f:
            f.write(content)
    
    def test_load_valid_keys(self):
        """Test loading valid API keys from file"""
        self.write_keys_file("AIzaSyTestKey1\nAIzaSyTestKey2\nAIzaSyTestKey3\n")
        self.app.cargar_keys()
        self.assertEqual(len(self.app.keys), 3)
        self.assertEqual(self.app.keys[0], "AIzaSyTestKey1")
        self.assertEqual(self.app.keys[1], "AIzaSyTestKey2")
        self.assertEqual(self.app.keys[2], "AIzaSyTestKey3")
    
    def test_ignore_empty_lines(self):
        """Test that empty lines are ignored"""
        self.write_keys_file("\n\nAIzaSyTestKey1\n\nAIzaSyTestKey2\n\n")
        self.app.cargar_keys()
        self.assertEqual(len(self.app.keys), 2)
    
    def test_ignore_comments(self):
        """Test that comment lines starting with # are ignored"""
        self.write_keys_file("""
# This is a comment
AIzaSyTestKey1
# Another comment
AIzaSyTestKey2
# Last comment
""")
        self.app.cargar_keys()
        self.assertEqual(len(self.app.keys), 2)
        self.assertEqual(self.app.keys[0], "AIzaSyTestKey1")
        self.assertEqual(self.app.keys[1], "AIzaSyTestKey2")
    
    def test_strip_whitespace(self):
        """Test that whitespace around keys is stripped"""
        self.write_keys_file("  AIzaSyTestKey1  \n\tAIzaSyTestKey2\t\n")
        self.app.cargar_keys()
        self.assertEqual(self.app.keys[0], "AIzaSyTestKey1")
        self.assertEqual(self.app.keys[1], "AIzaSyTestKey2")
    
    @patch('sys.exit')
    def test_no_keys_file(self, mock_exit):
        """Test behavior when keys file doesn't exist"""
        self.app.keys_file = "nonexistent_file.txt"
        with patch('builtins.print') as mock_print:
            self.app.cargar_keys()
            mock_exit.assert_called_once_with(1)
    
    @patch('sys.exit')
    def test_empty_keys_file(self, mock_exit):
        """Test behavior when keys file is empty"""
        self.write_keys_file("")
        with patch('builtins.print') as mock_print:
            self.app.cargar_keys()
            mock_exit.assert_called_once_with(1)
    
    @patch('sys.exit')
    def test_only_comments_in_keys_file(self, mock_exit):
        """Test behavior when keys file has only comments"""
        self.write_keys_file("# This is a comment\n# Another comment\n")
        with patch('builtins.print') as mock_print:
            self.app.cargar_keys()
            mock_exit.assert_called_once_with(1)


class TestXONICHATKeyRotation(unittest.TestCase):
    """Test API key rotation functionality"""
    
    def setUp(self):
        self.app = XONICHAT()
        self.app.keys = ["key1", "key2", "key3"]
        self.app.current_key_index = 0  # Reset to first key
    
    def test_initial_key_index(self):
        """Test that initial key index is 0"""
        self.assertEqual(self.app.current_key_index, 0)
        self.assertEqual(self.app.get_current_key(), "key1")
    
    def test_change_key(self):
        """Test changing to next key"""
        self.app.cambiar_key()
        self.assertEqual(self.app.current_key_index, 1)
        self.assertEqual(self.app.get_current_key(), "key2")
    
    def test_key_rotation_cyclic(self):
        """Test that key rotation cycles back to start"""
        # Rotate through all keys
        self.app.cambiar_key()  # to key2
        self.app.cambiar_key()  # to key3
        self.app.cambiar_key()  # back to key1
        self.assertEqual(self.app.current_key_index, 0)
        self.assertEqual(self.app.get_current_key(), "key1")
    
    def test_key_rotation_multiple_times(self):
        """Test multiple key rotations"""
        for i in range(5):  # Rotate 5 times
            self.app.cambiar_key()
        # With 3 keys, after 5 rotations: 0 -> 1 -> 2 -> 0 -> 1 -> 2
        self.assertEqual(self.app.current_key_index, 2)
        self.assertEqual(self.app.get_current_key(), "key3")
    
    def test_get_current_key(self):
        """Test get_current_key method"""
        self.assertEqual(self.app.get_current_key(), "key1")
        self.app.current_key_index = 1
        self.assertEqual(self.app.get_current_key(), "key2")
        self.app.current_key_index = 2
        self.assertEqual(self.app.get_current_key(), "key3")


class TestXONICHATConversationHistory(unittest.TestCase):
    """Test conversation history management"""
    
    def setUp(self):
        self.app = XONICHAT()
        self.app.conversation_history = []
        self.app.max_history = 3  # Set small for testing
    
    def test_initial_history_empty(self):
        """Test that history starts empty"""
        self.assertEqual(len(self.app.conversation_history), 0)
    
    def test_add_messages_to_history(self):
        """Test adding messages to history"""
        self.app.conversation_history.append({"role": "user", "content": "Hello"})
        self.app.conversation_history.append({"role": "assistant", "content": "Hi there"})
        
        self.assertEqual(len(self.app.conversation_history), 2)
        self.assertEqual(self.app.conversation_history[0]["role"], "user")
        self.assertEqual(self.app.conversation_history[0]["content"], "Hello")
        self.assertEqual(self.app.conversation_history[1]["role"], "assistant")
        self.assertEqual(self.app.conversation_history[1]["content"], "Hi there")


@patch('requests.post')
class TestXONICHATAPICalls(unittest.TestCase):
    """Test API call functionality"""
    
    def setUp(self):
        self.app = XONICHAT()
        self.app.keys = ["test_key_1", "test_key_2"]
        self.app.current_key_index = 0
        self.app.conversation_history = []
    
    def test_successful_api_call(self, mock_post):
        """Test successful API response"""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {"text": "This is a test response"}
                        ]
                    }
                }
            ]
        }
        mock_post.return_value = mock_response
        
        response = self.app.hacer_peticion("Test message")
        
        self.assertEqual(response, "This is a test response")
        self.assertEqual(len(self.app.conversation_history), 2)
        self.assertEqual(self.app.conversation_history[0]["role"], "user")
        self.assertEqual(self.app.conversation_history[0]["content"], "Test message")
        self.assertEqual(self.app.conversation_history[1]["role"], "assistant")
        self.assertEqual(self.app.conversation_history[1]["content"], "This is a test response")
    
    def test_empty_response(self, mock_post):
        """Test handling of empty API response"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response
        
        response = self.app.hacer_peticion("Test message")
        
        self.assertEqual(response, "[WARNING] Empty response")
    
    def test_quota_exceeded(self, mock_post):
        """Test handling of quota exceeded (429)"""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_post.return_value = mock_response
        
        with patch.object(self.app, 'cambiar_key') as mock_cambiar:
            response = self.app.hacer_peticion("Test message")
            self.assertIsNone(response)
            mock_cambiar.assert_called_once()
    
    def test_invalid_key(self, mock_post):
        """Test handling of invalid key (403/404)"""
        for status_code in [403, 404]:
            mock_response = MagicMock()
            mock_response.status_code = status_code
            mock_post.return_value = mock_response
            
            with patch.object(self.app, 'cambiar_key') as mock_cambiar:
                response = self.app.hacer_peticion("Test message")
                self.assertIsNone(response)
                if len(self.app.keys) > 1:
                    mock_cambiar.assert_called_once()
    
    def test_server_error(self, mock_post):
        """Test handling of server error (500)"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        
        response = self.app.hacer_peticion("Test message")
        self.assertIsNone(response)
    
    def test_timeout_error(self, mock_post):
        """Test handling of timeout"""
        mock_post.side_effect = requests.exceptions.Timeout()
        
        response = self.app.hacer_peticion("Test message")
        self.assertIsNone(response)
    
    def test_connection_error(self, mock_post):
        """Test handling of connection error"""
        mock_post.side_effect = Exception("Connection failed")
        
        response = self.app.hacer_peticion("Test message")
        self.assertIsNone(response)


class TestXONICHATCommands(unittest.TestCase):
    """Test command processing"""
    
    def setUp(self):
        self.app = XONICHAT()
    
    @patch('sys.exit')
    def test_exit_command(self, mock_exit):
        """Test /salir command"""
        result = self.app.procesar_comando("/salir")
        self.assertTrue(result)
        mock_exit.assert_called_once_with(0)
    
    def test_unknown_command(self):
        """Test unknown command handling"""
        result = self.app.procesar_comando("/unknown")
        self.assertFalse(result)
    
    def test_non_command_input(self):
        """Test that normal input is not treated as command"""
        result = self.app.procesar_comando("Hello, how are you?")
        self.assertFalse(result)


class TestXONICHATInitialization(unittest.TestCase):
    """Test app initialization"""
    
    def test_max_history_default(self):
        """Test default max_history value"""
        app = XONICHAT()
        self.assertEqual(app.max_history, 50)
    
    def test_model_default(self):
        """Test default model"""
        app = XONICHAT()
        # Update this if you change the model in start.py
        self.assertEqual(app.model, "gemini-2.5-flash")
    
    def test_api_base_default(self):
        """Test default API base URL"""
        app = XONICHAT()
        self.assertEqual(app.api_base, "https://generativelanguage.googleapis.com/v1")


def run_tests():
    """Run all tests with verbose output"""
    print("=" * 60)
    print("XONICHAT - Test Suite")
    print("=" * 60)
    print(f"Python version: {sys.version}")
    print(f"Testing XONICHAT from: {os.path.abspath('start.py')}")
    print("=" * 60)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    
    # If command line arguments specify which tests to run
    if len(sys.argv) > 1 and sys.argv[1] not in ['-v', '--verbose']:
        # Run specific test class
        suite = loader.loadTestsFromName(sys.argv[1])
    else:
        # Run all tests
        suite = loader.loadTestsFromTestCase(TestXONICHATKeyManagement)
        suite.addTests(loader.loadTestsFromTestCase(TestXONICHATKeyRotation))
        suite.addTests(loader.loadTestsFromTestCase(TestXONICHATConversationHistory))
        suite.addTests(loader.loadTestsFromTestCase(TestXONICHATAPICalls))
        suite.addTests(loader.loadTestsFromTestCase(TestXONICHATCommands))
        suite.addTests(loader.loadTestsFromTestCase(TestXONICHATInitialization))
    
    # Configure verbosity
    verbosity = 2 if '-v' in sys.argv or '--verbose' in sys.argv else 1
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Ran: {result.testsRun} tests")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
    else:
        print("\n❌ SOME TESTS FAILED!")
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    # Make sure requests is available
    try:
        import requests
    except ImportError:
        print("ERROR: requests module not found")
        print("Please install it: pip install requests")
        sys.exit(1)
    
    # Run tests
    sys.exit(run_tests())
