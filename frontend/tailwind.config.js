/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        fontFamily: {
            sans: ['Graphik', 'sans-serif'],
            serif: ['Merriweather', 'serif'],
        },
        extend: {
            colors: {
                // theme colors will be inserted here
                primary: {
                    DEFAULT: "#151515",
                },
                secondary: {
                    DEFAULT: "#fb7340",
                    50: "#fee3d9",
                    100: "#fdc7b3",
                    200: "#fdab8c",
                    300: "#fc8f66",
                    400: "#fb7340",
                    500: "#c95c33",
                    600: "#974526",
                    700: "#642e1a",
                },
                tertiary: {
                    DEFAULT: "#00cfc1",
                    "50": "#ebebeb",
                    "100": "#d6d6d6",
                    "200": "#adadad",
                    "300": "#858585",
                    "400": "#5c5c5c",
                    "500": "#333333",
                    "600": "#292929",
                    "700": "#1f1f1f",
                    "800": "#141414",
                    "900": "#0a0a0a"
                },
            }
        },
    },
    plugins: [],
}

