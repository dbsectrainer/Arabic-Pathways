class LessonDay {
  final int dayNumber;
  final String title;
  final String arabicContent;
  final String transliterationContent;
  final String englishContent;
  final String arabicAudioPath;
  final String englishAudioPath;
  final String? videoId;
  final String level;

  LessonDay({
    required this.dayNumber,
    required this.title,
    required this.arabicContent,
    required this.transliterationContent,
    required this.englishContent,
    required this.arabicAudioPath,
    required this.englishAudioPath,
    this.videoId,
    required this.level,
  });

  String get levelName {
    if (dayNumber <= 7) return 'Level 1: Foundations';
    if (dayNumber <= 14) return 'Level 2: Essential Daily Phrases';
    if (dayNumber <= 22) return 'Level 3: Cultural & Social';
    if (dayNumber <= 30) return 'Level 4: Professional Communication';
    return 'Level 5: Advanced Fluency';
  }

  String get levelColor {
    if (dayNumber <= 7) return '#4A90E2';
    if (dayNumber <= 14) return '#50C878';
    if (dayNumber <= 22) return '#FF6B6B';
    if (dayNumber <= 30) return '#9B59B6';
    return '#F39C12';
  }
}
