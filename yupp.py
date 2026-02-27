import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Configuration de la page
st.set_page_config(page_title="Statisticien Genius Sports", layout="wide")
st.title("📝 Outil de collecte de données sportives")
st.markdown("---")

# Informations du match (À remplir avant de commencer)
with st.expander("📋 Informations du match", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        match_id = st.text_input("ID du match", "SEN_CIV_20260226")
    with col2:
        competition = st.text_input("Compétition", "Éliminatoires Coupe du Monde FIBA 2027")
    with col3:
        date_match = st.date_input("Date", datetime.now())
    
    col1, col2 = st.columns(2)
    with col1:
        equipe_domicile = st.text_input("Équipe domicile", "Sénégal")
    with col2:
        equipe_exterieur = st.text_input("Équipe extérieur", "Côte d'Ivoire")

# Initialisation des données
if 'actions' not in st.session_state:
    st.session_state.actions = []
    st.session_state.score_domicile = 0
    st.session_state.score_exterieur = 0

# Interface de saisie (3 colonnes pour plus d'options)
st.subheader("➕ Enregistrer une action")
col1, col2, col3, col4 = st.columns(4)

with col1:
    minute = st.number_input("Minute", 1, 120, 1)
    seconde = st.number_input("Seconde", 0, 59, 0)

with col2:
    equipe = st.selectbox("Équipe", [equipe_domicile, equipe_exterieur])
    
with col3:
    type_action = st.selectbox(
        "Action",
        ["Tir", "Tir cadré", "But", "Faute", "Carton jaune", 
         "Carton rouge", "Corner", "Hors-jeu", "Arrêt", "Remplacement"]
    )

with col4:
    joueur = st.text_input("Joueur", "")
    # Boutons rapides pour actions courantes
    st.caption("Actions rapides:")

# Actions rapides en dessous
col_rapide1, col_rapide2, col_rapide3, col_rapide4 = st.columns(4)
with col_rapide1:
    if st.button("⚽ But"):
        action_rapide = "But"
with col_rapide2:
    if st.button("🟨 Carton jaune"):
        action_rapide = "Carton jaune"
with col_rapide3:
    if st.button("🔄 Remplacement"):
        action_rapide = "Remplacement"
with col_rapide4:
    if st.button("⏱️ Mi-temps"):
        action_rapide = "Mi-temps"

# Bouton d'ajout principal
if st.button("➕ Enregistrer l'action", type="primary"):
    action = {
        'match_id': match_id,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'minute': f"{minute}:{seconde:02d}",
        'equipe': equipe,
        'action': type_action,
        'joueur': joueur if joueur else "Non spécifié"
    }
    st.session_state.actions.append(action)
    st.success(f"✅ Action enregistrée : {type_action} à la {minute}'{seconde:02d}")
    
    # Mise à jour automatique du score
    if type_action == "But":
        if equipe == equipe_domicile:
            st.session_state.score_domicile += 1
        else:
            st.session_state.score_exterieur += 1

# Affichage du score en direct
st.markdown("---")
col_score1, col_score2, col_score3 = st.columns(3)
with col_score1:
    st.markdown(f"## 🏠 {equipe_domicile}")
with col_score2:
    st.markdown(f"## {st.session_state.score_domicile} - {st.session_state.score_exterieur}")
with col_score3:
    st.markdown(f"## {equipe_exterieur} ✈️")

# Résumé et statistiques
if st.session_state.actions:
    st.subheader("📊 Statistiques du match")
    df = pd.DataFrame(st.session_state.actions)
    
    # Filtres
    col1, col2 = st.columns(2)
    with col1:
        equipe_filter = st.multiselect("Filtrer par équipe", df['equipe'].unique(), default=df['equipe'].unique())
    with col2:
        action_filter = st.multiselect("Filtrer par action", df['action'].unique(), default=df['action'].unique())
    
    df_filtered = df[(df['equipe'].isin(equipe_filter)) & (df['action'].isin(action_filter))]
    
    # Métriques
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total actions", len(df_filtered))
    with col2:
        tirs = len(df_filtered[df_filtered['action'].str.contains('Tir', na=False)])
        st.metric("Tirs", tirs)
    with col3:
        fautes = len(df_filtered[df_filtered['action'] == 'Faute'])
        st.metric("Fautes", fautes)
    with col4:
        corners = len(df_filtered[df_filtered['action'] == 'Corner'])
        st.metric("Corners", corners)
    
    # Tableau des actions
    st.dataframe(df_filtered, use_container_width=True)
    
    # Export options
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💾 Exporter en CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Télécharger CSV",
                csv,
                f"match_{match_id}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                "text/csv"
            )
    
    with col2:
        if st.button("📤 Exporter en JSON"):
            json_str = df.to_json(orient='records', indent=2)
            st.download_button(
                "📥 Télécharger JSON",
                json_str,
                f"match_{match_id}_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                "application/json"
            )
    
    with col3:
        if st.button("🔄 Réinitialiser le match"):
            st.session_state.actions = []
            st.session_state.score_domicile = 0
            st.session_state.score_exterieur = 0
            st.rerun()
    
    # Aperçu du format API Genius Sports
    with st.expander("🔍 Voir le format API Genius Sports"):
        if len(df) > 0:
            exemple = df.iloc[-1].to_dict()
            st.json({
                "match_id": exemple.get('match_id'),
                "action": {
                    "type": exemple.get('action'),
                    "minute": exemple.get('minute'),
                    "team": exemple.get('equipe'),
                    "player": exemple.get('joueur')
                },
                "score": {
                    "home": st.session_state.score_domicile,
                    "away": st.session_state.score_exterieur
                },
                "timestamp": exemple.get('timestamp')
            })
else:
    st.info("👆 Commencez à enregistrer les actions du match !")

# Pied de page
st.markdown("---")
st.caption(f"Statisticien: Cheikh Youssou Bamar GUEYE | Préparé pour Genius Sports | {datetime.now().strftime('%d/%m/%Y')}")