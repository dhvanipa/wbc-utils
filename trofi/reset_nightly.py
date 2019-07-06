from safe_schedule import SafeScheduler
import time
from config import db


def run_nightly():
    all_restaurants = db.collection(u'restaurants').where(
        u'is_active', u'==', True).stream()

    for restaurant in all_restaurants:
        print("Working on restaurant: " + str(restaurant.id))
        # res_public_data = restaurant.to_dict()

        all_hours = db.collection(u'restaurants').document(
            restaurant.id).collection("hours").stream()

        for hour in all_hours:
            print("Working on hour: " + str(hour.id))
            hour_data = hour.to_dict()

            all_discounts = hour_data["discounts"]
            new_discounts = {}
            for discount in sorted(all_discounts):
                if discount == "0_00":
                    new_discounts[discount] = {
                        "is_active": True,
                        "current_contributed": 0,
                    }
                else:
                    new_discounts[discount] = {
                        "is_active": False,
                        "current_contributed": 0,
                    }

            hour_ref = db.collection(u'restaurants').document(
                restaurant.id).collection("hours").document(hour.id)

            hour_ref.update({u'discounts': new_discounts})


run_nightly()


# def job():
#     run_nightly()


# scheduler = SafeScheduler()
# scheduler.every().day.at('23:59').do(job)

# while True:
#     scheduler.run_pending()
#     time.sleep(1)
