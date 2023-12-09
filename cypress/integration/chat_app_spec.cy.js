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

    it('Displays bot response in chat', () => {
        const userMessage = 'Hello, bot!';
        cy.get('#message-input').type(userMessage);
        cy.get('#send-btn').click();

        cy.get('.bot-message').should('be.visible'); // Wait for bot's response
    });

    it('Sends message on Enter key press', () => {
        const userMessage = 'Sending with Enter key';

        cy.get('#message-input').type(`${userMessage}{enter}`);
        cy.get('.bot-message').should('be.visible'); // Wait for bot's response
    });

    it('Handles empty message gracefully', () => {
        // First, ensure the chat-box is available in the DOM
        cy.get('.chat-box').should('be.visible').then($chatBox => {
            // Store the initial number of messages
            const initialMsgCount = $chatBox.children().length;

            // Attempt to send an empty message by clicking the send button
            cy.get('#send-btn').click();

            // Then check that the number of messages has not increased
            cy.get('.chat-box').should($chatBoxAfter => {
                expect($chatBoxAfter.children().length).to.eq(initialMsgCount);
            });
        });
    });


    it('Automatically scrolls down on new messages', () => {
        const userMessage = 'Testing scrolling';
        cy.get('#message-input').type(userMessage);
        cy.get('#send-btn').click();

        cy.get('.bot-message').should('be.visible'); // Wait for bot's response

        // Check if the chat box has overflowed and is scrollable
        cy.get('.chat-box').then($box => {
            if ($box[0].scrollHeight > $box[0].clientHeight) {
                expect($box[0].scrollTop).to.be.greaterThan(0);
            } else {
                // If not scrollable, either there's not enough content or the test should be reevaluated
                cy.log('Not enough content to overflow and scroll');
            }
        });
    });

});
