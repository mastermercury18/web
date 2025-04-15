import matplotlib.pyplot as plt
import sqlite3
import numpy as np
import mpld3
import os
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.tsa.arima.model import ARIMA
from flask import Flask, render_template, make_response, request, redirect, url_for, jsonify

ACF_lags = dict()
arima_order = dict()
normal_test = dict()
durbin_watson = dict()

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    string_cookie = request.cookies.get('user_logged_in')
    if (string_cookie == "True") :
        logged_in = True
    else :
        logged_in = False

    # PREPARE PAGE
    if (logged_in) :
        resp = make_response( render_template('index.html') )
    else :
        resp = make_response( render_template('logged_in_false.html') )
    resp.set_cookie('user_logged_in', str(logged_in))
    return resp

@app.route('/login', methods=['GET', 'POST'])
def login_processor():
  resp = make_response(redirect(url_for('home')))
  resp.set_cookie('user_logged_in', "True")
  return resp

@app.route('/logout')
def logout_processor():

  resp = make_response(redirect(url_for('home')))
  resp.set_cookie('user_logged_in', "False")
  return resp

data_options = {
    "Sunspot Data": "sunspot.html",
    "Nile Data": "nile.html",
    "Qubit Data": "qubit.html"
}

# Load Sunspot Data
sun_dta = sm.datasets.sunspots.load_pandas().data
sun_dta.index = pd.Index(sm.tsa.datetools.dates_from_range("1700", "2008"))
sun_dta.index.freq = sun_dta.index.inferred_freq
del sun_dta["YEAR"]

# Create Sunspot Plot
fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(sun_dta.values.squeeze(), lags=200, ax=ax1)

arma_mod = ARIMA(sun_dta, order=(3, 0, 0)).fit()
fig2 = plt.figure(figsize=(12, 8))
ax2 = fig2.add_subplot(111)
ax2 = arma_mod.resid.plot(ax=ax2)

# Dictionary  
ACF_lags["Sunspot"] = 200
arima_order["Sunspot"] = 3
normal_test["Sunspot"] = stats.normaltest(arma_mod.resid)
durbin_watson["Sunspot"] = sm.stats.durbin_watson(arma_mod.resid.values)

# Save Sunspot Plot
html_file = os.path.join("static", "sunspot.html")
with open(html_file, "w") as f:
    f.write(mpld3.fig_to_html(fig))
    f.write(mpld3.fig_to_html(fig2))

#Load Nile River Data
nile_dta = sm.datasets.nile.load_pandas().data.volume

# Create Nile Plot
fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(nile_dta.values.squeeze(), lags=90, ax=ax1)

arma_mod = ARIMA(nile_dta, order=(10, 0, 0)).fit()
fig2 = plt.figure(figsize=(12, 8))
ax2 = fig2.add_subplot(111)
ax2 = arma_mod.resid.plot(ax=ax2)

# Dictionary 
ACF_lags["Nile"] = 90
arima_order["Nile"] = 10
normal_test["Nile"] = stats.normaltest(arma_mod.resid)
durbin_watson["Nile"] = sm.stats.durbin_watson(arma_mod.resid.values)

# Save Nile Plot
html_file = os.path.join("static", "nile.html") # Looked this up
with open(html_file, "w") as f:
    f.write(mpld3.fig_to_html(fig))
    f.write(mpld3.fig_to_html(fig2))

