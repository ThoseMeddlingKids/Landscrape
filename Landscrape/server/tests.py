from Scraper import scrape
import unittest

class TestOutputSingle(unittest.TestCase):
    #This Tests that a dictionary is returned when the "get_results" fucntion is called on a single search term

    def test_Get_Output_Given_Input_Single(self):
        # Single Term Test, Checking if a single input produces something.

        #First, generate the results for single term
        testInput_SingleTerm= 'Coffee'
        TestScraper = scrape.Scraper([testInput_SingleTerm,'Lawrence', 'Kansas'])
        results = TestScraper.get_results()

        # Check a Bunch of stuff based on those results (the meat of our test suite)

        #Check that the results dictionary even exists
        self.assertTrue(results)

        #We expect the dictionary to be length 1, so we are testing that this is true
        self.assertEqual(len(results), 1)

        #Check to see if the
        for term in results:
            self.assertEqual(len(results[term]), 3)


class TestOutputMulti(unittest.TestCase):
    #This Tests that a dictionary is returned when the function "get_results" is called with multiple terms

    def test_Get_Output_Given_Input_Multi(self):
        # Multi-Term Test, Checking that something is returned
        #Set up the test by running a query
        testInput_MultiTerm = 'Coffee, Bars, Tacos'
        TestScraper = scrape.Scraper([testInput_MultiTerm, 'Lawrence', 'Kansas'])
        results = TestScraper.get_results()

        #First, check that we even got results
        self.assertTrue(results)

        # Make sure that the length of the results dictionary is the same length as number of terms
        self.assertEqual(len(results), 3)

        #Now, we have to check if each of the sub-dictionaries has a length of 3, since we set this as the maximum number of results to return
        for term in results:
            self.assertEqual(len(results[term]), 3)

        #Check that each of the entries are actually there
        for term in results:
            for entry in results[term]:
                self.assertTrue(entry)


    # Add unit testing for each term in the dictionary
    # I think this is all the tests we need? Please review

#Test Suite Standalone Can be Run if "python tests.py" is called in this directory
if __name__ == '__main__':
    unittest.main()
