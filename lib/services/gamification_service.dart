import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/achievement.dart';
import '../utils/app_theme.dart';

class GamificationService extends ChangeNotifier {
  static const String _userStatsKey = 'user_stats';
  static const String _achievementsKey = 'achievements';

  UserStats _userStats = UserStats();
  List<Achievement> _achievements = [];

  UserStats get userStats => _userStats;
  List<Achievement> get achievements => _achievements;
  List<Achievement> get unlockedAchievements =>
      _achievements.where((a) => a.isUnlocked).toList();
  int get unlockedCount => unlockedAchievements.length;

  GamificationService() {
    _initializeAchievements();
  }

  void _initializeAchievements() {
    _achievements = [
      Achievement(
        id: 'first_day',
        title: 'First Steps',
        description: 'Complete your first day',
        icon: Icons.star,
        color: AppTheme.primaryColor,
        type: AchievementType.daysCompleted,
        requiredValue: 1,
      ),
      Achievement(
        id: 'week_one',
        title: 'Week Warrior',
        description: 'Complete 7 days',
        icon: Icons.local_fire_department,
        color: AppTheme.secondaryColor,
        type: AchievementType.daysCompleted,
        requiredValue: 7,
      ),
      Achievement(
        id: 'half_way',
        title: 'Halfway Hero',
        description: 'Complete 20 days',
        icon: Icons.trending_up,
        color: AppTheme.accentColor,
        type: AchievementType.daysCompleted,
        requiredValue: 20,
      ),
      Achievement(
        id: 'master',
        title: 'Arabic Master',
        description: 'Complete all 40 days',
        icon: Icons.emoji_events,
        color: AppTheme.orangeColor,
        type: AchievementType.daysCompleted,
        requiredValue: 40,
      ),
      Achievement(
        id: 'streak_3',
        title: 'Getting Consistent',
        description: 'Maintain a 3-day streak',
        icon: Icons.whatshot,
        color: Colors.orange,
        type: AchievementType.streakMaintained,
        requiredValue: 3,
      ),
      Achievement(
        id: 'streak_7',
        title: 'Week Streak',
        description: 'Maintain a 7-day streak',
        icon: Icons.whatshot,
        color: Colors.deepOrange,
        type: AchievementType.streakMaintained,
        requiredValue: 7,
      ),
      Achievement(
        id: 'streak_14',
        title: 'Two Week Champion',
        description: 'Maintain a 14-day streak',
        icon: Icons.whatshot,
        color: Colors.red,
        type: AchievementType.streakMaintained,
        requiredValue: 14,
      ),
      Achievement(
        id: 'level_1',
        title: 'Foundation Builder',
        description: 'Complete Level 1',
        icon: Icons.workspace_premium,
        color: AppTheme.primaryColor,
        type: AchievementType.levelCompleted,
        requiredValue: 1,
      ),
      Achievement(
        id: 'level_2',
        title: 'Daily Communicator',
        description: 'Complete Level 2',
        icon: Icons.workspace_premium,
        color: AppTheme.secondaryColor,
        type: AchievementType.levelCompleted,
        requiredValue: 2,
      ),
      Achievement(
        id: 'level_3',
        title: 'Cultural Explorer',
        description: 'Complete Level 3',
        icon: Icons.workspace_premium,
        color: AppTheme.accentColor,
        type: AchievementType.levelCompleted,
        requiredValue: 3,
      ),
      Achievement(
        id: 'level_4',
        title: 'Professional Speaker',
        description: 'Complete Level 4',
        icon: Icons.workspace_premium,
        color: AppTheme.purpleColor,
        type: AchievementType.levelCompleted,
        requiredValue: 4,
      ),
      Achievement(
        id: 'level_5',
        title: 'Fluency Achiever',
        description: 'Complete Level 5',
        icon: Icons.workspace_premium,
        color: AppTheme.orangeColor,
        type: AchievementType.levelCompleted,
        requiredValue: 5,
      ),
      Achievement(
        id: 'perfect_week',
        title: 'Perfect Week',
        description: 'Complete all 7 days in a week',
        icon: Icons.check_circle,
        color: Colors.green,
        type: AchievementType.perfectWeek,
        requiredValue: 1,
      ),
      Achievement(
        id: 'dedicated',
        title: 'Dedicated Learner',
        description: 'Study for 30 consecutive days',
        icon: Icons.school,
        color: Colors.purple,
        type: AchievementType.dedicated,
        requiredValue: 30,
      ),
    ];
  }

