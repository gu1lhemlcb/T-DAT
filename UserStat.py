import pandas as pd
import math
import sys
import json

if len(sys.argv) != 2:
    print('Client ID must be given as argument')
    quit()

client_id = str(sys.argv[1])

if (client_id.isnumeric() == False):
    print('Invalid client ID given as argument')
    quit()

print ("Client ID: " + client_id)

data = pd.read_csv('./KaDo.csv')
df = data.copy()
df = df.query('CLI_ID == '+  client_id) # 997385337

if (df.shape[0] == 0):
    print('No available data on this client')
    quit()

stats = {"user": client_id, "stats" : {}}

# NB achats total par MAILLE
print("Nb achats total par MAILLE: \n", df['MAILLE'].value_counts().to_frame(), "\n")
sales_per_maille_data = {}
sales_per_maille_count = df['MAILLE'].value_counts()
for idx, val in zip(sales_per_maille_count.index, sales_per_maille_count.values):
    sales_per_maille_data[idx] = int(val)

stats["stats"]["SALES_PER_MAILLE"] = {"title" : "Nb achats total par MAILLE", "data" : sales_per_maille_data}

# NB achats total par FAMILLE
print("Nb achats total par FAMILLE: \n", df['FAMILLE'].value_counts().to_frame(), "\n")

sales_per_famille_data = {}
sales_per_famille_count = df['FAMILLE'].value_counts()
for idx, val in zip(sales_per_famille_count.index, sales_per_famille_count.values):
    sales_per_famille_data[idx] = int(val)

stats["stats"]["SALES_PER_FAMILLE"] = {"title" : "Nb achats total par FAMILLE", "data" : sales_per_famille_data}

# NB achats total par MOIS
sales_count = df['MOIS_VENTE'].value_counts()
months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Décembre"]
sales_per_months_data = {"Janvier" : 0, "Février" : 0, "Mars" : 0, "Avril" : 0, "Mai" : 0, "Juin" : 0, "Juillet" : 0, "Aout" : 0, "Septembre" : 0, "Octobre" : 0, "Novembre" : 0, "Décembre" : 0}

for idx, val in zip(sales_count.index, sales_count.values):
    sales_per_months_data[months[idx - 1]] = int(val)

print("Nb achats total par MOIS:")
for month in sales_per_months_data:
    print(month + "\t\t" + str(sales_per_months_data[month]))
stats["stats"]["SALES_PER_MONTH"] = {"title" : "Nb achats total par MOIS", "data" : sales_per_months_data}

# Prix par mois

price_per_month_df = df.copy()
to_drop = ['TICKET_ID', 'MAILLE', 'FAMILLE', 'UNIVERS', 'LIBELLE', 'CLI_ID']
price_per_month_df.drop(to_drop, inplace=True, axis=1)

print("\nDépenses totales:" + str(round(price_per_month_df["PRIX_NET"].sum(), 2)))
stats["stats"]["TOTAL_SPENT"] = {"title" : "Dépenses totales", "data" : round(price_per_month_df["PRIX_NET"].sum(), 2)}

money_per_months_data = {}
print("\nDépenses moyennes par MOIS:")
for month in range(1, 13):
    quantity = price_per_month_df.query('MOIS_VENTE == ' + str(month))["PRIX_NET"].sum()
    money_per_months_data[months[month - 1]] = (0 if math.isnan(quantity) else round(quantity, 2))
    print(months[month - 1] + "\t\t" + str(0 if math.isnan(quantity) else round(quantity, 2)))

stats["stats"]["SPENT_PER_MONTH"] = {"title" : "Dépenses moyennes par MOIS", "data" : money_per_months_data}

# Ticket ID / par mois et total

nb_sales_df = df.copy()
to_drop = ['MAILLE', 'FAMILLE', 'UNIVERS', 'LIBELLE', 'CLI_ID']
nb_sales_df.drop(to_drop, inplace=True, axis=1)
print("\nNb d'achats:")
print(nb_sales_df["TICKET_ID"].value_counts().sum())
stats["stats"]["ARTICLES_SOLD"] = {"title" : "Nb d'achats", "data" : int(nb_sales_df["TICKET_ID"].value_counts().sum())}

print("Nb de commande total:")
print(nb_sales_df["TICKET_ID"].value_counts().count())
stats["stats"]["TOTAL_ORDER"] = {"title" : "Nb de commande total", "data" : int(nb_sales_df["TICKET_ID"].value_counts().count())}

