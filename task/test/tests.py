from hstest import StageTest, TestedProgram, CheckResult, dynamic_test
import re
import random
from chromadb import Client

class LangchainTest(StageTest):
    # Key concepts for each planet for instance, earth has atmosphere, oxygen, magnetic field, life support. The test data is a list of tuples where each tuple contains the query and the expected planet name.
    test_data = [
        ("Which planet is known for its red appearance?", "Mars", r"red appearance|iron oxide|thin atmosphere|carbon dioxide"),
        ("Which planet is closest to the Sun?", "Mercury", r"closest to the Sun|smallest planet|elliptical orbit|thin atmosphere|cratered surface"),
        ("Which planet has a ring system?", "Saturn", r"ring system|gas giant|hydrogen|helium|many moons|hexagonal storm"),
        ("Which planet is categorized as a dwarf planet?", "Pluto", r"dwarf planet|Kuiper Belt|rock|ice|thin atmosphere|five moons|elliptical orbit")
    ]

    @dynamic_test(time_limit=0)
    def test1_planetInfo(self):
        # Randomly select one query and its associated planet name
        for i in range(3):
            query, planet_name, additional_description = random.choice(self.test_data)

            # Start the tested program
            main = TestedProgram()
            main.start()

            # Send the selected planet name as input and get the output
            output = main.execute(query)

            # Check if the output contains the expected planet name (case-insensitive)
            if planet_name.lower() not in output.lower():
                return CheckResult.wrong(
                    f"The output for '{query}' does not contain the expected planet name: {planet_name}\n\nOutput was:\n{output}"
                )

            # Check if the output contains at least one of the expected keywords (case-insensitive)
            if not re.search(additional_description, output, re.IGNORECASE):
                return CheckResult.wrong(
                    f"The output for '{query}' does not contain any of the expected keywords:\n{additional_description}\n\nOutput was:\n{output}"
                )

        client = Client()
        collections = client.list_collections()

        # check if a collection exists
        if not collections:
            return CheckResult.wrong("No collections found in the Chroma database.")

        return CheckResult.correct()


if __name__ == '__main__':
    LangchainTest().run_tests()
