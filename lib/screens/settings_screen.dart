import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/settings_service.dart';
import '../services/progress_service.dart';
import '../services/gamification_service.dart';
import '../utils/app_theme.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
        elevation: 0,
      ),
      body: Consumer<SettingsService>(
        builder: (context, settingsService, child) {
          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              _buildSection(
                context,
                'Appearance',
                [
                  _buildSwitchTile(
                    context,
                    'Dark Mode',
                    'Enable dark theme',
                    Icons.dark_mode,
                    settingsService.isDarkMode,
                    (value) => settingsService.setDarkMode(value),
                  ),
                  _buildTextSizeTile(context, settingsService),
                ],
              ),
              const SizedBox(height: 24),
              _buildSection(
                context,
                'Audio & Notifications',
                [
                  _buildSwitchTile(
                    context,
                    'Sound Effects',
                    'Play audio feedback',
                    Icons.volume_up,
                    settingsService.soundEffectsEnabled,
                    (value) => settingsService.setSoundEffectsEnabled(value),
                  ),
                  _buildSwitchTile(
                    context,
                    'Notifications',
                    'Daily reminders and streak alerts',
                    Icons.notifications,
                    settingsService.notificationsEnabled,
                    (value) => settingsService.setNotificationsEnabled(value),
                  ),
                ],
              ),
              const SizedBox(height: 24),
              _buildSection(
                context,
                'Data & Privacy',
                [
                  _buildActionTile(
                    context,
                    'Reset Progress',
                    'Clear all learning data',
                    Icons.refresh,
                    () => _showResetDialog(context),
                    Colors.red,
                  ),
                ],
              ),
              const SizedBox(height: 24),
              _buildSection(
                context,
                'About',
                [
                  _buildInfoTile(
                    context,
                    'App Version',
                    '1.0.0',
                    Icons.info_outline,
                  ),
                  _buildInfoTile(
                    context,
                    'Terms of Service',
                    'View terms and conditions',
                    Icons.description,
                  ),
                  _buildInfoTile(
                    context,
                    'Privacy Policy',
                    'View privacy policy',
                    Icons.privacy_tip,
                  ),
                ],
              ),
            ],
          );
        },
      ),
    );
  }

  Widget _buildSection(
    BuildContext context,
    String title,
    List<Widget> children,
  ) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 16, bottom: 8),
          child: Text(
            title,
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  color: AppTheme.primaryColor,
                  fontWeight: FontWeight.bold,
                ),
          ),
        ),
        Card(
          child: Column(
            children: children,
          ),
        ),
      ],
    );
  }

  Widget _buildSwitchTile(
    BuildContext context,
    String title,
    String subtitle,
    IconData icon,
    bool value,
    Function(bool) onChanged,
  ) {
    return SwitchListTile(
      title: Text(title),
      subtitle: Text(subtitle),
      secondary: Icon(icon, color: AppTheme.primaryColor),
      value: value,
      onChanged: onChanged,
      activeColor: AppTheme.primaryColor,
    );
  }

  Widget _buildTextSizeTile(BuildContext context, SettingsService settings) {
    return ListTile(
      leading: const Icon(Icons.text_fields, color: AppTheme.primaryColor),
      title: const Text('Text Size'),
      subtitle: Text(settings.getTextSizeLabel()),
      trailing: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          IconButton(
            icon: const Icon(Icons.remove_circle_outline),
            onPressed: settings.textScaleFactor > 0.85
                ? () => settings.setTextScaleFactor(
                      (settings.textScaleFactor - 0.1).clamp(0.85, 1.3),
                    )
                : null,
          ),
          IconButton(
            icon: const Icon(Icons.add_circle_outline),
            onPressed: settings.textScaleFactor < 1.3
                ? () => settings.setTextScaleFactor(
                      (settings.textScaleFactor + 0.1).clamp(0.85, 1.3),
                    )
                : null,
          ),
        ],
      ),
    );
  }

  Widget _buildActionTile(
    BuildContext context,
    String title,
    String subtitle,
    IconData icon,
    VoidCallback onTap,
    Color? color,
  ) {
    return ListTile(
      leading: Icon(icon, color: color ?? AppTheme.primaryColor),
      title: Text(
        title,
        style: TextStyle(color: color),
      ),
      subtitle: Text(subtitle),
      trailing: const Icon(Icons.chevron_right),
      onTap: onTap,
    );
  }

  Widget _buildInfoTile(
    BuildContext context,
    String title,
    String subtitle,
    IconData icon,
  ) {
    return ListTile(
      leading: Icon(icon, color: AppTheme.primaryColor),
      title: Text(title),
      subtitle: Text(subtitle),
    );
  }

  Future<void> _showResetDialog(BuildContext context) async {
    return showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Reset Progress'),
          content: const Text(
            'Are you sure you want to reset all your progress? This action cannot be undone.',
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () async {
                final progressService = ProgressService();
                final gamificationService =
                    Provider.of<GamificationService>(context, listen: false);

                await progressService.resetProgress();
                await gamificationService.resetStats();

                if (context.mounted) {
                  Navigator.of(context).pop();
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('Progress has been reset'),
                      backgroundColor: AppTheme.secondaryColor,
                    ),
                  );
                }
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.red,
              ),
              child: const Text('Reset'),
            ),
          ],
        );
      },
    );
  }
}
