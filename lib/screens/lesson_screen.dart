import 'package:flutter/material.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:youtube_player_flutter/youtube_player_flutter.dart';
import 'package:provider/provider.dart';
import '../models/lesson_day.dart';
import '../services/content_service.dart';
import '../services/progress_service.dart';
import '../services/gamification_service.dart';
import '../utils/app_theme.dart';

class LessonScreen extends StatefulWidget {
  final int dayNumber;

  const LessonScreen({super.key, required this.dayNumber});

  @override
  State<LessonScreen> createState() => _LessonScreenState();
}

class _LessonScreenState extends State<LessonScreen> {
  final ContentService _contentService = ContentService();
  final ProgressService _progressService = ProgressService();
  final AudioPlayer _audioPlayer = AudioPlayer();

  LessonDay? _lesson;
  bool _isLoading = true;
  bool _isCompleted = false;
  String _selectedLanguage = 'arabic';
  bool _isPlayingArabic = false;
  bool _isPlayingEnglish = false;
  YoutubePlayerController? _videoController;
  double _playbackSpeed = 1.0;
  bool _repeatMode = false;

  @override
  void initState() {
    super.initState();
    _loadLesson();
  }

  Future<void> _loadLesson() async {
    final lesson = await _contentService.loadDay(widget.dayNumber);
    final completed = await _progressService.getCompletedDays();

    if (lesson.videoId != null && lesson.videoId!.isNotEmpty) {
      _videoController = YoutubePlayerController(
        initialVideoId: lesson.videoId!,
        flags: const YoutubePlayerFlags(
          autoPlay: false,
          mute: false,
        ),
      );
    }

    setState(() {
      _lesson = lesson;
      _isCompleted = completed.contains(widget.dayNumber);
      _isLoading = false;
    });
  }

  Future<void> _toggleCompletion() async {
    if (_isCompleted) {
      await _progressService.markDayIncomplete(widget.dayNumber);
      setState(() {
        _isCompleted = false;
      });
    } else {
      await _progressService.markDayComplete(widget.dayNumber);

      // Update gamification stats and check for achievements
      final gamificationService =
          Provider.of<GamificationService>(context, listen: false);
      final newAchievements =
          await gamificationService.recordDayCompletion(widget.dayNumber);

      setState(() {
        _isCompleted = true;
      });

      // Show achievement dialog if any were unlocked
      if (newAchievements.isNotEmpty && mounted) {
        _showAchievementDialog(newAchievements);
      }
    }
  }

