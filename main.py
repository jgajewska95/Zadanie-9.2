import requests
import csv
from flask import Flask, render_template, request

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

rates = data[0]['rates']

with open('rates.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=';')

    writer.writerow(['Nazwa', 'kod', 'Cena zakupu', 'Cena sprzedaży'])

    currencies_codes = []
    for rate in rates:
        writer.writerow([rate['currency'], rate['code'], rate['bid'], rate['ask']])
        currencies_codes.append(rate['code'])

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        money = request.form.get('money')
        currency = request.form.get('currency')
        rate_value = 1
        for rate in rates:
            if rate['code'] == currency:
                rate_value = rate['bid']
                break
        result = float(money) * rate_value
        return render_template("index.html", currencies=currencies_codes, result=result)
    else:
        return render_template("index.html", currencies=currencies_codes)


if __name__ == "__main__":
    app.run(debug=True)