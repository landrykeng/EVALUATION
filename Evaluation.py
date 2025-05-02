import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


st.set_page_config(page_title="FORMULAIRE EVALUATION DES ENSEIGNANT", page_icon="📊", layout="wide")
st.title("EVALUATION DES ENSEIGNENTS DE LA FORMATION CONTINUE, SEMESTRE 1")


data=pd.read_excel('Classification.xlsx')
student_eval=pd.read_excel('Base.xlsx', sheet_name="Etudiant")

st.dataframe(student_eval)
nested_dict = {}
for _, row in data.iterrows():
    classe = row['Classe']
    cours = row['Cours']
    enseignant = row['Enseignant']
    
    if classe not in nested_dict:
        nested_dict[classe] = {}
    
    nested_dict[classe][enseignant] = cours


#st.dataframe(data, use_container_width=True)

st.write("## Formulaire d'évaluation des enseignants")

# Sélection de la classe

classe_selectionnee = st.radio("Classe",[""] + list(nested_dict.keys()), index=0)
nom_etudiant = st.text_input("Nom")
prenom_etudiant = st.text_input("Prénom")
matricule = st.text_input("Matricule")
#st.write(student_eval["Matricule"].value_counts())
#st.write(list(student_eval["Matricule"]).count(matricule))

sexe = st.radio("Sexe", ["","Masculin", "Féminin"], index=0)
if str(matricule) in student_eval["Matricule"]:
    st.error("Vous avez déjà fait votre évaluation")
else:
    #enseignant_selectionne = st.selectbox("Sélectionnez un enseignant", list(nested_dict[classe_selectionnee].keys()))
    if classe_selectionnee!="" and nom_etudiant!="" and prenom_etudiant!="" and matricule !="" :
        for enseignant, cours in nested_dict[classe_selectionnee].items():
            with st.expander(enseignant + ": " + cours, expanded=False):
                st.write(f" Evaluation de M. {enseignant} pour le cours de {cours}")
                Q_01=st.radio("GLOBALEMENT, ETES-VOUS SATISFAIT DE  ENSEIGNANT ?", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=1, key=classe_selectionnee+enseignant+cours+"_01")
                Q_02=st.radio("ENONCE DES OBJECTIFS DU COURS", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=1,key=classe_selectionnee+enseignant+cours+"_02")
                Q_03=st.radio("CONTENU DU COURS", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=1,key=classe_selectionnee+enseignant+cours+"_03")
                Q_04=st.radio("TAUX DE COUVERTURE DU PROGRAMME", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=1,key=classe_selectionnee+enseignant+cours+"_04")
                Q_05=st.radio("CONNAISSANCES THEORIQUES ACQUISES", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=1,key=classe_selectionnee+enseignant+cours+"_05")
                Q_06=st.radio("CONNAISSANCES PRATIQUES", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=1,key=classe_selectionnee+enseignant+cours+"_06")
                Q_07=st.radio("CONFORMITE DES EVALUATIONS AU CONTENU", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=1,key=classe_selectionnee+enseignant+cours+"_07")
                Q_08=st.radio("RAPPORT DUREE/CONTENU DE L'EPREUVE", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=1,key=classe_selectionnee+enseignant+cours+"_08")
                Q_09=st.radio("ASSIDUITE", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=1,key=classe_selectionnee+enseignant+cours+"_09")
                Q_10=st.radio("PONCTUALITE", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=1,key=classe_selectionnee+enseignant+cours+"_10")
                Q_11=st.radio("TENUE VESTIMENTAIRE", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=1,key=classe_selectionnee+enseignant+cours+"_11")
                Q_12=st.radio("UTILISATION DES OUTILS ET MATERIELS DIDACTIQUES", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=1,key=classe_selectionnee+enseignant+cours+"_12")
                Q_13=st.radio("DISPONIBILITE A ECOUTER LES ETUDIANTS", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=1,key=classe_selectionnee+enseignant+cours+"_13")
                Q_14=st.radio("MAITRISE DE LA SALLE DE COURS", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=1,key=classe_selectionnee+enseignant+cours+"_14")
                Q_15=st.radio("INTERACTION ENSEIGNANTS-ETUDIANTS (QUESTIONS-REPONSES)",["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=1,key=classe_selectionnee+enseignant+cours+"_15")
                Q_16=st.radio("INTEGRATION DES TICS DANS LES COURS (VIDEO PROJECTEUR, INTERNET OU COURS SAISIS)",["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=1,key=classe_selectionnee+enseignant+cours+"_16")
                Q_17=st.radio("ORGANISATION ET SUIVI DES TP, TPE ET TD",["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=1,key=classe_selectionnee+enseignant+cours+"_17")
                Q_18=st.radio("CAPACITE DE TRANSMISSION DU COURS",["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=1,key=classe_selectionnee+enseignant+cours+"_18")
                Q_19=st.text_area("COMMENTEZ LES ASPECTS POSITIFS", height=100,key=classe_selectionnee+enseignant+cours+"_19")
                Q_20=st.text_area("COMMENTEZ LES ASPECTS NEGATIFS", height=100,key=classe_selectionnee+enseignant+cours+"_20")
                Q_21=st.text_area("SUGGESTIONS", height=100,key=classe_selectionnee+enseignant+cours+"_21")

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
            
            
        soumission=st.button("Soumettre mon evaluation")
        # Collecting student information
        if soumission:
    
            etudiant_data = {
                "Classe": [classe_selectionnee],
                "Nom": [nom_etudiant],
                "Prénom": [prenom_etudiant],
                "Sexe": [sexe],
                "Matricule": [matricule]
            }
            etudiant_df = pd.DataFrame(etudiant_data)

            # Collecting evaluation data
            evaluation_data = []
            missing_responses = []
            if classe_selectionnee != "":
                for enseignant, cours in nested_dict[classe_selectionnee].items():
                    responses = {
                        "Classe": classe_selectionnee,
                        "Sexe": sexe,
                        "Enseignant": enseignant,
                        "Cours": cours
                    }
                    for i in range(1, 22):
                        question_key = f"Q_{i:02d}"
                        response = st.session_state.get(classe_selectionnee + enseignant + cours + f"_{i:02d}", "")
                        responses[question_key] = response
                        if response == "":
                            missing_responses.append(
                                f"Pour le cours de   {cours} dispensé par M. {enseignant}, vous n'avez pas donné de réponse à la question {question_dict[question_key]}."
                            )
                    evaluation_data.append(responses)

            evaluation_df = pd.DataFrame(evaluation_data)

            # Displaying the dataframes for verification
            st.write("### Données de l'étudiant")
            st.dataframe(etudiant_df)

            st.write("### Données d'évaluation")
            st.dataframe(evaluation_df)

            if len(missing_responses)==0:
            # Load the Excel file
                excel_file = "Base.xlsx"
                with pd.ExcelWriter(excel_file, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
                    # Append student data to the "Etudiant" sheet
                    etudiant_df.to_excel(writer, sheet_name="Etudiant", index=False, header=False, startrow=writer.sheets["Etudiant"].max_row)

                    # Append evaluation data to the "Evaluation" sheet
                    evaluation_df.to_excel(writer, sheet_name="Evaluation", index=False, header=False, startrow=writer.sheets["Evaluation"].max_row)
                st.success("Votre évaluation a été soumise avec succès.")
            else:
                st.error("La soumission du questionnaire ne sera valide que si toutes les réponses sont non vides.")
                for message in missing_responses:
                    st.markdown(message)
