import 'package:shared_preferences/shared_preferences.dart';

class ProgressService {
  static const String _completedDaysKey = 'completed_days';
  static const String _currentDayKey = 'current_day';

  Future<Set<int>> getCompletedDays() async {
    final prefs = await SharedPreferences.getInstance();
    final completedList = prefs.getStringList(_completedDaysKey) ?? [];
    return completedList.map((e) => int.parse(e)).toSet();
  }

  Future<void> markDayComplete(int dayNumber) async {
    final prefs = await SharedPreferences.getInstance();
    final completed = await getCompletedDays();
    completed.add(dayNumber);
    await prefs.setStringList(
      _completedDaysKey,
      completed.map((e) => e.toString()).toList(),
    );
  }

  Future<void> markDayIncomplete(int dayNumber) async {
    final prefs = await SharedPreferences.getInstance();
    final completed = await getCompletedDays();
    completed.remove(dayNumber);
    await prefs.setStringList(
      _completedDaysKey,
      completed.map((e) => e.toString()).toList(),
    );
  }

  Future<int> getCurrentDay() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getInt(_currentDayKey) ?? 1;
  }

  Future<void> setCurrentDay(int dayNumber) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt(_currentDayKey, dayNumber);
  }

  Future<double> getProgressPercentage() async {
    final completed = await getCompletedDays();
    return (completed.length / 40) * 100;
  }

  Future<void> resetProgress() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_completedDaysKey);
    await prefs.setInt(_currentDayKey, 1);
  }
}
