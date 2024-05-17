import unittest
from crud_recipe.reducer_function import recipe_reducer
from crud_recipe.validate_recipe_form import ValidationError,validate_add_recipe_form


class TestRecipeReducer(unittest.TestCase):
    
    def test_simple_reducer(self):
        ingredients = [
            ('salt', 2, 'tbsp'), 
            ('salt', 2, 'tbsp'),
        ]
        real_result = recipe_reducer(ingredients)
        expected_result = [
            ('salt', 4, 'tablespoon'),
        ]
        self.assertEqual(real_result, expected_result)

    def test_same_class_msmts(self):
        ingredients = [
            ('salt', 1, 'tsp'),
            ('salt', 2, 'teaspoons'),
        ]
        real_result = recipe_reducer(ingredients)
        expected_result = [
            ('salt', 3, 'teaspoon'),
        ]
        self.assertEqual(real_result, expected_result)

    def test_different_dimensions(self):
        ingredients = [
            ('salt', 4, 'tablespoons'),
            ('salt', 4, 'tablespoons'),
            ('salt', 3, 'ounces'),
            ('salt', 3, 'ounces'),
        ]
        real_result = recipe_reducer(ingredients)
        expected_result = [
            ('salt', 8, 'tablespoon'),
            ('salt', 6, 'ounce'),
        ]
        self.assertEqual(real_result, expected_result)



class TestAddRecipe(unittest.TestCase):

    def test_validation_error(self):

        bad_recipe_data = [
            'rice, 1pound', 
            'milk, 1, tbsp', 
            'salt, 3, tsp'
            ]

        with self.assertRaises(ValidationError) as err_context:
            validate_add_recipe_form(bad_recipe_data)
        
        # We want to see a tuple length error thrown for line 1
        expectation = '1'
        self.assertEquals(
            err_context.exception.errors['tuple length'], 
            expectation
        )