describe('Chat Application Tests', () => {
    beforeEach(() => {
        cy.visit('http://localhost:8080'); // Replace with the correct URL of your chat app
    });

    it('Sends a user message', () => {
        const userMessage = 'Hello, world!';

        // Type a message in the textarea
        cy.get('#message-input').type(userMessage);

        // Click the send button
        cy.get('#send-btn').click();

        // Check if the message is displayed in the chat box
        cy.get('.chat-box').should('contain', userMessage);
    });

    it('Handles empty message gracefully', () => {
        // Click the send button without typing a message
        cy.get('#send-btn').click();

        // Check that no new message is added to the chat box
        cy.get('.user-message').should('not.exist');
    });

    // More tests can be added here
});
