from search import keyword_to_titles, title_to_info, search, article_length,key_by_author, filter_to_author, filter_out, articles_from_year
from search_tests_helper import get_print, print_basic, print_advanced, print_advanced_option
from wiki import article_metadata
from unittest.mock import patch
from unittest import TestCase, main

class TestSearch(TestCase):

    ##############
    # UNIT TESTS #
    ##############


    def test_keyword_to_titles(self):
        list_one = [
            ['Texture (music)', 'Bearcat', 1161070178, 3626, ['music', 'texture', 'the', 'and']],
            ['Register (music)', 'Pegship', 1082665179, 598, ['register', 'the', 'and', 'vocal']]                       
        ]
        dct_one = {
            'music': ['Texture (music)'],
            'texture': ['Texture (music)'],
            'the': ['Texture (music)', 'Register (music)'],
            'and': ['Texture (music)', 'Register (music)'],
            'register': ['Register (music)'],
            'vocal': ['Register (music)']
        } 
        self.assertEqual(keyword_to_titles(list_one), dct_one)
    def test_keyword_to_title_single_list(self):
        list_two = [
            ['Texture (music)', 'Bearcat', 1161070178, 3626, ['music', 'texture', 'the', 'and']],
        ]
        dict_two = {
            'music': ['Texture (music)'],
            'texture': ['Texture (music)'],
            'the': ['Texture (music)'],
            'and': ['Texture (music)'],
        }
        self.assertEqual(keyword_to_titles(list_two), dict_two)
    def test_keyword_to_title_empty(self):
        list_three = []
        dict_three = {}
        self.assertEqual(keyword_to_titles(list_three), dict_three)




    def test_title_to_info(self):
        info_list_one = [
            ['Texture (music)', 'Bearcat', 1161070178, 3626, ['music', 'texture', 'the', 'and']],
            ['Register (music)', 'Pegship', 1082665179, 598, ['register', 'the', 'and', 'vocal']]                       
        ]
        info_dct_one = {
            'Texture (music)': {'author': 'Bearcat', 'timestamp': 1161070178, 'length': 3626},
            'Register (music)': {'author': 'Pegship', 'timestamp':1082665179, 'length': 598}
        } 
        self.assertEqual(title_to_info(info_list_one), info_dct_one)
    def test_title_to_info_two(self):
        list_two = [
            ['French pop music', 'Mack Johnson', 1172208041, 5569, ['french', 'pop', 'music', 'the', 'france', 'and', 'radio']],
            ['Ken Kennedy (computer scientist)', 'Mack Johnson', 1246308670, 4144, ['kennedy', 'was', 'computer', 'and', 'the', 'for', 'award']],
            ['Endogenous cannabinoid', 'Pegship', 1168971903, 26, []]             
        ]
        dct_two = {
            'French pop music': {'author': 'Mack Johnson', 'timestamp': 1172208041, 'length': 5569},
            'Ken Kennedy (computer scientist)': {'author': 'Mack Johnson', 'timestamp': 1246308670, 'length': 4144},
            'Endogenous cannabinoid': {'author': 'Pegship', 'timestamp': 1168971903, 'length': 26}
        } 
        self.assertEqual(title_to_info(list_two), dct_two)
    def test_title_to_info_three(self):
        list_three = []
        dct_three = {} 
        self.assertEqual(title_to_info(list_three), dct_three)
    

    def test_search(self):
        dct_one = {
            'music': ['Texture (music)'],
            'texture': ['Texture (music)'],
            'the': ['Texture (music)', 'Register (music)'],
            'and': ['Texture (music)', 'Register (music)'],
            'register': ['Register (music)'],
            'vocal': ['Register (music)']
        }
        list_one = ['Texture (music)']
        self.assertEqual(search('music', dct_one), list_one)
    def test_search_two(self):
        dct_two = {
            'dog': ['Break', 'item', 'pastor'],
            'cat': ['Loki', 'Ghost'],
            'chicken': ['burna boy', 'wizkid', 'shalipopi']
        }
        list_two = ['burna boy', 'wizkid', 'shalipopi']
        self.assertEqual(search('chicken', dct_two), list_two)
    def test_search_three(self):
        dct_three = {
            'music': ['Texture (music)'],
            'texture': ['Texture (music)'],
            'the': ['Texture (music)', 'Register (music)'],
            'and': ['Texture (music)', 'Register (music)'],
            'register': ['Register (music)'],
            'vocal': ['Register (music)'],
            'dog': ['Break', 'item', 'pastor'],
            'cat': ['Loki', 'Ghost'],
            'chicken': ['burna boy', 'wizkid', 'shalipopi']
        }
        list_three = []
        self.assertEqual(search('bot', dct_three), list_three)


    def test_article_length(self):
        max_length = 1000
        length_two = 5000
        length_three = 0

        article_titles = ['Texture (music)', 'Register (music)', 'Endogenous cannabinoid']
        titles_two = ['French pop music', 'Ken Kennedy (computer scientist)']
        titles_three = ['Follow God', 'Money', 'Fried Rice']

        title_to_info = {
            'Texture (music)': {'author': 'Bearcat', 'timestamp': 1161070178, 'length': 3626},
            'Register (music)': {'author': 'Pegship', 'timestamp':1082665179, 'length': 598},
            'Endogenous cannabinoid': {'author': 'Pegship', 'timestamp': 1168971903, 'length': 26}
        }
        info_two = {
            'French pop music': {'author': 'Mack Johnson', 'timestamp': 1172208041, 'length': 5569},
            'Ken Kennedy (computer scientist)': {'author': 'Mack Johnson', 'timestamp': 1246308670, 'length': 4144},
        }
        info_three = {
            'Follow God': {'author': 'me', 'timestamp': 1161078, 'length': 36},
            'Money': {'author': 'dog', 'timestamp':10826659, 'length': 8},
            'Fried Rice': {'author': 'jerry', 'timestamp': 11689, 'length': 257777}          
        }

        list_one = ['Register (music)', 'Endogenous cannabinoid']
        list_two = ['Ken Kennedy (computer scientist)']
        list_three = []

        self.assertEqual(article_length(max_length, article_titles, title_to_info), list_one)
        self.assertEqual(article_length(length_two, titles_two, info_two), list_two)
        self.assertEqual(article_length(length_three, titles_three, info_three), list_three)



    def test_key_author(self):

        article_titles = ['Texture (music)', 'Register (music)', 'Endogenous cannabinoid']
        titles_two = ['French pop music', 'Ken Kennedy (computer scientist)']
        titles_three = ['Follow God', 'Money', 'Fried Rice']

        title_to_info = {
            'Texture (music)': {'author': 'Bearcat', 'timestamp': 1161070178, 'length': 3626},
            'Register (music)': {'author': 'Pegship', 'timestamp':1082665179, 'length': 598},
            'Endogenous cannabinoid': {'author': 'Pegship', 'timestamp': 1168971903, 'length': 26}
        }
        info_two = {
            'French pop music': {'author': 'Mack Johnson', 'timestamp': 1172208041, 'length': 5569},
            'Ken Kennedy (computer scientist)': {'author': 'Mack Johnson', 'timestamp': 1246308670, 'length': 4144},
        }
        info_three = {
            'Follow God': {'author': 'me', 'timestamp': 1161078, 'length': 36},
            'Money': {'author': 'Andre', 'timestamp': 2434, 'length': 22},
            'Fried Rice': {'author': 'jerry', 'timestamp': 11689, 'length': 257777}          
        }

        list_one = {
            'Bearcat': ['Texture (music)'],
            'Pegship': ['Register (music)', 'Endogenous cannabinoid']
        }
        list_two = {
            'Mack Johnson': ['French pop music', 'Ken Kennedy (computer scientist)']
        }
        list_three = {
            'me': ['Follow God'],
            'Andre': ['Money'],
            'jerry': ['Fried Rice']
        }

        self.assertEqual(key_by_author(article_titles, title_to_info), list_one)
        self.assertEqual(key_by_author(titles_two, info_two), list_two)
        self.assertEqual(key_by_author(titles_three, info_three), list_three)


    def test_filter_author(self):

        article_titles = ['Texture (music)', 'Register (music)', 'Endogenous cannabinoid']
        titles_two = ['French pop music', 'Ken Kennedy (computer scientist)']
        titles_three = ['Follow God', 'Money', 'Fried Rice']

        title_to_info = {
            'Texture (music)': {'author': 'Bearcat', 'timestamp': 1161070178, 'length': 3626},
            'Register (music)': {'author': 'Pegship', 'timestamp':1082665179, 'length': 598},
            'Endogenous cannabinoid': {'author': 'Pegship', 'timestamp': 1168971903, 'length': 26}
        }
        info_two = {
            'French pop music': {'author': 'Mack Johnson', 'timestamp': 1172208041, 'length': 5569},
            'Ken Kennedy (computer scientist)': {'author': 'Mack Johnson', 'timestamp': 1246308670, 'length': 4144},
        }
        info_three = {
            'Follow God': {'author': 'me', 'timestamp': 1161078, 'length': 36},
            'Money': {'author': 'Andre', 'timestamp': 2434, 'length': 22},
            'Fried Rice': {'author': 'jerry', 'timestamp': 11689, 'length': 257777}       
        }

        list_one = ['Register (music)', 'Endogenous cannabinoid']
        list_two = ['French pop music', 'Ken Kennedy (computer scientist)']
        list_three = ['Fried Rice']

        self.assertEqual(filter_to_author('Pegship', article_titles, title_to_info), list_one)
        self.assertEqual(filter_to_author('Mack Johnson', titles_two, info_two), list_two)
        self.assertEqual(filter_to_author('jerry', titles_three, info_three), list_three)




if __name__ == "__main__":
    main()