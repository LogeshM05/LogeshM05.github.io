const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// Parse JSON requests
app.use(bodyParser.json());

// Define a sample endpoint
app.get('/', (req, res) => {
    res.send('Hello, this is your API!');
});

// Define a POST endpoint for receiving JSON data
app.post('/api/data', (req, res) => {
    const dataReceived = req.body;
    console.log('Received data:', dataReceived);
    res.json({ message: 'Data received successfully', data: dataReceived });
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
