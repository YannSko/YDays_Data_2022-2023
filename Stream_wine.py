import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
data = pd.read_csv("wine.csv")








#__________________________________________________ Personnalisation de l'interface_______________________________________________________________
st.set_page_config(page_title="Cherche ton vin", page_icon=":wine_glass:", layout="wide")


st.markdown("<h1 style='text-align: center; color: black;'>Cherche ton vin Beau Gosse</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: black;'>Via le site Wine And Co : recherche ton type de vin en fonction des critères proposés!</p>", unsafe_allow_html=True)

#_____________________________________________Tableau de donnée avec filtre ______________________________________
st.subheader("Tableau de données")

# filtres en fonction critères appelation , couleur et région
appellations = sorted(data["appellation"].unique().tolist())
filtre_appellation = st.multiselect("Appellation", appellations)

couleurs = sorted(data["couleur"].unique().tolist())
filtre_couleur = st.multiselect("Couleur", couleurs)

regions = sorted(data["region"].unique().tolist())
filtre_region = st.multiselect("Région", regions)

# Filtrage de la dataframe
donnees_filtrees = data[(data["appellation"].isin(filtre_appellation)) &
                        (data["couleur"].isin(filtre_couleur)) &
                        (data["region"].isin(filtre_region))]

# Plot
st.dataframe(donnees_filtrees)


# _________________________________GRAPH 1  filtre par prix, couleur et appellation ______________________________
st.subheader("Filtre par prix, couleur et appellation")
couleurs = data["couleur"].unique()
appellations = data["appellation"].unique()
prix_min, prix_max = st.slider("Sélectionnez une plage de prix", float(data["price"].min()), data["price"].max(), (0.0, data["price"].max()))

couleur = st.selectbox("Sélectionnez une couleur", couleurs)
appellation = st.selectbox("Sélectionnez une appellation", appellations)
filtre_prix = (data["price"] >= prix_min) & (data["price"] <= prix_max)
filtre_couleur = data["couleur"] == couleur
filtre_appellation = data["appellation"] == appellation
donnees_filtrees = data[filtre_prix & filtre_couleur & filtre_appellation]

if not donnees_filtrees.empty:
    g = sns.catplot(data=donnees_filtrees, x="wine_name", y="price", kind="bar", height=5, aspect=3)
    fig = g.fig

    st.pyplot(fig)
else:
    st.warning("Aucun vin ne correspond à ces critères de sélection.")

#______________________________Graph2 filtre par culture et prix pour trouver l'appellation_______________________
st.subheader("Filtre par culture et prix pour trouver l'appellation")
cultures = data["culture"].unique()
prix_max = st.slider("Sélectionnez un prix maximum", data["price"].min(), data["price"].max(), data["price"].max())
culture = st.selectbox("Sélectionnez une culture", cultures)
filtre_prix = data["price"] <= prix_max
filtre_culture = data["culture"] == culture
donnees_filtrees = data[filtre_prix & filtre_culture]

if not donnees_filtrees.empty:
    appellations = donnees_filtrees["appellation"].unique()
    st.write("Les appellations correspondantes sont :", ", ".join(appellations))
else:
    st.warning("Aucun vin ne correspond à ces critères de sélection.")

#_____________________________________ Filtre couleur et cepage  > Obtention du prix ________________________________
def filter_data(df, couleur, cepage):
    filtered_data = df[(df["couleur"] == couleur) & (df["cepages"].str.contains(cepage))]
    return filtered_data


couleur_selectionnee = st.sidebar.selectbox("Sélectionnez une couleur :", options=["Blanc", "Rouge", "Rosé"])
cepage_selectionne = st.sidebar.selectbox("Sélectionnez un cépage :", options=data["cepages"].unique())

# Filtrer les données en fonctions selections
donnees_filtrees = filter_data(data, couleur_selectionnee, cepage_selectionne)

if not donnees_filtrees.empty:
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sns.barplot(data=donnees_filtrees, y="wine_name", x="price", palette="muted", ax=ax)
    
    ax.set_title(f"Prix des vins {couleur_selectionnee.lower()}s contenant du {cepage_selectionne}", fontsize=16)
    ax.set_xlabel("Prix (en euros)", fontsize=12)
    ax.set_ylabel("Nom du vin", fontsize=12)
    
    for i, p in enumerate(ax.patches):
        ax.annotate(f"{p.get_width():.2f}", (p.get_width() + 0.5, p.get_y() + 0.5))

    plt.tight_layout()
    plt.savefig("plot.png")
    st.image("plot.png", use_column_width=True)
else:
    st.warning("Aucun vin ne correspond à ces critères de sélection.")


