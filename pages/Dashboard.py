import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from my_fonction import *

from streamlit_echarts import st_echarts
from Evaluation import  data_eval, student_eval
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

st.markdown("""
        <style>
            /* Styling for tabs */
            .stTabs [data-baseweb="tab-list"] {
                gap: 20px;
                background-color: #f8f9fa;
                border-radius: 15px;
                padding: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .stTabs [data-baseweb="tab"] {
                background-color: transparent;
                border-radius: 10px;
                padding: 10px 20px;
                color: #495057;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            .stTabs [data-baseweb="tab"]:hover {
                background-color: #e9ecef;
                color: #0066cc;
            }
            
            .stTabs [aria-selected="true"] {
                background-color: #0066cc !important;
                color: white !important;
                border-radius: 10px;
            }
            
            /* Content area styling */
            .stTabs [data-baseweb="tab-panel"] {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
                margin-top: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            }
        </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
        .stMarkdown {font-family: 'Helvetica', sans-serif;}
        .stButton button {
            background-color: #0066cc;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            border: none;
            transition: background-color 0.3s;
        }
        .stButton button:hover {
            background-color: #0052a3;
        }
        .stRadio > label {
            color: #2c3e50;
            font-weight: 500;
        }
        .stExpander {
            background-color: #f8f9fa;
            border-radius: 10px;
            margin: 10px 0;
            border: 1px solid #dee2e6;
        }
        .stTextInput input {
            border-radius: 5px;
            border: 2px solid #e9ecef;
        }
        h1 {
            color: #1e3d59;
            text-align: center;
            padding: 20px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .stSidebar {
            background-color: #f1f3f5;
            padding: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        /* Card-like effect for expanders */
        .stExpander {
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .stExpander:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        }
        
        /* Gradient background for header */
        h1 {
            background: linear-gradient(45deg, #1e3d59, #2c5282);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Animated button hover effect */
        .stButton button {
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* Radio button styling */
        .stRadio > div {
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 8px;
            transition: background-color 0.2s;
        }
        .stRadio > div:hover {
            background-color: #e9ecef;
        }
        
        /* Text input focus effect */
        .stTextInput input:focus {
            border-color: #0066cc;
            box-shadow: 0 0 0 2px rgba(0,102,204,0.2);
        }
        
        /* Sidebar hover effect */
        .stSidebar:hover {
            box-shadow: 2px 0 8px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    body {
        font-size: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


if not authentication_system():
    st.stop()

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
            {
                "type": "heatmap",
                "data": heatmap_data,
                "label": {"show": True},
                "emphasis": {"itemStyle": {"borderColor": "#333", "borderWidth": 1}},
            }
        ],
    }

    # Render the heatmap
    st_echarts(options=options, height=height, key=cle)

question_dict={
            "Q_01":"GLOBALEMENT, ETES-VOUS SATISFAIT DE  ENSEIGNANT ?",
            "Q_02":"ENONCE DES OBJECTIFS DU COURS",
            "Q_03":"CONTENU DU COURS",
            "Q_04":"TAUX DE COUVERTURE DU PROGRAMME",
            "Q_05":"CONNAISSANCES THEORIQUES ACQUISES",
            "Q_06":"CONNAISSANCES PRATIQUES",
            "Q_07":"CONFORMITE DES EVALUATIONS AU CONTENU",
            "Q_08":"RAPPORT DUREE/CONTENU DE L'EPREUVE",
            "Q_09":"ASSIDUITE",
            "Q_10":"PONCTUALITE",
            "Q_11":"TENUE VESTIMENTAIRE",
            "Q_12":"UTILISATION DES OUTILS ET MATERIELS DIDACTIQUES",
            "Q_13":"DISPONIBILITE A ECOUTER LES ETUDIANTS",
            "Q_14":"MAITRISE DE LA SALLE DE COURS",
            "Q_15":"INTERACTION ENSEIGNANTS-ETUDIANTS (QUESTIONS-REPONSES)",
            "Q_16":"INTEGRATION DES TICS DANS LES COURS (VIDEO PROJECTEUR, INTERNET OU COURS SAISIS)",
            "Q_17":"ORGANISATION ET SUIVI DES TP, TPE ET TD",
            "Q_18":"CAPACITE DE TRANSMISSION DU COURS",
            "Q_19":"COMMENTEZ LES ASPECTS POSITIFS",
            "Q_20":"COMMENTEZ LES ASPECTS NEGATIFS",
            "Q_21":"SUGGESTIONS" }

            # Create a new dictionary with reversed key-value pairs from question_dict
reversed_question_dict = {value: key for key, value in question_dict.items()}

colors_palette = ["#81DBF7", "#0FAADB", "#0B7A9D", "#06465A", "#4CF2BF", "#0EC48C","#09855F","#064E38","#F77DF1","#F127E7","#9E0A97","#660661"]
colors_palette2 = ["#FC1414", "#F61AEC", "#7F09E1", "#074BE3", "#05B0E5", "#06E49F","#08E212","#BEE208","#E47A06","#E13709","#9E0A97","#660661"]

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
    options = {
        "title": {"text": title},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": cross_table.columns.tolist()},
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

                # Create options for the donut chart
                options = {
                    "title": {"text": title, "left": "center"},
                    "tooltip": {"trigger": "item"},
                    "legend": {"orient": "vertical", "left": "left", "data": list(data.keys())},
                    "series": [
                        {
                            "name": "Evaluation",
                            "type": "pie",
                            "radius": ["40%", "70%"],
                            "avoidLabelOverlap": False,
                            "itemStyle": {"borderRadius": 10, "borderColor": "#fff", "borderWidth": 2},
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

st.title("Tableau de bord pour le suivi des évaluations des enseignants")
st.markdown(
    """
    <style>
    body {
        font-size: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


col=st.columns(2)

with col[0]:
    # Prepare data for the chart
    class_sex_counts = student_eval.groupby(["Classe", "Sexe"]).size().unstack(fill_value=0)
    st.markdown("##### Repartition des etudaints ayant soumis leur évaluation")
    make_grouped_bar_chart(
        data=class_sex_counts.reset_index(),
        x_col="Classe",
        y_cols=["Masculin", "Féminin"],
        title="",
        x_label_rotation=0,
        colors=["#5470C6", "#91CC75"],
        height="400px",
        cle="graph"
    )
    

    
with col[1]:
    pass #make_cross_hist_2(student_eval,var1="Sexe",var2="Classe", titre="Effectif des evaluations par classe")
    # Dropdown to select the class
    

    data_reponse=data_eval[["Classe","Q_01","Q_02","Q_03","Q_04","Q_05","Q_06","Q_07","Q_08","Q_09","Q_10","Q_11","Q_12","Q_13","Q_14","Q_15","Q_16","Q_17","Q_18"]]
    dict_reponse = {}
    for classe in data_reponse["Classe"].unique():
        data_classe = data_reponse[data_reponse["Classe"] == classe].drop(columns=["Classe"])
        response_counts = data_classe.apply(pd.Series.value_counts).fillna(0).sum(axis=1)
        for response in ["Très satisfait", "Satisfait", "Moyen", "Mauvais"]:
            if response not in response_counts:
                response_counts[response] = 0
        dict_reponse[classe] = response_counts.loc[["Très satisfait", "Satisfait", "Moyen", "Mauvais"]].to_dict()
    # Prepare data for the selected class
   
    # Prepare data for all classes
    all_classes_data = {response: [] for response in ["Très satisfait", "Satisfait", "Moyen", "Mauvais"]}
    for classe in dict_reponse:
        for response in all_classes_data:
            all_classes_data[response].append(dict_reponse[classe].get(response, 0))

    
    cross_table = pd.DataFrame(all_classes_data, index=list(dict_reponse.keys()))
    tab_temp=cross_table.T
    for colone in tab_temp.columns:
        tab_temp[colone]=round(100*tab_temp[colone]/tab_temp[colone].sum(),2)
    
    st.markdown("##### Notation Générale par classe")
    make_cross_echart(tab_temp.T,  x_label_rotation=0,cle="compare")

cl=st.columns(3)
with cl[0]:
    selected_question = st.selectbox("Choisir un aspect de l'évaluation", reversed_question_dict.keys())
    if reversed_question_dict[selected_question] not in ["Q_19","Q_20","Q_21"]:
        data_quest = data_eval[["Classe", reversed_question_dict[selected_question]]]
        #st.dataframe(data_quest)
        dict_reponse_quest = {}
        for classe in data_quest["Classe"].unique():
            data_classe_quest = data_quest[data_quest["Classe"] == classe].drop(columns=["Classe"])
            response_counts_quest = data_classe_quest.apply(pd.Series.value_counts).fillna(0).sum(axis=1)
            for rep in ["Très satisfait", "Satisfait", "Moyen", "Mauvais"]:
                if rep not in response_counts_quest:
                    response_counts_quest[rep] = 0
            #response_counts
            dict_reponse_quest[classe] = response_counts_quest.loc[["Très satisfait", "Satisfait", "Moyen", "Mauvais"]].to_dict()
        
        
    
        # Prepare data for all classes
        all_classes_data_quest = {rep: [] for rep in ["Très satisfait", "Satisfait", "Moyen", "Mauvais"]}
        for classe in dict_reponse_quest:
            for rep in all_classes_data_quest:
                all_classes_data_quest[rep].append(dict_reponse_quest[classe].get(rep, 0))

        
        cross_table_quest = pd.DataFrame(all_classes_data_quest, index=list(dict_reponse_quest.keys()))
        tab_temp_2=cross_table_quest.T
        for colone in tab_temp_2.columns:
            tab_temp_2[colone]=round(100*tab_temp_2[colone]/tab_temp_2[colone].sum(),2)
        st.markdown(f" Evaluation Générale de {selected_question}")
        make_cross_echart(tab_temp_2.T, colors=colors_palette2[3:], x_label_rotation=0,cle="juijb")

with cl[1]:
    selected_enseignant = st.selectbox("Choisir un enseignant", data_eval["Enseignant"].unique())
    data_enseignant = data_eval[data_eval["Enseignant"] == selected_enseignant][["Classe", "Q_01", "Q_02", "Q_03", "Q_04", "Q_05", "Q_06", "Q_07", "Q_08", "Q_09", "Q_10", "Q_11", "Q_12", "Q_13", "Q_14", "Q_15", "Q_16", "Q_17","Q_18"]]
    dict_reponse_enseignant = {}
    for classe in data_enseignant["Classe"].unique():
        data_classe_enseignant = data_enseignant[data_enseignant["Classe"] == classe].drop(columns=["Classe"])
        response_counts_enseignant = data_classe_enseignant.apply(pd.Series.value_counts).fillna(0).sum(axis=1)
        for rep in ["Très satisfait", "Satisfait", "Moyen", "Mauvais"]:
            if rep not in response_counts_enseignant:
                response_counts_enseignant[rep] = 0
        dict_reponse_enseignant[classe] = response_counts_enseignant.loc[["Très satisfait", "Satisfait", "Moyen", "Mauvais"]].to_dict()
    
    if len(dict_reponse_enseignant.keys())==1:
        cross_table_enseignant = pd.DataFrame(dict_reponse_enseignant)
        make_donut_chart(dict_reponse_enseignant[classe])
    else:
        cross_table_enseignant = pd.DataFrame(dict_reponse_enseignant, index=list(response_counts_enseignant.keys()))
        tab_temp_3=cross_table_enseignant
        for colone in tab_temp_3.columns:
            tab_temp_3[colone]=round(100*tab_temp_3[colone]/tab_temp_3[colone].sum(),2)
        st.markdown(f" Evaluation Générale de M. {selected_enseignant}")
        make_cross_echart(tab_temp_3.T, colors=colors_palette2[5:], x_label_rotation=40,cle="jui")

with cl[2]:
    new_class=st.selectbox("Choisir une classe pour evaluer", data_eval["Classe"].unique())
    new_data_eval=data_eval[data_eval["Classe"] == new_class]
    selected_cours= st.selectbox("Choisir un cours", new_data_eval["Cours"].unique())
    data_cours = new_data_eval[new_data_eval["Cours"] == selected_cours][["Classe", "Q_01", "Q_02", "Q_03", "Q_04", "Q_05", "Q_06", "Q_07", "Q_08", "Q_09", "Q_10", "Q_11", "Q_12", "Q_13", "Q_14", "Q_15", "Q_16", "Q_17","Q_18"]]
    dict_reponse_cours = {}
    for classe in data_cours["Classe"].unique():
        data_classe_cours = data_cours[data_cours["Classe"] == classe].drop(columns=["Classe"])
        response_counts_cours = data_classe_cours.apply(pd.Series.value_counts).fillna(0).sum(axis=1)
        for rep in ["Très satisfait", "Satisfait", "Moyen", "Mauvais"]:
            if rep not in response_counts_cours:
                response_counts_cours[rep] = 0
        dict_reponse_cours[classe] = response_counts_cours.loc[["Très satisfait", "Satisfait", "Moyen", "Mauvais"]].to_dict()
    if len(dict_reponse_cours.keys())==1:
        cross_table_cours = pd.DataFrame(dict_reponse_cours)
        st.markdown(f" Evaluation Générale de {new_class}")
        make_donut_chart(dict_reponse_cours[classe],cle="jbkjn")
    else:
        cross_table_cours = pd.DataFrame(dict_reponse_cours, index=list(response_counts_cours.keys()))
        tab_temp_4=cross_table_cours
        for colone in tab_temp_4.columns:
            tab_temp_4[colone]=round(100*tab_temp_4[colone]/tab_temp_4[colone].sum(),2)
        st.markdown(f" Evaluation Générale de {new_class}")
        make_cross_echart(tab_temp_4.T, colors=colors_palette2[3:], x_label_rotation=40,cle="juij")

ncl=st.columns(2)
with ncl[0]:
    class_choosed= st.selectbox("Sélectionner une classe", data_eval["Classe"].unique())
    class_df= data_eval[data_eval["Classe"] == class_choosed]
with ncl[1]:
    cours_choosed= st.selectbox("Sélectionner un cours", class_df["Cours"].unique())
    cours_df= class_df[class_df["Cours"] == cours_choosed][["Q_01", "Q_02", "Q_03", "Q_04", "Q_05", "Q_06", "Q_07", "Q_08", "Q_09", "Q_10", "Q_11", "Q_12", "Q_13", "Q_14", "Q_15", "Q_16", "Q_17","Q_18"]]
choosed_counts = cours_df.apply(pd.Series.value_counts).fillna(0)
for c in choosed_counts.columns:
    choosed_counts=choosed_counts.rename(columns={c:question_dict[c]})
    for col in choosed_counts.columns:
        choosed_counts[col] = round(100 * choosed_counts[col] / choosed_counts[col].sum(), 2)

make_heatmap_echart(choosed_counts, title="Taux de satisfaction (%)", x_label_rotation=90, height="400px", cle="heatmap")

# Filtrer la base student_eval par classe

st.markdown("# MANIPULATION ET EXPORTATION DES TABLEAU DE DONNES")
st.markdown("### 1. Table des étudiants ayant déjà évaluer les enseignants")
cb=st.columns([2.5,7.5])

with cb[0]: 
    selected_class = st.multiselect("Sélectionner une classe pour filtrer les étudiants", student_eval["Classe"].unique(),default=student_eval["Classe"].unique())
    filtered_students = student_eval[student_eval["Classe"].isin(selected_class)]
    file_name = st.text_input("Nom du fichier à télécharger (sans extension)", value="student")
    if st.button("📥Télécharger"):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            filtered_students.to_excel(writer, index=False, sheet_name="Étudiants")
        output.seek(0)
        st.download_button(
            label="📥Télécharger le fichier Excel",
            data=output,
            file_name=f"{file_name}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

with cb[1]:
# Afficher les données filtrées
    st.dataframe(filtered_students, use_container_width=True,hide_index=True)

st.markdown("### 2. Table des evaluations")
cc=st.columns([7.5,2.5])
with cc[1]: 
    selected_class = st.multiselect("Sélectionner une classe pour filtrer les évaluations", data_eval["Classe"].unique(), default=data_eval["Classe"].unique())
    filtered_evaluations = data_eval[data_eval["Classe"].isin(selected_class)]
    file_name = st.text_input("Nom du fichier (sans extension)", value="evaluation")
    if st.button("📥Télécharger", key="hjblb"):
        output = io.BytesIO()
        labels = pd.DataFrame.from_dict(question_dict, orient="index", columns=["Question"])
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            filtered_evaluations.to_excel(writer, index=False, sheet_name="Evaluations")
            labels.to_excel(writer, index_label="Code", sheet_name="Labels")
        output.seek(0)
        st.download_button(
            label="📥Télécharger le fichier Excel",
            data=output,
            file_name=f"{file_name}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
with cc[0]:
# Afficher les données filtrées
    st.dataframe(filtered_evaluations, use_container_width=True,hide_index=True)