# Load Qubit Data
coherence_times = [2.4057736649510563e-05, 2.18482485807106e-05, 2.6641319587831166e-05, 2.2827785269471553e-05, 2.356049404484696e-05, 2.3565073584033854e-05, 2.5791365925555306e-05, 2.6004792675055962e-05, 2.7338710513028527e-05, 2.569945382407464e-05, 2.9530260467683714e-05, 2.9993623654710115e-05, 2.75964701162354e-05, 2.8268740580420686e-05, 3.145119957955423e-05, 3.0149201617319098e-05, 2.640058048389081e-05, 3.098115973839775e-05, 3.216372434909371e-05, 3.131043335112776e-05, 2.881944221522125e-05, 2.722689826096605e-05, 2.758763656307149e-05, 2.7876026999597062e-05, 2.6233057422252945e-05, 3.0236662284756008e-05, 2.6692254106895503e-05, 3.209155946787704e-05, 2.8057824852528934e-05, 2.7116190595395236e-05, 2.9410813476633505e-05, 2.4612693838197994e-05, 2.9247550342495855e-05, 3.132564234914013e-05, 3.210769778359254e-05, 3.1151229481699865e-05, 2.9296196485652356e-05, 2.9475514065225156e-05, 3.2970984877808185e-05, 3.172751336996069e-05, 2.7905134009915023e-05, 2.742054108909934e-05, 2.578038458299001e-05, 2.9845007079946194e-05, 3.0809733292251914e-05, 3.023751525790923e-05, 2.6794677105537964e-05, 1.879531349466416e-05, 2.2890188200123e-05, 2.5841183913501052e-05, 2.815717101706527e-05, 2.552288861075037e-05, 3.317572111322395e-05, 2.1578516565062622e-05, 2.7031006044127807e-05, 3.0780953321576e-05, 2.921743078801677e-05, 2.306898453445079e-05, 2.3680778692714632e-05, 2.543320275323522e-05, 2.15604479571535e-05, 2.1717182903301156e-05, 1.3069738463857753e-05, 2.860789748117498e-05, 1.989344453667808e-05, 2.3634712797370493e-05, 2.358262330874879e-05, 1.9515065304927636e-05, 2.3877170082487857e-05, 2.1841721228143658e-05, 1.9569975478150562e-05, 2.340955193681317e-05, 2.8825669858424364e-05, 2.9052503549924525e-05, 2.8163793353390552e-05, 2.8729847270744547e-05, 2.0956133553036852e-05, 2.5018740672193557e-05, 2.2633223215421897e-05, 2.711854383424664e-05, 3.222337972897021e-05, 2.1682990730414706e-05, 3.3644702056930154e-05, 2.8426205706993464e-05, 3.12405404598026e-05, 2.2895093974658977e-05, 3.224407262397809e-05, 3.242657925402749e-05, 3.260512276071194e-05, 3.1753082218303874e-05, 3.2622924062611044e-05, 3.0790176144499196e-05, 3.088209027081803e-05, 2.791476343168018e-05, 2.2729182992665815e-05, 2.5336532479556503e-05, 2.8739834031385537e-05, 3.296842201377293e-05, 2.9441264359029054e-05, 3.280820069906201e-05, 3.137717753868018e-05, 2.9608853102215665e-05, 2.983692279195728e-05, 3.221319477096681e-05, 2.7276308344052457e-05, 2.9601898526963e-05, 2.9766325645637913e-05, 3.1595188684098936e-05, 2.6806303769081534e-05, 2.4919995922136982e-05, 3.307711394182265e-05, 2.8467572121357102e-05, 3.009766128102996e-05, 2.876394771827477e-05, 2.710725202187219e-05, 2.5523348093665118e-05, 3.1016789547962074e-05, 2.58158021938102e-05, 2.3952919573917945e-05, 3.137741976488344e-05, 3.100267757716924e-05, 2.5251749585478712e-05, 2.9164019391300195e-05, 3.157151674468989e-05, 2.630444625416997e-05, 2.597874432613692e-05, 2.6138136851748344e-05, 2.5488741207984828e-05, 2.4674401369646318e-05, 2.5388375044840444e-05, 2.678446438563697e-05, 2.8838587695541724e-05, 2.1971384674760138e-05, 2.684369424052469e-05, 2.5925879063669384e-05, 2.5503566989938774e-05, 2.2917715241483113e-05, 2.9175315027360048e-05, 2.9033766876842303e-05, 2.2629719334199614e-05, 2.7148939524169802e-05, 2.0055538002954514e-05, 2.807375106221161e-05, 3.0371313669670456e-05, 2.980428140990267e-05, 2.8989760191894967e-05, 2.0240811233176838e-05, 2.73119129680869e-05, 2.2481921484802384e-05, 2.190507628129518e-05, 3.0032701812955505e-05, 2.7565753604337294e-05, 2.526727218683769e-05, 2.351133438472458e-05, 2.820026071970848e-05, 2.9520148189340206e-05, 3.0920604818029625e-05, 2.9723766065874368e-05, 2.6335144237104537e-05, 2.8841470913556397e-05, 2.8688112390875114e-05, 2.5547556450496793e-05, 2.4783697581653628e-05, 2.5151567082492384e-05, 2.4303622608271316e-05, 2.109672886095694e-05, 2.2062424354889064e-05, 2.5823584722769657e-05, 2.988370524492285e-05]
times = np.array(list(range(0, len(coherence_times), 1)))
qubit_dta = pd.DataFrame({'Iterations': times, 'Coherence Times': coherence_times})['Coherence Times']

