import streamlit as st
from PyPDF2 import PdfReader
import re
from collections import Counter

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Smart Study Companion PRO", layout="wide")

st.title("🧠 Smart Study Companion PRO")

# ---------------------------
# PDF TEXT EXTRACTION
# ---------------------------
def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# ---------------------------
# CLEAN WORDS (important improvement)
# ---------------------------
def get_keywords(text):
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text)
    stop_words = {
        "this","that","with","from","have","will","your","they","what",
        "which","when","were","been","being","there","their","about",
        "would","could","should","into","over","after","before"
    }

    filtered = [w for w in words if w not in stop_words]
    freq = Counter(filtered)

    return [w for w, _ in freq.most_common(15)]

# ---------------------------
# SMART QUESTION GENERATOR
# ---------------------------
def generate_questions(text):
    keywords = get_keywords(text)

    short_q = []
    long_q = []

    for k in keywords:
        short_q.append(f"What is {k}?")
        short_q.append(f"Write key points about {k}.")

        long_q.append(f"Explain {k} in detail with examples.")
        long_q.append(f"Discuss the concept of {k} with real-life applications.")

    return short_q[:10], long_q[:10]

# ---------------------------
# FLASHCARDS
# ---------------------------
def generate_flashcards(text):
    keywords = get_keywords(text)
    cards = []

    for k in keywords[:8]:
        cards.append((f"What is {k}?", f"{k} is an important concept from your notes."))

    return cards

# ---------------------------
# SIMPLE Q&A SEARCH
# ---------------------------
def find_relevant_chunk(text, query):
    sentences = text.split(".")
    relevant = [s for s in sentences if query.lower() in s]
    return " ".join(relevant[:5]) if relevant else "No exact match found in notes."

# ---------------------------
# UPLOAD PDF
# ---------------------------
pdf = st.file_uploader("📄 Upload any subject PDF")

if pdf:
    text = extract_text(pdf)
    st.success("✅ PDF processed successfully!")

    # ---------------------------
    # ASK QUESTION
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
            "What is the main concept from your notes?",
            "Explain one important topic from your PDF.",
            "What did you learn from the document?"
        ]

        score = 0

        for i, q in enumerate(questions):
            ans = st.text_input(q, key=f"quiz_{i}")

            if ans:
                if len(ans) > 10:
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
