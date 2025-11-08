import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'services/settings_service.dart';
import 'services/gamification_service.dart';
import 'screens/onboarding_screen.dart';
import 'screens/main_navigation.dart';
import 'utils/app_theme.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Set preferred orientations
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
    DeviceOrientation.landscapeLeft,
    DeviceOrientation.landscapeRight,
  ]);

  // Initialize services
  final settingsService = SettingsService();
  await settingsService.loadSettings();

  final gamificationService = GamificationService();
  await gamificationService.loadStats();

  // Check if onboarding is completed
  final prefs = await SharedPreferences.getInstance();
  final onboardingCompleted = prefs.getBool('onboarding_completed') ?? false;

  runApp(ArabicPathwaysApp(
    settingsService: settingsService,
    gamificationService: gamificationService,
    showOnboarding: !onboardingCompleted,
  ));
}

class ArabicPathwaysApp extends StatelessWidget {
  final SettingsService settingsService;
  final GamificationService gamificationService;
  final bool showOnboarding;

  const ArabicPathwaysApp({
    super.key,
    required this.settingsService,
    required this.gamificationService,
    required this.showOnboarding,
  });

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider.value(value: settingsService),
        ChangeNotifierProvider.value(value: gamificationService),
      ],
      child: Consumer<SettingsService>(
        builder: (context, settings, child) {
          return MaterialApp(
            title: 'Arabic Pathways',
            theme: AppTheme.getLightTheme(settings.textScaleFactor),
            darkTheme: AppTheme.getDarkTheme(settings.textScaleFactor),
            themeMode: settings.isDarkMode ? ThemeMode.dark : ThemeMode.light,
            debugShowCheckedModeBanner: false,
            home: showOnboarding
                ? const OnboardingScreen()
                : const MainNavigation(),
          );
        },
      ),
    );
  }
}
