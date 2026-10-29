import unittest
from app import run_demo


class ProjectTests(unittest.TestCase):
    def test_demo_returns_a_dictionary(self):
        result = run_demo("Give me a sample demonstration")
        self.assertIsInstance(result, dict)
        self.assertTrue(result)

    def test_result_identifies_project(self):
        result = run_demo("Python SQL testing")
        self.assertIn("project", result)
        self.assertTrue(result["project"])

    def test_empty_input_is_handled(self):
        result = run_demo("")
        self.assertIsInstance(result, dict)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
