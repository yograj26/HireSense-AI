import hashlib
import json

import streamlit as st
from matcher import score_match, extract_skills
import pandas as pd
from app.recruiter_assistant import generate_recruiter_insights
from evaluation import evaluate_candidate
from batch_screening import screen_uploaded_resumes
from storage import init_db, save_screening, get_screening_history
from analytics import (
    compare_candidates,
    get_recruiter_insights,
    get_score_distribution,
)
from explainability import generate_explanation
from semantic_matcher import semantic_analysis
init_db()
TAXONOMY=['Python','SQL','Machine Learning','Scikit-learn','Pandas','NumPy','TensorFlow','PyTorch','NLP','Natural Language Processing','Power BI','Tableau','Excel','Git','Docker','Java','JavaScript','React','FastAPI','Flask','AWS','Data Visualization','Statistics','Deep Learning']
DEMO=[
 {'name':'Aarav Sharma','skills':['Python','SQL','Machine Learning','Pandas','Scikit-learn','Git'],'experience':'2 years','projects':'Customer churn prediction, analytics pipeline'},
 {'name':'Priya Singh','skills':['Python','TensorFlow','Deep Learning','NLP','Pandas','SQL'],'experience':'1 year','projects':'Text classification, sentiment analysis'},
 {'name':'Kabir Mehta','skills':['SQL','Power BI','Excel','Tableau','Python'],'experience':'3 years','projects':'Business dashboards, sales analytics'},
 {'name':'Neha Verma','skills':['Python','Java','Docker','FastAPI','Git','Machine Learning'],'experience':'1 year','projects':'API deployment, ML microservice'},
 {'name':'Rohan Gupta','skills':['Python','NumPy','Pandas','Statistics','Machine Learning'],'experience':'Fresher','projects':'Regression model, exploratory data analysis'}]
st.set_page_config(page_title='SmartHire AI',page_icon='🎯',layout='wide')
st.title('🎯 SmartHire AI')
st.caption('AI-Based Resume Screening & Job Matching System | Recruiter demo')
st.sidebar.header('Job Requirements')
SAMPLE_JOBS={'Junior Data Scientist': {'required': ['Python', 'SQL', 'Machine Learning'], 'preferred': ['Pandas', 'Scikit-learn', 'Data Visualization'], 'description': 'Build data-driven solutions, develop machine learning models, and analyze data.'}, 'ML Engineer': {'required': ['Python', 'Machine Learning', 'Docker', 'FastAPI'], 'preferred': ['PyTorch', 'AWS', 'Git'], 'description': 'Build, deploy and maintain machine learning services and APIs.'}, 'Data Analyst': {'required': ['SQL', 'Python', 'Excel'], 'preferred': ['Power BI', 'Tableau', 'Statistics'], 'description': 'Analyze datasets, build dashboards, and communicate business insights.'}}
job_template = st.sidebar.selectbox(
    'Load demo job',
    list(SAMPLE_JOBS.keys()),
    key="demo_job_selector"
)
job_title=st.sidebar.text_input('Job title',job_template)
required=st.sidebar.multiselect('Required skills',TAXONOMY,default=SAMPLE_JOBS[job_template]['required'])
preferred=st.sidebar.multiselect('Preferred skills',TAXONOMY,default=SAMPLE_JOBS[job_template]['preferred'])
job_desc=st.sidebar.text_area('Job description',SAMPLE_JOBS[job_template]['description'])
files=st.sidebar.file_uploader('Upload resumes (PDF/TXT)',accept_multiple_files=True,type=['pdf','txt','docx'])

