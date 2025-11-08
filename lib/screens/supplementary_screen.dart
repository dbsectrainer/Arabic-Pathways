import 'package:flutter/material.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:youtube_player_flutter/youtube_player_flutter.dart';
import '../models/supplementary_content.dart';
import '../services/content_service.dart';
import '../utils/app_theme.dart';

class SupplementaryScreen extends StatefulWidget {
  const SupplementaryScreen({super.key});

  @override
  State<SupplementaryScreen> createState() => _SupplementaryScreenState();
}

class _SupplementaryScreenState extends State<SupplementaryScreen> {
  final ContentService _contentService = ContentService();
  final AudioPlayer _audioPlayer = AudioPlayer();

  String? _selectedContentId;
  SupplementaryContent? _currentContent;
  bool _isLoading = false;
  String _selectedLanguage = 'arabic';
  bool _isPlayingArabic = false;
  bool _isPlayingEnglish = false;
  YoutubePlayerController? _videoController;

  @override
  void dispose() {
    _audioPlayer.dispose();
    _videoController?.dispose();
    super.dispose();
  }

  Future<void> _loadContent(String contentId) async {
    setState(() {
      _isLoading = true;
      _selectedContentId = contentId;
    });

    final content = await _contentService.loadSupplementaryContent(contentId);

    YoutubePlayerController? controller;
    if (content.videoId != null && content.videoId!.isNotEmpty) {
      controller = YoutubePlayerController(
        initialVideoId: content.videoId!,
        flags: const YoutubePlayerFlags(
          autoPlay: false,
          mute: false,
        ),
      );
    }

    setState(() {
      _currentContent = content;
      _videoController?.dispose();
      _videoController = controller;
      _isLoading = false;
    });
  }

  Future<void> _playAudio(String audioPath, bool isArabic) async {
    try {
      await _audioPlayer.stop();
      await _audioPlayer.play(AssetSource(audioPath));
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
        setState(() {
          _isPlayingArabic = false;
          _isPlayingEnglish = false;
        });
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error playing audio: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Supplementary Content'),
      ),
      body: Column(
        children: [
          _buildContentList(),
          if (_isLoading)
            const Expanded(
              child: Center(child: CircularProgressIndicator()),
            )
          else if (_currentContent != null)
            Expanded(
              child: SingleChildScrollView(
                child: _buildContentView(_currentContent!),
              ),
            )
          else
            Expanded(
              child: Center(
                child: Text(
                  'Select a topic to start learning',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        color: Colors.grey,
                      ),
                ),
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildContentList() {
    final contentIds = _contentService.getSupplementaryContentIds();
    return Container(
      height: 120,
      padding: const EdgeInsets.all(16),
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: contentIds.length,
        itemBuilder: (context, index) {
          final contentId = contentIds[index];
          final isSelected = contentId == _selectedContentId;
          return _buildContentCard(contentId, isSelected);
        },
      ),
    );
  }

  Widget _buildContentCard(String contentId, bool isSelected) {
    final icons = {
      'daily_life': Icons.home,
      'emotions': Icons.favorite,
      'education': Icons.school,
      'hobbies': Icons.sports_soccer,
      'comparisons': Icons.compare_arrows,
    };

    final titles = {
      'daily_life': 'Daily Life',
      'emotions': 'Emotions',
      'education': 'Education',
      'hobbies': 'Hobbies',
      'comparisons': 'Comparisons',
    };

    return Container(
      width: 140,
      margin: const EdgeInsets.only(right: 12),
      child: InkWell(
        onTap: () => _loadContent(contentId),
        borderRadius: BorderRadius.circular(12),
        child: Card(
          elevation: isSelected ? 8 : 2,
          color: isSelected ? AppTheme.primaryColor : null,
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  icons[contentId] ?? Icons.book,
                  size: 32,
                  color: isSelected ? Colors.white : AppTheme.primaryColor,
                ),
                const SizedBox(height: 8),
                Text(
                  titles[contentId] ?? contentId,
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                    color: isSelected ? Colors.white : Colors.black87,
                  ),
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildContentView(SupplementaryContent content) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: AppTheme.primaryColor.withOpacity(0.1),
            border: Border(
              bottom: BorderSide(color: AppTheme.primaryColor, width: 2),
            ),
          ),
          child: Text(
            content.title,
            style: const TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: AppTheme.primaryColor,
            ),
            textAlign: TextAlign.center,
          ),
        ),
        _buildLanguageSelector(),
        _buildContent(content),
        const SizedBox(height: 16),
        _buildAudioControls(content),
        const SizedBox(height: 16),
        if (_videoController != null) _buildVideoPlayer(),
        const SizedBox(height: 24),
      ],
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

  Widget _buildContent(SupplementaryContent content) {
    String contentText;
    TextDirection direction = TextDirection.ltr;
    String fontFamily = 'Poppins';

    switch (_selectedLanguage) {
      case 'arabic':
        contentText = content.arabicContent;
        direction = TextDirection.rtl;
        fontFamily = 'NotoSansArabic';
        break;
      case 'transliteration':
        contentText = content.transliterationContent;
        break;
      case 'english':
        contentText = content.englishContent;
        break;
      default:
        contentText = content.arabicContent;
    }

    return Container(
      padding: const EdgeInsets.all(16),
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Text(
            contentText,
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

  Widget _buildAudioControls(SupplementaryContent content) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16),
      child: Row(
        children: [
          Expanded(
            child: ElevatedButton.icon(
              onPressed: () => _playAudio(content.arabicAudioPath, true),
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
              onPressed: () => _playAudio(content.englishAudioPath, false),
              icon: Icon(_isPlayingEnglish ? Icons.stop : Icons.play_arrow),
              label: Text(_isPlayingEnglish ? 'Stop English' : 'Play English'),
              style: ElevatedButton.styleFrom(
                backgroundColor: AppTheme.secondaryColor,
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
            ),
          ),
        ],
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
