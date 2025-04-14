import os
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import streamlit as st 
from googletrans import Translator, LANGUAGES
import time


GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)

# Function to extract video ID from YouTube URL
def extract_video_id(youtube_url):
    try:
        if "youtube.com" in youtube_url:
            return youtube_url.split("v=")[1].split("&")[0]
        elif "youtu.be" in youtube_url:
            return youtube_url.split("/")[-1]
        else:
            return None
    except IndexError:
        return None

# Function to fetch transcript
def fetch_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # Combine all transcript text
        full_transcript = " ".join([entry['text'] for entry in transcript])
        return full_transcript
    except Exception:
        return None

# Function to split large text into smaller chunks
def chunk_text(text, max_length=5000):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(" ".join(current_chunk)) + len(word) + 1 <= max_length:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

# Function to summarize transcript with mode handling
def summarize_transcript(transcript, mode):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        chunks = chunk_text(transcript)
        chunk_summaries = []

        for chunk in chunks:
            prompt = (
                f"Provide a brief summary of the following youtube video transcription:\n{chunk}"
                if mode == "abstract"
                else f"Provide a detailed explanation of the following youtube video transcription:\n{chunk}"
            )
            response = model.generate_content(prompt)
            chunk_summaries.append(response.text)
            time.sleep(2)

        # Summarize all chunk summaries into a final summary
        combined_summary = " ".join(chunk_summaries)
        final_prompt = (
            "Summarize the following text briefly:\n" + combined_summary
            if mode == "abstract"
            else "Summarize the following text in detail:\n" + combined_summary
        )
        final_response = model.generate_content(final_prompt)
        return final_response.text  
    except Exception as e:
        return f"Error summarizing transcript: {e}"


# Function to translate text into target language
def translate_text(text, target_language):
    if target_language == "Original":  # No translation needed
        return
    try:
        translator = Translator()
        if text:
            assert isinstance(text, str), "Text must be a string."
            # Translate the text
            translated_text = translator.translate(text, dest=target_language).text
            return translated_text
        else:
            return "Error: No text provided for translation."
    except Exception as e:
        return f"Error translating text: {e}"

# Streamlit App
def main():
    st.title("YouTube Video Summarizer")

    # Input field for YouTube video URL
    youtube_url = st.text_input("Enter a YouTube video URL", "")

    # Initialize session state
    if "mode" not in st.session_state:
        st.session_state.mode = None
    if "language" not in st.session_state:
        st.session_state.language = "Original"

    # Mode selection buttons
    st.session_state.mode = st.radio(
        "Choose summarization mode:", 
        options=["Abstract", "Deep"], 
        index=0 if st.session_state.mode is None else ["Abstract", "Deep"].index(st.session_state.mode)
    )
    
    st.session_state.language = st.selectbox(
        "Choose the language for the summary",
        ["Original"] + [LANGUAGES[code].capitalize() for code in LANGUAGES.keys()],
        index=0  # Default to "Original"
    )  
    
        
    if st.button("Summarize"):
        video_id = extract_video_id(youtube_url)
        if video_id:
            # with st.spinner("Fetching transcript..."):
            transcript = fetch_youtube_transcript(video_id)

            if transcript:
                # st.write("✅ Transcript fetched successfully!")
                with st.spinner(f"Generating summary in {st.session_state.mode} mode..."):
                    summary = summarize_transcript(transcript, st.session_state.mode)
                
                # st.write("✅ Summary generated successfully!")
                st.subheader("Summary:")
                st.write(summary)
                summary = str(summary)  # Ensure summary is a string for translation
                
                # Translate transcript if needed
                if st.session_state.language != "Original":  
                    st.write("\n\n\n")                  
                    with st.spinner(f"Translating language: {st.session_state.language}"):
                        translated_summary = translate_text(summary, st.session_state.language.lower())
                        # st.write(f"✅Summary translated to **{st.session_state.language}**")
                                
                    st.subheader("Translated summary:")
                    st.write(translated_summary)      
                
            else:
                st.error("Could not fetch transcript for the given video. Please try another video.")
        else:
            st.error("Invalid YouTube URL. Please enter a valid URL.")

if __name__ == "__main__":
    main()
