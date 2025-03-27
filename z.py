import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Analyse des Ventes - Beans & Pods")
st.write("Bienvenue sur l'application interactive d'analyse des ventes. Téléchargez votre fichier CSV pour commencer !")

fichier = st.file_uploader("Téléchargez un fichier CSV", type=["csv"])

if fichier is not None:
    try:
        # Charger les données
        data = pd.read_csv(fichier, encoding='utf-8')  
        st.success("Fichier chargé avec succès !")
    except :
        st.error("Une erreur s'est produite lors du chargement du fichier")
        st.stop()  
    data.columns = data.columns.str.strip()  

    colonnes_attendues = ['Channel', 'Region', 'Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']
   
    peek=data.head()
    st.subheader(" Aperçu des données")
    st.dataframe(peek)

    st.sidebar.header("Filtres")
    canal = st.sidebar.selectbox("Sélectionner un canal", data["Channel"].unique())
    regions = st.sidebar.multiselect(
        "Sélectionner les régions", 
        data["Region"].unique() if 'Region' in data.columns else ["Toutes"], 
        default=data["Region"].unique() if 'Region' in data.columns else ["Toutes"]
    )

    if 'Region' in data.columns:
        filtered_data = data[(data["Channel"] == canal) & (data["Region"].isin(regions))]
    else:
        filtered_data = data[data["Channel"] == canal]

    st.subheader(f" Données filtrées ({canal})")
    st.dataframe(filtered_data)

    st.subheader("Ventes totales par produit")
    produits_disponibles = [col for col in colonnes_attendues[2:] if col in data.columns]
    ventes_produits = filtered_data[produits_disponibles].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=ventes_produits.index, y=ventes_produits.values, palette="magma", ax=ax)
    ax.set_title("Produits les plus vendus")
    ax.set_xlabel("Produits")
    ax.set_ylabel("Total des ventes")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    
    st.subheader(" Comparaison des ventes par Canal (Store vs Online)")
    ventes_par_canal = data.groupby("Channel").sum(numeric_only=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    ventes_par_canal.T.plot(kind="bar", colormap="viridis", edgecolor="black", ax=ax)
    ax.set_title("Ventes par Canal")
    ax.set_xlabel("Produits")
    ax.set_ylabel("Nombre de ventes")
    st.pyplot(fig)

    if 'Region' in data.columns:
        st.subheader(" Comparaison des ventes par Région")
        ventes_par_region = data.groupby("Region").sum(numeric_only=True)

        fig, ax = plt.subplots(figsize=(10, 5))
        ventes_par_region.T.plot(kind="bar", colormap="coolwarm", edgecolor="black", ax=ax)
        ax.set_title("Ventes par Région")
        ax.set_xlabel("Produits")
        ax.set_ylabel("Nombre de ventes")
        st.pyplot(fig)
    else:
        st.warning("La comparaison des ventes par région n'est pas possible (colonne absente).")
     

    if 'Region' in data.columns:
        st.subheader(" Produits populaires par Région et Canal")

        ventes_par_region_canal = data.groupby(["Region", "Channel"])[produits_disponibles].sum()

        recommandations = []
        for (region, channel), ventes in ventes_par_region_canal.iterrows():
            produit_populaire = ventes.idxmax()
            recommandations.append(f" **Dans la région {region}, via {channel}, le produit le plus vendu est {produit_populaire}.**")

        for reco in recommandations:
            st.write(reco)

    st.subheader(" Recommandations Marketing")
    st.write("""
    -  **Publicité ciblée** : Mettre en avant les produits les plus populaires dans chaque région via des campagnes publicitaires locales.
    -  **Gestion des stocks** : Adapter l’inventaire en fonction des tendances de vente observées par canal et par région.
    -  **Offres promotionnelles** : Proposer des réductions sur les produits moins vendus pour équilibrer les ventes.
    -  **Optimisation des canaux de vente** : Renforcer les campagnes en ligne si certains produits se vendent mieux sur le web que dans les magasins physiques.
    """)

    

else:
    st.info("Veuillez télécharger un fichier CSV pour commencer l'analyse.")





