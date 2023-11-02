const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const { Configuration, OpenAIApi } = require('openai');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

// Body Parser Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Set up OpenAI API credentials
const configuration = new Configuration({
  apiKey: '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',
});
const openai = new OpenAIApi(configuration);

// Define the default route to return the index.html file
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

// Define the /api route to handle POST requests
app.post('/api', async (req, res) => {
  try {
    // Get the message from the POST request
    const message = req.body.message;

    // Send the message to OpenAI's API and receive the response
    const completion = await openai.createChatCompletion({
      model: 'gpt-3.5-turbo',
      messages: [
        { role: 'user', content: message }
      ]
    });

    const responseMessage = completion.data.choices[0].message;
    if (responseMessage !== null) {
      res.json({ message: responseMessage.content });
    } else {
      res.status(500).send('Failed to generate response!');
    }
  } catch (error) {
    console.error(error);
    res.status(500).send('An error occurred while processing your request.');
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
