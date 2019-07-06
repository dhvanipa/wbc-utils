from config import db
import json

res_public_id = "trofi-res-test-123k"


def fix_hours():
    all_hours = db.collection(u'restaurants').document(
        res_public_id).collection(u'hours').stream()
    for hour in all_hours:
        hour_ref = db.collection(u'restaurants').document(
            res_public_id).collection(u'hours').document(hour.id)
        hour_ref.update({"is_active": True})


def fix_menu():
    all_foods = db.collection(u'foods').where(
        u'restaurant_id', u'==', res_public_id).stream()

    for food in all_foods:
        # print(u'{} => {}'.format(food.id, food.to_dict()))
        # food_data = food.to_dict()

        private_info = db.collection(u'foods').document(
            food.id).collection(u'private').stream()
        for info in private_info:
            # print(u'{} => {}'.format(info.id, info.to_dict()))
            food_ref = db.collection(u'foods').document(
                food.id).collection(u'private').document(info.id)

            food_ref.update(
                {"credit_card_fee": 0.01, "ingredients_cost": 0.01, "profit_margin": 0.01})


def main():
    # load menu
    # fix_menu()
    fix_hours()
    # print("Opening file...")
    # with open('shawerma_plus_menu.txt', 'r') as menu:
    #     print("Parsing file as JSON...")
    #     food_data = json.loads(menu.read())
    #     food_list = food_data["list"]
    #     print("Found: " + str(len(food_list)) + " items")
    #     for food_item in food_list:
    #         print("Writing: " + food_item["public"]["name"])
    #         upload_food_item(food_item)
    # print("Finished!")


def upload_food_item(food_item):
    try:
        new_food_ref = db.collection(u'foods').document()
        new_food_ref.set(food_item["public"])
        private_ref = new_food_ref.collection(u'private').document()
        private_ref.set(food_item["private"])
    except:
        print("DB Error!")


main()
