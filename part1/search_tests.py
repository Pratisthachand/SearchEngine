from search import search, title_length, article_count, random_article, favorite_article, multiple_keywords, display_result
from search_tests_helper import get_print, print_basic, print_advanced, print_advanced_option
from wiki import article_titles
from unittest.mock import patch
from unittest import TestCase, main

class TestSearch(TestCase):

    ##############
    # UNIT TESTS #
    ##############

    def test_example_unit_test(self):
        # Storing into a variable so don't need to copy and paste long list every time
        # If you want to store search results into a variable like this, make sure you pass a copy of it when
        # calling a function, otherwise the original list (ie the one stored in your variable) might be
        # mutated. To make a copy, you may use the .copy() function for the variable holding your search result.
        expected_dog_search_results = ['Edogawa, Tokyo', 'Kevin Cadogan', 'Endogenous cannabinoid', 'Black dog (ghost)', '2007 Bulldogs RLFC season', 'Mexican dog-faced bat', 'Dalmatian (dog)', 'Guide dog', '2009 Louisiana Tech Bulldogs football team', 'Georgia Bulldogs football', 'Endoglin', 'Sun dog', 'The Mandogs', 'Georgia Bulldogs football under Robert Winston', 'Landseer (dog)']
        self.assertEqual(search('dog'), expected_dog_search_results)

    def test_search_keyword(self):

        expected_soccer_search_results = ['Spain national beach soccer team', 'Will Johnson (soccer)', 'Steven Cohen (soccer)', 'Craig Martin (soccer)', "United States men's national soccer team 2009 results", 'China national soccer team', "Wake Forest Demon Deacons men's soccer"]
        self.assertEqual(search('soccer'),expected_soccer_search_results)
        self.assertEqual(search('SoCcEr'),expected_soccer_search_results)

        expected_language_search_results = ['C Sharp (programming language)', 'B (programming language)', 'Python (programming language)', 'Lua (programming language)', 'Comparison of programming languages (basic instructions)','Ruby (programming language)']
        self.assertEqual(search('language'), expected_language_search_results)
        self.assertEqual(search('LANGUAGE'), expected_language_search_results)

        expected_list_keyword_search_results = ['List of Canadian musicians', 'List of soul musicians', 'List of overtone musicians', 'List of Saturday Night Live musical sketches', 'List of dystopian music, TV programs, and games', 'List of gospel musicians', 'List of computer role-playing games', 'List of video games with time travel']
        self.assertEqual(search('list'), expected_list_keyword_search_results)
        self.assertEqual(search('LisT'), expected_list_keyword_search_results)
        
        expected_keyword_not_found_search_results = []
        self.assertEqual(search('jump'), expected_keyword_not_found_search_results)
        self.assertEqual(search('apple'), expected_keyword_not_found_search_results)

    def test_title_length(self):

        self.assertEqual(title_length(23,search('soccer')), ['Will Johnson (soccer)', 'Steven Cohen (soccer)', 'Craig Martin (soccer)'])
        self.assertEqual(title_length(25,search('language')), ['B (programming language)'])
        self.assertEqual(title_length(0,search('language')), [])
        self.assertEqual(title_length(50,search('list')), ['List of Canadian musicians', 'List of soul musicians', 'List of overtone musicians', 'List of Saturday Night Live musical sketches', 'List of dystopian music, TV programs, and games', 'List of gospel musicians', 'List of computer role-playing games', 'List of video games with time travel'])

    def test_article_count(self):

        soccer_search_results = ['Spain national beach soccer team', 'Will Johnson (soccer)', 'Steven Cohen (soccer)', 'Craig Martin (soccer)', "United States men's national soccer team 2009 results", 'China national soccer team', "Wake Forest Demon Deacons men's soccer"]
        self.assertEqual(article_count(2, soccer_search_results.copy()), ['Spain national beach soccer team', 'Will Johnson (soccer)'])
        self.assertEqual(article_count(10, soccer_search_results.copy()), ['Spain national beach soccer team', 'Will Johnson (soccer)', 'Steven Cohen (soccer)', 'Craig Martin (soccer)', "United States men's national soccer team 2009 results", 'China national soccer team', "Wake Forest Demon Deacons men's soccer"])
        self.assertEqual(article_count(0, soccer_search_results.copy()), [])

    def test_random_article(self):
        
        soccer_search_results = ['Spain national beach soccer team', 'Will Johnson (soccer)', 'Steven Cohen (soccer)', 'Craig Martin (soccer)', "United States men's national soccer team 2009 results", 'China national soccer team', "Wake Forest Demon Deacons men's soccer"]
        self.assertEqual(random_article(1, soccer_search_results.copy()), 'Will Johnson (soccer)')
        self.assertEqual(random_article(6, soccer_search_results.copy()), "Wake Forest Demon Deacons men's soccer")
        self.assertEqual(random_article(-2, soccer_search_results.copy()), '')
        self.assertEqual(random_article(10, soccer_search_results.copy()), '')

    def test_favorite_article(self):

        soccer_search_results = ['Spain national beach soccer team', 'Will Johnson (soccer)', 'Steven Cohen (soccer)', 'Craig Martin (soccer)', "United States men's national soccer team 2009 results", 'China national soccer team', "Wake Forest Demon Deacons men's soccer"]
        self.assertEqual(favorite_article('Spain national beach soccer team', soccer_search_results.copy()), True)
        self.assertEqual(favorite_article('Play in Nepal', soccer_search_results.copy()), False)
        self.assertEqual(favorite_article('', soccer_search_results.copy()), False)

    def test_multiple_keywords(self):

        soccer_search_results = ['Spain national beach soccer team', 'Will Johnson (soccer)', 'Steven Cohen (soccer)', 'Craig Martin (soccer)', "United States men's national soccer team 2009 results", 'China national soccer team', "Wake Forest Demon Deacons men's soccer"]
        self.assertEqual(multiple_keywords('list', soccer_search_results.copy()), ['Spain national beach soccer team', 'Will Johnson (soccer)', 'Steven Cohen (soccer)', 'Craig Martin (soccer)', "United States men's national soccer team 2009 results", 'China national soccer team', "Wake Forest Demon Deacons men's soccer",'List of Canadian musicians', 'List of soul musicians', 'List of overtone musicians', 'List of Saturday Night Live musical sketches', 'List of dystopian music, TV programs, and games', 'List of gospel musicians', 'List of computer role-playing games', 'List of video games with time travel'])
        self.assertEqual(multiple_keywords('language', soccer_search_results.copy()), ['Spain national beach soccer team', 'Will Johnson (soccer)', 'Steven Cohen (soccer)', 'Craig Martin (soccer)', "United States men's national soccer team 2009 results", 'China national soccer team', "Wake Forest Demon Deacons men's soccer", 'C Sharp (programming language)', 'B (programming language)', 'Python (programming language)', 'Lua (programming language)', 'Comparison of programming languages (basic instructions)','Ruby (programming language)'])
        self.assertEqual(multiple_keywords('jump', soccer_search_results.copy()), ['Spain national beach soccer team', 'Will Johnson (soccer)', 'Steven Cohen (soccer)', 'Craig Martin (soccer)', "United States men's national soccer team 2009 results", 'China national soccer team', "Wake Forest Demon Deacons men's soccer"])
        self.assertEqual(multiple_keywords('', soccer_search_results.copy()), ['Spain national beach soccer team', 'Will Johnson (soccer)', 'Steven Cohen (soccer)', 'Craig Martin (soccer)', "United States men's national soccer team 2009 results", 'China national soccer team', "Wake Forest Demon Deacons men's soccer"])
        
    #####################
    # INTEGRATION TESTS #
    #####################

    @patch('builtins.input')
    def test_example_integration_test(self, input_mock):
        keyword = 'dog'
        advanced_option = 6

        # Output of calling display_results() with given user input. If a different
        # advanced option is included, append further user input to this list (after `advanced_option`)
        output = get_print(input_mock, [keyword, advanced_option])
        # Expected print outs from running display_results() with above user input
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nHere are your articles: ['Edogawa, Tokyo', 'Kevin Cadogan', 'Endogenous cannabinoid', 'Black dog (ghost)', '2007 Bulldogs RLFC season', 'Mexican dog-faced bat', 'Dalmatian (dog)', 'Guide dog', '2009 Louisiana Tech Bulldogs football team', 'Georgia Bulldogs football', 'Endoglin', 'Sun dog', 'The Mandogs', 'Georgia Bulldogs football under Robert Winston', 'Landseer (dog)']\n"

        # Test whether calling display_results() with given user input equals expected printout
        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_option_1(self, input_mock):
        keyword = 'soccer'
        advanced_option = 1
        title_length = 23

        output = get_print(input_mock, [keyword, advanced_option, title_length])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option)  + '\n' + print_advanced_option(advanced_option)+ str(title_length) + "\n\nHere are your articles: ['Will Johnson (soccer)', 'Steven Cohen (soccer)', 'Craig Martin (soccer)']\n"
       
        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_option_2(self, input_mock):
        keyword = 'soccer'
        advanced_option = 2
        article_count = 2

        output = get_print(input_mock, [keyword, advanced_option, article_count])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option)  + '\n' + print_advanced_option(advanced_option)+ str(article_count) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Will Johnson (soccer)']\n"
        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_option_3(self, input_mock):
        keyword = 'soccer'
        advanced_option = 3
        index = 6

        output = get_print(input_mock, [keyword, advanced_option, index])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option)  + '\n' + print_advanced_option(advanced_option)+ str(index) + "\n\nHere are your articles: Wake Forest Demon Deacons men's soccer\n"
        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_option_4(self, input_mock):
        keyword = 'soccer'
        advanced_option = 4
        favorite = 'China national soccer team'

        output = get_print(input_mock, [keyword, advanced_option, favorite])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option)  + '\n' + print_advanced_option(advanced_option)+ str(favorite) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Will Johnson (soccer)', 'Steven Cohen (soccer)', 'Craig Martin (soccer)', \"United States men's national soccer team 2009 results\", 'China national soccer team', \"Wake Forest Demon Deacons men's soccer\"]\nYour favorite article is in the returned articles!\n"
        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_option_5(self, input_mock):
        keyword = 'soccer'
        advanced_option = 5
        extra_keyword = 'dog'

        output = get_print(input_mock, [keyword, advanced_option, extra_keyword])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + extra_keyword + "\n\nHere are your articles: ['Spain national beach soccer team', 'Will Johnson (soccer)', 'Steven Cohen (soccer)', 'Craig Martin (soccer)', \"United States men's national soccer team 2009 results\", 'China national soccer team', \"Wake Forest Demon Deacons men's soccer\", 'Edogawa, Tokyo', 'Kevin Cadogan', 'Endogenous cannabinoid', 'Black dog (ghost)', '2007 Bulldogs RLFC season', 'Mexican dog-faced bat', 'Dalmatian (dog)', 'Guide dog', '2009 Louisiana Tech Bulldogs football team', 'Georgia Bulldogs football', 'Endoglin', 'Sun dog', 'The Mandogs', 'Georgia Bulldogs football under Robert Winston', 'Landseer (dog)']\n"
        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_option_6(self, input_mock):
        keyword = 'soccer'
        advanced_option = 6

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option)  + '\n' + print_advanced_option(advanced_option)+ "\nHere are your articles: ['Spain national beach soccer team', 'Will Johnson (soccer)', 'Steven Cohen (soccer)', 'Craig Martin (soccer)', \"United States men's national soccer team 2009 results\", 'China national soccer team', \"Wake Forest Demon Deacons men's soccer\"]\n"
        self.assertEqual(output, expected)
        

# Write tests above this line. Do not remove.
if __name__ == "__main__":
    main()