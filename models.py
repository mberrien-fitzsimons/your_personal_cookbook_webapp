import collections
import numpy as np
import pandas as pd
import pickle
import random

from collections import Counter

infile = open('./crf_ingred_dict','rb')
recipe_dict = pickle.load(infile)
infile.close()

infile = open('./crf_tag_dict','rb')
recipe_tags_dict = pickle.load(infile)
infile.close()

infile = open('./crf_ingred_dict','rb')
recipe_dict = pickle.load(infile)
infile.close()

infile = open('./crf_links_dict','rb')
recipe_links_dict = pickle.load(infile)
infile.close()

# infile = open('./data_matrix','rb')
# data_matrix = pickle.load(infile)
# infile.close()

with open('data_matrix', 'rb') as f:
    data_matrix = pickle.load(f)

database_food_list = list(data_matrix.columns)

class recipeRecommender(object):

    def __init__(self, shopping_list, meal):
        self.shopping_list = shopping_list
        self.meal = meal.title()

    def similair_food_items(self):
        user_food_inputs = []
        for item in self.shopping_list:
            if item in database_food_list:
                user_food_inputs.append(item)
        # Construct a new dataframe with the 10 closest neighbours (most similar)
        # create empty dataframe with correct column names
        data_neighbours = pd.DataFrame(index=data_matrix.columns, columns=range(1,11))
        # build matrix with top 10 similair items
        for i in range(0, len(data_matrix.columns)):
            data_neighbours.ix[i,:10] = data_matrix.ix[0:,i].sort_values(ascending=False)[:10].index

        # Construct the neighbourhood from the most similar items to the ones our user has already liked.
        most_similar_to_likes = data_neighbours.loc[user_food_inputs]
        similar_list = most_similar_to_likes.values.tolist()
        self.similar_list = [item for sublist in similar_list for item in sublist]

        return self.similar_list

    def recipe_recommendations(self):

        listofkeys = []
        recipes = []
        recipe_final = []
        listofitems = recipe_dict.items()

        for item in listofitems:
            self.ingred_list = self.extract_ingredients(item[1])
            recipe_title = item[0]
            recipes.append(self.ingredient_recipe_matcher(self.ingred_list, self.similar_list, recipe_title))
        filtered_recipes = filter(None, recipes)

        for lst in filtered_recipes:
            for item in lst:
                recipe_final.append(item)

        restricted_recipes = []
        for title in recipe_final:
            if self.meal in recipe_tags_dict[title]:
                restricted_recipes.append(title)

        if len(restricted_recipes) > 5:
            random_recipes = random.choices(restricted_recipes, k=5)
        else:
            random_recipes = restricted_recipes

        links=[]
        for title in random_recipes:
            links.append(recipe_links_dict[title])

        return random_recipes, links

    @staticmethod
    def extract_ingredients(ing_list):
        ingredients_list = []
        for ingredient in ing_list:
            ingredients_list.append(ingredient['name'])
        return ingredients_list

    @staticmethod
    def ingredient_recipe_matcher(ingredients_list, similar_list, recipe_title):
        matching_recipes = []
        matching_ingredients = []
        return_recipes = []

        for element in similar_list:
            if any(element in s for s in ingredients_list):
                matching_recipes.append(recipe_title)
        count_recipe_dict = dict(Counter(matching_recipes))

        for key, val in count_recipe_dict.items():
            return_recipes.append(key)

        return return_recipes
