import csv
from faker import Faker
import random
from datetime import date, timedelta

fake = Faker()
dataset = []

old_mm_values = [100, 150, 200, 250, 300]
today = date.today()

for _ in range(1000):
    name = fake.name()
    phone = ""
    old_mm = random.choice(old_mm_values)
    new_mm = old_mm + random.choice([50, 100])
    
    start_date = today - timedelta(days=90) 
    end_date = today
    date = fake.date_between(start_date=start_date, end_date=end_date) #Gera os dados fictícios pros últimos 3 meses até hoje.


    if random.random() < 0.75:
        delivery_date = fake.date_between(start_date=date, end_date=end_date)
        delivery_state = random.choice(["Feito", "Entregue"])
    else:
        delivery_date = None
        delivery_state = "Em Producao"


    dataset.append([name, phone, old_mm, new_mm, date, delivery_date, delivery_state])

filename = "dataset.csv"

with open(filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["name", "phone", "old_mm", "new_mm", "date", "delivery_date", "delivery_state"])  # Cabeçalho
    writer.writerows(dataset)

print(f"Dados escritos com sucesso no arquivo '{filename}'.")