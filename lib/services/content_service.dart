import 'dart:convert';
import 'package:flutter/services.dart';
import '../models/lesson_day.dart';
import '../models/supplementary_content.dart';

class ContentService {
  // Cache for loaded content
  final Map<int, LessonDay> _dayCache = {};
  final Map<String, SupplementaryContent> _supplementaryCache = {};
  Map<String, String>? _videos;
  Map<String, String>? _supplementaryVideos;

  Future<String> _loadTextFile(String path) async {
    try {
      return await rootBundle.loadString(path);
    } catch (e) {
      return '';
    }
  }

  Future<Map<String, String>> _loadVideos() async {
    if (_videos != null) return _videos!;
    try {
      final jsonString = await rootBundle.loadString('videos.json');
      final Map<String, dynamic> decoded = json.decode(jsonString);
      _videos = decoded.map((key, value) => MapEntry(key, value.toString()));
      return _videos!;
    } catch (e) {
      _videos = {};
      return _videos!;
    }
  }

  Future<Map<String, String>> _loadSupplementaryVideos() async {
    if (_supplementaryVideos != null) return _supplementaryVideos!;
    try {
      final jsonString = await rootBundle.loadString('videos_supplementary.json');
      final Map<String, dynamic> decoded = json.decode(jsonString);
      _supplementaryVideos = decoded.map((key, value) => MapEntry(key, value.toString()));
      return _supplementaryVideos!;
    } catch (e) {
      _supplementaryVideos = {};
      return _supplementaryVideos!;
    }
  }

  Future<LessonDay> loadDay(int dayNumber) async {
    if (_dayCache.containsKey(dayNumber)) {
      return _dayCache[dayNumber]!;
    }

    final videos = await _loadVideos();
    final arabicContent = await _loadTextFile('text_files/day${dayNumber}_ar.txt');
    final transliterationContent = await _loadTextFile('text_files/day${dayNumber}_transliteration.txt');
    final englishContent = await _loadTextFile('text_files/day${dayNumber}_en.txt');

    final day = LessonDay(
      dayNumber: dayNumber,
      title: 'Day $dayNumber',
      arabicContent: arabicContent,
      transliterationContent: transliterationContent,
      englishContent: englishContent,
      arabicAudioPath: 'audio_files/day${dayNumber}_ar.mp3',
      englishAudioPath: 'audio_files/day${dayNumber}_en.mp3',
      videoId: videos['day$dayNumber'],
      level: '',
    );

    _dayCache[dayNumber] = day;
    return day;
  }

  Future<List<LessonDay>> loadAllDays() async {
    final days = <LessonDay>[];
    for (int i = 1; i <= 40; i++) {
      days.add(await loadDay(i));
    }
    return days;
  }

  Future<SupplementaryContent> loadSupplementaryContent(String contentId) async {
    if (_supplementaryCache.containsKey(contentId)) {
      return _supplementaryCache[contentId]!;
    }

    final videos = await _loadSupplementaryVideos();
    final arabicContent = await _loadTextFile('text_files/supplementary/${contentId}_ar.txt');
    final transliterationContent = await _loadTextFile('text_files/supplementary/${contentId}_transliteration.txt');
    final englishContent = await _loadTextFile('text_files/supplementary/${contentId}_en.txt');

    final content = SupplementaryContent(
      id: contentId,
      title: _getSupplementaryTitle(contentId),
      arabicContent: arabicContent,
      transliterationContent: transliterationContent,
      englishContent: englishContent,
      arabicAudioPath: 'audio_files/supplementary/${contentId}_ar.mp3',
      englishAudioPath: 'audio_files/supplementary/${contentId}_en.mp3',
      videoId: videos[contentId],
    );

    _supplementaryCache[contentId] = content;
    return content;
  }

  String _getSupplementaryTitle(String id) {
    switch (id) {
      case 'daily_life':
        return 'Daily Life Conversations';
      case 'emotions':
        return 'Emotions & Feelings';
      case 'education':
        return 'Education';
      case 'hobbies':
        return 'Hobbies & Interests';
      case 'comparisons':
        return 'Comparative Phrases';
      default:
        return id;
    }
  }

  List<String> getSupplementaryContentIds() {
    return ['daily_life', 'emotions', 'education', 'hobbies', 'comparisons'];
  }
}
