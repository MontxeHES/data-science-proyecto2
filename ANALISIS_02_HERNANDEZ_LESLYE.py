import pandas as pd

df = pd.read_csv("synergy_logistics_database.csv")
df["route"] = df[["origin", "destination"]].apply(lambda x: "-".join(x), axis=1)
df["country"] = df[["origin", "destination", "direction"]].apply(lambda x: x[1] if x[2] == "Exports" else x[0] , axis=1)

#df.head()
#print(df[df["direction"] == "Imports"].head())
#print(df.shape)
#print(df.describe())

# Analisis opcion 1 rutas
df_total_routes = df.groupby("route")[["total_value"]].sum().reset_index()
df_top_routes = df_total_routes.nlargest(10, "total_value")


df_total_routes_x = df[df["direction"] == "Exports"].groupby("route")[["total_value"]].sum().reset_index()
df_top_routes_x = df_total_routes_x.nlargest(10, "total_value")


df_total_routes_i = df[df["direction"] == "Imports"].groupby("route")[["total_value"]].sum().reset_index()
df_top_routes_i = df_total_routes_i.nlargest(10, "total_value")
#print(df_top_routes)
#print(df_top_routes_x)
#print(df_top_routes_i)


# Analisis opcion 2 tipo de transporte
df_total_transport = df.groupby("transport_mode")[["total_value"]].sum().reset_index()
df_top_transport = df_total_transport.nlargest(3, "total_value")


df_total_transport_x = df[df["direction"] == "Exports"].groupby("transport_mode")[["total_value"]].sum().reset_index()
df_top_transport_x = df_total_transport_x.nlargest(3, "total_value")


df_total_transport_i = df[df["direction"] == "Imports"].groupby("transport_mode")[["total_value"]].sum().reset_index()
df_top_transport_i = df_total_transport_i.nlargest(3, "total_value")

#print(df_top_transport)
#print(df_top_transport_x)
#print(df_top_transport_i)

# Analisis opcion 3 valor de las exportaciones
df_cumsum_country = df.groupby("destination")["total_value"].sum().sort_values(ascending=False).reset_index()
#print(df_cumsum_country)

df_cumsum_country["cum_percent"] = 100*(df_cumsum_country["total_value"].cumsum()/df_cumsum_country["total_value"].sum())
print(df_cumsum_country)