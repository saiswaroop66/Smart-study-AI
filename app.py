import streamlit as st
from PyPDF2 import PdfReader
import random

# ---------------------------
# PDF TEXT EXTRACTION
# ---------------------------
def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.lower()

# ---------------------------
# SIMPLE CHUNK SEARCH (basic fix for your issue)
# ---------------------------
def find_relevant_chunk(text, query):
    sentences = text.split(".")
    relevant = [s for s in sentences if query.lower() in s]
    return " ".join(relevant[:5]) if relevant else text[:500]

# ---------------------------
# QUESTION GENERATOR
# ---------------------------
def generate_questions(text):
    topics = ["variable", "loop", "function", "python", "data type"]

    short_q = []
    long_q = []

    for t in topics:
        if t in text:
            short_q.append(f"What is {t}?")
            short_q.append(f"Name features of {t}.")

            long_q.append(f"Explain {t} in detail with example.")
            long_q.append(f"Write a note on {t} in Python.")

    return short_q, long_q

# ---------------------------
# FLASHCARDS
# ---------------------------
def generate_flashcards(text):
    cards = []
    if "variable" in text:
        cards.append(("What is a variable?", "A container to store data values"))
    if "loop" in text:
        cards.append(("What is a loop?", "Used for repeating tasks"))
    if "function" in text:
        cards.append(("What is a function?", "Reusable block of code"))
    return cards

# ---------------------------
# UI
# ---------------------------
st.title("🧠 Smart Study Companion PRO")

pdf = st.file_uploader("📄 Upload your notes (PDF)")

if pdf:
    text = extract_text(pdf)
    st.success("File processed successfully!")

    # ---------------------------
    # Q&A SECTION
    # ---------------------------
    st.header("💬 Ask from your notes")
    q = st.text_input("Enter your question")

    if q:
        answer = find_relevant_chunk(text, q)
        st.write("📌 Answer:")
        st.write(answer)

    # ---------------------------
    # IMPORTANT QUESTIONS
    # ---------------------------
    st.header("📌 Important Questions Generator")

    if st.button("Generate Questions"):
        short_q, long_q = generate_questions(text)

        st.subheader("🔹 Short Answer Questions")
        for i, q in enumerate(short_q, 1):
            st.write(f"{i}. {q}")

        st.subheader("🔸 Long Answer Questions")
        for i, q in enumerate(long_q, 1):
            st.write(f"{i}. {q}")

    # ---------------------------
    # FLASHCARDS
    # ---------------------------
    st.header("🧾 Flashcards")

    cards = generate_flashcards(text)

    for i, (q, a) in enumerate(cards):
        with st.expander(f"Card {i+1}: {q}"):
            st.write(a)

    # ---------------------------
    # QUIZ MODE
    # ---------------------------
    st.header("🧪 Quiz Mode")

    if st.button("Start Quiz"):
        questions = [
            "What is a variable?",
            "What is a loop?",
            "What is a function?"
        ]

        score = 0

        for i, q in enumerate(questions):
            ans = st.text_input(q, key=i)
            if ans:
                if "variable" in q.lower() and "store" in ans.lower():
                    score += 1
                if "loop" in q.lower() and "repeat" in ans.lower():
                    score += 1
                if "function" in q.lower() and "block" in ans.lower():
                    score += 1

        st.write("🎯 Score:", score, "/", len(questions))

    # ---------------------------
    # KEYWORD SEARCH
    # ---------------------------
    st.header("🔍 Keyword Search")

    keyword = st.text_input("Search in notes")

    if keyword:
        result = find_relevant_chunk(text, keyword)
        st.write(result)