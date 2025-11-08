import 'dart:convert';

class VideoInfo {
  final String day;
  final String videoId;

  VideoInfo({
    required this.day,
    required this.videoId,
  });

  factory VideoInfo.fromJson(Map<String, dynamic> json) {
    return VideoInfo(
      day: json['day'] as String,
      videoId: json['videoId'] as String,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'day': day,
      'videoId': videoId,
    };
  }
}

class VideoDatabase {
  static Map<String, String> parseVideosJson(String jsonString) {
    final Map<String, dynamic> decoded = json.decode(jsonString);
    return decoded.map((key, value) => MapEntry(key, value.toString()));
  }
}
