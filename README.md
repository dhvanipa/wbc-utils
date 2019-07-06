# wbc-utils

## Trofi:

    master.py

To be run when after restaurant signs up. Initializes all the restaurant hours () and once all the details are filled out, runs the trofi algorithm which calculates all the contributions and discounts.

    capture.py

Every hour figures out the final discount, captures the amount accordingly. Also updates each order document.

    reset_nightly.py

Every night (11:59 pm), resets the discounts dictionary for each hour by setting all the contributions to 0.
TODO: Make it copy over the day's discounts into a log's document.

    upload_menu.py

Uploads the specified menu from a .txt file with JSON format. The trofi code is linked with each food item so that when a restaurant signs up, it can then be transferred over.

## Third Party:

json-firestore credit:
https://gist.github.com/sturmenta/cbbe898227cb1eaca7f85d0191eaec7e
