import streamlit as st
import fitz  # PyMuPDF
import re

st.set_page_config(page_title="Anonymiseur de CV", layout="centered")
st.title("🔒 Anonymiseur intelligent de CV")

uploaded_file = st.file_uploader("📄 Dépose ton CV au format PDF", type="pdf")

if uploaded_file:
    with open("cv.pdf", "wb") as f:
        f.write(uploaded_file.read())

    doc = fitz.open("cv.pdf")
    texte_complet = ""
    for page in doc:
        texte_complet += page.get_text()

    st.subheader("🔍 Aperçu du contenu extrait")
    st.text_area("Texte extrait", texte_complet, height=300)

    if st.button("🧼 Anonymiser automatiquement"):
        texte_anonyme = texte_complet
        texte_anonyme = re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", "[email masqué]", texte_anonyme)
        texte_anonyme = re.sub(r"(\+33\s?|0)[67](\s?\d{2}){4}", "[téléphone masqué]", texte_anonyme)
        texte_anonyme = re.sub(r"linkedin\.com/in/[a-zA-Z0-9-]+", "[linkedin masqué]", texte_anonyme)
        texte_anonyme = re.sub(r"\b(19[5-9]\d|200[0-5])\b", "[année masquée]", texte_anonyme)

        entreprises = ["Bee2link", "Modis", "Michelin", "Google", "Airbus"]
        for nom in entreprises:
            texte_anonyme = re.sub(rf"\b{re.escape(nom)}\b", "[entreprise masquée]", texte_anonyme, flags=re.IGNORECASE)

        lignes = texte_anonyme.splitlines()
        if lignes and len(lignes[0].split()) <= 5:
            texte_anonyme = texte_anonyme.replace(lignes[0], "[nom masqué]")

        st.text_area("✅ Résultat anonymisé", texte_anonyme, height=300)

        # Création PDF anonymisé
        new_doc = fitz.open()
        new_page = new_doc.new_page()
        new_page.insert_text((72, 72), texte_anonyme, fontsize=10)
        new_doc.save("cv_anonyme.pdf")

        with open("cv_anonyme.pdf", "rb") as f:
            st.download_button("📥 Télécharger le CV anonymisé", f, file_name="cv_anonyme.pdf")
