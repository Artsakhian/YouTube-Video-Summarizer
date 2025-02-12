# YouTube-Video-Summarizer
<<<<<<< HEAD
This project is a Streamlit-based web application that provides a summary of YouTube videos using Gemini as the LLM. The app allows users to input a YouTube video URL, choose a summarization mode (abstract or deep), and specify the output language. The app then generates an explanation of the video.
=======
========================

This project is a Streamlit-based web application that provides a summary of YouTube videos using Gemini as the LLM. The app allows users to input a YouTube video URL, choose a summarization mode (abstract or deep), and specify the output language. The app then generates an explanation of the video.

Features
--------

*   Summarize YouTube videos in multiple languages.
    
*   Choose between abstract and deep summarization modes.
    
*   User-friendly interface powered by Streamlit.
    

Installation
------------

1.  git clone cd youtube-video-summarizer
    
2.  python3 -m transcript_env venvsource venv/bin/activate # On Windows: transcript_env\\Scripts\\activate
    
3.  pip install -r requirements.txt #Optional (should be done if problems with packages will be occured.)
    
4.  GEMINI\_API\_KEY1=your\_api\_key
    

Usage
-----

1.  streamlit run summarizer.py
    
2.  Open the URL provided by Streamlit in your browser.
    
3.  Input the following:
    
    *   YouTube video URL.
        
    *   Summarization mode (abstract or deep).
        
    *   Desired output language.
        
4.  Click the **Summarize** button to receive the summary.
    

Technologies Used
-----------------

*   Python
    
*   Streamlit
    
*   Gemini API
    
*   Virtual Environment for package management
    

Example
-------

*   **Input**: YouTube video URL, "Deep" summarization mode, output language "English."
    
*   **Output**: A detailed summary of the video in English.
    

Contribution
------------

Feel free to submit pull requests to improve the app or add new features. Ensure your changes pass existing tests and add new tests if required.
>>>>>>> 7e71c28 (Initial commit)
