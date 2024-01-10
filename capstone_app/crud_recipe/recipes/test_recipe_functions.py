import unittest
from crud_recipe.reducer_function import recipe_reducer


class TestRecipeReducer(unittest.TestCase):
    
    def test_simple_reducer(self):
        ingredients = [
            ('parsley', 2, 'oz'), 
            ('cream', 2, 'cups'), 
            ('guanciale', 6, 'oz'), 
            ('ziti', 1, 'pound'), 
            ('parmesan', 8, 'ounces'), 
            ('cream', 1.5, 'cups'), 
            ('ziti', 2, 'pounds'), 
            ('parmesan', 12, 'oz'), 
            ('butter', 0.5, 'lbs')
        ]
        actual_result = recipe_reducer(ingredients) # exercise our function
        expected_result = [
            ('parsley', 2, 'ounce'), 
            ('cream', 3, 'cup'), 
            ('guanciale', 6, 'ounce'), 
            ('ziti', 3, 'pound'), 
            ('parmesan', 20, 'ounce'), 
            ('butter', 0, 'pound')
        ]
        self.assertEqual(actual_result, expected_result)

