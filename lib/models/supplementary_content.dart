class SupplementaryContent {
  final String id;
  final String title;
  final String arabicContent;
  final String transliterationContent;
  final String englishContent;
  final String arabicAudioPath;
  final String englishAudioPath;
  final String? videoId;

  SupplementaryContent({
    required this.id,
    required this.title,
    required this.arabicContent,
    required this.transliterationContent,
    required this.englishContent,
    required this.arabicAudioPath,
    required this.englishAudioPath,
    this.videoId,
  });
}