  Future<void> loadStats() async {
    final prefs = await SharedPreferences.getInstance();
    final statsJson = prefs.getString(_userStatsKey);
    if (statsJson != null) {
      _userStats = UserStats.fromJson(json.decode(statsJson));
    }

    final achievementsJson = prefs.getString(_achievementsKey);
    if (achievementsJson != null) {
      final List<dynamic> achievementsList = json.decode(achievementsJson);
      for (var i = 0; i < _achievements.length; i++) {
        final savedData = achievementsList.firstWhere(
          (a) => a['id'] == _achievements[i].id,
          orElse: () => null,
        );
        if (savedData != null) {
          _achievements[i] =
              Achievement.fromJson(savedData, _achievements[i]);
        }
      }
    }
    notifyListeners();
  }

  Future<void> _saveStats() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_userStatsKey, json.encode(_userStats.toJson()));
    await prefs.setString(
      _achievementsKey,
      json.encode(_achievements.map((a) => a.toJson()).toList()),
    );
    notifyListeners();
  }

  Future<List<Achievement>> recordDayCompletion(int dayNumber) async {
    final now = DateTime.now();
    final today = DateTime(now.year, now.month, now.day);

    // Update streak
    int newStreak = 1;
    if (_userStats.lastStudyDate != null) {
      final lastStudy = DateTime(
        _userStats.lastStudyDate!.year,
        _userStats.lastStudyDate!.month,
        _userStats.lastStudyDate!.day,
      );
      final daysDifference = today.difference(lastStudy).inDays;

      if (daysDifference == 0) {
        // Same day, keep current streak
        newStreak = _userStats.currentStreak;
      } else if (daysDifference == 1) {
        // Consecutive day
        newStreak = _userStats.currentStreak + 1;
      }
      // else: streak broken, newStreak stays at 1
    }

    _userStats = _userStats.copyWith(
      totalDaysCompleted: _userStats.totalDaysCompleted + 1,
      currentStreak: newStreak,
      longestStreak: newStreak > _userStats.longestStreak
          ? newStreak
          : _userStats.longestStreak,
      lastStudyDate: now,
    );

    // Check for newly unlocked achievements
    final newlyUnlocked = await _checkAchievements(dayNumber);
    await _saveStats();
    return newlyUnlocked;
  }

  Future<void> recordAudioPlay() async {
    _userStats = _userStats.copyWith(
      totalAudioPlays: _userStats.totalAudioPlays + 1,
    );
    await _saveStats();
  }

  Future<void> recordVideoWatch() async {
    _userStats = _userStats.copyWith(
      totalVideoWatches: _userStats.totalVideoWatches + 1,
    );
    await _saveStats();
  }

  Future<List<Achievement>> _checkAchievements(int currentDay) async {
    final newlyUnlocked = <Achievement>[];

    for (var i = 0; i < _achievements.length; i++) {
      if (_achievements[i].isUnlocked) continue;

      bool shouldUnlock = false;

      switch (_achievements[i].type) {
        case AchievementType.daysCompleted:
          shouldUnlock = _userStats.totalDaysCompleted >= _achievements[i].requiredValue;
          break;
        case AchievementType.streakMaintained:
          shouldUnlock = _userStats.currentStreak >= _achievements[i].requiredValue;
          break;
        case AchievementType.levelCompleted:
          final levelEndDay = _achievements[i].requiredValue * 7;
          if (_achievements[i].requiredValue == 5) {
            shouldUnlock = _userStats.totalDaysCompleted >= 40;
          } else {
            shouldUnlock = _userStats.totalDaysCompleted >= levelEndDay;
          }
          break;
        case AchievementType.perfectWeek:
          shouldUnlock = _userStats.currentStreak >= 7;
          break;
        case AchievementType.dedicated:
          shouldUnlock = _userStats.currentStreak >= 30;
          break;
        default:
          break;
      }

      if (shouldUnlock) {
        _achievements[i] = _achievements[i].copyWith(
          isUnlocked: true,
          unlockedAt: DateTime.now(),
        );
        newlyUnlocked.add(_achievements[i]);
      }
    }

    return newlyUnlocked;
  }

  Future<void> resetStats() async {
    _userStats = UserStats();
    _initializeAchievements();
    await _saveStats();
  }
}