  void _showAchievementDialog(List<dynamic> achievements) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Row(
          children: [
            Icon(Icons.emoji_events, color: AppTheme.orangeColor, size: 32),
            SizedBox(width: 12),
            Text('Achievement Unlocked!'),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: achievements.map((achievement) {
            return Padding(
              padding: const EdgeInsets.symmetric(vertical: 8),
              child: Row(
                children: [
                  Icon(achievement.icon, color: achievement.color, size: 24),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          achievement.title,
                          style: const TextStyle(fontWeight: FontWeight.bold),
                        ),
                        Text(
                          achievement.description,
                          style: const TextStyle(fontSize: 12),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            );
          }).toList(),
        ),
        actions: [
          ElevatedButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Awesome!'),
          ),
        ],
      ),
    );
  }

  Future<void> _playAudio(String audioPath, bool isArabic) async {
    try {
      await _audioPlayer.stop();
      await _audioPlayer.setPlaybackRate(_playbackSpeed);
      await _audioPlayer.play(AssetSource(audioPath));

      // Record audio play in gamification
      final gamificationService =
          Provider.of<GamificationService>(context, listen: false);
      await gamificationService.recordAudioPlay();

      setState(() {
        if (isArabic) {
          _isPlayingArabic = true;
          _isPlayingEnglish = false;
        } else {
          _isPlayingArabic = false;
          _isPlayingEnglish = true;
        }
      });

      _audioPlayer.onPlayerComplete.listen((_) {
        if (_repeatMode && mounted) {
          // Replay the audio if repeat mode is on
          _audioPlayer.play(AssetSource(audioPath));
        } else {
          setState(() {
            _isPlayingArabic = false;
            _isPlayingEnglish = false;
          });
        }
      });
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error playing audio: $e')),
        );
      }
    }
  }

  Future<void> _stopAudio() async {
    await _audioPlayer.stop();
    setState(() {
      _isPlayingArabic = false;
      _isPlayingEnglish = false;
    });
  }

  @override
  void dispose() {
    _audioPlayer.dispose();
    _videoController?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        appBar: AppBar(title: Text('Day ${widget.dayNumber}')),
        body: const Center(child: CircularProgressIndicator()),
      );
    }

    final lesson = _lesson!;
    final levelColor = AppTheme.getLevelColor(widget.dayNumber);

    return Scaffold(
      appBar: AppBar(
        title: Text('Day ${widget.dayNumber}'),
        backgroundColor: levelColor,
        actions: [
          IconButton(
            icon: Icon(_isCompleted ? Icons.check_circle : Icons.circle_outlined),
            onPressed: _toggleCompletion,
            tooltip: _isCompleted ? 'Mark Incomplete' : 'Mark Complete',
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            _buildLevelBanner(lesson, levelColor),
            _buildLanguageSelector(),
            _buildContent(lesson),
            const SizedBox(height: 16),
            _buildAudioControls(lesson),
            const SizedBox(height: 16),
            if (_videoController != null) _buildVideoPlayer(),
            const SizedBox(height: 24),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.pop(context, true);
        },
        backgroundColor: levelColor,
        child: const Icon(Icons.arrow_back),
      ),
    );
  }

  Widget _buildLevelBanner(LessonDay lesson, Color color) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        border: Border(bottom: BorderSide(color: color, width: 2)),
      ),
      child: Column(
        children: [
          Text(
            lesson.levelName,
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: color,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 4),
          Text(
            'Day ${widget.dayNumber} of 40',
            style: TextStyle(
              fontSize: 14,
              color: Colors.grey[700],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLanguageSelector() {
    return Container(
      padding: const EdgeInsets.all(16),
      child: Row(
        children: [
          Expanded(child: _buildLanguageButton('Arabic', 'arabic')),
          const SizedBox(width: 8),
          Expanded(child: _buildLanguageButton('Transliteration', 'transliteration')),
          const SizedBox(width: 8),
          Expanded(child: _buildLanguageButton('English', 'english')),
        ],
      ),
    );
  }

  Widget _buildLanguageButton(String label, String value) {
    final isSelected = _selectedLanguage == value;
    return ElevatedButton(
      onPressed: () => setState(() => _selectedLanguage = value),
      style: ElevatedButton.styleFrom(
        backgroundColor: isSelected ? AppTheme.primaryColor : Colors.grey[300],
        foregroundColor: isSelected ? Colors.white : Colors.black87,
        padding: const EdgeInsets.symmetric(vertical: 12),
      ),
      child: Text(label, style: const TextStyle(fontSize: 12)),
    );
  }

  Widget _buildContent(LessonDay lesson) {
    String content;
    TextDirection direction = TextDirection.ltr;
    String fontFamily = 'Poppins';

    switch (_selectedLanguage) {
      case 'arabic':
        content = lesson.arabicContent;
        direction = TextDirection.rtl;
        fontFamily = 'NotoSansArabic';
        break;
      case 'transliteration':
        content = lesson.transliterationContent;
        break;
      case 'english':
        content = lesson.englishContent;
        break;
      default:
        content = lesson.arabicContent;
    }

    return Container(
      padding: const EdgeInsets.all(16),
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Text(
            content,
            style: TextStyle(
              fontSize: _selectedLanguage == 'arabic' ? 20 : 16,
              height: 1.8,
              fontFamily: fontFamily,
            ),
            textDirection: direction,
          ),
        ),
      ),
    );
  }

  Widget _buildAudioControls(LessonDay lesson) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16),
      child: Column(
        children: [
          Row(
            children: [
              Expanded(
                child: ElevatedButton.icon(
                  onPressed: _isPlayingArabic
                      ? _stopAudio
                      : () => _playAudio(lesson.arabicAudioPath, true),
                  icon: Icon(_isPlayingArabic ? Icons.stop : Icons.play_arrow),
                  label: Text(_isPlayingArabic ? 'Stop Arabic' : 'Play Arabic'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppTheme.primaryColor,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: ElevatedButton.icon(
                  onPressed: _isPlayingEnglish
                      ? _stopAudio
                      : () => _playAudio(lesson.englishAudioPath, false),
                  icon: Icon(_isPlayingEnglish ? Icons.stop : Icons.play_arrow),
                  label:
                      Text(_isPlayingEnglish ? 'Stop English' : 'Play English'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppTheme.secondaryColor,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        'Playback Speed',
                        style: TextStyle(fontWeight: FontWeight.w500),
                      ),
                      Row(
                        children: [
                          _buildSpeedButton(0.75),
                          const SizedBox(width: 8),
                          _buildSpeedButton(1.0),
                          const SizedBox(width: 8),
                          _buildSpeedButton(1.25),
                          const SizedBox(width: 8),
                          _buildSpeedButton(1.5),
                        ],
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        'Repeat Mode',
                        style: TextStyle(fontWeight: FontWeight.w500),
                      ),
                      Switch(
                        value: _repeatMode,
                        onChanged: (value) {
                          setState(() {
                            _repeatMode = value;
                          });
                        },
                        activeColor: AppTheme.primaryColor,
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSpeedButton(double speed) {
    final isSelected = _playbackSpeed == speed;
    return InkWell(
      onTap: () {
        setState(() {
          _playbackSpeed = speed;
        });
        if (_isPlayingArabic || _isPlayingEnglish) {
          _audioPlayer.setPlaybackRate(speed);
        }
      },
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
        decoration: BoxDecoration(
          color: isSelected ? AppTheme.primaryColor : Colors.grey[200],
          borderRadius: BorderRadius.circular(20),
        ),
        child: Text(
          '${speed}x',
          style: TextStyle(
            color: isSelected ? Colors.white : Colors.black87,
            fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
            fontSize: 12,
          ),
        ),
      ),
    );
  }

  Widget _buildVideoPlayer() {
    return Container(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Video Lesson',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 12),
          YoutubePlayer(
            controller: _videoController!,
            showVideoProgressIndicator: true,
            progressIndicatorColor: AppTheme.primaryColor,
          ),
        ],
      ),
    );
  }
}
