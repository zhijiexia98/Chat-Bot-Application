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

    it('Toggles themes correctly', () => {
        // Switch to dark theme and verify
        cy.get('button').contains('Dark Theme').click();
        cy.get('body').should('have.class', 'dark');

        // Switch to light theme and verify
        cy.get('button').contains('Light Theme').click();
        cy.get('body').should('not.have.class', 'dark');
    });

    it('Handles avatar selection', () => {
        const fileName = 'avatar.jpg';

        // Simulate selecting an avatar
        cy.get('#avatarInput').attachFile(fileName);
        cy.get('#avatarInput').then(input => {
            expect(input[0].files[0].name).to.equal(fileName);
        });
    });

    it('Automatically scrolls down on new messages', () => {
        const userMessage = 'Testing scrolling';

        cy.get('#message-input').type(userMessage);
        cy.get('#send-btn').click();

        // Wait for the message to be added to the chat
        cy.wait(1000); // Adjust wait time based on response time

        cy.get('.chat-box').should($box => {
            expect($box[0].scrollTop).to.be.greaterThan(0);
        });
    });

    it('Displays bot response in chat', () => {
        const userMessage = 'Hello, bot!';

        cy.get('#message-input').type(userMessage);
        cy.get('#send-btn').click();

        // Check for bot's response
        cy.get('.chat-box').should('contain', 'gpt.jpg'); // Assuming bot's messages have a specific avatar
    });

    it('Sends message on Enter key press', () => {
        const userMessage = 'Sending with Enter key';

        cy.get('#message-input').type(`${userMessage}{enter}`);
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
