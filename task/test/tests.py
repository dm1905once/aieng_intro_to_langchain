from hstest import StageTest, TestedProgram, CheckResult, dynamic_test
import re

class LangchainTest(StageTest):
    test_data = [
        ("What is the distance of Jupiter from the Sun?", r"Jupiter is approximately 5.2 AU from the Sun."),
        ("What is up with Pluto?", r"dwarf planet|Kuiper Belt|rock|ice|thin atmosphere|five moons|elliptical orbit"),
        ("Tell me something about Mercury.", r"closest to the Sun|smallest planet|elliptical orbit|thin atmosphere|cratered surface"),
        ("How long does Pluto take to orbit the Sun?", r"Pluto takes approximately 248 Earth years to revolve around the Sun."),
        ("What is the distance of Saturn from the Sun?", r"Information about the distance of saturn from the sun is not available in this tool."),
    ]

    # create a list of expected keywords for the chain's info
    # the full output of the chain's info is too long to check for
    # so we will check for these keywords instead which should be present in the output of the chain's info
    expected_keywords = ["first", "PromptTemplate", "template","middle", "RunnableBinding", "bound", "tools", "function", "PlanetDistanceSun", "PlanetRevolutionPeriod", "PlanetGeneralInfo", "last", "RunnableLambda"]


    @dynamic_test(time_limit=0)
    def test_planet_tools(self):
        for query, expected_output in self.test_data:
            main = TestedProgram()
            main.start()
            output = main.execute(query).strip()  # Send query and capture combined output, strip whitespace

            if not re.search(expected_output, output, re.IGNORECASE):
                return CheckResult.wrong(
                    "Information about a planet was not found in the output. Did you call the correct tool and print the output?"
                )
            for keyword in self.expected_keywords:
                if keyword not in output:
                    return CheckResult.wrong(
                        "Information about the chain was not found in the output. Did you print the chain's info?"
                    )

        return CheckResult.correct()

if __name__ == '__main__':
    LangchainTest().run_tests()