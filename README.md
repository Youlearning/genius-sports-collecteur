# ⚽ Outil de collecte de données sportives - Genius Sports

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![Statut](https://img.shields.io/badge/Statut-Terminé-success)

## 📋 Présentation

Outil de **collecte manuelle de données sportives** développé en Python/Streamlit pour simuler le travail d'un statisticien terrain chez **Genius Sports**.

Ce projet a été réalisé dans le cadre de ma préparation à une candidature chez Genius Sports. Il démontre ma compréhension du workflow de collecte de données en temps réel.

## 🏀 Fonctionnalités

- ✅ Interface intuitive de saisie des actions de match
- ✅ Horodatage précis (minute + seconde)
- ✅ Score en direct automatique
- ✅ Statistiques en temps réel (tirs, fautes, corners)
- ✅ Export aux formats **CSV** et **JSON**
- ✅ Aperçu du format API Genius Sports

## 🎯 Démonstration réelle

J'ai testé cet outil en simulant la collecte du match **Sénégal vs Côte d'Ivoire** du 26 février 2026 (Éliminatoires Coupe du Monde FIBA 2027) :

- Score final : Sénégal 90 - 80 Côte d'Ivoire
- 6 tirs à 3 pts de la Côte d'Ivoire dans le 1er quart
- Actions clés : interceptions de Ibou Faye, contres de Badji

## 🛠️ Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/ton-pseudo/genius-sports-collecteur.git

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
streamlit run collecteur.py