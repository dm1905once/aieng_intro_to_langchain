from hstest import StageTest, TestedProgram, CheckResult, dynamic_test
import re

class LangchainTest(StageTest):
    test_data = [
        ("How long does Earth take to orbit the Sun?", r"Earth takes approximately 1 Earth year to revolve around the Sun.", ["PlanetRevolutionPeriod", "tool_call", "Earth"]),
        ("What is the distance of Jupiter from the Sun?", r"Jupiter is approximately 5.2 AU from the Sun.", ["PlanetDistanceSun", "tool_call", "Jupiter"]),
        ("What is up with Pluto?", r"dwarf planet|Kuiper Belt|rock|ice|thin atmosphere|five moons|elliptical orbit", ["PlanetGeneralInfo", "tool_call", "Pluto"]),
        ("Tell me something about Mercury.", r"closest to the Sun|smallest planet|elliptical orbit|thin atmosphere|cratered surface", ["PlanetGeneralInfo", "tool_call", "Mercury"]),
        ("What is the distance of Venus from the Sun?", r"Information about the distance of venus from the sun is not available in this tool.", ["PlanetDistanceSun", "tool_call", "Venus"]),
    ]

    @dynamic_test(time_limit=0)
    def test_planet_tools(self):
        for query, expected_output, expected_keywords in self.test_data:
            main = TestedProgram()
            main.start()
            output = main.execute(query).strip()  # Send query and capture combined output, strip whitespace

            if not re.search(expected_output, output, re.IGNORECASE):
                return CheckResult.wrong(
                    "Information about a planet was not found in the output. Did you call the correct tool and print the output?"
                )

            for keyword in expected_keywords:
                if keyword not in output:
                    return CheckResult.wrong(
                        "Information about tool calls was not found in the output. Did you print the tool calls?"
                    )

        return CheckResult.correct()

if __name__ == '__main__':
    LangchainTest().run_tests()