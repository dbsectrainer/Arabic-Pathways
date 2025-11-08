import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../services/gamification_service.dart';
import '../models/achievement.dart';

class AchievementsScreen extends StatelessWidget {
  const AchievementsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Achievements'),
        elevation: 0,
      ),
      body: Consumer<GamificationService>(
        builder: (context, gamificationService, child) {
          final achievements = gamificationService.achievements;
          final unlockedCount = gamificationService.unlockedCount;

          return SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                _buildProgressCard(
                  context,
                  unlockedCount,
                  achievements.length,
                ),
                const SizedBox(height: 24),
                _buildAchievementCategories(context, achievements),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildProgressCard(BuildContext context, int unlocked, int total) {
    final percentage = (unlocked / total * 100).toStringAsFixed(0);

    return Card(
      child: Container(
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(12),
          gradient: const LinearGradient(
            colors: [Color(0xFF4A90E2), Color(0xFF50C878)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Column(
          children: [
            const Icon(
              Icons.emoji_events,
              size: 60,
              color: Colors.white,
            ),
            const SizedBox(height: 16),
            Text(
              '$unlocked / $total',
              style: const TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Achievements Unlocked',
              style: TextStyle(
                fontSize: 16,
                color: Colors.white.withOpacity(0.9),
              ),
            ),
            const SizedBox(height: 16),
            ClipRRect(
              borderRadius: BorderRadius.circular(10),
              child: LinearProgressIndicator(
                value: unlocked / total,
                backgroundColor: Colors.white.withOpacity(0.3),
                valueColor: const AlwaysStoppedAnimation<Color>(Colors.white),
                minHeight: 12,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              '$percentage% Complete',
              style: const TextStyle(
                fontSize: 14,
                color: Colors.white,
                fontWeight: FontWeight.w500,
              ),
            ),
          ],
        ),
      ),
    )
        .animate()
        .fadeIn(duration: 400.ms)
        .scale(begin: const Offset(0.9, 0.9), end: const Offset(1, 1));
  }

  Widget _buildAchievementCategories(
    BuildContext context,
    List<Achievement> achievements,
  ) {
    final categories = {
      'Progress Milestones': achievements
          .where((a) => a.type == AchievementType.daysCompleted)
          .toList(),
      'Streak Master': achievements
          .where((a) => a.type == AchievementType.streakMaintained)
          .toList(),
      'Level Champion': achievements
          .where((a) => a.type == AchievementType.levelCompleted)
          .toList(),
      'Special Achievements': achievements
          .where((a) =>
              a.type == AchievementType.perfectWeek ||
              a.type == AchievementType.dedicated)
          .toList(),
    };

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: categories.entries.map((entry) {
        if (entry.value.isEmpty) return const SizedBox.shrink();

        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 8),
              child: Text(
                entry.key,
                style: Theme.of(context).textTheme.titleLarge,
              ),
            ),
            ...entry.value.map((achievement) => _buildAchievementCard(
                  context,
                  achievement,
                )),
            const SizedBox(height: 16),
          ],
        );
      }).toList(),
    );
  }

  Widget _buildAchievementCard(BuildContext context, Achievement achievement) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(12),
          gradient: achievement.isUnlocked
              ? LinearGradient(
                  colors: [
                    achievement.color.withOpacity(0.1),
                    achievement.color.withOpacity(0.05),
                  ],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                )
              : null,
        ),
        child: ListTile(
          contentPadding: const EdgeInsets.all(16),
          leading: Container(
            width: 60,
            height: 60,
            decoration: BoxDecoration(
              color: achievement.isUnlocked
                  ? achievement.color
                  : Colors.grey[300],
              shape: BoxShape.circle,
            ),
            child: Icon(
              achievement.icon,
              color: achievement.isUnlocked ? Colors.white : Colors.grey[600],
              size: 30,
            ),
          ),
          title: Text(
            achievement.title,
            style: TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 16,
              color: achievement.isUnlocked ? null : Colors.grey[600],
            ),
          ),
          subtitle: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 4),
              Text(
                achievement.description,
                style: TextStyle(
                  color: achievement.isUnlocked
                      ? Colors.grey[700]
                      : Colors.grey[500],
                ),
              ),
              if (achievement.isUnlocked && achievement.unlockedAt != null) ...[
                const SizedBox(height: 8),
                Row(
                  children: [
                    Icon(
                      Icons.check_circle,
                      size: 16,
                      color: achievement.color,
                    ),
                    const SizedBox(width: 4),
                    Text(
                      'Unlocked ${DateFormat('MMM d, y').format(achievement.unlockedAt!)}',
                      style: TextStyle(
                        fontSize: 12,
                        color: achievement.color,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ],
                ),
              ],
            ],
          ),
          trailing: achievement.isUnlocked
              ? Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: achievement.color.withOpacity(0.2),
                    shape: BoxShape.circle,
                  ),
                  child: Icon(
                    Icons.lock_open,
                    color: achievement.color,
                    size: 20,
                  ),
                )
              : Icon(
                  Icons.lock_outline,
                  color: Colors.grey[400],
                  size: 24,
                ),
        ),
      ),
    )
        .animate()
        .fadeIn(
          delay: Duration(milliseconds: achievements.indexOf(achievement) * 50),
          duration: 400.ms,
        )
        .slideX(begin: -0.2, end: 0);
  }
}
