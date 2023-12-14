# Chat Application Requirements Document

## 1. Introduction

This document outlines the functional and non-functional requirements for a web-based chat application. The application will facilitate real-time communication between users and include features such as message history, theme customization, and avatar selection.

### 1.1 Purpose

The purpose of the chat application is to provide a platform for users to communicate in real-time through text messages. The application should be easy to use, reliable, and customizable. It should reply anything user asked.

### 1.2 Document Conventions

This document follows the standard requirement document structure with the use of MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY to describe the requirement levels.

### 1.3 Intended Audience and Reading Suggestions

This document is intended for the development team, project managers, and stakeholders involved in the chat application project.

### 1.4 Project Scope

The scope of the project includes the design, development, testing, and deployment of the chat application on the web platform.

## 2. Overall Description
The chatbot application offers users five distinct functions:

Interactive Chatbot:

Enables users to engage in conversations with our chatbot.
Dark Theme Switch:

Allows users to switch to a dark theme for a different visual experience.
Light Theme Switch:

Provides the option for users to switch to a light theme.
Conversation History Clearing:

Empowers users to clear the conversation history for a fresh start.
Message Sending:

Permits users to send messages within the application.
Our chatbot is equipped to:

Confirmation Response:

Responds with a thoughtful "let me think :)" to acknowledge receipt of user information.
Real-time Answers:

Utilizes the ChatGPT API to provide prompt and accurate responses to user queries.
### 2.1 Product Perspective

The chat application is a self-contained system that does not require integration with existing systems. It will be accessible via modern web browsers.

### 2.2 Product Features

- **User Authentication**: Users must be able to create accounts, log in, and log out.
- **Real-time Messaging**: Users must be able to send and receive messages instantly.
- **Message History**: Users should be able to view their chat history.
- **Avatar Selection**: Users may be able to select and change their avatars.
- **Theme Customization**: Users should be able to toggle between light and dark themes.
- **Rate Limiting**: The application must prevent spam by implementing rate limiting on messages.

### 2.3 User Classes and Characteristics

- **Registered Users**: Users with created accounts who can access all features.
- **Guest Users**: Users who can access limited features, primarily for demonstration purposes.

### 2.4 Operating Environment

The chat application will operate in a web environment and should be compatible with all major browsers including Chrome, Firefox, Safari, and Edge.

### 2.5 Design and Implementation Constraints

- The application will be built using Flask for the backend and HTML, CSS, and JavaScript for the frontend.
- The backend will be implemented in Python, with Flask-SocketIO for real-time communication.
- The application should be responsive and work on both desktop and mobile browsers.
- OpenAI's GPT-3 may be used for automated responses and chatbots.

### 2.6 User Documentation

User documentation will be provided in the form of an FAQ and a Getting Started guide within the application.

## 3. System Features
Our chatbot application boasts a range of features designed to enhance user interaction and experience:

Intuitive Chat Interaction:

Seamlessly engage in conversations with our chatbot, facilitating a natural and user-friendly experience.
Theme Customization:

Personalize the visual aesthetics with the option to switch between a Dark Theme and a Light Theme, catering to diverse user preferences.
Conversation History Management:

Empower users with the ability to clear their conversation history, providing a clean slate for future interactions.
Message Sending Capability:

Enable users to actively participate by sending messages, fostering a dynamic and interactive environment.
Efficient Information Confirmation:

Implement a responsive confirmation mechanism, exemplified by a thoughtful "let me think :)" response, assuring users that their information has been received.
Real-time Answers via ChatGPT API:

Leverage the ChatGPT API to deliver timely and accurate responses, enhancing the chatbot's capabilities and providing users with valuable information.
These system features collectively contribute to a robust and user-centric platform, ensuring a versatile and enjoyable chatbot experience.

### 3.1 User Authentication

#### 3.1.1 Description and Priority

High priority. The system must authenticate users to access personalized features.

#### 3.1.2 Stimulus/Response Sequences

Users will input their username and password to log in. The system will authenticate and grant access.

#### 3.1.3 Functional Requirements

- Users MUST be able to register with an email and password.
- Users MUST be able to log in with a valid email and password.
- Users MUST be able to log out.

### 3.2 Real-time Messaging
Achieved though using ChatGPT Api.

#### 3.2.1 Description and Priority

High priority. Users must be able to send and receive messages with minimal latency.

#### 3.2.2 Stimulus/Response Sequences

Users will send a message which is then instantly visible in the recipient's chat window.

#### 3.2.3 Functional Requirements

- Users MUST be able to send text messages in real-time.
- Users SHOULD be notified when a message is received.

### 3.3 Message History

#### 3.3.1 Description and Priority

Medium priority. Users should be able to view past conversations.

#### 3.3.2 Stimulus/Response Sequences

Upon opening a chat, users should see their previous messages.

#### 3.3.3 Functional Requirements

- Users SHOULD be able to view their message history.
- The system SHOULD NOT display messages from before the user's account creation.

## 4. External Interface Requirements

### 4.1 User Interfaces

- The application MUST have a clean and intuitive interface.
- The interface SHOULD be responsive and adapt to different screen sizes.

### 4.2 Hardware Interfaces

No hardware interfaces are required for this application.

### 4.3 Software Interfaces

- Web Browser: The application MUST be accessible through a web browser.
- Database: The application MUST interface with a database for storing user information and chat history.

### 4.4 Communications Interfaces

- HTTP/HTTPS protocols MUST be used for client-server communication.
- WebSockets MAY be used for real-time communication.

## 5. Nonfunctional Requirements

### 5.1 Performance Requirements

- The system SHOULD support up to 1000 concurrent users without significant degradation of performance.

### 5.2

 Security Requirements

- User passwords MUST be stored securely using modern cryptographic methods.
- The application MUST implement rate limiting to prevent abuse.
- User data MUST be transmitted over HTTPS.

### 5.3 Software Quality Attributes

- **Reliability**: The system MUST be reliable and have an uptime of 99.9%.
- **Usability**: The application MUST be user-friendly and require minimal training to use.
- **Maintainability**: The codebase SHOULD be well-documented to allow easy maintenance and updates.

### 5.4 Business Rules

- User privacy MUST be protected, and data collection SHOULD be minimal and transparent.

## 6. Other Requirements

Any additional requirements not covered above should be addressed here.

## Appendices

### Appendix A: Glossary

- Define any terms or acronyms used in this document for clarity.

### Appendix B: Analysis Models

- Include any models used during analysis, such as data flow diagrams or domain models.

### Appendix C: To-Be-Determined List

- List any items that are still to be determined in the requirements phase.
