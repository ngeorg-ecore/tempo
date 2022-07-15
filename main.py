from factory import application

# From Application Factory
app = application()

if __name__ == '__main__':
    app.run(debug=True, port=5002, host="0.0.0.0")

