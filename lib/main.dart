import 'package:flutter/material.dart';

// Import your screens
import 'pages/HomePage.dart';  // <-- create this file with a basic homepage
import 'pages/auth.dart';      // <-- your SignInScreen and SignUpScreen file

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // Replace this with your real authentication check
  final bool isSignedIn = false;

  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Auth App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        fontFamily: 'Roboto',
      ),
      home: isSignedIn ? HomePage() : SignInScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}
