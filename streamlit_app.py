import streamlit as st
import os

# Directory to save uploaded songs
SONG_DIR = "uploaded_songs"

# Ensure the directory exists
if not os.path.exists(SONG_DIR):
    os.makedirs(SONG_DIR)

# Load songs from the directory
def load_songs_from_directory():
    songs = []
    for filename in os.listdir(SONG_DIR):
        file_path = os.path.join(SONG_DIR, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                songs.append({'name': filename, 'file': f.read()})
    return songs

# Initialize session state for storing the library
if 'library' not in st.session_state:
    st.session_state.library = load_songs_from_directory()

def main():
    st.title("Persistent Music Listening Platform")

    # Upload multiple music files
    st.header("Upload Music Files")
    uploaded_files = st.file_uploader("Choose music files", type=["mp3", "wav", "ogg"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                # Save the uploaded file to disk
                file_path = os.path.join(SONG_DIR, uploaded_file.name)
                with open(file_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                
                # Update the session state library
                st.session_state.library.append({
                    'name': uploaded_file.name,
                    'file': uploaded_file.getvalue()
                })
                st.success(f"Uploaded and saved {uploaded_file.name} successfully!")
            except Exception as e:
                st.error(f"An error occurred with {uploaded_file.name}: {e}")

    # Display the music library
    if st.session_state.library:
        st.header("Your Music Library")
        for index, song in enumerate(st.session_state.library):
            st.subheader(f"Track {index + 1}: {song['name']}")
            st.audio(song['file'], format="audio/mp3")

    # Optionally, clear the library
    if st.button('Clear Library'):
        st.session_state.library.clear()
        for filename in os.listdir(SONG_DIR):
            os.remove(os.path.join(SONG_DIR, filename))
        st.success("Library cleared!")

if __name__ == "__main__":
    main()