c1,c2,c3=st.columns(3)
c1.metric('Demo candidates',len(DEMO)); c2.metric('Required skills',len(required)); c3.metric('Preferred skills',len(preferred))
tabs = st.tabs([
    "Candidate Ranking",
    "Resume Analyzer",
    "Analytics",
    "Methodology",
    "Batch Screening",
    "Screening History"
])
with tabs[0]:
 st.subheader(f'Candidates for: {job_title}')
 candidates=DEMO.copy()
 if files:
  for f in files:
   text=''
   if f.name.lower().endswith('.txt'):
    text=f.getvalue().decode('utf-8',errors='ignore')
   elif f.name.lower().endswith('.docx'):
    try:
     from docx import Document
     import io
     doc=Document(io.BytesIO(f.getvalue())); text=' '.join(p.text for p in doc.paragraphs)
    except Exception as e: st.warning(f'Could not parse {f.name}: {e}')
   elif f.name.lower().endswith('.docx'):
    try:
     from docx import Document
     import io
     doc=Document(io.BytesIO(f.getvalue())); text=' '.join(p.text for p in doc.paragraphs)
    except Exception as e: st.warning(f'Could not parse {f.name}: {e}')
   else:
    try:
     import fitz
     doc=fitz.open(stream=f.getvalue(),filetype='pdf'); text=' '.join(p.get_text() for p in doc)
    except Exception as e: st.warning(f'Could not parse {f.name}: {e}')
   skills=extract_skills(text,TAXONOMY)
   candidates.append({'name':f.name,'skills':skills,'experience':'Not extracted','projects':'Extracted resume text','resume_text':text})
 job_context = "\n".join([
     f"Job title: {job_title}",
     f"Job description: {job_desc}",
     f"Required skills: {', '.join(required)}",
     f"Preferred skills: {', '.join(preferred)}",
 ])
 candidate_texts = [
     "\n".join(
         part
         for part in [
             f"Resume: {candidate.get('resume_text', '')}",
             f"Skills: {', '.join(candidate['skills'])}",
             f"Experience: {candidate['experience']}",
             f"Projects: {candidate['projects']}",
         ]
         if part.strip()
     )
     for candidate in candidates
 ]
 semantic_signature = hashlib.sha256(
     json.dumps(
         [job_context, candidate_texts],
         ensure_ascii=False,
     ).encode("utf-8")
 ).hexdigest()
 st.caption(
     "Semantic similarity is an optional text-relevance signal; "
     "it does not replace the skill-coverage score."
 )
 if st.button("Calculate semantic matches", key="calculate_semantic_matches"):
     with st.spinner("Loading the semantic model and comparing profiles..."):
         semantic_scores = semantic_analysis(job_context, candidate_texts)
     st.session_state["semantic_match_results"] = {
         "signature": semantic_signature,
         "scores": semantic_scores,
     }
 cached_semantic = st.session_state.get("semantic_match_results")
 semantic_scores = None
 if cached_semantic:
     if cached_semantic["signature"] == semantic_signature:
         semantic_scores = cached_semantic["scores"]
     else:
         st.info("Job details or candidate profiles changed. Recalculate semantic matches.")
 rows=[]
 for index,cand in enumerate(candidates):
  res=score_match(cand['skills'],required,preferred)
  row={'Candidate':cand['name'],'Score (%)':res['score'],'Matched Required':', '.join(res['matched_required']),'Missing Required':', '.join(res['missing_required']),'Preferred Match':', '.join(res['matched_preferred']),'Experience':cand['experience'],'Projects':cand['projects'],'Skills':cand['skills']}
  if semantic_scores is not None:
   row['Semantic Match (%)']=semantic_scores[index]
  rows.append(row)
 df=pd.DataFrame(rows).sort_values('Score (%)',ascending=False)
 display_columns=['Candidate','Score (%)','Matched Required','Missing Required','Preferred Match','Experience']
 if 'Semantic Match (%)' in df.columns:
  display_columns.insert(2,'Semantic Match (%)')
 st.dataframe(df[display_columns],width='stretch',hide_index=True)
 pick=st.selectbox('Inspect candidate',df['Candidate'].tolist())
 r=df[df['Candidate']==pick].iloc[0]
 st.markdown(f'### {pick} — {r["Score (%)"]}% compatibility (decision-support only)')
 st.write('**Matched required skills:**',r['Matched Required'] or 'None identified')
 st.write('**Missing required skills:**',r['Missing Required'] or 'None identified')
 st.write('**Preferred skills evidenced:**',r['Preferred Match'] or 'None identified')
 st.write('**Resume skills detected:**',', '.join(r['Skills']))
 semantic_score = r.get('Semantic Match (%)')
 with st.expander("Explainable match details"):
  explanation = generate_explanation(
      evaluate_candidate(r['Skills'],required,preferred),
      semantic_score=semantic_score,
  )
  for item in explanation:
   st.write(f"- {item}")
 st.info('Scores reflect skill overlap only. They are not a validated prediction of job performance and should not be used for automatic rejection.')
