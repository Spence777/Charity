/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/js/**/*.js',
    './**/templates/**/*.html',  // Ensure it checks all Django templates
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
