import 'package:flutter/material.dart';

class AppTheme {
  static const Color primaryColor = Color(0xFF4A90E2);
  static const Color secondaryColor = Color(0xFF50C878);
  static const Color accentColor = Color(0xFFFF6B6B);
  static const Color purpleColor = Color(0xFF9B59B6);
  static const Color orangeColor = Color(0xFFF39C12);

  static ThemeData get lightTheme {
    return ThemeData(
      primaryColor: primaryColor,
      scaffoldBackgroundColor: Colors.white,
      fontFamily: 'Poppins',
      colorScheme: const ColorScheme.light(
        primary: primaryColor,
        secondary: secondaryColor,
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: primaryColor,
        foregroundColor: Colors.white,
        elevation: 0,
        centerTitle: true,
        titleTextStyle: TextStyle(
          fontFamily: 'Poppins',
          fontSize: 20,
          fontWeight: FontWeight.bold,
          color: Colors.white,
        ),
      ),
      cardTheme: CardTheme(
        elevation: 4,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryColor,
          foregroundColor: Colors.white,
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),
      textTheme: const TextTheme(
        displayLarge: TextStyle(
          fontSize: 32,
          fontWeight: FontWeight.bold,
          color: Colors.black87,
        ),
        displayMedium: TextStyle(
          fontSize: 24,
          fontWeight: FontWeight.bold,
          color: Colors.black87,
        ),
        bodyLarge: TextStyle(
          fontSize: 16,
          color: Colors.black87,
        ),
        bodyMedium: TextStyle(
          fontSize: 14,
          color: Colors.black87,
        ),
      ),
    );
  }

  static Color getLevelColor(int dayNumber) {
    if (dayNumber <= 7) return primaryColor;
    if (dayNumber <= 14) return secondaryColor;
    if (dayNumber <= 22) return accentColor;
    if (dayNumber <= 30) return purpleColor;
    return orangeColor;
  }

  static String getLevelName(int dayNumber) {
    if (dayNumber <= 7) return 'Level 1: Foundations';
    if (dayNumber <= 14) return 'Level 2: Essential Daily Phrases';
    if (dayNumber <= 22) return 'Level 3: Cultural & Social';
    if (dayNumber <= 30) return 'Level 4: Professional Communication';
    return 'Level 5: Advanced Fluency';
  }
}
