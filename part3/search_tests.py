from search import keyword_to_titles, title_to_info, search, article_length,key_by_author, filter_to_author, filter_out, articles_from_year
from search_tests_helper import get_print, print_basic, print_advanced, print_advanced_option
from wiki import article_metadata
from unittest.mock import patch
from unittest import TestCase, main

class TestSearch(TestCase):

    ##############
    # UNIT TESTS #
    ##############

    def test_example_unit_test(self):
        dummy_keyword_dict = {
            'cat': ['title1', 'title2', 'title3'],
            'dog': ['title3', 'title4']
        }
        expected_search_results = ['title3', 'title4']
        self.assertEqual(search('dog', dummy_keyword_dict), expected_search_results)

    def test_keyword_to_titles(self):
    
        #One article only. 
        metadata_1 = [['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562, ['johnson', 'canadian', 'soccer', 'player']]]
        expected_results_1 = {'johnson': ['Will Johnson (soccer)'], 'canadian' : ['Will Johnson (soccer)'], 'soccer' : ['Will Johnson (soccer)'], 'player' : ['Will Johnson (soccer)']}
        
        #Multiple articles with some common keywords.
        metadata_2 = [['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562, ['johnson', 'canadian', 'soccer', 'player']],
                      ['Lights (musician)', 'Burna Boy', 1213914297, 5898, ['lights', 'april', 'canadian', 'and']]]
        expected_results_2 = {'johnson': ['Will Johnson (soccer)'], 'canadian' : ['Will Johnson (soccer)', 'Lights (musician)'], 'soccer' : ['Will Johnson (soccer)'], 'player' : ['Will Johnson (soccer)'], 'lights': ['Lights (musician)'], 'april' : ['Lights (musician)'], 'and': ['Lights (musician)']}

        #Multiple articles with unique keywords.
        metadata_3 = [['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562, ['johnson', 'canadian', 'soccer', 'player']],
                      ['Lights (musician)', 'Burna Boy', 1213914297, 5898, ['lights', 'april', 'canadian', 'and']],
                      ['Black dog (ghost)', 'Pegship', 1220471117, 14746, ['black', 'dog', 'found']]]
        expected_results_3 = {'johnson': ['Will Johnson (soccer)'], 'canadian' : ['Will Johnson (soccer)', 'Lights (musician)'], 'soccer' : ['Will Johnson (soccer)'], 'player' : ['Will Johnson (soccer)'], 'lights': ['Lights (musician)'], 'april' : ['Lights (musician)'], 'and': ['Lights (musician)'], 'black': ['Black dog (ghost)'], 'dog': ['Black dog (ghost)'], 'found': ['Black dog (ghost)']}

        #Edge case - empty list:
        metadata_4 = [[]]
        expected_results_4 = {}
        
        self.assertEqual(keyword_to_titles(metadata_1), expected_results_1)
        self.assertEqual(keyword_to_titles(metadata_2), expected_results_2)
        self.assertEqual(keyword_to_titles(metadata_3), expected_results_3)
        self.assertEqual(keyword_to_titles(metadata_4), expected_results_4)

    def test_title_to_info(self):
        metadata_1 = [['Spain national beach soccer team', 'jack johnson', 1233458894, 1526, ['beach', 'soccer', 'fifa']]]
        metadata_2 = [['Spain national beach soccer team', 'jack johnson', 1233458894, 1526, ['beach', 'soccer', 'fifa']],['Black dog (ghost)', 'Pegship', 1220471117, 14746, ['black', 'dog', 'found']], ['Lights (musician)', 'Burna Boy', 1213914297, 5898, ['lights', 'april', 'canadian', 'and']]]
        metadata_3 = [[]]  

        self.assertEqual(title_to_info(metadata_1), {'Spain national beach soccer team': {'author': 'jack johnson', 'timestamp': 1233458894, 'length': 1526}})
        self.assertEqual(title_to_info(metadata_2), {'Spain national beach soccer team': {'author': 'jack johnson', 'timestamp': 1233458894, 'length': 1526}, 'Black dog (ghost)': {'author': 'Pegship', 'timestamp': 1220471117, 'length': 14746}, 'Lights (musician)': {'author': 'Burna Boy', 'timestamp': 1213914297, 'length':5898}})
        self.assertEqual(title_to_info(metadata_3), {})

    def test_search_results(self):
        keyword_dict = {'johnson': ['Will Johnson (soccer)'], 'canadian' : ['Will Johnson (soccer)', 'Lights (musician)'], 'soccer' : ['Will Johnson (soccer)'], 'player' : ['Will Johnson (soccer)'], 'lights': ['Lights (musician)'], 'april' : ['Lights (musician)'], 'and': ['Lights (musician)'], 'black': ['Black dog (ghost)'], 'dog': ['Black dog (ghost)'], 'found': ['Black dog (ghost)']}
        
        self.assertEqual(search('canadian',keyword_dict), ['Will Johnson (soccer)', 'Lights (musician)'])
        self.assertEqual(search('soccer',keyword_dict), ['Will Johnson (soccer)'])
        self.assertEqual(search('SOCCer',keyword_dict), [])
        self.assertEqual(search('',keyword_dict), [])

    def test_article_length(self):
        
        article_titles = ['Will Johnson (soccer)','Lights (musician)','Black dog (ghost)','Spain national beach soccer team']
        title_to_info = {'Will Johnson (soccer)': {'author': 'Burna Boy', 'timestamp': 1218489712, 'length': 3562}, 'Lights (musician)': {'author': 'Burna Boy', 'timestamp': 1213914297, 'length': 5898}, 'Black dog (ghost)' : {'author': 'Pegship', 'timestamp': 1220471117, 'length': 14746}, 'Spain national beach soccer team': {'author': 'jack johnson', 'timestamp': 1233458894, 'length': 1526}}

        self.assertEqual(article_length(15000,article_titles,title_to_info),['Will Johnson (soccer)','Lights (musician)','Black dog (ghost)','Spain national beach soccer team'])
        self.assertEqual(article_length(4000,article_titles,title_to_info),['Will Johnson (soccer)','Spain national beach soccer team'])
        self.assertEqual(article_length(0,article_titles,title_to_info),[])

    def test_key_by_author(self):

        #All articles with same author.
        article_titles_1 = ['Will Johnson (soccer)','Lights (musician)']
        title_to_info_1 = {'Will Johnson (soccer)': {'author': 'Burna Boy', 'timestamp': 1218489712, 'length': 3562}, 'Lights (musician)': {'author': 'Burna Boy', 'timestamp': 1213914297, 'length': 5898}}

        #All articles with unique authors.
        article_titles_2 = ['Black dog (ghost)','Spain national beach soccer team']
        title_to_info_2 = {'Black dog (ghost)' : {'author': 'Pegship', 'timestamp': 1220471117, 'length': 14746}, 'Spain national beach soccer team': {'author': 'jack johnson', 'timestamp': 1233458894, 'length': 1526}} 

        #Articles with same authors and unique authors.
        article_titles_3 = ['Will Johnson (soccer)','Lights (musician)','Black dog (ghost)','Spain national beach soccer team']
        title_to_info_3 = {'Will Johnson (soccer)': {'author': 'Burna Boy', 'timestamp': 1218489712, 'length': 3562}, 'Lights (musician)': {'author': 'Burna Boy', 'timestamp': 1213914297, 'length': 5898}, 'Black dog (ghost)' : {'author': 'Pegship', 'timestamp': 1220471117, 'length': 14746}, 'Spain national beach soccer team': {'author': 'jack johnson', 'timestamp': 1233458894, 'length': 1526}} 

        self.assertEqual(key_by_author(article_titles_1,title_to_info_1),{'Burna Boy':['Will Johnson (soccer)','Lights (musician)']})
        self.assertEqual(key_by_author(article_titles_2,title_to_info_2),{'Pegship': ['Black dog (ghost)'],'jack johnson':['Spain national beach soccer team']})
        self.assertEqual(key_by_author(article_titles_3,title_to_info_3),{'Burna Boy':['Will Johnson (soccer)','Lights (musician)'], 'Pegship': ['Black dog (ghost)'],'jack johnson':['Spain national beach soccer team']})
        
        #how to check case sensitivity in this function?

    def test_filter_to_author(self):
        article_titles = ['Will Johnson (soccer)','Lights (musician)','Black dog (ghost)','Spain national beach soccer team']
        title_to_info = {'Will Johnson (soccer)': {'author': 'Burna Boy', 'timestamp': 1218489712, 'length': 3562}, 'Lights (musician)': {'author': 'Burna Boy', 'timestamp': 1213914297, 'length': 5898}, 'Black dog (ghost)' : {'author': 'Pegship', 'timestamp': 1220471117, 'length': 14746}, 'Spain national beach soccer team': {'author': 'jack johnson', 'timestamp': 1233458894, 'length': 1526}} 

        self.assertEqual(filter_to_author('Burna Boy',article_titles,title_to_info),['Will Johnson (soccer)','Lights (musician)'])
        self.assertEqual(filter_to_author('BURNA BoY',article_titles,title_to_info),[])
        self.assertEqual(filter_to_author('Pratistha',article_titles,title_to_info),[])
        self.assertEqual(filter_to_author('',article_titles,title_to_info),[])

    def test_filter_out(self):
        article_titles = ['Will Johnson (soccer)','Lights (musician)','2009 in music']
        keyword_to_titles = {'johnson': ['Will Johnson (soccer)'], 'canadian' : ['Will Johnson (soccer)', 'Lights (musician)','2009 in music'], 'soccer' : ['Will Johnson (soccer)'], 'player' : ['Will Johnson (soccer)'], 'lights': ['Lights (musician)'], 'april' : ['Lights (musician)'], 'and': ['Lights (musician)'], 'music': ['2009 in music'], 'american': ['2009 in music'], 'british': ['2009 in music']}
        
        self.assertEqual(filter_out('british',article_titles,keyword_to_titles),['Will Johnson (soccer)','Lights (musician)'])
        self.assertEqual(filter_out('canadian',article_titles,keyword_to_titles),[])
        self.assertEqual(filter_out('NEPAL',article_titles,keyword_to_titles),['Will Johnson (soccer)','Lights (musician)','2009 in music'])
        self.assertEqual(filter_out('',article_titles,keyword_to_titles),['Will Johnson (soccer)','Lights (musician)','2009 in music'])

    def test_articles_from_year(self):
        article_titles = ['List of Canadian musicians', '2009 in music', 'Lights (musician)', 'Will Johnson (soccer)']
        title_to_info = {'List of Canadian musicians': {'author': 'Jack Johnson', 'timestamp': 1181623340, 'length': 21023}, '2009 in music': {'author': 'RussBot', 'timestamp': 1235133583, 'length' : 69451}, 'Lights (musician)': {'author': 'Burna Boy', 'timestamp': 1213914297, 'length': 5898}, 'Will Johnson (soccer)': {'author': 'Burna Boy', 'timestamp': 1218489712, 'length': 3562}}
        
        self.assertEqual(articles_from_year(2008,article_titles,title_to_info),['Lights (musician)', 'Will Johnson (soccer)'])
        self.assertEqual(articles_from_year(2009,article_titles,title_to_info),['2009 in music'])
        self.assertEqual(articles_from_year(2020,article_titles,title_to_info),[])
        self.assertEqual(articles_from_year(0,article_titles,title_to_info),[])
        self.assertEqual(articles_from_year(-34,article_titles,title_to_info),[])

    #####################
    # INTEGRATION TESTS #
    #####################

    @patch('builtins.input')
    def test_example_integration_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 5
        advanced_response = 2009

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Steven Cohen (soccer)']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_advanced_option_1(self, input_mock):
        keyword = 'canadian'
        advanced_option = 1
        advanced_response = 4000

        output = get_print(input_mock, [keyword, advanced_option,advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Will Johnson (soccer)']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_advanced_option_2(self, input_mock):
        keyword = 'canadian'
        advanced_option = 2

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nHere are your articles: {'Jack Johnson': ['List of Canadian musicians'], 'RussBot': ['2009 in music'], 'Burna Boy': ['Lights (musician)', 'Will Johnson (soccer)', '2008 in music'], 'Bearcat': ['2007 in music']}\n"

        self.assertEqual(output, expected)    
    
    @patch('builtins.input')
    def test_advanced_option_3(self, input_mock):
        keyword = 'canadian'
        advanced_option = 3
        advanced_response = 'Burna Boy'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Lights (musician)', 'Will Johnson (soccer)', '2008 in music']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_advanced_option_4(self, input_mock):
        keyword = 'canadian'
        advanced_option = 4
        advanced_response = 'soccer'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['List of Canadian musicians', '2009 in music', 'Lights (musician)', '2007 in music', '2008 in music']\n"

        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_advanced_option_5(self, input_mock):
        keyword = 'canadian'
        advanced_option = 5
        advanced_response = 2008

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Lights (musician)', 'Will Johnson (soccer)', '2008 in music']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_advanced_option_6(self, input_mock):
        keyword = 'canadian'
        advanced_option = 6

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nHere are your articles: ['List of Canadian musicians', '2009 in music', 'Lights (musician)', 'Will Johnson (soccer)', '2007 in music', '2008 in music']\n"

        self.assertEqual(output, expected)
    
# Write tests above this line. Do not remove.
if __name__ == "__main__":
    main()