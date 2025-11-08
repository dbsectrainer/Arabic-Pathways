import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import 'package:fl_chart/fl_chart.dart';
import '../services/progress_service.dart';
import '../services/gamification_service.dart';
import '../utils/app_theme.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  final ProgressService _progressService = ProgressService();
  Set<int> _completedDays = {};

  @override
  void initState() {
    super.initState();
    _loadProgress();
  }

  Future<void> _loadProgress() async {
    final completed = await _progressService.getCompletedDays();
    setState(() {
      _completedDays = completed;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Your Profile'),
        elevation: 0,
      ),
      body: RefreshIndicator(
        onRefresh: _loadProgress,
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              _buildProfileHeader(),
              const SizedBox(height: 24),
              _buildStatsGrid(),
              const SizedBox(height: 24),
              _buildLevelProgress(),
              const SizedBox(height: 24),
              _buildActivityChart(),
              const SizedBox(height: 24),
              _buildRecentActivity(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildProfileHeader() {
    return Consumer<GamificationService>(
      builder: (context, gamificationService, child) {
        final stats = gamificationService.userStats;

        return Card(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              children: [
                Container(
                  width: 100,
                  height: 100,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    gradient: const LinearGradient(
                      colors: [AppTheme.primaryColor, AppTheme.secondaryColor],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                  ),
                  child: const Icon(
                    Icons.person,
                    size: 50,
                    color: Colors.white,
                  ),
                )
                    .animate()
                    .scale(
                      duration: 600.ms,
                      curve: Curves.elasticOut,
                    )
                    .fadeIn(),
                const SizedBox(height: 16),
                Text(
                  'Arabic Learner',
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                const SizedBox(height: 8),
                Text(
                  stats.lastStudyDate != null
                      ? 'Last studied: ${DateFormat('MMM d, y').format(stats.lastStudyDate!)}'
                      : 'Start your journey today!',
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: Colors.grey[600],
                      ),
                ),
                const SizedBox(height: 16),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    _buildProfileStat(
                      'Streak',
                      '${stats.currentStreak}',
                      Icons.local_fire_department,
                      AppTheme.accentColor,
                    ),
                    Container(
                      width: 1,
                      height: 40,
                      color: Colors.grey[300],
                    ),
                    _buildProfileStat(
                      'Progress',
                      '${((stats.totalDaysCompleted / 40) * 100).toStringAsFixed(0)}%',
                      Icons.trending_up,
                      AppTheme.primaryColor,
                    ),
                    Container(
                      width: 1,
                      height: 40,
                      color: Colors.grey[300],
                    ),
                    _buildProfileStat(
                      'Achievements',
                      '${gamificationService.unlockedCount}',
                      Icons.emoji_events,
                      AppTheme.orangeColor,
                    ),
                  ],
                ),
              ],
            ),
          ),
        ).animate().fadeIn(duration: 400.ms).slideY(begin: -0.2, end: 0);
      },
    );
  }

  Widget _buildProfileStat(String label, String value, IconData icon, Color color) {
    return Column(
      children: [
        Icon(icon, color: color, size: 24),
        const SizedBox(height: 4),
        Text(
          value,
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: color,
          ),
        ),
        Text(
          label,
          style: TextStyle(
            fontSize: 12,
            color: Colors.grey[600],
          ),
        ),
      ],
    );
  }

  Widget _buildStatsGrid() {
    return Consumer<GamificationService>(
      builder: (context, gamificationService, child) {
        final stats = gamificationService.userStats;

        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Your Statistics',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 12),
            GridView.count(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              crossAxisCount: 2,
              crossAxisSpacing: 12,
              mainAxisSpacing: 12,
              childAspectRatio: 1.8,
              children: [
                _buildStatCard(
                  'Days Completed',
                  stats.totalDaysCompleted.toString(),
                  Icons.check_circle,
                  AppTheme.secondaryColor,
                ),
                _buildStatCard(
                  'Current Streak',
                  '${stats.currentStreak} days',
                  Icons.whatshot,
                  AppTheme.accentColor,
                ),
                _buildStatCard(
                  'Longest Streak',
                  '${stats.longestStreak} days',
                  Icons.emoji_events,
                  AppTheme.orangeColor,
                ),
                _buildStatCard(
                  'Audio Played',
                  stats.totalAudioPlays.toString(),
                  Icons.headphones,
                  AppTheme.purpleColor,
                ),
              ],
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
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, color: color, size: 28),
            const SizedBox(height: 8),
            Text(
              value,
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: color,
              ),
              textAlign: TextAlign.center,
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

  Widget _buildLevelProgress() {
    final completedInLevels = {
      1: _completedDays.where((d) => d >= 1 && d <= 7).length,
      2: _completedDays.where((d) => d >= 8 && d <= 14).length,
      3: _completedDays.where((d) => d >= 15 && d <= 22).length,
      4: _completedDays.where((d) => d >= 23 && d <= 30).length,
      5: _completedDays.where((d) => d >= 31 && d <= 40).length,
    };

    final levelSizes = {1: 7, 2: 7, 3: 8, 4: 8, 5: 10};

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Level Progress',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 16),
            _buildLevelProgressBar(
              'Level 1: Foundations',
              completedInLevels[1]!,
              levelSizes[1]!,
              AppTheme.primaryColor,
            ),
            const SizedBox(height: 12),
            _buildLevelProgressBar(
              'Level 2: Essential Daily',
              completedInLevels[2]!,
              levelSizes[2]!,
              AppTheme.secondaryColor,
            ),
            const SizedBox(height: 12),
            _buildLevelProgressBar(
              'Level 3: Cultural & Social',
              completedInLevels[3]!,
              levelSizes[3]!,
              AppTheme.accentColor,
            ),
            const SizedBox(height: 12),
            _buildLevelProgressBar(
              'Level 4: Professional',
              completedInLevels[4]!,
              levelSizes[4]!,
              AppTheme.purpleColor,
            ),
            const SizedBox(height: 12),
            _buildLevelProgressBar(
              'Level 5: Advanced Fluency',
              completedInLevels[5]!,
              levelSizes[5]!,
              AppTheme.orangeColor,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLevelProgressBar(
    String title,
    int completed,
    int total,
    Color color,
  ) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              title,
              style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w500),
            ),
            Text(
              '$completed/$total',
              style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
          ],
        ),
        const SizedBox(height: 6),
        ClipRRect(
          borderRadius: BorderRadius.circular(8),
          child: LinearProgressIndicator(
            value: completed / total,
            backgroundColor: Colors.grey[200],
            valueColor: AlwaysStoppedAnimation<Color>(color),
            minHeight: 8,
          ),
        ),
      ],
    );
  }

  Widget _buildActivityChart() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Learning Activity',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 20),
            SizedBox(
              height: 200,
              child: _buildBarChart(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildBarChart() {
    final levelData = [
      _completedDays.where((d) => d >= 1 && d <= 7).length,
      _completedDays.where((d) => d >= 8 && d <= 14).length,
      _completedDays.where((d) => d >= 15 && d <= 22).length,
      _completedDays.where((d) => d >= 23 && d <= 30).length,
      _completedDays.where((d) => d >= 31 && d <= 40).length,
    ];

    return BarChart(
      BarChartData(
        alignment: BarChartAlignment.spaceAround,
        maxY: 10,
        barTouchData: BarTouchData(enabled: true),
        titlesData: FlTitlesData(
          show: true,
          bottomTitles: AxisTitles(
            sideTitles: SideTitles(
              showTitles: true,
              getTitlesWidget: (value, meta) {
                return Text(
                  'L${value.toInt() + 1}',
                  style: const TextStyle(fontSize: 12),
                );
              },
            ),
          ),
          leftTitles: AxisTitles(
            sideTitles: SideTitles(
              showTitles: true,
              reservedSize: 30,
              getTitlesWidget: (value, meta) {
                return Text(
                  value.toInt().toString(),
                  style: const TextStyle(fontSize: 10),
                );
              },
            ),
          ),
          topTitles: const AxisTitles(
            sideTitles: SideTitles(showTitles: false),
          ),
          rightTitles: const AxisTitles(
            sideTitles: SideTitles(showTitles: false),
          ),
        ),
        borderData: FlBorderData(show: false),
        barGroups: List.generate(5, (index) {
          final colors = [
            AppTheme.primaryColor,
            AppTheme.secondaryColor,
            AppTheme.accentColor,
            AppTheme.purpleColor,
            AppTheme.orangeColor,
          ];
          return BarChartGroupData(
            x: index,
            barRods: [
              BarChartRodData(
                toY: levelData[index].toDouble(),
                color: colors[index],
                width: 20,
                borderRadius: const BorderRadius.vertical(
                  top: Radius.circular(4),
                ),
              ),
            ],
          );
        }),
      ),
    );
  }

  Widget _buildRecentActivity() {
    final recentDays = _completedDays.toList()
      ..sort((a, b) => b.compareTo(a));
    final displayDays = recentDays.take(5).toList();

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Recent Activity',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 16),
            if (displayDays.isEmpty)
              Center(
                child: Padding(
                  padding: const EdgeInsets.all(20),
                  child: Text(
                    'No activity yet. Start your first lesson!',
                    style: TextStyle(color: Colors.grey[600]),
                  ),
                ),
              )
            else
              ...displayDays.map((day) => _buildActivityItem(day)),
          ],
        ),
      ),
    );
  }

  Widget _buildActivityItem(int dayNumber) {
    final color = AppTheme.getLevelColor(dayNumber);
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        children: [
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: color.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Center(
              child: Text(
                '$dayNumber',
                style: TextStyle(
                  color: color,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Day $dayNumber Completed',
                  style: const TextStyle(
                    fontWeight: FontWeight.w500,
                  ),
                ),
                Text(
                  AppTheme.getLevelName(dayNumber),
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey[600],
                  ),
                ),
              ],
            ),
          ),
          const Icon(
            Icons.check_circle,
            color: AppTheme.secondaryColor,
            size: 20,
          ),
        ],
      ),
    );
  }
}
