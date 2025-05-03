import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from my_fonction import *
from Evaluation import *


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
    make_cross_hist_2(student_eval,var2="Classe", var1="Sexe", typ_bar=2, titre="Effectif des evaluations par classe")
with col[1]:
    pass #make_cross_hist_2(student_eval,var1="Sexe",var2="Classe", titre="Effectif des evaluations par classe")
    # Dropdown to select the class
    selected_class = st.selectbox("Choisir une classe", student_eval["Classe"].unique())

    # Filter data for the selected class
    filtered_data = data_eval[data_eval["Classe"] == selected_class]
    data_reponse=data_eval[["Q_01","Q_02","Q_03","Q_04","Q_05","Q_06","Q_07","Q_08","Q_09","Q_10","Q_11","Q_12","Q_13","Q_14","Q_15","Q_16","Q_17","Q_18"]]
    # Count occurrences of each response category globally
    response_counts = data_reponse.apply(pd.Series.value_counts).fillna(0).sum(axis=1).loc[["Très satisfait", "Satisfait", "Moyen", "Mauvais"]]
    #response_counts = data_reponse.apply(pd.Series.value_counts).fillna(0).sum(axis=1).loc[["Très satisfait", "Satisfait", "Moyen", "Mauvais"]]

    # Display the response counts as a table
    st.table(response_counts)

st.dataframe(student_eval, use_container_width=True)
st.dataframe(data_eval, use_container_width=True)