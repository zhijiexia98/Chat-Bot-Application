const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    // If you're using Cypress version 10 or later, use specPattern instead of integrationFolder
    specPattern: 'cypress/integration/**/*.cy.{js,jsx,ts,tsx}',
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
