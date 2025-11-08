import 'package:flutter/material.dart';
import '../services/progress_service.dart';
import '../services/content_service.dart';
import '../utils/app_theme.dart';
import 'lesson_screen.dart';
import 'supplementary_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final ProgressService _progressService = ProgressService();
  final ContentService _contentService = ContentService();
  Set<int> _completedDays = {};
  double _progressPercentage = 0;
  int _currentPage = 0;
  final int _daysPerPage = 10;

  @override
  void initState() {
    super.initState();
    _loadProgress();
  }

  Future<void> _loadProgress() async {
    final completed = await _progressService.getCompletedDays();
    final percentage = await _progressService.getProgressPercentage();
    setState(() {
      _completedDays = completed;
      _progressPercentage = percentage;
    });
  }

  void _navigateToLesson(int dayNumber) async {
    final result = await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => LessonScreen(dayNumber: dayNumber),
      ),
    );
    if (result == true) {
      _loadProgress();
    }
  }

  void _navigateToSupplementary() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => const SupplementaryScreen(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final startDay = _currentPage * _daysPerPage + 1;
    final endDay = (startDay + _daysPerPage - 1).clamp(1, 40);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Arabic Pathways'),
        actions: [
          IconButton(
            icon: const Icon(Icons.library_books),
            onPressed: _navigateToSupplementary,
            tooltip: 'Supplementary Content',
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            _buildHeader(),
            const SizedBox(height: 24),
            _buildProgressSection(),
            const SizedBox(height: 24),
            _buildLevelIndicators(),
            const SizedBox(height: 24),
            _buildDayGrid(startDay, endDay),
            const SizedBox(height: 16),
            _buildPagination(),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            const Icon(
              Icons.school,
              size: 48,
              color: AppTheme.primaryColor,
            ),
            const SizedBox(height: 12),
            Text(
              'Master Arabic in 40 Days',
              style: Theme.of(context).textTheme.displayMedium,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 8),
            Text(
              'Structured lessons from basics to fluency',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: Colors.grey[600],
                  ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildProgressSection() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Your Progress',
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                Text(
                  '${_progressPercentage.toStringAsFixed(0)}%',
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        color: AppTheme.primaryColor,
                        fontWeight: FontWeight.bold,
                      ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            LinearProgressIndicator(
              value: _progressPercentage / 100,
              backgroundColor: Colors.grey[200],
              valueColor: const AlwaysStoppedAnimation<Color>(
                AppTheme.primaryColor,
              ),
              minHeight: 10,
            ),
            const SizedBox(height: 8),
            Text(
              '${_completedDays.length} of 40 days completed',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: Colors.grey[600],
                  ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLevelIndicators() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Levels',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            _buildLevelIndicator('Level 1: Foundations', AppTheme.primaryColor, '1-7'),
            _buildLevelIndicator('Level 2: Essential Daily', AppTheme.secondaryColor, '8-14'),
            _buildLevelIndicator('Level 3: Cultural & Social', AppTheme.accentColor, '15-22'),
            _buildLevelIndicator('Level 4: Professional', AppTheme.purpleColor, '23-30'),
            _buildLevelIndicator('Level 5: Advanced Fluency', AppTheme.orangeColor, '31-40'),
          ],
        ),
      ),
    );
  }

  Widget _buildLevelIndicator(String title, Color color, String days) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Container(
            width: 12,
            height: 12,
            decoration: BoxDecoration(
              color: color,
              shape: BoxShape.circle,
            ),
          ),
          const SizedBox(width: 8),
          Expanded(child: Text(title)),
          Text(
            'Days $days',
            style: TextStyle(color: Colors.grey[600], fontSize: 12),
          ),
        ],
      ),
    );
  }

  Widget _buildDayGrid(int startDay, int endDay) {
    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        childAspectRatio: 1.5,
        crossAxisSpacing: 12,
        mainAxisSpacing: 12,
      ),
      itemCount: endDay - startDay + 1,
      itemBuilder: (context, index) {
        final dayNumber = startDay + index;
        return _buildDayCard(dayNumber);
      },
    );
  }

  Widget _buildDayCard(int dayNumber) {
    final isCompleted = _completedDays.contains(dayNumber);
    final color = AppTheme.getLevelColor(dayNumber);

    return InkWell(
      onTap: () => _navigateToLesson(dayNumber),
      borderRadius: BorderRadius.circular(12),
      child: Card(
        child: Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(12),
            border: Border.all(
              color: color.withOpacity(0.3),
              width: 2,
            ),
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 8,
                      vertical: 4,
                    ),
                    decoration: BoxDecoration(
                      color: color,
                      borderRadius: BorderRadius.circular(4),
                    ),
                    child: Text(
                      'Day $dayNumber',
                      style: const TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                        fontSize: 12,
                      ),
                    ),
                  ),
                  if (isCompleted)
                    const Icon(
                      Icons.check_circle,
                      color: AppTheme.secondaryColor,
                      size: 20,
                    ),
                ],
              ),
              const SizedBox(height: 8),
              const Icon(
                Icons.play_circle_outline,
                size: 32,
                color: Colors.grey,
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildPagination() {
    final totalPages = (40 / _daysPerPage).ceil();
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        IconButton(
          icon: const Icon(Icons.chevron_left),
          onPressed: _currentPage > 0
              ? () => setState(() => _currentPage--)
              : null,
        ),
        Text(
          'Page ${_currentPage + 1} of $totalPages',
          style: Theme.of(context).textTheme.bodyMedium,
        ),
        IconButton(
          icon: const Icon(Icons.chevron_right),
          onPressed: _currentPage < totalPages - 1
              ? () => setState(() => _currentPage++)
              : null,
        ),
      ],
    );
  }
}
