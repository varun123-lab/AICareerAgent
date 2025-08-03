# AI Career Agent

This project is an AI Career Agent website that connects users with career advice and job opportunities using a Python backend and a web frontend built with React.

## Project Structure

```
AICareerAgent/
├── backend/                            # Python + OpenAI backend
│   ├── app.py
│   ├── requirements.txt
│   ├── .env
│   ├── agents/
│   │   ├── career_agent.py
│   │   ├── resume_agent.py
│   │   ├── interview_agent.py
│   │   └── learning_agent.py
│   ├── utils/
│   │   └── openai_helper.py
│   └── README.md

├── frontend/                           # Web frontend (HTML, CSS, JS or React)
│   ├── public/
│   │   └── index.html                  # Main HTML file
│   ├── src/
│   │   ├── index.js                    # Entry point for JS/React
│   │   ├── App.js                      # App wrapper
│   │   ├── components/                 # Reusable UI components
│   │   │   ├── CareerForm.js
│   │   │   ├── ResumeForm.js
│   │   │   ├── InterviewPrep.js
│   │   │   └── LearningResources.js
│   │   ├── api/                        # JS files that call the backend
│   │   │   ├── careerAPI.js
│   │   │   ├── resumeAPI.js
│   │   │   ├── interviewAPI.js
│   │   │   └── learningAPI.js
│   │   └── styles/                     # CSS or Tailwind configs
│   │       └── main.css
│   └── package.json                    # Frontend dependencies

├── demo/                               # Screenshots/video for judging
│   ├── demo.mp4
│   └── screenshots/

├── .gitignore
├── LICENSE
├── README.md                           # Full project overview + setup instructions
```

## Backend

The backend is built using Python (Flask) and integrates with OpenAI's API to provide intelligent career advice, resume feedback, interview preparation, and learning resources.

### Setup

1. Navigate to the `backend` directory.
2. Copy `.env.example` to `.env` and add your OpenAI API key.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python app.py
   ```

## Frontend

The frontend is built with React and provides a user-friendly interface for interacting with the AI Career Agent.

### Setup

1. Navigate to the `frontend` directory.
2. Install dependencies:
   ```
   npm install
   ```
3. Start the development server:
   ```
   npm start
   ```

## Demo

Find demo videos and screenshots in the `demo/` folder.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
