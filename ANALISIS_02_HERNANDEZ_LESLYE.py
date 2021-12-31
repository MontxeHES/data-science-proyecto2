import pandas as pd
import math

df = pd.read_csv("synergy_logistics_database.csv")
df["route"] = df[["origin", "destination"]].apply(lambda x: "-".join(x), axis=1)
df["country"] = df[["origin", "destination", "direction"]].apply(lambda x: x[1] if x[2] == "Exports" else x[0] , axis=1)

#df.head()
#print(df[df["direction"] == "Imports"].head())
#print(df.shape)
#print(df.describe())


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
df_top_routes_fn = top_values(df, 10, "route", "total_value")
df_top_routes_fn_x = top_values(df, 10, "route", "total_value", 
"direction", "Exports")
df_top_routes_fn_i = top_values(df, 10, "route", "total_value", "direction", "Imports")


# Analisis opcion 2 tipo de transporte
df_top_transport_fn = top_values(df, 3, "transport_mode", "total_value")
df_top_transport_fn_x = top_values(df, 3, "transport_mode", "total_value", "direction", "Exports")
df_top_transport_fn_i = top_values(df, 3, "transport_mode", "total_value", "direction", "Imports")

#print(df_top_transport_i)

# Analisis opcion 3 valor de las exportaciones
df_cumsum_country_fn = market_share(df, "destination", "total_value", 80)
print(df_cumsum_country_fn)