with tabs[1]:
    st.subheader("Resume / Text Skill Analyzer")

    txt = st.text_area(
        "Paste resume text here",
        height=220,
        placeholder="Paste candidate resume content..."
    )

    required_input = st.text_input(
        "Required skills (comma-separated)",
        placeholder="Python, SQL, Machine Learning"
    )

    preferred_input = st.text_input(
        "Preferred skills (comma-separated)",
        placeholder="Pandas, Git, Power BI"
    )
    include_semantic = st.checkbox(
        "Include semantic similarity",
        help="Compares the pasted resume with the job description in the sidebar. This score is not a probability.",
    )

    if st.button("Evaluate Candidate", key="extract"):
        if not txt.strip():
            st.warning("Please paste resume text.")
        elif not required_input.strip():
            st.warning("Enter at least one required skill.")
        else:
            found = extract_skills(txt, TAXONOMY)

            required = [
                s.strip() for s in required_input.split(",")
                if s.strip()
            ]

            preferred = [
                s.strip() for s in preferred_input.split(",")
                if s.strip()
            ]

            result = evaluate_candidate(
                found,
                required,
                preferred
            )
            semantic_score = None
            if include_semantic:
                analyzer_job_context = "\n".join(
                    [
                        f"Job title: {job_title}",
                        f"Job description: {job_desc}",
                        f"Required skills: {required_input}",
                        f"Preferred skills: {preferred_input}",
                    ]
                )
                with st.spinner("Loading the semantic model and comparing text..."):
                    semantic_score = semantic_analysis(
                        analyzer_job_context,
                        [txt],
                    )[0]

            st.markdown("### Candidate Evaluation")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Overall Skills Score",
                f"{result['overall_score']}%"
            )

            col2.metric(
                "Required Skills",
                f"{result['required_score']}%"
            )

            col3.metric(
                "Preferred Skills",
                f"{result['preferred_score']}%"
            )

            st.progress(
                min(result["overall_score"] / 100, 1.0)
            )

            st.markdown(
                f"### {result['recommendation']}"
            )

            st.success(
                "Matched required skills: "
                + (", ".join(result["matched_required"])
                   or "None")
            )

            st.info(
                "Matched preferred skills: "
                + (", ".join(result["matched_preferred"])
                   or "None")
            )

            st.error(
                "Missing required skills: "
                + (", ".join(result["missing_required"])
                   or "None")
            )

            st.warning(
                "Missing preferred skills: "
                + (", ".join(result["missing_preferred"])
                   or "None")
            )

            st.caption(
                "This score measures skill coverage only. "
                "It is not a validated prediction of job performance."
            )
            with st.expander("Explainable evaluation"):
                for item in generate_explanation(
                    result,
                    semantic_score=semantic_score,
                ):
                    st.write(f"- {item}")
with tabs[2]:
 st.subheader('Screening analytics')
 if 'df' in locals():
  st.bar_chart(df.set_index('Candidate')['Score (%)'])
  st.write('Ranked candidate count:',len(df))
  st.download_button('Download screening results CSV',df.drop(columns=['Skills','Projects']).to_csv(index=False),'screening_results.csv','text/csv')
 if "batch_df" in st.session_state:
     df = st.session_state["batch_df"]

     if not df.empty:
         insights = get_recruiter_insights(df)

         st.subheader("Recruiter Intelligence")

         c1, c2, c3, c4 = st.columns(4)

         c1.metric("Candidates", insights["total_candidates"])
         c2.metric("Average Match", f'{insights["average_score"]}%')
         c3.metric("Top Match", f'{insights["top_score"]}%')
         c4.metric(
             "Qualification Rate",
             f'{insights["qualification_rate"]}%'
         )

         st.subheader("Candidate Score Distribution")

         distribution = get_score_distribution(df)
         st.bar_chart(distribution)

         st.subheader("Ranked Candidate Comparison")

         ranked = compare_candidates(df)

         st.dataframe(
             ranked,
             width="stretch",
             hide_index=True
         )
with tabs[3]:
 st.markdown('''### Matching methodology\n- Skill aliases are normalized (for example ML → Machine Learning).\n- Required skills contribute up to 80 points.\n- Preferred skills contribute up to 20 points.\n- Optional semantic matching compares job and candidate text using Sentence Transformer embeddings.\n- Semantic similarity is shown separately and does not change the weighted skills score.\n- Scores are decision-support signals, not hiring predictions; human review is required.\n- Demo profiles are synthetic.''')
 st.code('Score = Required Skill Coverage × 80 + Preferred Skill Coverage × 20')

