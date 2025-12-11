import 'package:flutter/material.dart';
import 'pages/login_page.dart';
import 'pages/home_page.dart';
import 'pages/add_feeling_page.dart';
import 'pages/progress_page.dart';
import 'pages/about_page.dart';
import 'pages/config_page.dart';

void main() {
  runApp(MoodMirrorApp());
}

class MoodMirrorApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "MoodMirror Demo",
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        fontFamily: "Sans",
        scaffoldBackgroundColor: Color(0xFFFFE7EE),
        primaryColor: Color(0xFFF4A8C0),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFFF4A8C0),
          elevation: 0,
          titleTextStyle: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: Color(0xFF333333),
          ),
          iconTheme: IconThemeData(color: Color(0xFF333333)),
        ),
      ),
      initialRoute: "/login",
      routes: {
        "/login": (_) => LoginPage(),
        "/home": (_) => HomePage(),
        "/add": (_) => AddFeelingPage(),
        "/progress": (_) => ProgressPage(),
        "/about": (_) => AboutPage(),
        "/config": (_) => ConfigPage(),
      },
    );
  }
}
