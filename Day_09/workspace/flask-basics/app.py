from flask import Flask, render_template

app = Flask('My frist flask webapp')

@app.route('/about')
def about_this_app():
    data = dict(
        title='About Vinod', 
        author_name='Vinod Kumar', 
        author_emails=[
            {'official': False, 'value': 'vinod@vinod.co'},
            {'official': True, 'value': 'vinod@cyblore.com'},
            {'official': True, 'value': 'vinod@knowledgeworksindia.com'}
        ])
    return render_template('about.html', **data)

@app.route('/')
def homepage():
    data = {
        'title': 'Flask App v2.0',
        'heading': 'Welcome to Flask Training',
        'subheading': 'Flask is easy'
    }
    return render_template('home.html', **data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')