import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from math import pi
import os
from weasyprint import HTML
import base64
from io import BytesIO
import streamlit.components.v1 as components
import json
import requests
import base64
import plotly.express as px
from streamlit_lottie import st_lottie

st.set_page_config(page_title="VARKify Quiz", layout="wide", initial_sidebar_state="auto")
st.markdown("""
    <style>
        html, body {
        background: linear-gradient(135deg, #a2d2ff, #bde0fe);
        font-family: 'Poppins', sans-serif;
        font-size: 18px;
        color: #333;
        padding: 0;
        margin: 0;
        }
        html, body, .stApp {
        background: linear-gradient(135deg, ##0f1116, #000000) !important;
        background-attachment: fixed;
        background-size: cover;
        }
        .main .block-container {
            padding: 2rem 2rem !important;
            max-width: 960px;
            margin: auto;
        }
        h2, h3 {
            text-align: center;
            margin-bottom: 18rem;
            color: #6a1b9a;
        }
        .about-text, li {
            line-height: 1.2;
            margin-bottom: 1.8rem;
            font-size: 1.1rem !important;
        }
        .section-title {
            font-size: 2rem;
            font-weight: 700;
            margin-top: 4rem;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        .image-box {
            padding: 2rem;
            border-radius: 14px;
            background: #ffffffcc;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
            text-align: center;
            margin: 1rem 0;
        }
        img {
            border-radius: 12px;
            margin: 1rem 0;
        }
        ul {
            padding-left: 1.5rem;
        }
        .main-title {
            font-size: 3em;
            font-weight: 800;
            text-align: center;
            color:rgb(214, 187, 187);
            margin: 40px 0 10px;
        }

        .glass-box {
            background: rgba(235, 220, 220, 0.95);
            border-radius: 20px;
            padding: 30px;
            margin: 30px auto;
            max-width: 800px;
            backdrop-filter: blur(15px);
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2);
            border: 1px solid rgba(241, 214, 214, 0.97);
        }

        .question {
            font-size: 1.3em;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 25px;
        }
        .nav-button {
            background: linear-gradient(120deg, #7f00ff, #e100ff);
            border: none;
            border-radius: 14px;
            padding: 14px 24px;
            font-size: 16px;
            font-weight: 600;
            color: white;
            cursor: pointer;
            width: 100%;
            text-align: center;
            margin: 10px 0;
            transition: all 0.2s ease-in-out;
        }
        .nav-button:hover {
            transform: scale(1.05);
            background: linear-gradient(120deg, #e100ff, #7f00ff);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
        }

        .cta-button {
            display: flex;
            justify-content: center;
            margin-top: 3rem;
            width: 1px;
        }

        /* Stylish Centered Button */
        .stButton > button {
            background: linear-gradient(135deg, rgb(127, 0, 255), rgb(225, 0, 255)) !important;
            color: white !important;
            border-radius: 14px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            padding: 14px 20px !important;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
            width: 240px ;
            min-height: 60px;
            margin: auto;
            display: block;
            transition: all 0.3s ease-in-out;
        }
        .option-button {
            background: linear-gradient(120deg, #7f00ff, #e100ff);
            border: none;
            border-radius: 14px;
            padding: 16px 24px;
            font-size: 16px;
            font-weight: 600;
            color: white;
            cursor: pointer;
            width: 100%;
            text-align: center;
            margin-bottom: 12px;
            transition: all 0.2s ease-in-out;
            display: block;
            word-wrap: break-word;
        }

        .option-button:hover {
            transform: scale(1.03);
            background: linear-gradient(120deg, #e100ff, #7f00ff);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
        }

        .quiz-button {
            background: linear-gradient(to right, #00c6ff, #0072ff);
            border: none;
            border-radius: 14px;
            padding: 16px 30px;
            font-size: 18px;
            font-weight: bold;
            color: white;
            cursor: pointer;
            text-align: center;
            transition: 0.3s ease;
            width: 100%;
            margin-top: 30px;
        }

        .quiz-button:hover {
            transform: translateY(-2px);
            background: linear-gradient(to right, #0072ff, #00c6ff);
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
        }
        .centered-button > button {
            background: linear-gradient(135deg, rgb(127, 0, 255), rgb(225, 0, 255)) !important;
            color: white !important;
            border-radius: 14px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            padding: 14px 20px !important;
            margin: 20px auto !important;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
            width: fit-content !important;
            min-width: 200px;
            max-width: 300px;
            display: block;
            min-height: 60px;
        }

        .stButton > button:hover {
            transform: scale(1.03);
            background: linear-gradient(135deg, rgb(225, 0, 255), rgb(127, 0, 255)) !important;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.2);
        }
        body, .main {
            overflow-y: auto !important;
        }
        .flex-container {
            display: flex;
            flex-direction: row;
            gap: 2rem;
            justify-content: space-between;
            align-items: stretch;
            flex-wrap: wrap;
            margin-top: 2rem;
        }

        .text-column, .image-column {
            flex: 1;
            min-width: 300px;
        }

        .text-column {
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .image-column {
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .image-column img {
            width: 100%;
            max-width: 100%;
            height: auto;
            border-radius: 12px;
            object-fit: cover;
        }

    </style>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
        .full-width-button button {
            width: 100% !important;
            padding: 0.75em 1em;
            font-size: 1.1em;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.05);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: background 0.3s, transform 0.1s ease-in-out;
        }

        .full-width-button button:hover {
            background: rgba(255, 255, 255, 0.15);
            transform: scale(1.02);
        }

        .full-width-button {
            width: 100%;
            margin-bottom: 1em;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'step' not in st.session_state:
    st.session_state.step = -1
if 'responses' not in st.session_state:
    st.session_state.responses = []
if 'name' not in st.session_state:
    st.session_state.name = ''
if 'age' not in st.session_state:
    st.session_state.age = ''

questions = [
    "When trying to fix something broken, what do you usually do first?",
    "How do you learn new software or apps most effectively?",
    "In a group project, how do you contribute best?",
    "How do you prefer to remember someone's name?",
    "When planning a trip, what part excites you the most?",
    "How do you typically express your thoughts or feelings?",
    "What's the best way for you to understand a math concept?",
    "When learning a dance or sport, how do you approach it?",
    "In a museum, what do you enjoy most?",
    "How do you prefer to revise or study for an exam?"
]

options = [
    [
        "Look for a diagram or a video tutorial",
        "Ask someone to explain it to you",
        "Read the manual or instructions",
        "Try fixing it by tinkering with it hands-on"
    ],
    [
        "Explore the interface using icons and layouts",
        "Listen to someone guide you through it",
        "Read online guides or help articles",
        "Start clicking and experimenting until you get it"
    ],
    [
        "Creating infographics, slides, or charts",
        "Leading discussions or explaining ideas aloud",
        "Writing reports, summaries, or documentation",
        "Building models, testing, or creating prototypes"
    ],
    [
        "Associate their face or outfit with their name",
        "Repeat their name out loud a few times",
        "Write it down or read it off a list",
        "Shake hands or engage in an activity with them"
    ],
    [
        "Looking at maps, travel videos, or scenic photos",
        "Talking to friends who've been there",
        "Reading reviews, blogs, and itineraries",
        "Packing, booking, and moving around"
    ],
    [
        "Through drawings, diagrams, or mood boards",
        "By talking to someone about them",
        "By writing in a journal or composing messages",
        "Through actions, gestures, or doing something physical"
    ],
    [
        "Seeing it in a graph, chart, or color-coded example",
        "Listening to someone explain it step by step",
        "Reading formulas and working through written examples",
        "Solving real-world problems or using physical objects"
    ],
    [
        "Watch a video or observe someone doing it",
        "Listen to a coach explain the moves",
        "Read instructions or descriptions of the movements",
        "Try it out physically and learn by doing"
    ],
    [
        "Observing visual exhibits and artwork",
        "Listening to the audio tour",
        "Reading the plaques and descriptions",
        "Interacting with hands-on exhibits"
    ],
    [
        "Use mind maps, colors, and visual aids",
        "Recite notes aloud or use recordings",
        "Read notes, highlight, and rewrite content",
        "Practice problems, labs, or real-world examples"
    ]
]

learning_styles = ['Visual', 'Auditory', 'Reading/Writing', 'Kinesthetic']

def render_glass_buttons(options):
    cols = st.columns(2)
    selected = None
    for i, option in enumerate(options):
        col = cols[i % 2]
        with col:
            st.markdown('<div class="full-width-button">', unsafe_allow_html=True)
            if st.button(option, key=f"option_{st.session_state.step}_{i}"):
                st.session_state.responses.append(i)
                st.session_state.step += 1
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    return selected

# ABOUT PAGE DISPLAY BEFORE QUIZ STARTS
if st.session_state.step == -1:
    # Full-width layout and custom styles
    st.markdown("""
        <style>
            .main .block-container {;
                padding-left: 2rem;
                padding-right: 2rem;
            }
            .section-title {
                font-size: 1.8rem;
                font-weight: 600;
                margin-top: 2rem;
                margin-bottom: 1rem;
            }
            .about-text {
                font-size: 18px;
                line-height: 1.7;
                margin-bottom: 1.2rem;
            }
            .image-box {
                border: 2px dashed #aaa;
                padding: 3rem;
                border-radius: 10px;
                text-align: center;
                font-style: italic;
                color: #777;
            }
        </style>
    """, unsafe_allow_html=True)

    # Logo placeholder
    st.markdown("""
    <div style="text-align: center; margin-top: -80px; margin-bottom: 20px;">
        <img src="data:image/png;base64,{logo_base64}" width="220" style="border-radius: 20px; box-shadow: 0 4px 14px rgba(0,0,0,0.15);" alt="VARKify Logo" />
    </div>
    """.format(logo_base64=base64.b64encode(open("/Users/sid/Documents/VARK Finale/Logo.png", "rb").read()).decode()), unsafe_allow_html=True)

    # Intro section
    st.markdown('<h2>🌟 <span style="color:#ffafcc;">About VARKify</span></h2>', unsafe_allow_html=True)
    st.markdown("""
    <p class="about-text" style="text-align: center;">
        Our platform uses intelligent analysis to help students, educators, and lifelong learners discover their dominant learning style
    </p>    
    <p class="about-text" style="text-align: center; margin-top: -10px;">
    <strong>Visual, Auditory, Reading/Writing, or Kinesthetic</strong> — through a fun, interactive quiz.
    </p>    """, unsafe_allow_html=True)

    # What We Do + Image (wider layout)
    left1, right1 = st.columns([1, 0.9])
    with left1:
        st.markdown('<div style="margin-top: 90px;"></div>', unsafe_allow_html=True)
        st.markdown("""
            <h3 class="section-title">🧠 What We Do</h3>
            <ul class="about-text">
                <li><strong>Interactive VARK quiz</strong>: A simple, engaging quiz designed to help you identify your dominant learning style.</li><br>
                <li><strong>Personalized insights</strong>: Receive a clear breakdown of your results and how it influences your learning process.</li><br>
                <li><strong>Tailored study tips</strong>: Get strategies and tools suited to your preferences.</li><br>
                <li><strong>Downloadable PDF report</strong>: Access a professional summary with study tips and recommendations.</li><br>
                <li><strong>User-friendly experience</strong>: Navigate easily through a beautifully designed interface.</li>
            </ul>
        """, unsafe_allow_html=True)
    with right1:
        st.image("/Users/sid/Documents/VARK Finale/pattern.png", use_container_width=True)

    # Who Is This For + second image (wider layout)
    left2, right2 = st.columns([1.2, 1])
    with right2:
        st.markdown('<div style="margin-top: 140px;"></div>', unsafe_allow_html=True)
        st.markdown("""
            <h3 class="section-title">🤝 Who Is This For?</h3>
            <ul class="about-text">
                <li><strong>Students</strong> looking to improve their study habits and academic performance.</li><br>
                <li><strong>Teachers</strong> adapting methods for varied learners.</li><br>
                <li><strong>Parents</strong> supporting their children’s learning journeys.</li><br>
                <li><strong>Lifelong learners</strong> enhancing their self-study and personal growth.</li><br>
                <li><strong>Professionals</strong> optimizing learning strategies for skill development.</li>
            </ul>
        """, unsafe_allow_html=True)
    with left2:
        st.image("/Users/sid/Documents/VARK Finale/success.png", use_container_width=True)

    # Call to action button
    with st.container():
        st.markdown('<div class="centered-button">', unsafe_allow_html=True)
        if st.button(" Go to Quiz Page ", key="go_to_quiz"):
            st.session_state.step = 0
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.step == 0:
    def load_lottie_file(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)
    # Example: Load and display
    lottie_animation = load_lottie_file("/Users/sid/Documents/VARK Finale/Animation - 1744970122882.json")  # 👈 your local path
    st_lottie(lottie_animation, height=300, key="placeholder")

    st.markdown('<div class="main-title"> Welcome to VARKify Quiz!</div>', unsafe_allow_html=True)
    with st.container():
        cols = st.columns([1, 2, 1])
        with cols[1]:
            st.session_state.name = st.text_input("Your name:", value=st.session_state.name)
            st.session_state.age = st.text_input("Your age:", value=st.session_state.age)
            st.markdown('<div class="centered-button">', unsafe_allow_html=True)
            if st.button("Take the Quiz", key="start_quiz", use_container_width=True):
                if st.session_state.name and st.session_state.age:
                    st.session_state.step = 1
                    st.rerun()
                else:
                    st.warning("Please enter your name and age to start the quiz.")
            st.markdown('</div>', unsafe_allow_html=True)

elif 0 < st.session_state.step <= len(questions):
    progress = st.progress((st.session_state.step-1)/len(questions))
    q_index = st.session_state.step - 1

    # Render options in evenly spaced columns with consistent height
    # Display the question
    st.markdown(f"""
    <div class="glass-box">
        <div class="question">Q{st.session_state.step}. {questions[q_index]}</div>
    </div>
    """, unsafe_allow_html=True)

    # Render the answer buttons
    selected = render_glass_buttons(options[q_index])

    # Add small Previous button centered below
    if st.session_state.step > 1:
        prev_col1, prev_col2, prev_col3 = st.columns([4, 2, 4])
        with prev_col2:
            if st.button("⬅ Previous", key="prev_btn"):
                if st.session_state.responses:
                    st.session_state.responses.pop()
                st.session_state.step -= 1

    # Add Next logic after selection
    if selected is not None:
        st.session_state.responses.append(selected)
        st.session_state.step += 1

elif st.session_state.step > len(questions):
    st.success("Quiz Completed Successfully! 🥳")
    
    def find_top_styles(scores):
        max_score = max(scores.values())
        top_styles = [style for style, score in scores.items() if score == max_score]
        return top_styles
    
    scores = {style: 0 for style in learning_styles}
    for i, ans in enumerate(st.session_state.responses):
        scores[learning_styles[ans]] += 1

    top_styles = find_top_styles(scores)  
    top_styles_str = ", ".join(top_styles)

# Then the content
    if len(top_styles) == 1:
        st.markdown(f"""
        <style>
            .animated-text {{
                font-size: 2.5em;
                font-weight: bold;
                color: #009688;
                text-shadow: 2px 2px 5px rgba(0, 150, 136, 0.6);
                letter-spacing: 1px;
                word-wrap: break-word;
                padding: 10px;
                text-align: center;
                display: inline-block;
                max-width: 100%;
                white-space: nowrap;
                overflow: hidden;
                width: 0;
                animation: typing 3s steps(40) 1s forwards;
                transform: translateX(90px); /* Shift right by 50px */
            }}

            @keyframes typing {{
                from {{
                    width: 0;
                }}
                to {{
                    width: 100%;
                }}
            }}

            .wrapper {{
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 30px 20px;
                text-align: center;
                max-width: 90%;
            }}
        </style>
        <div class="wrapper">
            <h2 class="animated-text">
                Your dominant learning style is: {top_styles_str}
            </h2>
        </div>
    """, unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <style>
            .animated-text {{
                font-size: 2.5em;
                font-weight: bold;
                color: #009688;
                text-shadow: 2px 2px 5px rgba(0, 150, 136, 0.6);
                letter-spacing: 1px;
                word-wrap: break-word;
                padding: 10px;
                text-align: center;
                display: inline-block;
                max-width: 100%;
                white-space: nowrap;
                overflow: hidden;
                width: 0;
                animation: typing 3s steps(40) 1s forwards;
                transform: translateX(80px); /* Shift right by 50px */
            }}

            @keyframes typing {{
                from {{
                    width: 0;
                }}
                to {{
                    width: 100%;
                }}
            }}

            .wrapper {{
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 30px 20px;
                text-align: center;
                max-width: 90%;
            }}
        </style>
        <div class="wrapper">
            <h2 class="animated-text">
                You have multiple dominant learning styles: {top_styles_str}
            </h2>
        </div>
    """, unsafe_allow_html=True)
        
    # Show score breakdown
    st.subheader("🧠 Your Learning Style Breakdown:")
    df = pd.DataFrame.from_dict(scores, orient='index', columns=['Score'])
    df = pd.DataFrame({
    'Style': list(scores.keys()),
    'Score': list(scores.values())
    })
    fig = px.bar(df, x='Style', y='Score', color='Style', 
             title='Your VARK Learning Style Scores',
             template='plotly_white',
             color_discrete_sequence=px.colors.qualitative.Pastel)

    st.plotly_chart(fig, use_container_width=True)

    # Tips and videos
    tips = {
        'Visual': [
        "Use diagrams, charts, and maps to represent information.",
        "Watch educational videos and infographics.",
        "Color-code your notes.",
        "Use mind maps for better structure.",
        "Create visual flashcards.",
        "Tools : ",
        "Lucidchart - create diagrams and flowcharts.",
        "Miro - collaborate with visual whiteboards.",
        "Canva - design infographics and visual notes.",
        "XMind - make mind maps and visual structures.",
        "YouTube - watch visual explainers and tutorials."
    ],
    'Auditory': [
        "Read aloud to yourself.",
        "Join group discussions.",
        "Use rhymes and mnemonics.",
        "Listen to podcasts or lectures.",
        "Use voice notes for revision.",
        "Tools : ",
        "Audible - listen to audiobooks on various subjects.",
        "Spotify Podcasts - explore educational podcasts.",
        "Otter.ai - record and transcribe spoken content.",
        "Google Docs Voice Typing - convert speech to text.",
        "Clubhouse - participate in live audio discussions."

    ],
    'Reading/Writing': [
        "Take structured notes.",
        "Summarize concepts in your own words.",
        "Practice writing essays or explanations.",
        "Use lists and headings.",
        "Read textbooks and articles.",
        "Tools : ",
        "Google Docs - write and organize notes.",
        "Notion - manage reading and note-taking in one place.",
        "Quizlet - study using text-based flashcards.",
        "Wikipedia - read summaries and deep articles.",
        "Obsidian - build connected text-based knowledge."
    ],
    'Kinesthetic': [
        "Use hands-on activities.",
        "Practice through simulation or role-play.",
        "Take frequent study breaks with movement.",
        "Use physical flashcards.",
        "Learn by teaching others.",
        "Tools : ",
        "Trello - manage learning tasks interactively.",
        "Arduino - build hands-on tech projects.",
        "Labster - use virtual science labs.",
        "Instructables - follow step-by-step learning projects.",
        "Google Expeditions - explore topics through VR experiences."
    ]
    }

    videos = {
        'Visual': [
        "https://www.youtube.com/watch?v=IN-_S_jj3gE",
        "https://www.youtube.com/watch?v=A4NqhPU-vh8"
    ],
    'Auditory': [
        "https://www.youtube.com/watch?v=bgIXy2dVXdc",
        "https://www.youtube.com/watch?v=3qgxqFqmsk0"
    ],
    'Reading/Writing': [
        "https://www.youtube.com/watch?v=CXdpSfDWbGY",
        "https://www.youtube.com/watch?v=I8yNIgFBuP8"
    ],
    'Kinesthetic': [
        "https://www.youtube.com/watch?v=GFoAtj4FLJ0",
        "https://www.youtube.com/watch?v=eBN_OO94uBQ"
    ]
    }
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### 🧩 Tips for Improving as a **{top_styles_str}** Learner(s)")
        for style in top_styles:
            st.markdown(f"#### Tips & Tools for **{style}** Learners:")
            for tip in tips[style]:
                st.markdown(f"- {tip}")
    with col2:
        st.markdown("### 🎥 Recommended Video Resources:")
        for style in top_styles:
            st.markdown(f"#### Videos for **{style}** Learners:")
            for link in videos[style]:
                st.video(link)

        # PDF generator
    def generate_pdf(name, age, scores, top_styles_str, fig):

        img_bytes = fig.to_image(format="png")
        img_base64 = base64.b64encode(img_bytes).decode()

        score_rows = "".join(
            f"<tr><td style='padding:8px;'>{style}</td><td style='padding:8px;text-align:center;'>{score}</td></tr>"
            for style, score in scores.items()
        )

        tips_html = ""
        for style in top_styles:
            tips_html += f"""
            <div class='page-section'>
                <h3>{style} Learner Tips:</h3>
                <ul>
                    {''.join(f'<li>{tip}</li>' for tip in tips[style])}
                </ul>
            </div>"""

        videos_html = ""
        for style in top_styles:
            videos_html += f"""
            <div class='page-section'>
                <h3>{style} Learner Videos:</h3>
                <ul>
                    {''.join(f"<li><a href='{vid}' target='_blank'>{vid}</a></li>" for vid in videos[style])}
                </ul>
            </div>"""

        html = f"""
        <html>
        <head>
            <style>
                @page {{
                    size: A4;
                    margin: 2cm;
                }}
                body {{
                    font-family: 'Helvetica Neue', sans-serif;
                    background: #fff;
                    color: #111;
                    font-size: 12pt;
                    line-height: 1.6;
                }}
                h1 {{
                    text-align: center;
                    font-size: 28pt;
                    font-weight: bold;
                    margin-bottom: 40px;
                    text-transform: uppercase;
                }}
                h2 {{
                    font-size: 18pt;
                    margin-top: 1.5em;
                    border-bottom: 1px solid #ddd;
                    padding-bottom: 0.3em;
                }}
                h3 {{
                    font-size: 14pt;
                    margin-top: 1.2em;
                    margin-bottom: 0.3em;
                    page-break-after: avoid;
                }}
                .section {{
                    margin-bottom: 40px;
                    page-break-inside: avoid;
                }}
                .page-section {{
                    page-break-inside: avoid;
                    margin-bottom: 30px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 10px;
                    page-break-inside: avoid;
                }}
                th, td {{
                    border: 1px solid #ccc;
                    padding: 10px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                    font-weight: bold;
                }}
                ul {{
                    margin: 0.5em 0 1.5em 1.5em;
                }}
                a {{
                    color: #004080;
                    text-decoration: none;
                }}
                img {{
                    max-width: 100%;
                    height: auto;
                    margin-top: 20px;
                    page-break-inside: avoid;
                }}
                .page-break {{
                    page-break-after: always;
                }}
            </style>
        </head>
        <body>
            <h1>🎓 VARKify Learning Style Report</h1>

            <div class="section">
                <h2>👤 Participant Details</h2>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Age:</strong> {age}</p>
                <p><strong>Dominant Style(s):</strong> {top_styles_str}</p>
            </div>

            <div class="section page-break">
                <h2>📈 Your Learning Style Scores</h2>
                <table>
                    <tr><th>Learning Style</th><th>Score</th></tr>
                    {score_rows}
                </table>
            </div>

            <div class="section page-break">
                <h2>🎯 Personalized Learning Tips</h2>
                {tips_html}
            </div>

            <div class="section page-break">
                <h2>🎥 Recommended Videos</h2>
                {videos_html}
            </div>

            <div class="section page-break">
                <h2>📊 Your Learning Style Visualization</h2>
                <img src="data:image/png;base64,{img_base64}" alt="Learning Style Chart">
            </div>
        </body>
        </html>
        """

        pdf = HTML(string=html).write_pdf()
        return pdf 

        # Offer PDF download
    if st.button("📄 Download Your VARKify Report"):
        pdf = generate_pdf(
            name=st.session_state.name,
            age=st.session_state.age,
            scores=scores,
            top_styles_str=top_styles_str,
            fig=fig
        )
        b64_pdf = base64.b64encode(pdf).decode('utf-8')
        st.markdown(f"""
        <a href="data:application/pdf;base64,{b64_pdf}" download="VARKify_Report_{st.session_state.name}.pdf">
            <button style="
                background-color: #009688;
                color: white;
                padding: 14px 28px;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 12px;
                box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
                cursor: pointer;
                margin-top: 20px;">
                📥 Download PDF Report
            </button>
        </a>
    """, unsafe_allow_html=True)

        # Restart button
    st.markdown("---")
    st.markdown("#### Would you like to retake the quiz?")
    if st.button("🔄 Restart Quiz"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
