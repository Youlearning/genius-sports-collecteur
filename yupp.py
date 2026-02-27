import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Configuration de la page
st.set_page_config(page_title="Statisticien Basketball - Genius Sports", layout="wide")
st.title("🏀 Outil de collecte - Basketball (Genius Sports)")
st.markdown("---")

# Informations du match
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

# Initialisation
if 'actions' not in st.session_state:
    st.session_state.actions = []
    st.session_state.score_domicile = 0
    st.session_state.score_exterieur = 0
    st.session_state.fautes_domicile = 0
    st.session_state.fautes_exterieur = 0

# Interface de saisie
st.subheader("➕ Enregistrer une action")
col1, col2, col3, col4 = st.columns(4)

with col1:
    minute = st.number_input("Minute", 1, 48, 1)  # 48 min pour un match FIBA
    seconde = st.number_input("Seconde", 0, 59, 0)

with col2:
    equipe = st.selectbox("Équipe", [equipe_domicile, equipe_exterieur])
    
with col3:
    type_action = st.selectbox(
        "Action",
        ["Panier à 2 pts", "Panier à 3 pts", "Lancer-franc réussi", 
         "Lancer-franc manqué", "Faute", "Faute antisportive", 
         "Rebond", "Interception", "Contre", "Perte de balle",
         "Temps-mort", "Fin de quart-temps"]
    )

with col4:
    joueur = st.text_input("Joueur", "")
    st.caption("Valeurs rapides:")

# Boutons rapides
col_rapide1, col_rapide2, col_rapide3, col_rapide4 = st.columns(4)
with col_rapide1:
    if st.button("🏀 2 pts"):
        type_action_rapide = "Panier à 2 pts"
with col_rapide2:
    if st.button("🎯 3 pts"):
        type_action_rapide = "Panier à 3 pts"
with col_rapide3:
    if st.button("🟨 Faute"):
        type_action_rapide = "Faute"
with col_rapide4:
    if st.button("⏱️ Fin quart"):
        type_action_rapide = "Fin de quart-temps"

# Bouton principal
if st.button("➕ Enregistrer l'action", type="primary"):
    # Déterminer les points marqués
    points = 0
    if type_action == "Panier à 2 pts":
        points = 2
    elif type_action == "Panier à 3 pts":
        points = 3
    elif type_action == "Lancer-franc réussi":
        points = 1
    
    action = {
        'match_id': match_id,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'minute': f"{minute}:{seconde:02d}",
        'equipe': equipe,
        'action': type_action,
        'joueur': joueur if joueur else "Non spécifié",
        'points': points
    }
    st.session_state.actions.append(action)
    st.success(f"✅ Action enregistrée : {type_action} à la {minute}'{seconde:02d}")
    
    # Mise à jour du score
    if points > 0:
        if equipe == equipe_domicile:
            st.session_state.score_domicile += points
        else:
            st.session_state.score_exterieur += points
    
    # Mise à jour des fautes
    if "Faute" in type_action:
        if equipe == equipe_domicile:
            st.session_state.fautes_domicile += 1
        else:
            st.session_state.fautes_exterieur += 1

# Affichage du score
st.markdown("---")
col_score1, col_score2, col_score3 = st.columns(3)
with col_score1:
    st.markdown(f"## 🏠 {equipe_domicile}")
    st.markdown(f"**Fautes:** {st.session_state.fautes_domicile}")
with col_score2:
    st.markdown(f"## {st.session_state.score_domicile} - {st.session_state.score_exterieur}")
with col_score3:
    st.markdown(f"## {equipe_exterieur} ✈️")
    st.markdown(f"**Fautes:** {st.session_state.fautes_exterieur}")

# Statistiques avancées
if st.session_state.actions:
    st.subheader("📊 Statistiques détaillées")
    df = pd.DataFrame(st.session_state.actions)
    
    # Métriques par équipe
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_points_domicile = df[df['equipe'] == equipe_domicile]['points'].sum()
        st.metric(f"🏠 {equipe_domicile} - Points", total_points_domicile)
    
    with col2:
        total_points_exterieur = df[df['equipe'] == equipe_exterieur]['points'].sum()
        st.metric(f"✈️ {equipe_exterieur} - Points", total_points_exterieur)
    
    with col3:
        tirs_reussis = len(df[df['action'].str.contains('Panier|Lancer-franc réussi')])
        st.metric("Tirs réussis", tirs_reussis)
    
    with col4:
        interceptions = len(df[df['action'] == 'Interception'])
        st.metric("Interceptions", interceptions)
    
    # Tableau des actions
    st.dataframe(df, use_container_width=True)
    
    # Export
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Exporter CSV"):
            csv = df.to_csv(index=False)
            st.download_button("📥 Télécharger", csv, f"basket_{match_id}.csv")
    
    with col2:
        if st.button("📤 Exporter JSON"):
            json_str = df.to_json(orient='records', indent=2)
            st.download_button("📥 Télécharger", json_str, f"basket_{match_id}.json")
    
    # Réinitialisation
    if st.button("🔄 Nouveau match"):
        st.session_state.actions = []
        st.session_state.score_domicile = 0
        st.session_state.score_exterieur = 0
        st.session_state.fautes_domicile = 0
        st.session_state.fautes_exterieur = 0
        st.rerun()

# Pied de page
st.markdown("---")
st.caption(f"Statisticien: Cheikh Youssou Bamar GUEYE | Préparé pour Genius Sports | {datetime.now().strftime('%d/%m/%Y')}")
