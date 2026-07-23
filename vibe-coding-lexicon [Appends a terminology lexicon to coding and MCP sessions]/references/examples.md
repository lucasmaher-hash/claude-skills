# Worked Examples — Terminology Lexicon

These are reference examples showing the expected tone, depth, and scope of a Terminology Lexicon appendix across different kinds of tasks. Match this register: plain, concrete, one to two sentences per term, no code.

## 1. Project setup & dependencies

User task: "Initialize the project folder for the mobile app and install the necessary animation libraries."

Claude response: [initialization and installation executed]

```
❇️❇️
Terminology Lexicon:
* package.json: A configuration file that acts as the blueprint for your project, listing all the external libraries (dependencies) the app needs to run.
* npm (Node Package Manager): A tool that downloads and manages the external software packages defined in your package.json.
* Root Directory: The highest-level folder of your project where the core configuration files are stored.
❇️❇️
```

## 2. Styling & layout

User task: "Make the buttons look like analog tactile keys and add a drop shadow."

Claude response: [CSS updates applied]

```
❇️❇️
Terminology Lexicon:
* .css (Cascading Style Sheets): A file format used to design and style the visual presentation of HTML elements, controlling colors, spacing, and animations.
* Hex Code: A six-digit code (e.g. #FFFFFF) used to represent specific colors in digital design.
* Padding vs. Margin: Padding is the internal space inside an element's border, while margin is the external space used to separate it from other elements.
❇️❇️
```

## 3. API integration

User task: "Connect the app to the backend database to fetch the saved diary entries."

Claude response: [API fetch logic implemented]

```
❇️❇️
Terminology Lexicon:
* API (Application Programming Interface): A bridge that allows two different software systems to talk to each other — in this case, your frontend app requesting data from a backend server.
* JSON (JavaScript Object Notation): A standard text format used to send and receive structured data across the web. It organizes data in simple key-value pairs.
* Endpoint: A specific web address (URL) provided by an API where your app sends its request to get or save specific data.
❇️❇️
```

## 4. Version control (Git)

User task: "Save the current state of the code so we don't lose progress on the drag-and-drop feature."

Claude response: [Git commit executed via MCP]

```
❇️❇️
Terminology Lexicon:
* Git: A version control system that tracks changes in your project files over time, acting like a time machine for your software.
* Commit: A saved snapshot of your project at a specific point in time.
* Repository (Repo): The digital storage space where your project's files and their entire revision history are kept.
❇️❇️
```

## 5. Frameworks & components

User task: "Extract the single to-do list item into a reusable element so we can use it on different screens."

Claude response: [component refactored]

```
❇️❇️
Terminology Lexicon:
* Component: A modular, reusable building block of a user interface (like a custom button or a list item) that contains its own structure, style, and logic.
* Props (Properties): The data passed from a parent component down to a child component to customize it (e.g. passing the specific text for a to-do item).
* State: The temporary memory of a component that holds information that might change based on user interaction (e.g. whether a checkbox is ticked or not).
❇️❇️
```

## 6. Asynchronous processes

User task: "Make the app wait and show a loading spinner until the 3D model is fully processed."

Claude response: [async logic and loading state added]

```
❇️❇️
Terminology Lexicon:
* Asynchronous (Async): A process that runs in the background, allowing the rest of the application to keep working and remain responsive while waiting for a slow task to finish.
* Promise: A placeholder object in the system representing the eventual completion (or failure) of an asynchronous operation.
* Loading State: A UI concept where visual feedback is intentionally shown to the user while background data fetching or processing completes.
❇️❇️
```

## 7. Error handling & security

User task: "Fix the bug where the app crashes if the user types special characters into the search bar."

Claude response: [input validation implemented]

```
❇️❇️
Terminology Lexicon:
* Exception / Error: A disruption in the normal flow of the program, usually caused by unexpected data, missing files, or system limits.
* Error Handling: A safety mechanism that "catches" unexpected issues before they crash the whole app, allowing the system to fail gracefully and show a warning instead.
* Sanitization: The process of cleaning user input (like removing harmful or invalid characters) before the system processes it to ensure stability.
❇️❇️
```

## 8. Environment variables (security)

User task: "Add the API key for the image generator, but make sure it isn't visible in the public code."

Claude response: [environment variables configured]

```
❇️❇️
Terminology Lexicon:
* .env (Environment Variables): A hidden configuration file used to store sensitive information (like passwords or API keys) locally, keeping them out of the main code base.
* .gitignore: A simple text file that tells the version control system exactly which files or folders to ignore and never track or upload.
* Authentication: The process of verifying identity, often using a unique secret key, so an external service knows your app is authorized to use its features.
❇️❇️
```

## 9. Build & deployment

User task: "Prepare the project files so we can host them live on the internet."

Claude response: [build script executed]

```
❇️❇️
Terminology Lexicon:
* Build Process: The automated step that compresses, optimizes, and bundles all your raw development files into a lean format ready for web browsers.
* Minification: The process of removing unnecessary characters (like spaces and comments) from files to make them smaller and load faster for the end-user.
* Deployment: The act of pushing your finished, built application files to a live server so users can access the app via a public URL.
❇️❇️
```

## 10. Routing & navigation

User task: "Set up a new screen for the user profile and make sure the back button works."

Claude response: [router configuration updated]

```
❇️❇️
Terminology Lexicon:
* Routing: The system that determines what UI or page should be displayed based on the current URL or user navigation path.
* SPA (Single Page Application): A web application architecture that loads a single HTML page and dynamically updates the content as the user interacts, rather than loading entirely new pages from the server.
* View / Viewport: The visible area of the app on the user's screen that changes depending on the routing state.
❇️❇️
```
