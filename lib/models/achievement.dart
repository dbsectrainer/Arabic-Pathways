import 'package:flutter/material.dart';

enum AchievementType {
  daysCompleted,
  streakMaintained,
  levelCompleted,
  perfectWeek,
  earlyBird,
  nightOwl,
  speedRunner,
  dedicated,
}

class Achievement {
  final String id;
  final String title;
  final String description;
  final IconData icon;
  final Color color;
  final AchievementType type;
  final int requiredValue;
  final bool isUnlocked;
  final DateTime? unlockedAt;

  Achievement({
    required this.id,
    required this.title,
    required this.description,
    required this.icon,
    required this.color,
    required this.type,
    required this.requiredValue,
    this.isUnlocked = false,
    this.unlockedAt,
  });

  Achievement copyWith({
    String? id,
    String? title,
    String? description,
    IconData? icon,
    Color? color,
    AchievementType? type,
    int? requiredValue,
    bool? isUnlocked,
    DateTime? unlockedAt,
  }) {
    return Achievement(
      id: id ?? this.id,
      title: title ?? this.title,
      description: description ?? this.description,
      icon: icon ?? this.icon,
      color: color ?? this.color,
      type: type ?? this.type,
      requiredValue: requiredValue ?? this.requiredValue,
      isUnlocked: isUnlocked ?? this.isUnlocked,
      unlockedAt: unlockedAt ?? this.unlockedAt,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'isUnlocked': isUnlocked,
      'unlockedAt': unlockedAt?.toIso8601String(),
    };
  }

  static Achievement fromJson(Map<String, dynamic> json, Achievement template) {
    return template.copyWith(
      isUnlocked: json['isUnlocked'] as bool? ?? false,
      unlockedAt: json['unlockedAt'] != null
          ? DateTime.parse(json['unlockedAt'] as String)
          : null,
    );
  }
}

class UserStats {
  final int totalDaysCompleted;
  final int currentStreak;
  final int longestStreak;
  final int totalMinutesStudied;
  final DateTime? lastStudyDate;
  final Map<int, int> dailyGoalStreak;
  final int perfectWeeks;
  final int totalAudioPlays;
  final int totalVideoWatches;

  UserStats({
    this.totalDaysCompleted = 0,
    this.currentStreak = 0,
    this.longestStreak = 0,
    this.totalMinutesStudied = 0,
    this.lastStudyDate,
    this.dailyGoalStreak = const {},
    this.perfectWeeks = 0,
    this.totalAudioPlays = 0,
    this.totalVideoWatches = 0,
  });

  UserStats copyWith({
    int? totalDaysCompleted,
    int? currentStreak,
    int? longestStreak,
    int? totalMinutesStudied,
    DateTime? lastStudyDate,
    Map<int, int>? dailyGoalStreak,
    int? perfectWeeks,
    int? totalAudioPlays,
    int? totalVideoWatches,
  }) {
    return UserStats(
      totalDaysCompleted: totalDaysCompleted ?? this.totalDaysCompleted,
      currentStreak: currentStreak ?? this.currentStreak,
      longestStreak: longestStreak ?? this.longestStreak,
      totalMinutesStudied: totalMinutesStudied ?? this.totalMinutesStudied,
      lastStudyDate: lastStudyDate ?? this.lastStudyDate,
      dailyGoalStreak: dailyGoalStreak ?? this.dailyGoalStreak,
      perfectWeeks: perfectWeeks ?? this.perfectWeeks,
      totalAudioPlays: totalAudioPlays ?? this.totalAudioPlays,
      totalVideoWatches: totalVideoWatches ?? this.totalVideoWatches,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'totalDaysCompleted': totalDaysCompleted,
      'currentStreak': currentStreak,
      'longestStreak': longestStreak,
      'totalMinutesStudied': totalMinutesStudied,
      'lastStudyDate': lastStudyDate?.toIso8601String(),
      'dailyGoalStreak': dailyGoalStreak,
      'perfectWeeks': perfectWeeks,
      'totalAudioPlays': totalAudioPlays,
      'totalVideoWatches': totalVideoWatches,
    };
  }

  factory UserStats.fromJson(Map<String, dynamic> json) {
    return UserStats(
      totalDaysCompleted: json['totalDaysCompleted'] as int? ?? 0,
      currentStreak: json['currentStreak'] as int? ?? 0,
      longestStreak: json['longestStreak'] as int? ?? 0,
      totalMinutesStudied: json['totalMinutesStudied'] as int? ?? 0,
      lastStudyDate: json['lastStudyDate'] != null
          ? DateTime.parse(json['lastStudyDate'] as String)
          : null,
      dailyGoalStreak: (json['dailyGoalStreak'] as Map<String, dynamic>?)
              ?.map((k, v) => MapEntry(int.parse(k), v as int)) ??
          {},
      perfectWeeks: json['perfectWeeks'] as int? ?? 0,
      totalAudioPlays: json['totalAudioPlays'] as int? ?? 0,
      totalVideoWatches: json['totalVideoWatches'] as int? ?? 0,
    );
  }
}
