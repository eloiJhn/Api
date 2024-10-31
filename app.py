from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import calendar
import holidays

app = Flask(__name__)
CORS(app)

# Liste des noms de jours de la semaine en français
week_days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

# Fonction pour obtenir le nombre de jours et les informations de chaque jour pour un mois donné dans une année donnée
def get_days_with_weekdays(year):
    days_per_month = []
    for month in range(1, 13):
        month_name = calendar.month_name[month]
        days_in_month = calendar.monthrange(year, month)[1]
        
        days_with_weekdays = []
        for day in range(1, days_in_month + 1):
            date = datetime(year, month, day)
            day_info = {
                "date": date.strftime("%Y-%m-%d"),
                "weekday": week_days[date.weekday()]  # Récupère le nom du jour de la semaine
            }
            days_with_weekdays.append(day_info)
        
        days_per_month.append({"name": month_name, "days": days_with_weekdays})
    return days_per_month

# Fonction pour obtenir les jours fériés pour chaque mois dans une année donnée (France)
def get_holidays_by_month(year):
    french_holidays = holidays.France(years=year)
    holidays_per_month = {i: [] for i in range(1, 13)}
    for date, name in french_holidays.items():
        month_index = date.month
        holidays_per_month[month_index].append({"date": date.strftime("%Y-%m-%d"), "name": name})
    return holidays_per_month

# Route principale pour récupérer les informations complètes des jours et jours fériés
@app.route('/days_per_month', methods=['GET'])
def days_per_month():
    year = request.args.get('year', default=datetime.now().year, type=int)
    
    # Récupère les informations des jours pour chaque mois avec les jours de la semaine
    days = get_days_with_weekdays(year)
    holidays = get_holidays_by_month(year)
    
    # Ajoute les jours fériés dans les données de chaque mois
    for month in days:
        month_index = list(calendar.month_name).index(month["name"])
        month["holidays"] = holidays[month_index]
    
    # Retourne le résultat en JSON avec les mois en ordre
    result = {
        "year": year,
        "months": days
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
