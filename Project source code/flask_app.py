from flask import Flask

app = Flask(__name__)

@app.route('/health')
def health_check():
    # Perform any necessary health checks here
    # Return a successful response if the application is healthy
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)