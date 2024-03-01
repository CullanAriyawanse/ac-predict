
# Predict Assetto Corsa Lap Times

This application predicts lap times for the racing simulation game Assetto Corsa. It includes a Flask backend and a React frontend. Follow the instructions below to get the application running on your system.

## Prerequisites

Before you start, ensure you have the following installed:
- Python (3.8 or later)
- Flask
- Node.js and npm

## Setting Up a Virtual Environment

For a smoother development experience and to avoid potential conflicts with other Python projects, we recommend setting up a virtual environment for this project. A virtual environment is an isolated Python environment where the dependencies for a specific project are installed without affecting the global Python installation.

### Creating a Virtual Environment
```bash
python3 -m venv (name of environment)
```

After creating the virtual environment, you need to activate it (*`<venv>`* must be replaced by thte path to the directory containing the virtual environment):

- **For Windows Command Prompt:**
    ```cmd
    <venv>\Scripts\activate
    ```

- **For Windows PowerShell:**
    ```powershell
    <venv>\Scripts\Activate.ps1
    ```

- **For Linux/Mac:**
    ```bash
    source <venv>/bin/activate
    ```

### Installing Dependencies

Once the virtual environment is activated, install the project dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

This will install all the necessary Python packages for the project.

## Setting Up the Flask Application

First, navigate to the root directory of the project. Then, set the environment variable for the Flask application using the command line. The command you use depends on your operating system:

- **For Windows Command Prompt:**

    ```cmd
    set FLASK_APP=src\server.py
    ```

- **For Windows PowerShell:**

    ```powershell
    $env:FLASK_APP="src\server.py"
    ```

    Note: The PowerShell command mistakenly had `"hello"` as the value. It should be `"src\server.py"` to correctly point to the Flask application.

- **For Linux/Mac:**

    ```bash
    export FLASK_APP=src/app.py
    ```

    Ensure you are using the correct path to the Flask application file. The example shows `src/app.py`, but adjust it according to your project's structure.

### Running the Flask Application

Once the environment variable is set, you can start the Flask server with the following command:

```bash
flask run
```

There's no need to specify `app` after `flask run` as the `FLASK_APP` environment variable already points to the application.

## Setting Up and Running the UI

The user interface is built with React. To start it, navigate to the `ui` directory and install the dependencies if you haven't done so:

```bash
cd ui
npm install
```

Then, run the UI:

```bash
npm start
```

This will launch the React application, typically available at `http://localhost:3000` in your web browser.
