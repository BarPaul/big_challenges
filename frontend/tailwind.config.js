/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
  ],
  theme: {
    extend: {
      colors: {
        primary: 'var(--color-primary)',
        secondary: 'var(--color-secondary)',
        dark: '#000000',
      },
      fontFamily: {
        sans: ['Gilroy', 'sans-serif'],
        heading: ['Halvar Breit', 'sans-serif'],
      },
      backgroundImage: {
        'gradient-main': 'linear-gradient(45deg, var(--color-primary), var(--color-secondary))',
      }
    },
  },
  plugins: [],
}