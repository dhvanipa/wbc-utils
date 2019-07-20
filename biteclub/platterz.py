
import requests
import json

# RAW relevant API calls
# https://api.platterz.ca/api/restaurant_locations/browse?count=12&page=1&sort_by=popular&seed=137&major_city_id=3
# https://api.platterz.ca/api/restaurant_locations?context=browse&count=10&major_city_id=3&restaurant_slug=shawarma-plus
# https://api.platterz.ca/api/offering_searches?count=25&group_order=false&offerings=true&page=1&product_kind%5B%5D=platter&product_kind%5B%5D=addon&restaurant_location_slug=shawarma-plus/waterloo-220-king-st-n-waterloo-on-n2j-2y7-canada&visible=true
# https://api.platterz.ca/api/restaurants/shawarma-plus/restaurant_locations/waterloo-220-king-st-n-waterloo-on-n2j-2y7-canada

# Important API calls (i.e. parsed)
# https://api.platterz.ca/api/restaurant_locations?restaurant_slug=shawarma-plus
# https://api.platterz.ca/api/menu_sections?restaurant_slug=shawarma-plus&page=1
# https://api.platterz.ca/api/offering_searches?restaurant_location_slug=shawarma-plus/waterloo-220-king-st-n-waterloo-on-n2j-2y7-canada&visible=true
# https://api.platterz.ca/api/unit_groups?offering_id=3521


def get_restaurant_info(restaurant_slug):
    # name
    # description
    # price level
    # address
    url = f"https://api.platterz.ca/api/restaurant_locations?restaurant_slug={restaurant_slug}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        # Only supporting first location as of now
        res_data = data["restaurant_locations"][0]
        price_level = res_data["price_level"]
        display_price_level = ""
        for _ in range(price_level):
            display_price_level += "$"

        parsed_data = {
            "name": res_data["restaurant_name"],
            "description": res_data["restaurant"]["description"],
            "price_level": display_price_level,
            "address": res_data["address"],
        }
        return parsed_data, res_data["full_slug"],
    else:
        return None, None


def get_menu_sections(restaurant_slug):
    # name
    url = f"https://api.platterz.ca/api/menu_sections?restaurant_slug={restaurant_slug}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        menu_sections = data["menu_sections"]
        parsed_data = []
        for section in menu_sections:
            parsed_data.append(section["name"])
        return parsed_data
    else:
        return None


def get_add_ons(offering_id):
    # category
    # name
    # price
    url = f"https://api.platterz.ca/api/unit_groups?offering_id={offering_id}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        parsed_data = []

        add_on_groups = data["unit_groups"]
        for add_on in add_on_groups:
            all_units = []
            for unit in add_on["units"]:
                parsed_unit = {
                    "name": unit["name"],
                    "price": unit["surcharge"],
                }
                all_units.append(parsed_unit)
            parsed_data.append({
                "category": add_on["name"],
                "units": all_units
            })
        return parsed_data
    else:
        return None


def get_menu_items(restaurant_location_slug):
    # title
    # description
    # price kind
    # serves min-max ppl
    # tags
    # add ons
    url = f"https://api.platterz.ca/api/offering_searches?restaurant_location_slug={restaurant_location_slug}&visible=true"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        offerings = data["offering_searches"]
        parsed_data = []
        for food in offerings:
            offering_data = food["offering"]
            food_data = offering_data["platter"]
            # TAKING DEFAULT PLATTER SIZE
            other_data = offering_data["platter_sizes"][0]
            tags = food_data["tags"]
            parsed_tags = []
            display_price_kind = ""
            if offering_data["price_kind"] == "per_person":
                display_price_kind = "Serves Family Style"
            for tag in tags:
                parsed_tags.append(tag["title"])

            parsed_add_ons = get_add_ons(food["offering_id"])

            parsed_food = {
                "title": food_data["title"],
                "description": food_data["description"],
                "price": other_data["price"],
                "price_kind": display_price_kind,
                "min_people": other_data["min_people"],
                "max_people": other_data["max_people"],
                "tags": parsed_tags,
                "add_ons": parsed_add_ons,
            }

            parsed_data.append(parsed_food)

        return parsed_data
    else:
        return None


def parse_restaurant(restaurant_slug):
    print("Starting parsing on...")
    working_restaurant = restaurant_slug
    print(working_restaurant)
    res_info, full_slug = get_restaurant_info(working_restaurant)
    if res_info:
        print("Got Restaurant info...")
        print("Parsing menu...")
        menu_sections = get_menu_sections(working_restaurant)
        menu_items = get_menu_items(full_slug)
        if not menu_items:
            return None, None, None
    else:
        print("Error!")
        return None, None, None

    print("Got Menu info...")
    parsed_restaurant_data = {
        "res_info": res_info,
        "menu_sections": menu_sections,
        "menu_items": menu_items
    }
    print("Finished parsing restaurant...")
    print(restaurant_slug)
    return parsed_restaurant_data


def main():
    res_data = parse_restaurant("shawarma-plus")
    # print(res_data)


main()
