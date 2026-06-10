from hstest import StageTest, TestedProgram, CheckResult, dynamic_test
import re
import random

class LangchainTest(StageTest):
    # 5 simple factual questions
    test_data = [
        ("What is the capital of France?", r"Paris"),
        ("What is the boiling point of water at sea level?", r"100 degrees Celsius|212 degrees Fahrenheit"),
        ("What is the tallest mountain in the world?", r"Mount Everest")
    ]

    @dynamic_test(time_limit=0)
    def test(self):
        try:
            # Randomly a question and its associated keyword pattern
            for i in range(3):
                question, expected_keywords = random.choice(self.test_data)

                # Start the tested program
                main = TestedProgram()
                main.start()

                # Send the selected planet name as input and get the output
                output = main.execute(question)

                # Check if the output contains at least one of the expected keywords (case-insensitive)
                if not re.search(expected_keywords, output, re.IGNORECASE):
                    return CheckResult.wrong(
                        f"The output for '{question}' does not contain any of the expected keywords:\n{expected_keywords}\n\nOutput was:\n{output}"
                    )

            return CheckResult.correct()
        except Exception as e:
            return CheckResult.wrong("An error occurred during testing. Please check your code.")

if __name__ == '__main__':
    LangchainTest().run_tests()
