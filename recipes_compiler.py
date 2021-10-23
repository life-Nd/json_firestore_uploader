import os
import json
from typing import Collection
import firebase_admin
from firebase_admin import firestore


class GetDirectoryList():
    def __init__(self, path):
        self.main_path = path
        self.absolute_path = []
        self.relative_path = []
        self.rep = 0

    def get_files_and_folders(self, resp, path):
        _all = os.listdir(path)
        filtered = _all[0:100]
        resp["files"] = []
        for file_folder in filtered:
            if file_folder != "." and file_folder != "..":
                if os.path.isdir(path + "/" + file_folder):
                    resp[file_folder] = {}
                    self.get_files_and_folders(
                        resp=resp[file_folder], path=path + "/" + file_folder)
                else:
                    resp["files"].append(file_folder)
                    self.absolute_path.append(path.replace(
                        self.main_path + "/", "") + "/" + file_folder)
                    self.relative_path.append(path + "/" + file_folder)
        return resp, self.relative_path, self.absolute_path

    @property
    def get_all_files_folder(self):
        self.resp = {self.main_path: {}}
        _all = self.get_files_and_folders(
            self.resp[self.main_path], self.main_path)
        return _all


if __name__ == '__main__':
    path_source = "/users/lifen/projects/recipes_a"
    mylib = GetDirectoryList(path=path_source)
    file_list = mylib.get_all_files_folder
    path_names = json.dumps(file_list)
    path_list = list(file_list[0]['files'])
    write_path = "/Users/lifen/Projects/code/recipes_ml/recipes_compiled.py"
    file = open(write_path, 'w+')
    cred = firebase_admin.credentials.Certificate(
        "/Users/lifen/Downloads/myxmiPythonSecretKey.json")
    firebase_admin.initialize_app(cred, {
        'projectId': 'myxmi-94982',
    })
    db = firestore.client()
    for x in path_list:

        with open(F"{path_source}/{x}") as f:
            try:
                lines = f.read()
                jsonMapped = json.loads(lines)
                _title = str(jsonMapped['title'])
                title = _title.lower()
                _ingredients = jsonMapped['ingredients']
                ingredients = dict(enumerate(_ingredients))
                keys_valuesIngredients = ingredients.items()
                strIngredients = {str(key): str(value)
                                  for key, value in keys_valuesIngredients}
                # print('ingredients', strIngredients)
                language = jsonMapped['language']
                source = jsonMapped['source']
                tags = jsonMapped['tags']
                url = jsonMapped['url']
                image = None
                # if('image' in jsonMapped):
                #     image = jsonMapped['image']
                steps = jsonMapped['directions']
                reviews = []
                # if (tags != []) and (tags != None):
                #     print('----tags-----', tags)
                if('Salad' in tags and 'image' in jsonMapped):
    
                    image = jsonMapped['image']
                    print(F'tags: #{tags}')
                    print('vegan found')
                    metaData = {
                        'title': title,
                        'steps_count': F'{len(steps)}',
                        'ingredients_count': F'{len(ingredients)}',
                        'stars': None,
                        'used_count': '1',
                        'image_url': image,
                        'uid': 'xQkQZgUlYYedGxgsBLRNCmzQcok2',
                        'duration': '20 min',
                        'category': 'food',
                        'sub_category': 'salad',
                        'access': 'public',
                        'difficulty': 'easy',
                        'reference': F'{hash(url)}',
                        'made': '',
                        'reviews_count': F'{len(reviews)}',
                        'portions': '4',
                        'likedBy': None,
                        'username': 'Ralph',
                        'photoUrl': 'https://firebasestorage.googleapis.com/v0/b/myxmi-94982.appspot.com/o/1633484360052-15857.jpg?alt=media&token=858e6507-d2ad-4f17-a441-333ccd4bb740',
                        'diet': '',
                        'tags': tags,
                        'language': 'en'
                    }
                    data = {
                        'title': title,
                        'steps': list(steps),
                        'ingredients': strIngredients,
                        'reviews': reviews,
                        'url': url
                    }

                    ref = db.collection(u'Recipes').document()
                    ref.set(metaData)
                    print('doc_ref',ref.id)
                    print('x: ', x)
                    print('tags', tags)
                    if (ref.id != None):
                        db.collection(u'Instructions').document(ref.id).set(data)

            except ValueError:
                print("Oops!  That was not a valid text.  Try again...")
