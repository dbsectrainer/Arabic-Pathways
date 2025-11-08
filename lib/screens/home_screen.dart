import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../services/progress_service.dart';
import '../services/gamification_service.dart';
import '../utils/app_theme.dart';
import 'lesson_screen.dart';
import 'supplementary_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final ProgressService _progressService = ProgressService();
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
      body: RefreshIndicator(
        onRefresh: _loadProgress,
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              _buildGreetingCard(),
              const SizedBox(height: 16),
              _buildStreakCard(),
              const SizedBox(height: 16),
              _buildProgressSection(),
              const SizedBox(height: 24),
              _buildQuickStats(),
              const SizedBox(height: 24),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Your Lessons',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  Text(
                    '${_completedDays.length}/40',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          color: AppTheme.primaryColor,
                          fontWeight: FontWeight.bold,
                        ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              _buildDayGrid(startDay, endDay),
              const SizedBox(height: 16),
              _buildPagination(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildGreetingCard() {
    final hour = DateTime.now().hour;
    String greeting;
    IconData icon;

    if (hour < 12) {
      greeting = 'Good Morning';
      icon = Icons.wb_sunny;
    } else if (hour < 17) {
      greeting = 'Good Afternoon';
      icon = Icons.wb_sunny_outlined;
    } else {
      greeting = 'Good Evening';
      icon = Icons.nightlight_round;
    }

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Row(
          children: [
            Icon(icon, size: 40, color: AppTheme.primaryColor),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    greeting,
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  Text(
                    DateFormat('EEEE, MMM d').format(DateTime.now()),
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: Colors.grey[600],
                        ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    ).animate().fadeIn(duration: 400.ms).slideX(begin: -0.2, end: 0);
  }

  Widget _buildStreakCard() {
    return Consumer<GamificationService>(
      builder: (context, gamificationService, child) {
        final streak = gamificationService.userStats.currentStreak;
        final longestStreak = gamificationService.userStats.longestStreak;

        return Card(
          child: Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(12),
              gradient: const LinearGradient(
                colors: [AppTheme.orangeColor, AppTheme.accentColor],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _buildStreakStat(
                  Icons.local_fire_department,
                  'Current Streak',
                  '$streak days',
                ),
                Container(
                  width: 1,
                  height: 40,
                  color: Colors.white.withOpacity(0.3),
                ),
                _buildStreakStat(
                  Icons.emoji_events,
                  'Best Streak',
                  '$longestStreak days',
                ),
              ],
            ),
          ),
        ).animate().fadeIn(delay: 200.ms, duration: 400.ms).slideX(begin: 0.2, end: 0);
      },
    );
  }

  Widget _buildStreakStat(IconData icon, String label, String value) {
    return Column(
      children: [
        Icon(icon, color: Colors.white, size: 32),
        const SizedBox(height: 8),
        Text(
          value,
          style: const TextStyle(
            color: Colors.white,
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
        Text(
          label,
          style: TextStyle(
            color: Colors.white.withOpacity(0.9),
            fontSize: 12,
          ),
        ),
      ],
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
                  'Overall Progress',
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
            const SizedBox(height: 16),
            ClipRRect(
              borderRadius: BorderRadius.circular(10),
              child: LinearProgressIndicator(
                value: _progressPercentage / 100,
                backgroundColor: Colors.grey[200],
                valueColor: const AlwaysStoppedAnimation<Color>(
                  AppTheme.primaryColor,
                ),
                minHeight: 16,
              ),
            ),
            const SizedBox(height: 12),
            Text(
              '${_completedDays.length} of 40 days completed',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: Colors.grey[600],
                  ),
            ),
          ],
        ),
      ),
    ).animate().fadeIn(delay: 400.ms, duration: 400.ms).slideY(begin: 0.2, end: 0);
  }

  Widget _buildQuickStats() {
    return Consumer<GamificationService>(
      builder: (context, gamificationService, child) {
        final stats = gamificationService.userStats;

        return Row(
          children: [
            Expanded(
              child: _buildStatCard(
                'Days\nCompleted',
                stats.totalDaysCompleted.toString(),
                Icons.check_circle,
                AppTheme.secondaryColor,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: _buildStatCard(
                'Achievements',
                gamificationService.unlockedCount.toString(),
                Icons.emoji_events,
                AppTheme.orangeColor,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: _buildStatCard(
                'Audio\nPlayed',
                stats.totalAudioPlays.toString(),
                Icons.headphones,
                AppTheme.purpleColor,
              ),
            ),
          ],
        );
      },
    );
  }

  Widget _buildStatCard(String label, String value, IconData icon, Color color) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Icon(icon, color: color, size: 28),
            const SizedBox(height: 8),
            Text(
              value,
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              label,
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 11,
                color: Colors.grey[600],
              ),
            ),
          ],
        ),
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
            gradient: isCompleted
                ? LinearGradient(
                    colors: [
                      color.withOpacity(0.1),
                      color.withOpacity(0.05),
                    ],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  )
                : null,
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
                      size: 24,
                    ),
                ],
              ),
              const SizedBox(height: 8),
              Icon(
                isCompleted ? Icons.replay : Icons.play_circle_outline,
                size: 32,
                color: isCompleted ? color : Colors.grey,
              ),
            ],
          ),
        ),
      ),
    )
        .animate()
        .fadeIn(
          delay: Duration(milliseconds: 100 * (dayNumber % 10)),
          duration: 400.ms,
        )
        .scale(begin: const Offset(0.8, 0.8), end: const Offset(1, 1));
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
        ...List.generate(totalPages, (index) {
          return Padding(
            padding: const EdgeInsets.symmetric(horizontal: 4),
            child: GestureDetector(
              onTap: () => setState(() => _currentPage = index),
              child: Container(
                width: _currentPage == index ? 32 : 8,
                height: 8,
                decoration: BoxDecoration(
                  color: _currentPage == index
                      ? AppTheme.primaryColor
                      : Colors.grey[300],
                  borderRadius: BorderRadius.circular(4),
                ),
              ),
            ),
          );
        }),
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
