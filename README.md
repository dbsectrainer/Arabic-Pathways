# Arabic Pathways

[![CI](https://github.com/dbsectrainer/Arabic-Pathways/actions/workflows/python-ci.yml/badge.svg)](https://github.com/dbsectrainer/Arabic-Pathways/actions/workflows/python-ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A focused Modern Standard Arabic learning platform designed to take learners from foundational script and pronunciation to advanced professional fluency over a 40-day journey. The program offers modular daily lessons through interactive audio‑visual materials, YouTube video demonstrations, real‑world conversation practice, and culturally relevant topics—ideal for travelers, professionals, and global citizens.

**Now available as a Flutter mobile application!** 📱

## Technical Skills Demonstrated

### Flutter/Mobile Development
- Cross-platform mobile application (iOS & Android) using Flutter & Dart
- Native performance with smooth animations and transitions
- Offline-first architecture with local asset management
- Material Design UI with custom theming and RTL support

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

### Flutter Application
- `lib/`: Flutter/Dart source code
  - `main.dart`: Application entry point
  - `models/`: Data models (LessonDay, SupplementaryContent, VideoInfo)
  - `screens/`: UI screens (Dashboard, Lesson, Supplementary)
  - `services/`: Business logic (ContentService, ProgressService)
  - `utils/`: Utilities (AppTheme, constants)
- `pubspec.yaml`: Flutter project configuration and dependencies
- `analysis_options.yaml`: Dart/Flutter linting rules

### Assets & Content
- `audio_files/`: MP3 audio files for lessons
  - `supplementary/`: Supplementary audio files
- `text_files/`: Lesson content in three languages
  - `supplementary/`: Supplementary text files
- `videos.json`: YouTube video IDs for each daily lesson
- `videos_supplementary.json`: IDs for supplementary videos

### Content Generation (Python)
- Python content generation scripts:
  - `arabic_phrases_days_01_07.py`: Phrases for days 1-7
  - `arabic_phrases_days_08_14.py`: Phrases for days 8-14
  - `arabic_phrases_days_15_22.py`: Phrases for days 15-22
  - `arabic_phrases_days_23_30.py`: Phrases for days 23-30
  - `arabic_phrases_days_31_40.py`: Phrases for days 31-40
  - `arabic_phrases_supplementary.py`: Supplementary phrases
  - `video_search.py`: Tool for searching relevant videos
- `requirements.txt`: Python package dependencies

### Legacy Web Version
- `index.html`, `day.html`, `supplementary.html`: Original web interface
- `css/`: Web stylesheets
- `js/`: Web JavaScript files

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

### Flutter Application Setup

#### Requirements
- Flutter SDK 3.0.0 or higher
- Dart SDK 3.0.0 or higher
- Android Studio / Xcode (for mobile deployment)
- An emulator or physical device

#### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/dbsectrainer/Arabic-Pathways.git
   cd Arabic-Pathways
   ```

2. Install Flutter dependencies:
   ```bash
   flutter pub get
   ```

3. Run the app:
   ```bash
   # On a connected device or emulator
   flutter run

   # For specific platforms
   flutter run -d android
   flutter run -d ios
   ```

#### Building for Production
```bash
# Android APK
flutter build apk

# Android App Bundle
flutter build appbundle

# iOS
flutter build ios
```

### Content Generation (Python)

#### Requirements
- Python 3.12+
- Required Python packages:
  ```bash
  pip install gtts edge-tts pandas
  ```

#### Generate Lessons
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

### Legacy Web Version
Open `index.html` in any modern browser—no server setup required.

## Usage Guide
1. Launch the app and view the dashboard with all 40 days
2. Select any day to start learning
3. Switch between Arabic, transliteration, and English views
4. Listen to native Arabic pronunciation and English explanations
5. Watch embedded YouTube videos for visual learning
6. Mark lessons complete to track your progress
7. Access supplementary content for additional practice

## Features

### Mobile App Features
- **Offline Support**: All lessons and audio work without internet
- **Progress Tracking**: Track completed lessons with persistent storage
- **Trilingual Display**: Toggle between Arabic, transliteration, and English
- **Audio Playback**: Built-in audio player for pronunciation practice
- **Video Integration**: Embedded YouTube videos for each lesson
- **Responsive Design**: Works on phones and tablets
- **RTL Support**: Proper right-to-left text rendering for Arabic

## Running Tests
```bash
# Python tests
pytest

# Flutter tests
flutter test
```

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
