# Fonts Setup

This Flutter application uses two font families:

## Required Fonts

### 1. Poppins
- Download from [Google Fonts](https://fonts.google.com/specimen/Poppins)
- Required weights:
  - `Poppins-Regular.ttf` (400)
  - `Poppins-Bold.ttf` (700)

### 2. Noto Sans Arabic
- Download from [Google Fonts](https://fonts.google.com/noto/specimen/Noto+Sans+Arabic)
- Required weights:
  - `NotoSansArabic-Regular.ttf` (400)
  - `NotoSansArabic-Bold.ttf` (700)

## Installation

1. Download the font files from the links above
2. Place them in this `fonts/` directory with the exact names listed
3. The fonts should be automatically detected by Flutter via `pubspec.yaml`

## Alternative: System Fonts

If you prefer not to bundle fonts, you can modify `lib/utils/app_theme.dart` to use system fonts instead by removing or commenting out the `fontFamily` properties.

## Font File Structure

After setup, your directory should look like:
```
fonts/
├── README.md (this file)
├── Poppins-Regular.ttf
├── Poppins-Bold.ttf
├── NotoSansArabic-Regular.ttf
└── NotoSansArabic-Bold.ttf
```
