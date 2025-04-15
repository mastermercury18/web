from flask import Flask, render_template, request, redirect, url_for, session
import time
import math
import logging

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem' 

@app.route('/')
def index():
    session['start_time'] = time.time()
    session['unlocked_rooms'] = ['puzzle1']
    return render_template('index.html')

@app.route('/puzzle1', methods=['GET', 'POST'])
def puzzle1():
    answer = request.form.get('answer')
    
    if answer == None:
        return render_template('puzzle1.html', unlocked_rooms = session.get('unlocked_rooms'))
    if answer.lower() == 'superman is weak':
        session['unlocked_rooms'].append('puzzle2')
        session.modified = True
        return redirect(url_for('puzzle2'))
    else:
        return render_template('puzzle1.html', error="Incorrect answer. Try again.", unlocked_rooms = session.get('unlocked_rooms'))

@app.route('/puzzle2', methods=['GET', 'POST'])
def puzzle2():
    answer = request.form.get('answer')

    if answer == None:
        return render_template('puzzle2.html', unlocked_rooms = session.get('unlocked_rooms'))
    if answer == 'Prepare for an endless winter Gotham. No one can stop the freeze!':
        session['unlocked_rooms'].append('puzzle3')
        session.modified = True
        return redirect(url_for('puzzle3'))
    else:
        return render_template('puzzle2.html', error="Incorrect answer. Try again.", unlocked_rooms = session.get('unlocked_rooms'))

@app.route('/puzzle3', methods=['GET', 'POST'])
def puzzle3():
    answer = request.form.get('answer')
    
    if answer == None:
        return render_template('puzzle3.html', unlocked_rooms = session.get('unlocked_rooms'))
    if answer.lower() == 'ggg':
        session['unlocked_rooms'].append('puzzle4')
        session.modified = True
        logging.debug(f"'puzzle4' added to unlocked_rooms. Updated session: {session}")
        return redirect(url_for('puzzle4'))
    else:
        return render_template('puzzle3.html', error="Incorrect answer. Try again.", unlocked_rooms = session.get('unlocked_rooms'))

@app.route('/puzzle4', methods=['GET', 'POST'])
def puzzle4():
    answer = request.form.get('answer')    

    if answer == None:
        return render_template('puzzle4.html', unlocked_rooms = session.get('unlocked_rooms'))
    if answer.lower() == 'red':
        session['unlocked_rooms'].append('puzzle5')
        session.modified = True
        logging.debug(f"'puzzle5' added to unlocked_rooms. Updated session: {session}")
        return redirect(url_for('puzzle5'))
    else:
        return render_template('puzzle4.html', error="Incorrect answer. Try again.", unlocked_rooms = session.get('unlocked_rooms'))

@app.route('/puzzle5', methods=['GET', 'POST'])
def puzzle5():
    answer = request.form.get('answer')
    
    if answer == None:
        return render_template('puzzle5.html', unlocked_rooms = session.get('unlocked_rooms'))
    
    if answer.lower() == 'joke':
        session['unlocked_rooms'].append('puzzle6')
        session.modified = True
        logging.debug(f"'puzzle6' added to unlocked_rooms. Updated session: {session}")
        return redirect(url_for('puzzle6'))
    else:
        return render_template('puzzle5.html', error="Incorrect answer. Try again.", unlocked_rooms = session.get('unlocked_rooms'))


@app.route('/puzzle6', methods=['GET', 'POST'])
def puzzle6():
    answer = request.form.get('answer')
    
    if answer == None:
        return render_template('puzzle6.html', unlocked_rooms = session.get('unlocked_rooms'))
    if answer.lower() == '24':
        session['unlocked_rooms'].append('congrats')
        session.modified = True
        return redirect(url_for('congrats'))
    else:
        return render_template('puzzle6.html', error="Incorrect answer. Try again.", unlocked_rooms = session.get('unlocked_rooms'))


@app.route('/congrats', methods=['GET', 'POST'])
def congrats():
    if 'congrats' not in session.get('unlocked_rooms', []):
        return redirect(url_for('index'))
    return render_template('congrats.html')


if __name__ == '__main__':
    app.run(debug=True)
