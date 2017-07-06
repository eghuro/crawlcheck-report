This is a web report app for [Crawlcheck](https://github.com/eghuro/crawlcheck).
It's a Flask based app. For detailed settings please refer to Flask documentation.

Basic usage:
 * Use virtualenv and install dependencies
   ```sh
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    ```

 * Create database
   ```sh
   $ python manage.py create_db
   ```

 * Run the app
   ```sh
   $ python manage.py runserver
   ```
