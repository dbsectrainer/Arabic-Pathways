# Arabic Pathways

## Overview

A focused Modern Standard Arabic learning platform designed to take learners from foundational script and pronunciation to advanced professional fluency over a 40-day journey. The program offers modular daily lessons through interactive audio‑visual materials, YouTube video demonstrations, real‑world conversation practice, and culturally relevant topics—ideal for travelers, professionals, and global citizens.

## Technical Skills Demonstrated

### Web Development
- Interactive, responsive web interface using HTML5, CSS3, and modern JavaScript
- Dynamic content updates and micro‑interactions for enhanced user engagement
- YouTube API integration for embedded instructional videos
- Mobile‑first responsive design using media queries and grid layouts

### Python Development
- Automated content generation scripts for lesson materials
- Efficient audio file processing (Arabic text‑to‑speech)
- Asynchronous programming for optimized performance

### Educational Technology
- Structured 40-day curriculum design with progressive learning paths
- Interactive learning tools and progress tracking systems
- Multimedia content integration (text, audio, video, interactive exercises)
- Curated YouTube content for visual learning reinforcement

### Multilingual Support
- Trilingual content management (Arabic script, transliteration, English)
- Dynamic language switching functionality
- Cultural context integration throughout lessons

### User Experience Design
- Progress tracking with completion badges
- Offline‑capable web application
- Persistent user preferences and progress storage
- Intuitive navigation and learning flow

### Audio Processing
- Dual‑language audio content (English explanations + native Arabic pronunciation)
- Custom audio playback controls
- Dialect variation support in advanced modules (e.g., Levantine, Egyptian)

## Project Structure

- `index.html`: Main dashboard with daily progress overview
- `day.html`: Daily lesson interface with audio, text, and exercises
- `supplementary.html`: Additional learning resources and practice materials
- `css/`: Stylesheets for the web interface
  - `styles.css`: Main stylesheet
  - `video-player.css`: Styles for the YouTube video player
  - `native-speaker.css`: Styles for native speaker content
- `js/`: JavaScript functionality and interactive features
  - `script.js`: Core application logic
  - `video-loader.js`: Loads YouTube videos for lessons
  - `video-loader-supplementary.js`: Loads supplementary YouTube videos
- `audio_files/`:
  - Supplementary audio files in `supplementary/`
- `text_files/`:
  - Supplementary text files in `supplementary/`
- `videos.json`: YouTube video IDs for each daily lesson
- `videos_supplementary.json`: IDs for supplementary videos
- Python content generation scripts:
  - `arabic_phrases_days_01_07.py`: Phrases for days 1-7
  - `arabic_phrases_days_08_14.py`: Phrases for days 8-14
  - `arabic_phrases_days_15_22.py`: Phrases for days 15-22
  - `arabic_phrases_days_23_30.py`: Phrases for days 23-30
  - `arabic_phrases_days_31_40.py`: Phrases for days 31-40
  - `arabic_phrases_supplementary.py`: Supplementary phrases
  - `video_search.py`: Tool for searching relevant videos
- `requirements.txt`: Python package dependencies

## Course Structure (40 Days)

### Foundations (Days 1–7)
- Arabic alphabet: letters, shapes, and handwriting
- Vowel marks (Harakat) and pronunciation basics
- Simple greetings, numbers, and time expressions

### Essential Daily Phrases (Days 8–14)
- Shopping, transportation, dining, and asking for directions
- Basic sentence patterns and grammar fundamentals
- Survival Arabic phrases for travelers

### Cultural Context & Social Interaction (Days 15–22)
- Family and social customs in Arabic‑speaking cultures
- Major festivals, traditions, and etiquette
- Everyday conversation in social settings

### Formal & Professional Communication (Days 23–30)
- Workplace vocabulary and business etiquette
- Formal correspondence: emails, reports, and presentations
- Online meetings and negotiation phrases

### Advanced Fluency & Real‑World Use (Days 31–40)
- Arabic idioms, proverbs, and colloquialisms
- Debates, storytelling, and persuasive speaking
- Dialect exposure: common Levantine and Egyptian expressions
- Contemporary media: news articles, podcasts, and videos
- Academic and technical Arabic terminology

## Features

### Interactive Learning Interface
- Dual audio tracks and interactive transcripts (Arabic script, transliteration, English)
- Daily progress tracker with completion badges
- Mobile‑friendly, offline‑capable web interface

### YouTube Video Integration
- Curated videos corresponding to each daily lesson
- Native speaker demonstrations and cultural insights
- Visual reinforcement of script and pronunciation
- Automatic video loading based on the day

### Arabic‑Specific Tools
- Script tracing and handwriting practice modules
- Harakat placement and vowel drills
- Dialect variation exercises for regional fluency
- Embedded cultural tips and context notes

## Why Arabic?

### Global Importance
- Spoken by over 400 million people worldwide
- Gateway to understanding Middle Eastern and North African markets

### Career & Business Edge
- High demand in diplomacy, energy, finance, and technology sectors
- Opens doors in international organizations, NGOs, and academia

### Cultural & Intellectual Access
- Direct access to rich literary, historical, and religious texts
- Deeper insight into regional geopolitics and cultural dynamics

## Development Setup

### Requirements
- Python 3.12+
- Required Python packages:
  ```bash
  pip install gtts edge-tts pandas
  ```

### Generate Lessons
```bash
# Generate content for days 1-40
python arabic_phrases_days_01_07.py
python arabic_phrases_days_08_14.py
python arabic_phrases_days_15_22.py
python arabic_phrases_days_23_30.py
python arabic_phrases_days_31_40.py

# Generate supplementary content
python arabic_phrases_supplementary.py
```

### Run the Site
Open `index.html` in any modern browser—no server setup required.

## Usage Guide
1. Launch the dashboard and select your current day
2. Listen to English explanations and native Arabic pronunciations
3. Read along with transliteration and Arabic script
4. Complete interactive exercises and script tracing drills
5. Watch YouTube demonstrations for cultural and pronunciation context
6. Earn daily badges and track your fluency progress

## Storage
Uses localStorage to save:
- Completed lessons and last visited day
- Audio playback preferences (e.g., speed, loop)
- Custom notes and bookmarks
