import io
import docx2txt
import streamlit as st
import PyPDF2

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def extract_skills_from_resume(resume_file):
    # Check the file type
    if resume_file.name.endswith('.docx'):
        text = docx2txt.process(resume_file)
    elif resume_file.name.endswith('.pdf'):
        text = extract_text_from_pdf(resume_file)
    else:
        st.error("Unsupported file format. Please upload a DOCX or PDF file.")
        return []

    # Define a list of skills
    skills_list = [
        "Python", "Data Analysis", "Communication",
        "C/C++", "Java", "HTML/CSS", "JavaScript", "EJS", "Handlebars", "Typescript",
        "MySQL", "MongoDB", "React", "Node.js", "Bootstrap", "Express", "SpringBoot",
        "pandas", "NumPy", "Matplotlib", "Seaborn", "Tensorflow",
        "Git/GitHub", "Unix", "VS Code", "Postman", "Figma", "Jupyter", "Eclipse", "PowerBI"
    ]

    # Extract skills based on keyword matching
    skills = [skill for skill in skills_list if skill.lower() in text.lower()]

    return skills

def calculate_skill_percentage(required_skills, resume_skills):
    # Calculate the percentage of required skills present in the resume
    matching_skills = set(required_skills) & set(resume_skills)
    percentage = (len(matching_skills) / len(required_skills)) * 100
    return percentage

def get_improvement_suggestions(required_skills, resume_skills):
    # Identify skills that are missing in the resume
    missing_skills = set(required_skills) - set(resume_skills)
    return missing_skills

def main():
    st.title("HR Recruitment System")

    # Upload a resume
    uploaded_file = st.file_uploader("Upload a resume", type=["docx", "pdf"])

    if uploaded_file is not None:
        # Define required skills (replace with your own list)
        required_skills = [
            "Python", "Data Analysis", "Communication",
            "C/C++", "Java", "HTML/CSS", "JavaScript", "EJS", "Handlebars", "Typescript",
            "MySQL", "MongoDB", "React", "Node.js", "Bootstrap", "Express", "SpringBoot",
            "pandas", "NumPy", "Matplotlib", "Seaborn", "Tensorflow",
            "Git/GitHub", "Unix", "VS Code", "Postman", "Figma", "Jupyter", "Eclipse", "PowerBI"
        ]

        # Extract skills from the uploaded resume
        resume_skills = extract_skills_from_resume(uploaded_file)

        # Calculate skill percentage
        percentage = calculate_skill_percentage(required_skills, resume_skills)

        # Display the percentage
        st.write(f"Skill Match Percentage: {percentage:.2f}%")

        # Provide improvement suggestions
        if percentage < 100:
            missing_skills = get_improvement_suggestions(required_skills, resume_skills)
            st.write("To improve your skill set, consider working on the following skills:")
            for skill in missing_skills:
                st.write(f"- {skill}")

if __name__ == "__main__":
    main()
