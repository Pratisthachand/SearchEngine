from search import search, article_length, unique_authors, most_recent_article, favorite_author, title_and_author, refine_search, display_result
from search_tests_helper import get_print, print_basic, print_advanced, print_advanced_option
from wiki import article_metadata
from unittest.mock import patch
from unittest import TestCase, main

class TestSearch(TestCase):

    ##############
    # UNIT TESTS #
    ##############

    def test_example_unit_test(self):
        expected_search_soccer_results = [
            ['Spain national beach soccer team', 'jack johnson', 1233458894, 1526],
            ['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562],
            ['Steven Cohen (soccer)', 'Mack Johnson', 1237669593, 2117]
        ]
        self.assertEqual(search('soccer'), expected_search_soccer_results)

    def test_search(self):
        expected_search_canadian_results = [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023], ['2009 in music', 'RussBot', 1235133583, 69451], ['Lights (musician)', 'Burna Boy', 1213914297, 5898], ['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562], ['2007 in music', 'Bearcat', 1169248845, 45652], ['2008 in music', 'Burna Boy', 1217641857, 107605]]
        
        self.assertEqual(search('canadian'),expected_search_canadian_results)
        self.assertEqual(search('CaNaDIAn'),expected_search_canadian_results)
        self.assertEqual(search('pingpong'),[])
        self.assertEqual(search(''),[])

    def test_article_length(self):
        canadian_search_results = [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023],['2009 in music', 'RussBot', 1235133583, 69451],['Lights (musician)', 'Burna Boy', 1213914297, 5898],['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562],['2007 in music', 'Bearcat', 1169248845, 45652],['2008 in music', 'Burna Boy', 1217641857, 107605]]
        
        self.assertEqual(article_length(20000, canadian_search_results),[['Lights (musician)', 'Burna Boy', 1213914297, 5898],['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562]])
        self.assertEqual(article_length(45652,canadian_search_results),[['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023],['Lights (musician)', 'Burna Boy', 1213914297, 5898],['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562],['2007 in music', 'Bearcat', 1169248845, 45652]])
        self.assertEqual(article_length(100,canadian_search_results),[])
        self.assertEqual(article_length(0,canadian_search_results),[])

    def test_unique_authors(self):
        canadian_search_results = [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023],['2009 in music', 'RussBot', 1235133583, 69451],['Lights (musician)', 'Burna Boy', 1213914297, 5898],['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562],['2007 in music', 'Bearcat', 1169248845, 45652],['2008 in music', 'Burna Boy', 1217641857, 107605]]
        
        self.assertEqual(unique_authors(3, canadian_search_results),[['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023],['2009 in music', 'RussBot', 1235133583, 69451],['Lights (musician)', 'Burna Boy', 1213914297, 5898]])
        self.assertEqual(unique_authors(10,canadian_search_results),[['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023],['2009 in music', 'RussBot', 1235133583, 69451],['Lights (musician)', 'Burna Boy', 1213914297, 5898],['2007 in music', 'Bearcat', 1169248845, 45652]])
        self.assertEqual(unique_authors(0,canadian_search_results),[])
        self.assertEqual(unique_authors(-5,canadian_search_results),[])
    
    def test_most_recent_article(self):
        canadian_search_results = [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023],['2009 in music', 'RussBot', 1235133583, 69451],['Lights (musician)', 'Burna Boy', 1213914297, 5898],['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562],['2007 in music', 'Bearcat', 1169248845, 45652],['2008 in music', 'Burna Boy', 1217641857, 107605]]
        self.assertEqual(most_recent_article(canadian_search_results),['2009 in music', 'RussBot', 1235133583, 69451])
    
        _2009_search_results = [['2009 in music', 'RussBot', 1235133583, 69451], ['Lights (musician)', 'Burna Boy', 1213914297, 5898], ['Annie (musical)', 'Jack Johnson', 1223619626, 27558], ['Tony Kaye (musician)', 'Burna Boy', 1141489894, 8419], ["Wake Forest Demon Deacons men's soccer", 'Burna Boy', 1260577388, 26745]]
        self.assertEqual(most_recent_article(_2009_search_results),["Wake Forest Demon Deacons men's soccer", 'Burna Boy', 1260577388, 26745])

        dog_search_results = [['Black dog (ghost)', 'Pegship', 1220471117, 14746], ['Mexican dog-faced bat', 'Mack Johnson', 1255316429, 1138], ['Dalmatian (dog)', 'Mr Jake', 1207793294, 26582], ['Guide dog', 'Jack Johnson', 1165601603, 7339], ['Sun dog', 'Mr Jake', 1208969289, 18050]]
        self.assertEqual(most_recent_article(dog_search_results),['Mexican dog-faced bat', 'Mack Johnson', 1255316429, 1138])

        self.assertEqual(most_recent_article([]),[])

    def test_favorite_author(self):
        canadian_search_results = [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023],['2009 in music', 'RussBot', 1235133583, 69451],['Lights (musician)', 'Burna Boy', 1213914297, 5898],['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562],['2007 in music', 'Bearcat', 1169248845, 45652],['2008 in music', 'Burna Boy', 1217641857, 107605]]
        self.assertEqual(favorite_author('BuRNA boy',canadian_search_results),True)
        self.assertEqual(favorite_author('burna boy',canadian_search_results),True)
        self.assertEqual(favorite_author('Mack Johnson',canadian_search_results),False)
        self.assertEqual(favorite_author('',canadian_search_results),None)

    def test_title_and_author(self):
        canadian_search_results = [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023],['2009 in music', 'RussBot', 1235133583, 69451],['Lights (musician)', 'Burna Boy', 1213914297, 5898],['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562],['2007 in music', 'Bearcat', 1169248845, 45652],['2008 in music', 'Burna Boy', 1217641857, 107605]]
        self.assertEqual(title_and_author(canadian_search_results),[('List of Canadian musicians', 'Jack Johnson'),('2009 in music', 'RussBot'),('Lights (musician)', 'Burna Boy'),('Will Johnson (soccer)', 'Burna Boy'),('2007 in music', 'Bearcat'),('2008 in music', 'Burna Boy')])
        
        _2009_search_results = [['2009 in music', 'RussBot', 1235133583, 69451], ['Lights (musician)', 'Burna Boy', 1213914297, 5898], ['Annie (musical)', 'Jack Johnson', 1223619626, 27558], ['Tony Kaye (musician)', 'Burna Boy', 1141489894, 8419], ["Wake Forest Demon Deacons men's soccer", 'Burna Boy', 1260577388, 26745]]
        self.assertEqual(title_and_author(_2009_search_results),[('2009 in music', 'RussBot'), ('Lights (musician)', 'Burna Boy'), ('Annie (musical)', 'Jack Johnson'), ('Tony Kaye (musician)', 'Burna Boy'), ("Wake Forest Demon Deacons men's soccer", 'Burna Boy')])

        dog_search_results = [['Black dog (ghost)', 'Pegship', 1220471117, 14746], ['Mexican dog-faced bat', 'Mack Johnson', 1255316429, 1138], ['Dalmatian (dog)', 'Mr Jake', 1207793294, 26582], ['Guide dog', 'Jack Johnson', 1165601603, 7339], ['Sun dog', 'Mr Jake', 1208969289, 18050]]
        self.assertEqual(title_and_author(dog_search_results),[('Black dog (ghost)', 'Pegship'), ('Mexican dog-faced bat', 'Mack Johnson'), ('Dalmatian (dog)', 'Mr Jake'), ('Guide dog', 'Jack Johnson'), ('Sun dog', 'Mr Jake')])

        self.assertEqual(title_and_author([]),[])

    def test_refine_search(self):
        canadian_search_results = [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023],['2009 in music', 'RussBot', 1235133583, 69451],['Lights (musician)', 'Burna Boy', 1213914297, 5898],['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562],['2007 in music', 'Bearcat', 1169248845, 45652],['2008 in music', 'Burna Boy', 1217641857, 107605]]
        self.assertEqual(refine_search('MUsic',canadian_search_results), [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023],['2009 in music', 'RussBot', 1235133583, 69451],['Lights (musician)', 'Burna Boy', 1213914297, 5898],['2007 in music', 'Bearcat', 1169248845, 45652],['2008 in music', 'Burna Boy', 1217641857, 107605]])
        self.assertEqual(refine_search('2007',canadian_search_results), [['2007 in music', 'Bearcat', 1169248845, 45652]])
        self.assertEqual(refine_search('soccer',canadian_search_results), [['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562]])
        self.assertEqual(refine_search('',canadian_search_results), [])

    #####################
    # INTEGRATION TESTS #
    #####################

    @patch('builtins.input')
    def test_example_integration_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 1
        advanced_response = 3000

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: [['Spain national beach soccer team', 'jack johnson', 1233458894, 1526], ['Steven Cohen (soccer)', 'Mack Johnson', 1237669593, 2117]]\n"

        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_advanced_option_1(self, input_mock):
        keyword = 'canadian'
        advanced_option = 1
        advanced_response = 20000

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: [['Lights (musician)', 'Burna Boy', 1213914297, 5898], ['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562]]\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_advanced_option_2(self, input_mock):
        keyword = 'canadian'
        advanced_option = 2
        advanced_response = 3

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023], ['2009 in music', 'RussBot', 1235133583, 69451], ['Lights (musician)', 'Burna Boy', 1213914297, 5898]]\n"

        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_advanced_option_3(self, input_mock):
        keyword = 'canadian'
        advanced_option = 3

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nHere are your articles: ['2009 in music', 'RussBot', 1235133583, 69451]\n"

        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_advanced_option_4(self, input_mock):
        keyword = 'canadian'
        advanced_option = 4
        advanced_response = 'Burna Boy'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023], ['2009 in music', 'RussBot', 1235133583, 69451], ['Lights (musician)', 'Burna Boy', 1213914297, 5898], ['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562], ['2007 in music', 'Bearcat', 1169248845, 45652], ['2008 in music', 'Burna Boy', 1217641857, 107605]]\nYour favorite author is in the returned articles!\n"

        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_advanced_option_5(self, input_mock):
        keyword = 'canadian'
        advanced_option = 5

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nHere are your articles: [('List of Canadian musicians', 'Jack Johnson'), ('2009 in music', 'RussBot'), ('Lights (musician)', 'Burna Boy'), ('Will Johnson (soccer)', 'Burna Boy'), ('2007 in music', 'Bearcat'), ('2008 in music', 'Burna Boy')]\n"

        self.assertEqual(output, expected)
     
    @patch('builtins.input')
    def test_advanced_option_6(self, input_mock):
        keyword = 'canadian'
        advanced_option = 6
        advanced_response = '2007'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: [['2007 in music', 'Bearcat', 1169248845, 45652]]\n"

        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_advanced_option_7(self, input_mock):
        keyword = 'canadian'
        advanced_option = 7

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nHere are your articles: [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023], ['2009 in music', 'RussBot', 1235133583, 69451], ['Lights (musician)', 'Burna Boy', 1213914297, 5898], ['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562], ['2007 in music', 'Bearcat', 1169248845, 45652], ['2008 in music', 'Burna Boy', 1217641857, 107605]]\n"

        self.assertEqual(output, expected)

# Write tests above this line. Do not remove.
if __name__ == "__main__":
    main()