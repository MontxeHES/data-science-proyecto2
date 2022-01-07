import pandas as pd
import math

#Se emplea la funcion read_csv de pandas
df = pd.read_csv("synergy_logistics_database.csv")
df["route"] = df[["origin", "destination"]].apply(lambda x: "-".join(x), axis=1)
df["country"] = df[["origin", "destination", "direction"]].apply(lambda x: x[1] if x[2] == "Exports" else x[0] , axis=1)

#df.head()
#print(df[df["direction"] == "Imports"].head())
#print(df.shape)
#print(df.describe())

#Se prosigue a obtener un dos def, en donde las funciones son nombradas como "total_value" y "market_share" y en los cuales se enlistan 4 o mas argumentos
def top_values(
            df, 
            top, 
            group_column, 
            acc_column,
            filter_column=None, 
            filter_value=None
):
    if filter_column and filter_value:
        df =  df[df[filter_column] == filter_value]
    df_total = df.groupby(group_column)[[acc_column]].sum().reset_index()
    return df_total.nlargest(top, acc_column)

def market_share(
                df, 
                group_column, 
                acc_column, 
                percent
):
    df_sorted = df.groupby(group_column)[acc_column].sum().sort_values(ascending=False).reset_index()
    df_sorted["cum_percent"] = 100*(df_sorted[acc_column].cumsum()/df_sorted[acc_column].sum())
    df_sorted["cum_percent"] = df_sorted["cum_percent"].apply(lambda x: math.ceil(x / 10) * 10)
    return df_sorted[df_sorted["cum_percent"] <= percent]

# Analisis opcion 1 rutas
#Se procede a encontrar las 10 mejores rutas, primero a nivel general y luego entre las exportaciones e importaciones
df_top_routes_fn = top_values(df, 10, "route", "total_value")
df_top_routes_fn_x = top_values(df, 10, "route", "total_value", 
"direction", "Exports")
df_top_routes_fn_i = top_values(df, 10, "route", "total_value", "direction", "Imports")

print(df_top_routes_fn)
print(df_top_routes_fn_x)
print(df_top_routes_fn_i)

# Analisis opcion 2 tipo de transporte
#A continuacion se busca el top 3 de los medios de transporte en general y posteriormente para las exportaciones e importaciones
df_top_transport_fn = top_values(df, 3, "transport_mode", "total_value")
df_top_transport_fn_x = top_values(df, 3, "transport_mode", "total_value", "direction", "Exports")
df_top_transport_fn_i = top_values(df, 3, "transport_mode", "total_value", "direction", "Imports")

print(df_top_transport_fn)
print(df_top_transport_fn_x)
print(df_top_transport_fn_i)

# Analisis opcion 3 valor de las exportaciones
#A continuacion se buscaran los paises que generen el 80% de los flujos entre las exportaciones e importaciones
df_cumsum_country_fn = market_share(df, "destination", "total_value", 80)

print(df_cumsum_country_fn)