# Create Qubit Plot
fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(qubit_dta.values.squeeze(), lags=50, ax=ax1)

arma_mod = ARIMA(nile_dta, order=(4, 0, 0)).fit()
fig2 = plt.figure(figsize=(12, 8))
ax2 = fig2.add_subplot(111)
ax2 = arma_mod.resid.plot(ax=ax2)

# Dictionary 
ACF_lags["Qubit"] = 50
arima_order["Qubit"] = 4
normal_test["Qubit"] = stats.normaltest(arma_mod.resid)
durbin_watson["Qubit"] = sm.stats.durbin_watson(arma_mod.resid.values)

# Save Qubit Plot
html_file = os.path.join("static", "qubit.html") # Looked this up
with open(html_file, "w") as f:
    f.write(mpld3.fig_to_html(fig))
    f.write(mpld3.fig_to_html(fig2))


@app.route('/redirect', methods=['POST'])
def handle_redirect():
    if request.method == 'POST':
        answer = request.form.get('answer')
        if answer in data_options:
            return redirect(url_for('static', filename=data_options[answer]))
    return render_template("index.html")  

# Dictionary 
def init_db():
    conn = sqlite3.connect("timeseries.db")
    cursor = conn.cursor()

    # Create Table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TimeSeriesMetrics (
            Metric TEXT PRIMARY KEY,
            Sunspot REAL,
            Nile REAL,
            Qubit REAL
        )
    ''')
    
    conn.commit()
    conn.close()

# Database
def insert_metrics():
    conn = sqlite3.connect("timeseries.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM TimeSeriesMetrics")

    data = {
        "ACF_lags": (ACF_lags.get("Sunspot"), ACF_lags.get("Nile"), ACF_lags.get("Qubit")),
        "ARIMA_order": (arima_order.get("Sunspot"), arima_order.get("Nile"), arima_order.get("Qubit")),
        "normal_test": (normal_test.get("Sunspot")[0], normal_test.get("Nile")[0], normal_test.get("Qubit")[0]),
        "durbin_watson": (durbin_watson.get("Sunspot"), durbin_watson.get("Nile"), durbin_watson.get("Qubit"))
    }

    for metric, values in data.items():
        cursor.execute(
            "INSERT INTO TimeSeriesMetrics (Metric, Sunspot, Nile, Qubit) VALUES (?, ?, ?, ?)",
            (metric, values[0], values[1], values[2])
        )

    conn.commit()
    conn.close()

@app.route('/metrics', methods=['GET'])
def get_metrics():
    conn = sqlite3.connect("timeseries.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TimeSeriesMetrics")
    rows = cursor.fetchall()
    conn.close()

    results = {}

    for row in rows:
        key = row[0]
        results[key] = {"Sunspot": row[1], "Nile": row[2], "Qubit": row[3]}
    return jsonify(results)

if __name__ == '__main__':
    init_db() 
    insert_metrics()  
    app.run(debug=True)  