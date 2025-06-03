import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from my_fonction import *
import re
from collections import Counter
import jieba
import random
from streamlit_echarts import st_echarts
import io
import hashlib
import json
import os
from datetime import datetime, timedelta


def hash_password(password):
    """Hash un mot de passe pour un stockage sécurisé"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Charge la base de données des utilisateurs depuis un fichier JSON"""
    default_user = {
        "users": {
            "Evaluation FC2025": {
                "password": hash_password("Dr GONDZE"),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    }
    
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    
    with open("users.json", "w") as f:
        json.dump(default_user, f, indent=4)
    return default_user

def save_users(users):
    """Sauvegarde la base de données des utilisateurs dans un fichier JSON"""
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

def check_credentials(username, password):
    """Vérifie si les identifiants sont corrects"""
    users = load_users()
    if username in users["users"]:
        if users["users"][username]["password"] == hash_password(password):
            return True
    return False

def change_password(username, old_password, new_password):
    """Change le mot de passe d'un utilisateur"""
    users = load_users()
    if username in users["users"]:
        if users["users"][username]["password"] == hash_password(old_password):
            users["users"][username]["password"] = hash_password(new_password)
            save_users(users)
            return True, "Mot de passe changé avec succès"
    return False, "Ancien mot de passe incorrect"

def authentication_system():
    """Système d'authentification pour le dashboard"""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = None
    if "login_time" not in st.session_state:
        st.session_state["login_time"] = None

    if st.session_state["authenticated"]:
        if st.session_state["login_time"] and datetime.now() - st.session_state["login_time"] > timedelta(hours=8):
            st.session_state["authenticated"] = False
            st.session_state["username"] = None
            st.session_state["login_time"] = None
            st.warning("Votre session a expiré. Veuillez vous reconnecter.")
        else:
            st.sidebar.success(f"Connecté en tant que {st.session_state['username']}")
            if st.sidebar.button("Déconnexion"):
                st.session_state["authenticated"] = False
                st.session_state["username"] = None
                st.session_state["login_time"] = None
                st.rerun()
            return True

    tab1, tab2 = st.tabs(["Connexion", "Changer le mot de passe"])

    with tab1:
        username = st.text_input("Nom d'utilisateur", key="login_username")
        password = st.text_input("Mot de passe", type="password", key="login_password")
        
        if st.button("Se connecter"):
            if check_credentials(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.session_state["login_time"] = datetime.now()
                st.success("Connexion réussie!")
                st.rerun()
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect")

    with tab2:
        st.header("Changer le mot de passe")
        username = st.text_input("Nom d'utilisateur", key="change_username")
        old_password = st.text_input("Ancien mot de passe", type="password", key="old_password")
        new_password = st.text_input("Nouveau mot de passe", type="password", key="new_password")
        confirm_password = st.text_input("Confirmer le nouveau mot de passe", type="password", key="confirm_password")
        
        if st.button("Changer le mot de passe"):
            if new_password != confirm_password:
                st.error("Les mots de passe ne correspondent pas")
            else:
                success, message = change_password(username, old_password, new_password)
                if success:
                    st.success(message)
                else:
                    st.error(message)

    return False


def make_heatmap_echart(data, title="", x_label_rotation=45, colors=None, height="400px", cle="heatmap"):
    """
    Generate a heatmap using st_echarts.

    Parameters:
    - data: pd.DataFrame, the data to plot (rows as y-axis, columns as x-axis).
    - title: str, the title of the chart.
    - x_label_rotation: int, rotation angle for x-axis labels.
    - colors: list, list of colors for the heatmap gradient.
    - height: str, height of the chart.

    Returns:
    - None, renders the heatmap in Streamlit.
    """
    if colors is None:
        colors = ["#B9B9FF", "#6D6DFF", "#0505FF","#00009A", "#000050", "#00000C"]  # Default gradient colors

    # Prepare data for the heatmap
    x_labels = data.columns.tolist()
    y_labels = data.index.tolist()
    heatmap_data = [
        [j, i, data.iloc[i, j]] for i in range(len(y_labels)) for j in range(len(x_labels))
    ]
    label_data = [[x[0],x[1],x[2]] for x in heatmap_data]
    
    # Create options for the heatmap
    options = {
        "title": {"text": title, "left": "center"},
        "tooltip": {"position": "top"},
        "xAxis": {
            "type": "category",
            "data": x_labels,
            "axisLabel": {"rotate": x_label_rotation},
        },
        "yAxis": {"type": "category", "data": y_labels},
        "toolbox": {
            "show": True,
            "orient": "vertical",
            "right": "0%",
            "top": "center",
            "feature": {
                "saveAsImage": {"show": True, "title": "Save"},
                "dataZoom": {"show": True, "yAxisIndex": "none"},
                "restore": {"show": True},
            },
        },
        "grid": {
            "left": "10%",
            "right": "10%",
            "bottom": "25%",
            "containLabel": False,
        },
        "visualMap": {
            "min": data.min().min(),
            "max": data.max().max(),
            "calculable": True,
            "orient": "vertical",
            "right": "5%",
            "top": "middle",
            "inRange": {"color": colors},
        },
        "series": [
            {   "name": "Evaluation",
                "type": "heatmap",
                "data": label_data,
                "label": {"show": True},
                "itemStyle": {
                    "borderColor": "#fff",
                    "borderWidth": 1,
                },
                "emphasis": {"itemStyle": {"borderColor": "#333", "borderWidth": 1}},
            }
        ],
    }

    # Render the heatmap
    st_echarts(options=options, height=height, key=cle)


def make_cross_echart(cross_table, title="", x_label_rotation=45, colors=None, height="400px",cle="b"):
    """
    Generate a grouped bar chart using st_echarts from a cross table.

    Parameters:
    - cross_table: pd.DataFrame, a cross table where rows are categories and columns are series.
    - title: str, the title of the chart.
    - x_label_rotation: int, rotation angle for x-axis labels.
    - colors: list, list of colors for the series.
    - height: str, height of the chart.

    Returns:
    - None, renders the chart in Streamlit.
    """
    if colors is None:
        # Default colors if not provided
        colors = ["#0DB329", "#E4E917", "#E79D19", "#E32B1D", "#0CA0B4", "#064C56"]
        

    # Prepare data for the chart
    categories = cross_table.index.tolist()
    series_data = [
        {
            "name": col,
            "data": cross_table[col].tolist(),
            "type": "bar",
            "stack": "total",
            "itemStyle": {"color": colors[i % len(colors)]},
        }
        for i, col in enumerate(cross_table.columns)
    ]

    # Create options for the e_chart
    # Add label formatter to show percentages
    options = {
        "title": {"text": title},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": cross_table.columns.tolist()},
        "xAxis": {
            "type": "category",
            "data": categories,
            "axisLabel": {"rotate": x_label_rotation},
        },
        "yAxis": {
            "type": "value",
            "axisLabel": {"formatter": "{value}%"}
        },
        "series": [{
            **series,
            "label": {
                "show": True,
                "formatter": "{c}%",
                "position": "inside"
            }
        } for series in series_data]
    }
    
    

    # Render the chart
    st_echarts(options=options, height=height, key=cle)


def make_grouped_bar_chart(data, x_col, y_cols, title="", x_label_rotation=45, colors=None, height="400px",cle="a"):
        """
        Generate a grouped bar chart using st_echarts.

        Parameters:
        - data: pd.DataFrame, the data to plot.
        - x_col: str, the column to use for the x-axis.
        - y_cols: list, the columns to use for the y-axis (grouped bars).
        - title: str, the title of the chart.
        - x_label_rotation: int, rotation angle for x-axis labels.
        - colors: list, list of colors for the bars.
        - height: str, height of the chart.

        Returns:
        - None, renders the chart in Streamlit.
        """
        if colors is None:
            # Default colors if not provided
            colors = ["#5470C6", "#91CC75", "#FAC858", "#EE6666", "#73C0DE"]

        # Prepare data for the chart
        categories = data[x_col].tolist()
        series_data = [
            {
                "name": col,
                "data": data[col].tolist(),
                "type": "bar",
                "itemStyle": {"color": colors[i % len(colors)]},
                "label": {
                    "show": True,
                    "position": "top",
                },
            }
            for i, col in enumerate(y_cols)
        ]

        # Create options for the e_chart
        options = {
            "title": {"text": title},
            "tooltip": {"trigger": "axis"},
            "legend": {"data": y_cols},
            "xAxis": {
                "type": "category",
                "data": categories,
                "axisLabel": {"rotate": x_label_rotation},
            },
            "yAxis": {"type": "value"},
            "series": series_data,
        }

        # Render the chart
        st_echarts(options=options, height=height, key=cle)

def make_donut_chart(data, title="", colors=None, height="400px", cle="donut"):
                """
                Generate a donut chart using st_echarts.

                Parameters:
                - data: dict, keys are labels and values are corresponding numerical values.
                - title: str, the title of the chart.
                - colors: list, list of colors for the segments.
                - height: str, height of the chart.

                Returns:
                - None, renders the chart in Streamlit.
                """
                if colors is None:
                    colors = ["#0DB329", "#E4E917", "#E79D19", "#E32B1D", "#0CA0B4", "#064C56"]

                # Prepare data for the chart
                series_data = [{"value": value, "name": key} for key, value in data.items()]
                # Add percentage data to the series_data
                for item in series_data:
                    item['value'] = round(item['value'] / sum(d['value'] for d in series_data) * 100, 2)
                    item['name'] = f"{item['name']} ({item['value']}%)"
                # Create options for the donut chart
                # Update value percentages in data for the legend
                data_with_percentages = {}
                total = sum(data.values())
                for key, value in data.items():
                    percentage = round((value / total) * 100, 2)
                    data_with_percentages[f"{key} ({percentage}%)"] = value
                options = {
                    "title": {"text": title, "left": "center"},
                    "tooltip": {"trigger": "item"},
                    "legend": {
                        "orient": "horizontal",
                        "top": "top",
                        "data": list(data.keys()),
                    },
                    "series": [
                        {
                            "name": "Evaluation",
                            "type": "pie",
                            "radius": ["30%", "70%"],
                            "avoidLabelOverlap": False,
                            "itemStyle": {"borderRadius": 3, "borderColor": "#fff", "borderWidth": 4},
                            "label": {"show": True, "position": "outside"},
                            "emphasis": {
                                "label": {"show": True, "fontSize": "16", "fontWeight": "bold"}
                            },
                            "data": series_data,
                        }
                    ],
                    "color": colors,
                }

                # Render the chart
                st_echarts(options=options, height=height, key=cle)


def generate_word_cloud(df, column_name, max_words=100, min_frequency=3, 
                        width=550, height=500, title="Nuage de mots", 
                        color_range=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'], random_seed=None):
    """
    Génère un nuage de mots interactif à partir d'une colonne de texte d'un DataFrame
    
    Paramètres:
    -----------
    df : pandas.DataFrame
        Le DataFrame contenant les données
    column_name : str
        Le nom de la colonne contenant le texte à analyser
    max_words : int, optionnel (défaut=100)
        Nombre maximum de mots à afficher
    min_frequency : int, optionnel (défaut=1)
        Fréquence minimale pour inclure un mot
    width : int, optionnel (défaut=800)
        Largeur du graphique en pixels
    height : int, optionnel (défaut=500)
        Hauteur du graphique en pixels
    title : str, optionnel (défaut="Nuage de mots")
        Titre du graphique
    color_range : list, optionnel (défaut=None)
        Liste de couleurs pour le nuage de mots, ex: ['#313695', '#4575b4', '#74add1', '#abd9e9']
    random_seed : int, optionnel (défaut=None)
        Graine aléatoire pour reproduire les résultats
    
    Retourne:
    ---------
    None - Affiche le graphique dans Streamlit
    """
    if random_seed is not None:
        random.seed(random_seed)
        np.random.seed(random_seed)
    
    # Définir les couleurs par défaut si non spécifiées
    if color_range is None:
        color_range = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    # Vérifier que la colonne existe
    if column_name not in df.columns:
        st.error(f"La colonne '{column_name}' n'existe pas dans le DataFrame.")
        return
    
    # Ignorer les valeurs NaN
    texts = df[column_name].dropna().astype(str).tolist()
    
    if not texts:
        st.warning(f"La colonne '{column_name}' ne contient pas de texte valide.")
        return
    
    # Combiner tous les textes
    all_text = " ".join(texts)
    
    # Nettoyer le texte
    all_text = all_text.lower()
    all_text = re.sub(r'[^\w\s]', '', all_text)  # Enlever la ponctuation
    
    # Tokenizer le texte (utilisation de jieba qui fonctionne bien pour le texte français également)
    words = jieba.lcut(all_text)
    
    # Filtrer les mots vides (vous pouvez ajouter votre propre liste de stopwords)
    stopwords = set(['le', 'la', 'les', 'du', 'de', 'des', 'un', 'une', 'et', 'est', 'à', 'en', 'que', 'qui', 
                      'pour', 'dans', 'ce', 'il', 'elle', 'ils', 'elles', 'nous', 'vous', 'on', 'je', 'tu',
                      'avec', 'par', 'au', 'aux', 'sur', 'ou', 'donc', 'or', 'ni', 'car', 'mais', 'où',
                      'comment', 'quand', 'pourquoi', 'si', 'ne', 'pas', 'plus', 'moins', 'peu', 'très'])
    words = [word for word in words if word not in stopwords and len(word) > 1]
    
    # Compter les fréquences des mots
    word_counts = Counter(words)
    
    # Filtrer par fréquence minimale
    word_counts = {word: count for word, count in word_counts.items() if count >= min_frequency}
    
    # Limiter au nombre maximum de mots
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:max_words]
    
    # Préparer les données pour ECharts avec des couleurs aléatoires pour chaque mot
    data = []
    for word, count in sorted_word_counts:
        data.append({
            "name": word, 
            "value": count,
            "textStyle": {
                "normal": {
                    "color": random.choice(color_range)
                }
            }
        })
    
    # Options pour ECharts
    options = {
        "title": {
            "text": title,
            "left": "center"
        },
        "tooltip": {},
        "series": [{
            "type": "wordCloud",
            "shape": "square",
            #"left": "left",
            "top": "center", 
            "width": "100%",
            "height": "100%",
            #"right": None,
            "bottom": None,
            "sizeRange": [12, 60],
            "rotationRange": [-90, 90],
            "rotationStep": 45,
            "gridSize": 8,
            "drawOutOfBound": False,
            "textStyle": {
                "fontFamily": "sans-serif",
                "fontWeight": "bold"
            },
            "emphasis": {
                "focus": "self",
                "textStyle": {
                    "shadowBlur": 10,
                    "shadowColor": "#333",
                    "color": color_range  
                }
            },
            "data": data
        }]
    }
    
    # Afficher le nuage de mots dans Streamlit
    st_echarts(options=options, height=height, width=width)