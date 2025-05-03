import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from my_fonction import *
from Evaluation import *
from streamlit_echarts import st_echarts


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
    classes = class_sex_counts.index.tolist()
    male_counts = class_sex_counts.get("Masculin", [0] * len(classes)).tolist()
    female_counts = class_sex_counts.get("Féminin", [0] * len(classes)).tolist()

    # Create options for the e_chart
    options = {
        "title": {"text": ""},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": ["Masculin", "Féminin"]},
        "xAxis": {
            "type": "category",
            "data": classes,
            "axisLabel": {"rotate": 45},
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": "Masculin",
                "data": male_counts,
                "type": "bar",
                "itemStyle": {"color": "#5470C6"},
                "label": {
                    "show": True,
                    "position": "top",
                },
            },
            {
                "name": "Féminin",
                "data": female_counts,
                "type": "bar",
                "itemStyle": {"color": "#91CC75"},
                "label": {
                    "show": True,
                    "position": "top",
                },
            },
        ],
    }

    # Render the chart
    st_echarts(options=options, height="400px")
    class_sex_counts = student_eval.groupby(["Classe", "Sexe"]).size().unstack(fill_value=0)
    classes = class_sex_counts.index.tolist()
    male_counts = class_sex_counts.get("Masculin", [0] * len(classes)).tolist()
    female_counts = class_sex_counts.get("Féminin", [0] * len(classes)).tolist()

    
with col[1]:
    pass #make_cross_hist_2(student_eval,var1="Sexe",var2="Classe", titre="Effectif des evaluations par classe")
    # Dropdown to select the class
    selected_class = st.selectbox("Choisir une classe", student_eval["Classe"].unique())

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
    selected_data = dict_reponse[selected_class]
    # Prepare data for all classes
    all_classes_data = {response: [] for response in ["Très satisfait", "Satisfait", "Moyen", "Mauvais"]}
    for classe in dict_reponse:
        for response in all_classes_data:
            all_classes_data[response].append(dict_reponse[classe].get(response, 0))

    # Create options for the grouped bar chart
    options = {
        "title": {"text": ""},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": ["Très satisfait", "Satisfait", "Moyen", "Mauvais"]},
        "xAxis": {
            "type": "category",
            "data": list(dict_reponse.keys()),
            "axisLabel": {"rotate": 45},
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": response,
                "data": all_classes_data[response],
                "type": "bar",
                "stack": "total",
                "itemStyle": {"color": color},
            }
            for response, color in zip(
                ["Très satisfait", "Satisfait", "Moyen", "Mauvais"],
                ["#5470C6", "#91CC75", "#FAC858", "#EE6666"],
            )
        ],
    }
   

    # Render the chart
    st_echarts(options=options, height="400px")
    dict_reponse
    

#st.dataframe(student_eval, use_container_width=True)
#st.dataframe(data_eval, use_container_width=True)