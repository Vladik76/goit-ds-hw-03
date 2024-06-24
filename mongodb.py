import pymongo
from pymongo import MongoClient
from pymongo.server_api import ServerApi

URI = ("mongodb+srv://vladislavputintsev:7%23%237fF%2ANACDPv6W@cluster0.yqxzmo3.mongodb.net/?retryWrites=true&w"
       "=majority&appName=Cluster0")
CLIENT = MongoClient(URI, server_api=ServerApi('1'))
DB = CLIENT.book


def errors_handler(func):
    """
    Decorator. Errors handler
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except pymongo.errors.OperationFailure as err:
            return err
        except TypeError as err:
            return str(err)
        except ValueError as err:
            return  str(err)

    return inner


@errors_handler
def get_all():
    for el in DB.cats.find({}):
        print(el)


@errors_handler
def get_cat():
    name = input("Name: ")
    result = DB.cats.find({'name': name})
    print(result)

@errors_handler
def cat_update(name:str,age:int):
    if type(age) is int:
        if age > 0:
            DB.cats.update_one({"name": name}, {"$set": {"age": age}})
            result = DB.cats.find({"name": name})
            print(result)
        else:
            raise ValueError("The age should be positive")
    else:
        raise TypeError("Age should be numeric")

@errors_handler
def cat_update_add_feature(name:str,feature:str):
    DB.cats.update_one({"name": name}, {"$addToSet": {"features": feature}})
    result = DB.cats.find_one({"name": name})
    print(result)

@errors_handler
def cat_delete(name:str):
    DB.cats.delete_one({"name": name})
    result = DB.cats.find_one({"name": name})
    print(result)
@errors_handler
def cat_delete_all():
    DB.cats.delete_many({})
    get_all()

def main():
    #Реалізуйте функцію для виведення всіх записів із колекції.
    get_all()
    #Реалізуйте функцію, яка дозволяє користувачеві ввести ім'я кота та виводить інформацію про цього кота.
    #get_cat()
    #Створіть функцію, яка дозволяє користувачеві оновити вік кота за ім'ям.
    #cat_update('Liza',2)
    #Створіть функцію, яка дозволяє додати нову характеристику до списку features кота за ім'ям.
    #cat_update_add_feature("Liza","ahhh")
    #Реалізуйте функцію для видалення запису з колекції за ім'ям тварини.
    #cat_delete("Liza")
    #Реалізуйте функцію для видалення всіх записів із колекції.
    #cat_delete_all()

if __name__ == "__main__":
    main()
