# COPYRIGHT: bihius.me
# AUTHOR: bihius
# TIME SPENT: 6 hours

# This file is the main file that runs the website. It imports the create_app function from the website package and runs the app.

from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)