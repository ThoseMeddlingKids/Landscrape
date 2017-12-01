#@file: tests.py
# PYTHON TEST SUITE FOR LandScrape
# Each "Test" is created as a class
# Every Function inside of the test is testing for a specific functionality
# The Results printed will be for two tests, but if any function within the test fails, the whole test will fail
# Console will print exactly where in the function the test failed if there is an issue.
# For more information, visit the python unittest documentation provided in our root Readme

from Scraper import scrape
import unittest
########################################################################
#@Class: TestOutputSingle
# The purpose of this test is to validate function of a single query search
class TestOutputSingle(unittest.TestCase):

    def test_Get_Output_Given_Input_Single(self):
        # Single Term Test, Checking if a single input produces something.

        #First, generate the results for single term
        testInput_SingleTerm= 'Coffee'
        TestScraper = scrape.Scraper([testInput_SingleTerm,'Lawrence', 'Kansas'])
        results = TestScraper.get_results()

        # Check a Bunch of stuff based on those results (the meat of our test suite)

        #Check that the results dictionary even exists
        print "Checking for Single Term Dictionary..."
        self.assertTrue(results)

        #We expect the dictionary to be length 1, so we are testing that this is true
        print "Checking Dictionary Length..."
        self.assertEqual(len(results), 1)

        #Check to see if the
        print "Checking term existance..."
        for term in results:
            self.assertEqual(len(results[term]), 3)

########################################################################
#@Class: TestOutputMulti
# The Purpose of this Test is to validate function of a multiple query search
class TestOutputMulti(unittest.TestCase):

    def test_Get_Output_Given_Input_Multi(self):
        # Multi-Term Test, Checking that something is returned
        #Set up the test by running a query
        testInput_MultiTerm = 'Coffee, Bars, Tacos'
        TestScraper = scrape.Scraper([testInput_MultiTerm, 'Lawrence', 'Kansas'])
        results = TestScraper.get_results()

        #First, check that we even got results
        print "Checking for multi-term dictionary..."
        self.assertTrue(results)

        # Make sure that the length of the results dictionary is the same length as number of terms
        print "Checking Dictionary Length..."
        self.assertEqual(len(results), 3)

        #Now, we have to check if each of the sub-dictionaries has a length of 3, since we set this as the maximum number of results to return
        print "Validating correct amount of content exists..."
        for term in results:
            self.assertEqual(len(results[term]), 3)

        #Check that each of the entries are actually there
        print "Validating existance of every requested piece of content..."
        for term in results:
            for entry in results[term]:
                self.assertTrue(entry)


#Test Suite Standalone Can be Run from terminal if "python tests.py" is called in this directory
    #If 'ok' for each test, then all test cases passed
    #If 'OK' displayed after all tests, then there were no errors encountered
if __name__ == '__main__':

    print "### Welcome to The LandScrape Test Suite! ###"
    print ""
    print "Starting Tests..."
    unittest.main(verbosity = 2)
