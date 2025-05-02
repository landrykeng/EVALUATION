import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from my_fonction import *
from Evaluation import *

st.set_page_config(page_title="TABLEAU DE BORD", layout="wide")
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

st.dataframe(student_eval, use_container_width=True)
st.dataframe(data_eval, use_container_width=True)