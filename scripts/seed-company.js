#!/usr/bin/env node

/**
 * Seed earnings data for a company using Exa.ai
 *
 * Usage:
 *   node scripts/seed-company.js --ticker=AAPL --quarter=Q4 --year=2024
 *
 * This will:
 * 1. Use Exa.ai to find existing YouTube earnings videos
 * 2. Extract financial data from web sources
 * 3. Create data JSON file for Remotion
 * 4. (Optional) Insert placeholder record in database
 *
 * NOTE: Requires EXA_API_KEY environment variable
 */

const fs = require('fs');
const path = require('path');

// Parse command line arguments
const args = process.argv.slice(2).reduce((acc, arg) => {
  const [key, value] = arg.replace('--', '').split('=');
  acc[key] = value;
  return acc;
}, {});

const { ticker, quarter, year } = args;

if (!ticker || !quarter || !year) {
  console.error('❌ Missing required arguments');
  console.log('Usage: node scripts/seed-company.js --ticker=AAPL --quarter=Q4 --year=2024');
  process.exit(1);
}

// Check for Exa API key
if (!process.env.EXA_API_KEY) {
  console.error('❌ Missing EXA_API_KEY environment variable');
  console.log('\nTo get an API key:');
  console.log('1. Visit https://exa.ai');
  console.log('2. Sign up for an account');
  console.log('3. Get your API key');
  console.log('4. Export it: export EXA_API_KEY="your-key-here"');
  process.exit(1);
}

console.log('🔍 Searching for earnings data using Exa.ai...\n');
console.log(`Company: ${ticker}`);
console.log(`Quarter: ${quarter} ${year}\n`);

// TODO: Implement Exa.ai search
// This is a placeholder - full implementation would use Exa.ai SDK

console.log('⚠️  This is a placeholder script.');
console.log('Full Exa.ai integration coming soon.\n');

console.log('📝 For now, create data files manually:');
console.log(`1. Copy studio/data/AAPL-Q4-2024.json as template`);
console.log(`2. Update with ${ticker} ${quarter} ${year} data`);
console.log(`3. Save as studio/data/${ticker}-${quarter}-${year}.json`);
console.log(`4. Run: npm run studio:render -- --props='@./data/${ticker}-${quarter}-${year}.json'`);

// Create template data file
const templatePath = path.join(__dirname, '..', 'studio', 'data', `${ticker}-${quarter}-${year}.json`);

if (fs.existsSync(templatePath)) {
  console.log(`\n✅ File already exists: ${templatePath}`);
  process.exit(0);
}

const template = {
  company: `${ticker} Inc.`,
  ticker: ticker,
  quarter: quarter,
  fiscal_year: parseInt(year),
  call_date: `${year}-01-01`, // Placeholder - update with actual date
  financials: {
    revenue: {
      current: 0, // Fill in actual data
      previous: 0,
      yoy_growth: 0
    },
    eps: {
      current: 0,
      estimate: 0,
      beat_miss: 'beat'
    },
    segments: [
      { name: 'Product A', revenue: 0 },
      { name: 'Services', revenue: 0 }
    ],
    margins: {
      gross: 0,
      operating: 0,
      net: 0
    }
  },
  highlights: [
    'Update with actual highlights from earnings call',
    'Another key highlight',
    'Third highlight'
  ]
};

fs.writeFileSync(templatePath, JSON.stringify(template, null, 2));

console.log(`\n✅ Created template: ${templatePath}`);
console.log('📝 Edit this file with actual earnings data before rendering');
