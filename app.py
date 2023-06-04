import streamlit as st
from video_comments import video_comments
from summarize import summarize
from word_freq import WordFreq

def refresh_page():
    st.experimental_rerun()

def process_form():
    video_link = st.text_input("Video link")
    num_sent = st.number_input("Number of summary sentences:")
    num_word = st.number_input("Number of important words:")
    
    if st.button("Submit"):
        if num_sent.is_integer() and num_sent >= 0:
            num_sent = int(num_sent)
            if len(video_link) > 0:
                vc = video_comments()
                video_id = vc.get_video_id(video_link)
                comments = vc.get_comments(video_id)
                count = vc.count
                sum = summarize(n=num_sent)
                extractive_summary = sum.extractive(comments)


                word_freq = WordFreq()
                text = extractive_summary
                image_path = word_freq.generate_word_cloud(text, int(num_word))
                st.image(image_path, caption="Word frequency chart")

                
                # abstractive_summary = sum.abstractive()
                abstractive_summary = "Not available with this version."
                
                st.title("Comment Summarization")
                st.write(f"Video id: {video_id}")
                st.write(f"Total {count} comments extracted")
                
                st.title("Abstractive Summary")
                st.write(abstractive_summary)
                
                st.title("Extractive Summary")
                st.write(extractive_summary)
                

            else:
                st.error("Please provide a valid link.")
        else:
            st.error("Please provide a non-negative integer value for the number of summary sentences.")

st.set_page_config(page_title="Youtube Comment Summarizer")

st.write("# Youtube Comment Summarizer")

refresh_button = st.button("Refresh")
if refresh_button:
    refresh_page()

process_form()
