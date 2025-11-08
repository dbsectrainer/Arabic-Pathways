import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class SettingsService extends ChangeNotifier {
  static const String _darkModeKey = 'dark_mode';
  static const String _textScaleKey = 'text_scale';
  static const String _languageKey = 'language';
  static const String _notificationsKey = 'notifications_enabled';
  static const String _soundEffectsKey = 'sound_effects_enabled';

  bool _isDarkMode = false;
  double _textScaleFactor = 1.0;
  String _language = 'en';
  bool _notificationsEnabled = true;
  bool _soundEffectsEnabled = true;

  bool get isDarkMode => _isDarkMode;
  double get textScaleFactor => _textScaleFactor;
  String get language => _language;
  bool get notificationsEnabled => _notificationsEnabled;
  bool get soundEffectsEnabled => _soundEffectsEnabled;

  Future<void> loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    _isDarkMode = prefs.getBool(_darkModeKey) ?? false;
    _textScaleFactor = prefs.getDouble(_textScaleKey) ?? 1.0;
    _language = prefs.getString(_languageKey) ?? 'en';
    _notificationsEnabled = prefs.getBool(_notificationsKey) ?? true;
    _soundEffectsEnabled = prefs.getBool(_soundEffectsKey) ?? true;
    notifyListeners();
  }

  Future<void> setDarkMode(bool value) async {
    _isDarkMode = value;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_darkModeKey, value);
    notifyListeners();
  }

  Future<void> setTextScaleFactor(double value) async {
    _textScaleFactor = value;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble(_textScaleKey, value);
    notifyListeners();
  }

  Future<void> setLanguage(String value) async {
    _language = value;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_languageKey, value);
    notifyListeners();
  }

  Future<void> setNotificationsEnabled(bool value) async {
    _notificationsEnabled = value;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_notificationsKey, value);
    notifyListeners();
  }

  Future<void> setSoundEffectsEnabled(bool value) async {
    _soundEffectsEnabled = value;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_soundEffectsKey, value);
    notifyListeners();
  }

  String getTextSizeLabel() {
    if (_textScaleFactor <= 0.85) return 'Small';
    if (_textScaleFactor <= 1.0) return 'Normal';
    if (_textScaleFactor <= 1.15) return 'Large';
    return 'Extra Large';
  }
}