order_per_months_data = {}
print("\nNb de commande par MOIS:")
for month in range(1, 13):
    quantity = nb_sales_df.query('MOIS_VENTE == ' + str(month))["TICKET_ID"].value_counts().count()
    order_per_months_data[months[month - 1]] = (0 if math.isnan(quantity) else int(quantity))
    print(months[month - 1] + "\t\t" + str(0 if math.isnan(quantity) else quantity))

stats["stats"]["ORDER_PER_MONTH"] = {"title" : "Nb de commande par MOIS", "data" : order_per_months_data}

# Panier par mois et total

print("\nPrix du panier moyen:")
print(round(nb_sales_df.groupby('TICKET_ID')["PRIX_NET"].sum().mean(), 2))
stats["stats"]["AVERAGE_CART"] = {"title" : "Prix du panier moyen", "data" : round(nb_sales_df.groupby('TICKET_ID')["PRIX_NET"].sum().mean(), 2)}

cart_per_months_data = {}
print("\nPrix du panier moyen par MOIS:")
for month in range(1, 13):
    quantity = nb_sales_df.query('MOIS_VENTE == ' + str(month)).groupby('TICKET_ID')["PRIX_NET"].sum().mean()
    cart_per_months_data[months[month - 1]] = (0 if math.isnan(quantity) else round(quantity, 2))
    print(months[month - 1] + "\t\t" + str(0 if math.isnan(quantity) else round(quantity, 2)))

stats["stats"]["AVERAGE_CART_PER_MONTH"] = {"title" : "Prix du panier moyen par MOIS", "data" : cart_per_months_data}

# PRIX_NET total par MAILLE par mois
row = df.groupby(['MAILLE', 'MOIS_VENTE']).sum()['PRIX_NET'].unstack()
newCols = []
for idx in row.columns.values:
    newCols.append(months[idx - 1])
row.columns = newCols
for col in months:
    if col not in row.keys():
        row[col] = 0
row = row.reindex(columns=months)
row = row.fillna(0)
print("\nPRIX_NET total par MAILLE par mois.\n", row)
print("\n")

stats["stats"]["SPENT_PER_MAILLE_PER_MONTH"] = {"title" : "PRIX_NET total par MAILLE par MOIS", "data" : json.loads(row.to_json(orient="index"))}

# PRIX_NET par FAMILLE par mois
print("\n")
row = df.groupby(['FAMILLE', 'MOIS_VENTE']).sum()['PRIX_NET'].unstack()
newCols = []
for idx in row.columns.values:
    newCols.append(months[idx - 1])
row.columns = newCols
for col in months:
    if col not in row.keys():
        row[col] = 0
row = row.reindex(columns=months)
row = row.fillna(0)
print("PRIX_NET par FAMILLE par mois.\n", row)
stats["stats"]["SPENT_PER_FAMILLE_PER_MONTH"] = {"title" : "PRIX_NET total par FAMILLE par MOIS", "data" : json.loads(row.to_json(orient="index"))}

print("\n")

# nombre de MAILLE par mois
print("\n")
row = df.groupby(['MAILLE', 'MOIS_VENTE']).count()['TICKET_ID'].unstack()
newCols = []
for idx in row.columns.values:
    newCols.append(months[idx - 1])
row.columns = newCols
for col in months:
    if col not in row.keys():
        row[col] = 0
row = row.reindex(columns=months)
row = row.fillna(0)
print("nombre de MAILLE par mois.\n", row)
stats["stats"]["SALES_PER_MAILLE_PER_MONTH"] = {"title" : "Nb d'achats par MAILLE par MOIS", "data" : json.loads(row.to_json(orient="index"))}
print("\n")

# nombre de FAMILLE par mois
print("\n")
row = df.groupby(['FAMILLE', 'MOIS_VENTE']).count()['TICKET_ID'].unstack()
newCols = []
for idx in row.columns.values:
    newCols.append(months[idx - 1])
row.columns = newCols
for col in months:
    if col not in row.keys():
        row[col] = 0
row = row.reindex(columns=months)
row = row.fillna(0)
print("nombre de FAMILLE par mois.\n", row)
stats["stats"]["SALES_PER_FAMILLE_PER_MONTH"] = {"title" : "Nb d'achats par FAMILLE par MOIS", "data" : json.loads(row.to_json(orient="index"))}
print("\n")

jsonData = json.dumps(stats, indent=4)
with open('./front-user-stat/public/stats.json', 'w') as writer:
    writer.write(jsonData)