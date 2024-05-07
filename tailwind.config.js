const colors = require("tailwindcss/colors");
const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "Helvetica Neue", "Helvetica", "sans-serif"],
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            color: theme('colors.dark'),
            '--tw-prose-bullets': theme('colors.dark'),
          },
        },
      }),
      boxShadow: {
        'service': 'rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;'
      }
    },
    colors: {
      // new colors
      amber: {
        300: '#FFD54F'
      },
      grey: {
        100: '#F5F5F5',
        700: '#616161',
        900: '#212121'
      },
      pink: {
        200: '#F48FB1'
      },

      transparent: "transparent",
      current: "currentColor",
      black: colors.black,
      white: colors.white,
      gray: colors.gray,
      yellow: "#FFDC00",
      red: "#F56081",
      green: "#3FCD76",
      primary: "#FFDC00", 
      dark: "#323232",
      danger: "#F56081",
      success: "#3FCD76",
      info: "#5A87FF",
      blue: "#1A73E9",
      muted: "#C4C4C4",
      neutral: {
        50: "#F0F0F0",
        100: "#DDDDDD", 
        200: "#C8C8C8",
        500: "#979797",
        600: "#D1D5DB"
      }, 
    },
  },
  content: ["./templates/**/*.html", "./static/js/**/*.js"],
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/line-clamp"),
    require("tailwindcss-debug-screens"),
    require('tailwind-scrollbar-hide'),
    require('tailwind-scrollbar')({ nocompatible: true }),
  ],
};
