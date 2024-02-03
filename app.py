import docx2txt
import streamlit as st
import PyPDF2
import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def extract_skills(text):
    doc = nlp(text)

    skill_keywords = ["Python", "Java", "C++", "HTML", "CSS", "JavaScript", "Git", "MySQL", "MongoDB", "Azure", "AWS"]

    matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp(skill) for skill in skill_keywords]
    matcher.add("Skills", None, *patterns)

    matches = matcher(doc)

    matched_skills = [doc[start:end].text for _, start, end in matches]

    return matched_skills

def calculate_skill_percentage(jd_skills, resume_skills):
    matching_skills = set(jd_skills) & set(resume_skills)
    percentage = (len(matching_skills) / len(jd_skills)) * 100
    return percentage

def get_improvement_suggestions(required_skills, resume_skills):
    missing_skills = set(required_skills) - set(resume_skills)
    return missing_skills

def main():
    st.title("HR Recruitment System")

    jd_file = st.file_uploader("Upload Job Description (JD)", type=["docx", "pdf"])

    uploaded_file = st.file_uploader("Upload a resume", type=["docx", "pdf"])

    if jd_file is not None and uploaded_file is not None:
        jd_text = extract_text_from_pdf(jd_file) if jd_file.name.endswith('.pdf') else docx2txt.process(jd_file)
        jd_skills = extract_skills(jd_text)

        resume_text = extract_text_from_pdf(uploaded_file) if uploaded_file.name.endswith('.pdf') else docx2txt.process(uploaded_file)
        resume_skills = extract_skills(resume_text)

        percentage = calculate_skill_percentage(jd_skills, resume_skills)

        st.write(f"Skill Match Percentage: {percentage:.2f}%")

        if percentage < 100:
            missing_skills = get_improvement_suggestions(jd_skills, resume_skills)
            st.write("To improve your skill set, consider working on the following skills:")
            for skill in missing_skills:
                st.write(f"- {skill}")

if __name__ == "__main__":
    main()
