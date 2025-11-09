import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './web/app/**/*.{js,ts,jsx,tsx,mdx}',
    './web/components/**/*.{js,ts,jsx,tsx,mdx}',
    './studio/src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Hawk Blue (Primary Brand)
        hawk: {
          50: '#EFF6FF',
          100: '#DBEAFE',
          200: '#BFDBFE',
          300: '#93C5FD',
          400: '#60A5FA',
          500: '#3B82F6', // PRIMARY
          600: '#2563EB',
          700: '#1D4ED8',
          800: '#1E40AF',
          900: '#1E3A8A',
          950: '#172554',
        },

        // Semantic Colors
        success: {
          50: '#ECFDF5',
          100: '#D1FAE5',
          500: '#10B981',
          600: '#059669',
          700: '#047857',
        },

        warning: {
          50: '#FFFBEB',
          100: '#FEF3C7',
          500: '#F59E0B',
          600: '#D97706',
        },

        error: {
          50: '#FFF1F2',
          100: '#FFE4E6',
          500: '#F43F5E',
          600: '#E11D48',
          700: '#BE123C',
        },

        // Market trend colors
        positive: '#10B981', // Green
        negative: '#F43F5E', // Rose/Red
        neutral: '#64748B',  // Slate

        // Company brand colors
        robinhood: {
          green: '#00C805',
          dark: '#0D0F0E',
        },
        palantir: {
          blue: '#0033A0',
          dark: '#000F2E',
        },
        apple: {
          gray: '#1D1D1F',
          blue: '#0071E3',
        },
      },

      fontFamily: {
        sans: [
          'Inter',
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'Helvetica Neue',
          'Arial',
          'sans-serif',
        ],
        mono: [
          'JetBrains Mono',
          'Fira Code',
          'Consolas',
          'Monaco',
          'Courier New',
          'monospace',
        ],
      },

      fontSize: {
        // Display sizes for hero sections
        'display-xl': ['4rem', { lineHeight: '1.1', fontWeight: '700' }],      // 64px
        'display-lg': ['3.5rem', { lineHeight: '1.1', fontWeight: '700' }],    // 56px
        'display-md': ['3rem', { lineHeight: '1.2', fontWeight: '700' }],      // 48px
        'display-sm': ['2.5rem', { lineHeight: '1.2', fontWeight: '700' }],    // 40px

        // Video overlays
        'video-title': ['4rem', { lineHeight: '1.1', fontWeight: '700' }],     // 64px
        'video-subtitle': ['2rem', { lineHeight: '1.3', fontWeight: '600' }],  // 32px
        'video-metric': ['3rem', { lineHeight: '1', fontWeight: '700' }],      // 48px
        'video-label': ['1.125rem', { lineHeight: '1.5', fontWeight: '600' }], // 18px
      },

      spacing: {
        // Custom spacing for financial data displays
        '18': '4.5rem',   // 72px
        '22': '5.5rem',   // 88px
        '26': '6.5rem',   // 104px
        '30': '7.5rem',   // 120px
        '34': '8.5rem',   // 136px
        '38': '9.5rem',   // 152px
      },

      borderRadius: {
        '4xl': '2rem',    // 32px
      },

      boxShadow: {
        // Custom shadows for financial UI
        'card': '0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06)',
        'card-hover': '0 4px 6px rgba(0, 0, 0, 0.07), 0 2px 4px rgba(0, 0, 0, 0.05)',
        'metric': '0 10px 40px rgba(0, 0, 0, 0.1)',
        'video-overlay': '0 8px 32px rgba(0, 0, 0, 0.15)',
        'glow-blue': '0 0 20px rgba(37, 99, 235, 0.3)',
        'glow-green': '0 0 20px rgba(16, 185, 129, 0.3)',
        'glow-red': '0 0 20px rgba(244, 63, 94, 0.3)',
      },

      animation: {
        // Custom animations
        'fade-in': 'fadeIn 0.5s ease-in',
        'slide-up': 'slideUp 0.5s ease-out',
        'slide-down': 'slideDown 0.5s ease-out',
        'scale-in': 'scaleIn 0.3s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },

      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
      },

      backdropBlur: {
        xs: '2px',
      },

      letterSpacing: {
        widest: '0.1em',
      },

      lineHeight: {
        'extra-tight': '1.1',
        'extra-loose': '2',
      },

      maxWidth: {
        '8xl': '88rem',   // 1408px
        '9xl': '96rem',   // 1536px
      },

      zIndex: {
        '60': '60',
        '70': '70',
        '80': '80',
        '90': '90',
        '100': '100',
      },

      screens: {
        'xs': '475px',
        '3xl': '1920px',
      },

      transitionDuration: {
        '400': '400ms',
      },

      aspectRatio: {
        'video': '16 / 9',
        'thumbnail': '16 / 9',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
};

export default config;