with tabs[4]:
    st.subheader("Batch Resume Screening")

    uploaded_files = st.file_uploader(
        "Upload multiple resumes",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

    if uploaded_files and st.button("Run Batch Screening"):
        batch_df = screen_uploaded_resumes(
            uploaded_files,
            TAXONOMY,
            required,
            preferred
        )

        if not batch_df.empty:
            batch_df = batch_df.sort_values(
                "Score (%)",
                ascending=False
            ).reset_index(drop=True)

            batch_df.insert(0, "Rank", range(1, len(batch_df) + 1))

            st.session_state["batch_df"] = batch_df
            save_screening(batch_df)
            st.success("Screening results saved to database!")

    if "batch_df" in st.session_state:
        batch_df = st.session_state["batch_df"]

        st.dataframe(batch_df)

        st.bar_chart(
            batch_df.set_index("Candidate")["Score (%)"]
        )

        st.download_button(
            "Download CSV",
            batch_df.to_csv(index=False),
            "HireSense_results.csv",
            "text/csv"
        )

with tabs[5]:
    st.header("Screening History")

    history = get_screening_history()

    if history.empty:
        st.info("No saved screening records yet.")
    else:
        c1, c2 = st.columns(2)

        c1.metric("Stored Records", len(history))
        c2.metric(
            "Average Score",
            f"{history['score'].mean():.2f}%"
        )

        st.dataframe(history, width="stretch")

        st.download_button(
            "Download History CSV",
            history.to_csv(index=False).encode("utf-8"),
            "HireSense_screening_history.csv",
            "text/csv"
        )
        st.divider()

st.subheader("Responsible AI & Fairness")

st.info(
    "HireSense AI is a decision-support tool and not an automated hiring "
    "decision system. Matching scores reflect skills alignment based on "
    "the provided job requirements. Recruiters must independently review "
    "candidate qualifications and avoid using scores as the sole basis "
    "for hiring or rejection."
)

st.caption(
    "The system does not validate job performance or guarantee "
    "fairness across candidate groups."
)



st.divider()
st.header("🤖 Recruiter Intelligence Assistant")

if "batch_results" in st.session_state and st.session_state["batch_results"] is not None:

    df = st.session_state["batch_results"]

    if not df.empty:
        st.success("Batch screening data detected!")

        candidate_column = next(
            (c for c in df.columns if c.lower() in ["candidate", "name", "candidate name"]),
            None
        )

        if candidate_column:
            selected_candidate = st.selectbox(
                "Select Candidate",
                df[candidate_column].astype(str).tolist()
            )

            candidate_row = df[
                df[candidate_column].astype(str) == selected_candidate
            ].iloc[0]

            skill_column = next(
                (c for c in df.columns if c.lower() in ["skills", "extracted skills", "candidate skills", "matched skills"]),
                None
            )

            if skill_column:
                raw_skills = candidate_row[skill_column]
                if isinstance(raw_skills, list):
                    candidate_skills = raw_skills
                else:
                    candidate_skills = [
                        s.strip() for s in str(raw_skills).replace(";", ",").split(",")
                        if s.strip()
                    ]
            else:
                candidate_skills = []

            job_skills_input = st.text_input(
                "Job Requirements (comma-separated)",
                placeholder="Python, SQL, Machine Learning, Docker"
            )

            if st.button("Generate Candidate Insights"):
                job_skills = [
                    s.strip() for s in job_skills_input.split(",")
                    if s.strip()
                ]

                if not candidate_skills or not job_skills:
                    st.warning("Candidate skills or job skills are missing.")
                else:
                    insights = generate_recruiter_insights(
                        {"skills": candidate_skills},
                        job_skills
                    )

                    st.subheader("Matched Skills")
                    st.write(insights["matched_skills"])

                    st.subheader("Missing Skills")
                    st.write(insights["missing_skills"])

                    st.subheader("Strengths")
                    for item in insights["strengths"]:
                        st.write("•", item)

                    st.subheader("Development Areas")
                    for item in insights["development_areas"]:
                        st.write("•", item)

                    st.subheader("Interview Questions")
                    for i, question in enumerate(
                        insights["interview_questions"], 1
                    ):
                        st.write(f"{i}. {question}")
    else:
        st.info("Batch screening results are empty.")

else:
    st.info("Run batch screening first to unlock recruiter insights.")



st.divider()
st.header("📊 Candidate Comparison")

if "batch_results" in st.session_state and st.session_state["batch_results"] is not None:

    comparison_df = st.session_state["batch_results"]

    if not comparison_df.empty:

        candidate_col = next(
            (c for c in comparison_df.columns
             if c.lower() in ["candidate", "candidate name", "name"]),
            None
        )

        score_col = next(
            (c for c in comparison_df.columns
             if "score" in c.lower() and "%" in c),
            None
        )

        if candidate_col and score_col:

            candidate_list = comparison_df[candidate_col].astype(str).tolist()

            selected = st.multiselect(
                "Select up to 3 candidates",
                candidate_list,
                max_selections=3
            )

            if selected:
                selected_df = comparison_df[
                    comparison_df[candidate_col].astype(str).isin(selected)
                ].copy()

                st.subheader("Comparison Table")
                st.dataframe(selected_df, use_container_width=True)

                st.subheader("Score Comparison")

                chart_df = selected_df.set_index(candidate_col)[score_col]
                st.bar_chart(chart_df)

                st.subheader("Ranking")

                ranked = selected_df.sort_values(
                    score_col, ascending=False
                )

                for i, (_, row) in enumerate(ranked.iterrows(), 1):
                    st.write(
                        f"**{i}. {row[candidate_col]}** — "
                        f"{row[score_col]}%"
                    )

        else:
            st.warning(
                "Candidate name or score columns could not be detected."
            )

    else:
        st.info("Screen candidates first to compare them.")

else:
    st.info("Run batch screening first to enable candidate comparison.")
