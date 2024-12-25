# ai-text-analyzer

#### Video Demo:  https://www.youtube.com/watch?v=ZLvD1Scc6GM

#### Description:
The AI Text Tone Analyzer is a smart tool that reads your text and determines whether it expresses positive or negative sentiment. Like an emotional detector for words, it quickly analyzes your input to reveal whether the overall message carries a positive or negative tone. In a world where digital communication dominates, understanding the emotional impact of our written words has become increasingly crucial.

The application is built with a clean separation between frontend and backend: `app.py` handles the core AI functionality and tone analysis processing, while the frontend leverages Vite and Vue for rapid development, coupled with a UI framework for seamless customization. This lightweight architecture ensures quick response times and easy maintenance. The decision to use Python for the backend was driven by its robust AI libraries and natural language processing capabilities, making it ideal for sentiment analysis tasks.

The core frontend component, `ToneAnalyzer.vue`, manages communication with the backend by sending analysis requests and relaying the results to its parent component, which displays the sentiment feedback through an intuitive notification system. This modular approach not only enhances code organization but also facilitates future expansions and improvements. The Vue framework's reactive nature ensures that users receive real-time feedback as they interact with the application, creating a smooth and responsive experience.

By utilizing modern web technologies and AI capabilities, this tool bridges the gap between written communication and emotional understanding. Whether you're crafting important business emails, social media posts, or personal messages, the Text Tone Analyzer helps ensure your message conveys the intended emotional tone. The combination of fast processing times, user-friendly interface, and accurate sentiment analysis makes it an invaluable tool for anyone who wants to communicate more effectively in the digital space.
## Setup Instructions

### Backend

1. Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    ```

2. Activate the virtual environment:

   - **Windows:**
     ```bash
     .\venv\Scripts\activate
     ```

   - **Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the backend server:
    ```bash
    python app.py
    ```

Additionally, you can also do this to start the app:

```bash
cd ..
cd front
pnpm start-backend
```

### Frontend

1. Navigate to the `front` directory:
    ```bash
    cd front
    ```

2. Install the required packages using pnpm:
    ```bash
    pnpm install
    ```

3. Run the frontend development server:
    ```bash
    pnpm dev
    ```

### Running the Project

1. Ensure the backend server is running (see Backend section).
2. Ensure the frontend server is running (see Frontend section).
3. Open your browser and navigate to `http://localhost:5173` to use the application.
4. You may need to open chrome to disable CORS check. You can do so by doing Windows + r and running
```bash
chrome.exe --user-data-dir="C://Chrome dev session" --disable-web-security
```
