// Global handler for uncaught exceptions
Cypress.on('uncaught:exception', (err, runnable) => {
    // return false to ignore the exception
    return false;
});

describe('Chat Application Tests', () => {
    beforeEach(() => {
        // Visit the chat application before each test
        cy.visit('http://127.0.0.1:5000');
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
        // Get the initial number of messages in the chat box
        cy.get('.chat-box').children().its('length').then(initialMsgCount => {
            // Click the send button without typing a message
            cy.get('#send-btn').click();

            // Check that the number of messages in the chat box has not increased
            cy.get('.chat-box').children().should('have.length', initialMsgCount);
        });
    });


    // More tests can be added here
});
