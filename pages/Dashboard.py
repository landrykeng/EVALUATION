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
    # graphique de la répartition du nombre de personne ayant rempli par classe et par sexe
    make_grouped_bar_chart(
        data=class_sex_counts.reset_index(),
        x_col="Classe",
        y_cols=["Masculin", "Féminin"],
        title="",
        x_label_rotation=45,
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
    
    make_cross_echart(tab_temp.T, colors=colors_palette, x_label_rotation=45,cle="compare")

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
        make_cross_echart(tab_temp_2.T, colors=colors_palette, x_label_rotation=45,cle="juijb")



#st.dataframe(student_eval, use_container_width=True)
#st.dataframe(data_eval, use_container_width=True)