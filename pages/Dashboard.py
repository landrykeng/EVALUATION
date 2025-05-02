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
        font-size: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.dataframe(student_eval, use_container_width=True)
st.dataframe(data_eval, use_container_width=True)

